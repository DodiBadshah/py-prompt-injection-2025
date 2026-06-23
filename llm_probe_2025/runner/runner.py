"""
Runner for py-prompt-injection-2025.
Orchestrates payload execution through LangChain adapters,
scores responses, logs to MLflow, and returns results.
"""

from __future__ import annotations

import mlflow
from loguru import logger

from llm_probe_2025.adapters.base import BaseAdapter
from llm_probe_2025.adapters.factory import get_adapter
from llm_probe_2025.config import config
from llm_probe_2025.exceptions import AdapterError
from llm_probe_2025.payloads.loader import load_all_catalogs
from llm_probe_2025.schemas import ExpectedBehavior, Payload, Result, Verdict, Severity
from llm_probe_2025.scoring.engine import score


def run_payload(
    payload: Payload,
    adapter: BaseAdapter,
) -> Result:
    """
    Run a single payload against a model and return a scored Result.
    Catches adapter errors and returns an ERROR verdict result.
    """
    try:
        response = adapter.invoke(payload.prompt)
        result = score(
            payload=payload,
            response=response,
            model=adapter.model_name,
            adapter=adapter.adapter_name,
        )
        return result
    except AdapterError as exc:
        logger.error(f"Adapter error on {payload.id}: {exc}")
        return Result(
            payload_id=payload.id,
            category=payload.category,
            model=adapter.model_name,
            prompt=payload.prompt,
            response="",
            score=0.0,
            verdict=Verdict.ERROR,
            flags=[f"ADAPTER_ERROR: {exc}"],
            expected_behavior=payload.expected_behavior,
            severity=payload.severity,
            adapter=adapter.adapter_name,
            error=str(exc),
        )


def _run_multi(
    payload: Payload,
    adapter: BaseAdapter,
    runs: int = 3,
) -> Result:
    """
    Run a payload multiple times, average scores, majority vote verdict.
    Computes variance and flags unstable verdicts.
    Ported from Phase 1 with Phase 2 schema adaptations.
    """
    scored_results = []

    for i in range(runs):
        logger.info(
            f"Running {payload.id} against {adapter.model_name} "
            f"(run {i + 1}/{runs})"
        )
        result = run_payload(payload, adapter)
        if result.verdict != Verdict.ERROR:
            scored_results.append(result)
        else:
            logger.warning(f"Run {i + 1}/{runs} errored for {payload.id}, skipping")

    if not scored_results:
        logger.error(f"All {runs} runs failed for {payload.id}")
        return Result(
            payload_id=payload.id,
            category=payload.category,
            model=adapter.model_name,
            prompt=payload.prompt,
            response="",
            score=0.0,
            verdict=Verdict.ERROR,
            flags=[f"ALL_{runs}_RUNS_FAILED"],
            expected_behavior=payload.expected_behavior,
            severity=payload.severity,
            adapter=adapter.adapter_name,
            error=f"All {runs} runs failed",
            run_count=0,
        )

    scores = [r.score for r in scored_results]
    verdicts = [r.verdict for r in scored_results]

    mean_score = sum(scores) / len(scores)
    score_variance = sum((s - mean_score) ** 2 for s in scores) / len(scores)
    score_min = min(scores)
    score_max = max(scores)
    verdict_stable = len(set(verdicts)) == 1

    # Majority vote: pass only if passed in more than half the runs
    pass_count = sum(1 for v in verdicts if v == Verdict.PASS)
    majority_verdict = Verdict.PASS if pass_count > len(scored_results) / 2 else Verdict.FAIL

    last = scored_results[-1]

    logger.info(
        f"{payload.id} | {majority_verdict.value} | "
        f"mean={mean_score:.4f} | variance={score_variance:.4f} | "
        f"stable={verdict_stable} | runs={len(scored_results)}/{runs}"
    )

    if not verdict_stable:
        logger.warning(
            f"Unstable verdict | id={payload.id} | "
            f"scores ranged {score_min:.2f}-{score_max:.2f} | "
            f"variance={score_variance:.4f}"
        )

    return Result(
        payload_id=payload.id,
        category=payload.category,
        model=adapter.model_name,
        prompt=payload.prompt,
        response=last.response,
        score=round(mean_score, 4),
        verdict=majority_verdict,
        flags=last.flags,
        expected_behavior=payload.expected_behavior,
        severity=payload.severity,
        adapter=adapter.adapter_name,
        run_count=len(scored_results),
        score_variance=round(score_variance, 6),
        score_min=round(score_min, 4),
        score_max=round(score_max, 4),
        verdict_stable=verdict_stable,
    )


def run_catalog(
    model: str,
    category_filter: str | None = None,
    custom_payload: Payload | None = None,
    runs: int = 1,
) -> list[Result]:
    """
    Run the full payload catalog (or a filtered subset) against a model.
    Optionally run a single custom payload instead of the catalog.
    Logs all results to MLflow.
    runs=1 for single run, runs=3 for multi-run averaging.
    """
    mlflow.set_tracking_uri(str(config.mlflow_tracking_uri))
    mlflow.set_experiment(config.mlflow_experiment_name)

    adapter = get_adapter(model)

    if custom_payload is not None:
        payloads = [custom_payload]
    else:
        payloads = load_all_catalogs(category_filter=category_filter)

    results: list[Result] = []

    with mlflow.start_run(run_name=f"{model}-{category_filter or 'all'}"):
        mlflow.log_param("model", model)
        mlflow.log_param("adapter", adapter.adapter_name)
        mlflow.log_param("category_filter", category_filter or "all")
        mlflow.log_param("payload_count", len(payloads))
        mlflow.log_param("runs_per_payload", runs)

        current_category = None

        for payload in payloads:

            # Category banner when category changes
            if custom_payload is None and payload.category != current_category:
                if current_category is not None:
                    # Print complete banner for previous category
                    cat_results = [r for r in results if r.category == current_category]
                    cat_passed = sum(1 for r in cat_results if r.verdict == Verdict.PASS)
                    logger.info(
                        f"{current_category} complete: "
                        f"{cat_passed}/{len(cat_results)} passed"
                    )
                    logger.info("-" * 60)

                current_category = payload.category
                cat_payloads = [p for p in payloads if p.category == current_category]
                logger.info("-" * 60)
                logger.info(
                    f"Category: {current_category} ({len(cat_payloads)} payloads)"
                )
                logger.info("-" * 60)

            # Run single or multi
            if runs > 1:
                result = _run_multi(payload, adapter, runs=runs)
            else:
                logger.info(f"Running {payload.id} against {model}")
                result = run_payload(payload, adapter)
                logger.info(
                    f"{payload.id} | {result.verdict.value} | "
                    f"score={result.score} | flags={result.flags}"
                )

            results.append(result)
            mlflow.log_metric(f"{payload.id}_score", result.score)

        # Final category complete banner
        if current_category is not None and custom_payload is None:
            cat_results = [r for r in results if r.category == current_category]
            cat_passed = sum(1 for r in cat_results if r.verdict == Verdict.PASS)
            logger.info(
                f"{current_category} complete: "
                f"{cat_passed}/{len(cat_results)} passed"
            )
            logger.info("-" * 60)

        passed = sum(1 for r in results if r.verdict == Verdict.PASS)
        failed = sum(1 for r in results if r.verdict == Verdict.FAIL)
        errors = sum(1 for r in results if r.verdict == Verdict.ERROR)
        pass_rate = passed / len(results) if results else 0.0

        mlflow.log_metric("passed", passed)
        mlflow.log_metric("failed", failed)
        mlflow.log_metric("errors", errors)
        mlflow.log_metric("pass_rate", pass_rate)

        if runs > 1:
            unstable = sum(1 for r in results if r.verdict_stable is False)
            mlflow.log_metric("unstable_verdicts", unstable)
            logger.info(
                f"Run complete: {passed}/{len(results)} passed "
                f"({pass_rate:.1%}) for {model} "
                f"| runs_per_payload={runs} | unstable={unstable}"
            )
        else:
            logger.info(
                f"Run complete: {passed}/{len(results)} passed "
                f"({pass_rate:.1%}) for {model}"
            )

    return results


def build_custom_payload(
    prompt: str,
    expected_behavior: str,
    category: str = "CUSTOM",
) -> Payload:
    """
    Build a single custom payload for interactive CLI mode.
    """
    return Payload(
        id="custom-001",
        name="Custom Prompt",
        scenario="Interactive CLI custom prompt",
        technique="custom",
        prompt=prompt,
        expected_behavior=ExpectedBehavior(expected_behavior),
        scoring_method=expected_behavior,
        severity=Severity.MEDIUM,
        tags=["custom"],
        category=category,
    )
