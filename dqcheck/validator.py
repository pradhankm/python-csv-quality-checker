from __future__ import annotations
import csv
from dataclasses import dataclass
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime
from dateutil.parser import parse as dateparse

from .models import Schema, Report, Issue

def _is_blank(v: Optional[str]) -> bool:
    return v is None or str(v).strip() == ""

def _parse_int(v: str) -> bool:
    try:
        int(v)
        return True
    except Exception:
        return False

def _parse_float(v: str) -> bool:
    try:
        float(v)
        return True
    except Exception:
        return False

def _parse_date(v: str, fmt: str) -> bool:
    # accept exact format if possible; otherwise fallback to parser
    try:
        datetime.strptime(v, fmt)
        return True
    except Exception:
        try:
            dateparse(v)
            return True
        except Exception:
            return False

def validate_csv(path: str, schema: Schema, key: Optional[str] = None, max_issues: int = 2000) -> Report:
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        colmap = schema.column_map()

        missing_cols = [c for c in schema.required_columns() if c not in headers]
        report = Report(file=path, total_rows=0, missing_columns=missing_cols)

        seen_keys = set()
        dupes = 0

        for i, row in enumerate(reader, start=1):
            report.total_rows += 1

            # duplicates
            if key:
                kv = row.get(key)
                if not _is_blank(kv):
                    if kv in seen_keys:
                        dupes += 1
                    else:
                        seen_keys.add(kv)

            # per-column checks
            for col_name, col in colmap.items():
                if col_name not in headers:
                    continue
                v = row.get(col_name)

                if col.required and _is_blank(v):
                    report.issues.append(Issue(row=i, column=col_name, issue="missing_required", detail="Required value is blank"))
                    continue

                if _is_blank(v):
                    continue  # optional blank ok

                t = col.type
                ok = True
                if t == "int":
                    ok = _parse_int(v)
                elif t == "float":
                    ok = _parse_float(v)
                elif t == "date":
                    ok = _parse_date(v, schema.date_format)

                if not ok:
                    report.issues.append(Issue(row=i, column=col_name, issue="invalid_type", detail=f"Expected {t}, got '{v}'"))

                if len(report.issues) >= max_issues:
                    report.issues.append(Issue(issue="max_issues_reached", detail=f"Stopped after {max_issues} issues"))
                    break

            if len(report.issues) >= max_issues:
                break

        report.duplicate_key_count = dupes
        return report
