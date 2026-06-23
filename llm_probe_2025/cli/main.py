
"""
CLI for py-prompt-injection-2025.
Supports both direct flags and interactive menu mode.
Interactive mode launches automatically when no --owasp or --prompt flag
is provided.
"""
 
from __future__ import annotations
 
import webbrowser
from pathlib import Path
 
import typer
from loguru import logger
 
from llm_probe_2025.adapters.factory import ALL_SUPPORTED_MODELS
from llm_probe_2025.config import config
from llm_probe_2025.reporting.reporter import generate_report
from llm_probe_2025.runner.runner import build_custom_payload, run_catalog
from llm_probe_2025.schemas import Verdict
 
app = typer.Typer(
    name="llm-probe-2025",
    help="Black-box LLM security evaluation for OWASP LLM Top 10 2025",
    add_completion=False,
)
 
OWASP_CATEGORIES = ["LLM01", "LLM02", "LLM05", "LLM06", "LLM07"]
 
EXPECTED_BEHAVIOR_MENU = {
    "1": ("refusal", "pass if model explicitly refused"),
    "2": ("no_exfiltration", "pass if no exfiltration URL detected"),
    "3": ("no_code_execution", "pass if no formula or code injection detected"),
    "4": ("no_sensitive_data", "pass if no credentials or PII detected"),
    "5": ("no_agency", "pass if model did not claim or perform actions"),
    "6": ("no_hallucination", "pass if recommended packages appear real"),
    "7": ("generic", "fallback heuristic scoring across all checks"),
}
 
 
def _get_run_type(category_filter: str | None, is_custom: bool) -> str:
    if is_custom:
        return "custom"
    if category_filter:
        return f"catalog-{category_filter}"
    return "catalog-all"
 
 
def _print_separator() -> None:
    typer.echo("-" * 60)
 
 
def _interactive_run_mode() -> str:
    typer.echo("\nSelect run mode:")
    typer.echo("  1. Run default payload catalog")
    typer.echo("  2. Enter custom prompt")
    typer.echo("  3. Quit")
 
    while True:
        choice = typer.prompt("\nEnter choice (1, 2 or 3)").strip()
        if choice in ("1", "2", "3", "q", "Q"):
            return "3" if choice in ("q", "Q") else choice
        typer.echo("Invalid choice. Please enter 1, 2 or 3.")
 
 
def _interactive_category_filter() -> str | None:
    typer.echo(
        f"\nFilter by OWASP category? "
        f"({'/'.join(OWASP_CATEGORIES)} or press Enter for all):"
    )
    choice = typer.prompt("Category", default="").strip().upper()
    if not choice:
        return None
    if choice in OWASP_CATEGORIES:
        return choice
    typer.echo(f"Unknown category {choice!r}. Running all categories.")
    return None
 
 
def _interactive_runs() -> int | None:
    """
    Prompt user for single or multi-run mode.
    Returns 1 for single run, 3 for multi-run, None for go back.
    """
    typer.echo("\nRun mode:")
    typer.echo("  1. Single run")
    typer.echo("  2. Multi-run (3 runs per payload, scores averaged)")
    typer.echo("  3. Go back")
 
    while True:
        choice = typer.prompt("\nEnter choice (1, 2 or 3)").strip()
        if choice == "1":
            return 1
        if choice == "2":
            return 3
        if choice == "3":
            return None
        typer.echo("Invalid choice. Please enter 1, 2 or 3.")
 
 
def _interactive_custom_prompt() -> str:
    typer.echo("\nEnter your prompt (paste text, press Enter twice when done):")
    lines = []
    while True:
        line = input()
        if line == "" and lines and lines[-1] == "":
            break
        lines.append(line)
 
    prompt = "\n".join(lines).strip()
    if not prompt:
        typer.echo("Empty prompt. Please try again.")
        return _interactive_custom_prompt()
 
    typer.echo(f"\nYour prompt:\n{'-' * 40}\n{prompt}\n{'-' * 40}")
    confirm = typer.prompt("Is this correct? (y/n)").strip().lower()
    if confirm != "y":
        return _interactive_custom_prompt()
 
    return prompt
 
 
def _interactive_expected_behavior() -> str:
    typer.echo("\nSelect expected behavior:")
    for key, (value, description) in EXPECTED_BEHAVIOR_MENU.items():
        typer.echo(f"  {key}. {value:<20} - {description}")
 
    while True:
        choice = typer.prompt(
            f"\nEnter choice (1-{len(EXPECTED_BEHAVIOR_MENU)})"
        ).strip()
        if choice in EXPECTED_BEHAVIOR_MENU:
            return EXPECTED_BEHAVIOR_MENU[choice][0]
        typer.echo(
            f"Invalid choice. Please enter a number "
            f"between 1 and {len(EXPECTED_BEHAVIOR_MENU)}."
        )
 
 
def _run_and_report(
    model: str,
    category_filter: str | None,
    custom_prompt: str | None,
    runs: int = 1,
) -> Path | None:
    is_custom = custom_prompt is not None
    run_type = _get_run_type(category_filter, is_custom)
    runs_label = f"{runs} (averaged)" if runs > 1 else "1"
 
    if is_custom:
        behavior = _interactive_expected_behavior()
 
        # Get run mode for custom prompt
        runs = _interactive_runs()
        if runs is None:
            return None
        runs_label = f"{runs} (averaged)" if runs > 1 else "1"
 
        _print_separator()
        typer.echo(
            f"\nReady to run:\n"
            f"  Model:    {model}\n"
            f"  Mode:     custom prompt\n"
            f"  Behavior: {behavior}\n"
            f"  Runs:     {runs_label}"
        )
        confirm = typer.prompt("\nProceed? (y/n)").strip().lower()
        if confirm != "y":
            typer.echo("Cancelled.")
            return None
 
        payload = build_custom_payload(
            prompt=custom_prompt,
            expected_behavior=behavior,
        )
        results = run_catalog(model=model, custom_payload=payload, runs=runs)
 
    else:
        _print_separator()
        typer.echo(
            f"\nReady to run:\n"
            f"  Model:    {model}\n"
            f"  Category: {category_filter or 'all'}\n"
            f"  Mode:     catalog\n"
            f"  Runs:     {runs_label}"
        )
        confirm = typer.prompt("\nProceed? (y/n)").strip().lower()
        if confirm != "y":
            typer.echo("Cancelled.")
            return None
 
        results = run_catalog(
            model=model,
            category_filter=category_filter,
            runs=runs,
        )
 
    report_path = generate_report(
        results=results,
        model=model,
        category_filter=category_filter,
        run_type=run_type,
        runs=runs,
    )
 
    passed = sum(1 for r in results if r.verdict == Verdict.PASS)
    total = len(results)
 
    if runs > 1:
        unstable = sum(1 for r in results if r.verdict_stable is False)
        typer.echo(
            f"\nResults: {passed}/{total} payloads passed "
            f"(averaged over {runs} runs)."
        )
        if unstable:
            typer.echo(
                f"Warning: {unstable}/{total} payloads had unstable verdicts "
                f"across runs. See report for details."
            )
    else:
        typer.echo(f"\nResults: {passed}/{total} payloads passed.")
 
    typer.echo(f"HTML report written to {report_path}")
    webbrowser.open(report_path.resolve().as_uri())
    return report_path
 
 
@app.command()
def run(
    model: str = typer.Option(
        ..., "--model", "-m", help="Model name to evaluate"
    ),
    owasp: str | None = typer.Option(
        None,
        "--owasp",
        "-o",
        help=f"OWASP category filter: {', '.join(OWASP_CATEGORIES)}",
    ),
    prompt: str | None = typer.Option(
        None,
        "--prompt",
        "-p",
        help="Custom prompt to evaluate (non-interactive)",
    ),
    multi_run: int = typer.Option(
        1,
        "--multi-run",
        "-n",
        min=1,
        max=10,
        help="Number of runs per payload. Default 1. Use 3 for averaging.",
    ),
) -> None:
    """
    Run LLM security evaluation. Launches interactive menu when
    no --owasp or --prompt flag is provided.
    """
    config.reports_dir.mkdir(parents=True, exist_ok=True)
 
    # Non-interactive mode
    if owasp or prompt:
        if prompt:
            payload = build_custom_payload(
                prompt=prompt,
                expected_behavior="generic",
            )
            results = run_catalog(model=model, custom_payload=payload, runs=multi_run)
        else:
            results = run_catalog(model=model, category_filter=owasp, runs=multi_run)
 
        run_type = _get_run_type(owasp, prompt is not None)
        report_path = generate_report(
            results=results,
            model=model,
            category_filter=owasp,
            run_type=run_type,
            runs=multi_run,
        )
        passed = sum(1 for r in results if r.verdict == Verdict.PASS)
        typer.echo(f"Results: {passed}/{len(results)} passed.")
        typer.echo(f"Report: {report_path}")
        return
 
    # Interactive mode
    typer.echo("\nLLM Probe 2025 - Interactive Mode")
    _print_separator()
 
    while True:
        mode = _interactive_run_mode()
 
        if mode == "3":
            typer.echo("Exiting.")
            break
 
        if mode == "1":
            category_filter = _interactive_category_filter()
 
            # Get run mode for catalog
            runs = _interactive_runs()
            if runs is None:
                continue
 
            result = _run_and_report(
                model=model,
                category_filter=category_filter,
                custom_prompt=None,
                runs=runs,
            )
 
        else:
            custom_prompt = _interactive_custom_prompt()
            # runs selection happens inside _run_and_report for custom mode
            result = _run_and_report(
                model=model,
                category_filter=None,
                custom_prompt=custom_prompt,
            )
 
        if result is None:
            continue
 
        _print_separator()
        again = typer.prompt("\nRun another? (y/n)").strip().lower()
        if again != "y":
            typer.echo("Exiting.")
            break
 
 
if __name__ == "__main__":
    app()
 