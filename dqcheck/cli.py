from __future__ import annotations
import json
import typer
from rich.console import Console
from rich.table import Table
from pathlib import Path

from .models import Schema
from .validator import validate_csv

app = typer.Typer(add_completion=False, help="CSV Data Quality Checker")
console = Console()

@app.command()
def check(
    csv_file: Path = typer.Argument(..., exists=True, readable=True, help="Path to CSV file"),
    schema: Path = typer.Option(..., "--schema", "-s", exists=True, readable=True, help="Path to schema JSON"),
    key: str = typer.Option(None, "--key", "-k", help="Optional column name to check duplicates"),
    out: Path = typer.Option(None, "--out", "-o", help="Write JSON report to a file"),
):
    """Validate a CSV file and print a summary."""
    schema_obj = Schema.model_validate_json(schema.read_text(encoding="utf-8"))
    report = validate_csv(str(csv_file), schema_obj, key=key)

    # pretty summary
    summary = report.summary()
    table = Table(title="Data Quality Summary")
    table.add_column("Metric", style="bold")
    table.add_column("Value", justify="right")

    for k, v in summary.items():
        table.add_row(k, str(v))

    console.print(table)

    if report.missing_columns:
        console.print(f"[yellow]Missing required columns:[/yellow] {', '.join(report.missing_columns)}")

    # show top issues
    if report.issues:
        issue_table = Table(title="Top Issues (first 20)")
        issue_table.add_column("Row", justify="right")
        issue_table.add_column("Column")
        issue_table.add_column("Issue")
        issue_table.add_column("Detail")

        for issue in report.issues[:20]:
            issue_table.add_row(str(issue.row or ""), str(issue.column or ""), issue.issue, issue.detail or "")

        console.print(issue_table)

    # output JSON
    if out:
        out.write_text(json.dumps(report.model_dump(), indent=2), encoding="utf-8")
        console.print(f"[green]Wrote report:[/green] {out}")

if __name__ == "__main__":
    app()
