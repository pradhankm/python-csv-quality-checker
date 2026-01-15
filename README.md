# python-csv-quality-checker

A small but real-world **Python CLI** that checks a CSV file for common data-quality issues and produces a report.

## What it does
- Validates required columns
- Checks missing values
- Validates types (int/float/date/string)
- Checks duplicates on a chosen key
- Outputs a **JSON report** and a human-friendly summary

## Tech
- Python 3.10+
- Typer (CLI)
- Pydantic (schema)
- Pytest (tests)

## Quick start
```bash
cd python-csv-quality-checker
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt

# Run against the sample file
python -m dqcheck check sample/customers.csv --schema sample/schema.json --key id --out report.json
```

## Example output
- Console summary with counts and top problems
- `report.json` with full details

## Commands
```bash
python -m dqcheck --help
python -m dqcheck check --help
```

## Running tests
```bash
pytest -q
```

## Project layout
- `dqcheck/` – application code
- `tests/` – unit tests
- `sample/` – sample CSV + schema JSON

## Notes
- This is intentionally small, but structured like a production CLI project.
- Great place to add enhancements: rules engine, HTML report, Great Expectations integration, etc.
