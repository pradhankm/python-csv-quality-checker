from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, List, Literal, Optional

ColumnType = Literal["int", "float", "string", "date"]

class SchemaColumn(BaseModel):
    name: str
    type: ColumnType = "string"
    required: bool = True

class Schema(BaseModel):
    columns: List[SchemaColumn]
    date_format: str = "%Y-%m-%d"

    def required_columns(self) -> List[str]:
        return [c.name for c in self.columns if c.required]

    def column_map(self) -> Dict[str, SchemaColumn]:
        return {c.name: c for c in self.columns}

class Issue(BaseModel):
    row: Optional[int] = None
    column: Optional[str] = None
    issue: str
    detail: Optional[str] = None

class Report(BaseModel):
    file: str
    total_rows: int
    missing_columns: List[str] = Field(default_factory=list)
    duplicate_key_count: int = 0
    issues: List[Issue] = Field(default_factory=list)

    def summary(self) -> Dict[str, int]:
        return {
            "total_rows": self.total_rows,
            "missing_columns": len(self.missing_columns),
            "duplicate_key_count": self.duplicate_key_count,
            "issue_count": len(self.issues),
        }
