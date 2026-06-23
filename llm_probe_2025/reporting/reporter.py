
"""
Report generator for py-prompt-injection-2025.
Renders HTML reports from run results using Jinja2.
"""
 
from __future__ import annotations
 
from datetime import datetime
from pathlib import Path
 
from jinja2 import Environment, FileSystemLoader
 
from llm_probe_2025.adapters.factory import sanitize_model_name
from llm_probe_2025.config import config
from llm_probe_2025.exceptions import ReportError
from llm_probe_2025.schemas import Result, Verdict
 
TEMPLATES_DIR = Path(__file__).parent / "templates"
 
 
def generate_report(
    results: list[Result],
    model: str,
    category_filter: str | None,
    run_type: str = "catalog-all",
    runs: int = 1,
) -> Path:
    """
    Render an HTML report from results and write to the reports directory.
    Returns the path to the written report file.
    """
    config.reports_dir.mkdir(parents=True, exist_ok=True)
 
    passed = sum(1 for r in results if r.verdict == Verdict.PASS)
    failed = sum(1 for r in results if r.verdict == Verdict.FAIL)
    total = len(results)
    pass_rate = f"{passed / total:.1%}" if total else "0.0%"
    adapter = results[0].adapter if results else "unknown"
 
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    template = env.get_template("report.html.j2")
 
    html = template.render(
        model=model,
        category_filter=category_filter or ("CUSTOM" if run_type == "custom" else "all"),
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M"),
        adapter=adapter,
        total=total,
        passed=passed,
        failed=failed,
        pass_rate=pass_rate,
        results=results,
        runs=runs,
        runs_label=f"{runs} (averaged)" if runs > 1 else "1",
    )
 
    safe_model = sanitize_model_name(model)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"{safe_model}_{run_type}_{timestamp}.html"
    output_path = config.reports_dir / filename
 
    try:
        output_path.write_text(html, encoding="utf-8")
    except OSError as exc:
        raise ReportError(f"Failed to write report to {output_path}: {exc}") from exc
 
    return output_path
 