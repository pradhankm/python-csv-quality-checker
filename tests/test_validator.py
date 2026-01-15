from dqcheck.models import Schema
from dqcheck.validator import validate_csv
from pathlib import Path

def test_sample_file_validates(tmp_path: Path):
    schema_path = Path(__file__).parent.parent / "sample" / "schema.json"
    csv_path = Path(__file__).parent.parent / "sample" / "customers.csv"
    schema = Schema.model_validate_json(schema_path.read_text(encoding="utf-8"))

    report = validate_csv(str(csv_path), schema, key="id")
    assert report.total_rows == 5
    assert report.duplicate_key_count == 1
    assert any(i.issue == "missing_required" and i.column == "name" for i in report.issues)
    assert any(i.issue == "invalid_type" and i.column == "spend" for i in report.issues)
