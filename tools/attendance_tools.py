"""MCP-style attendance tools.

In production these lived behind two MCP servers (attendance domain, academics domain).
Here we keep them as plain Python functions so the demo has zero infra. The contract —
business-semantic names, narrow signatures, no arbitrary SQL — is the whole point.
"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"


def query_student_attendance(student_name: str, date: str | None = None) -> str:
    """Look up a student's attendance record by name. Optionally filter by date (YYYY-MM-DD)."""
    df = pd.read_csv(DATA / "attendance.csv")
    rows = df[df["name"] == student_name]
    if date:
        rows = rows[rows["date"] == date]
    if rows.empty:
        return f"No attendance records found for {student_name}."
    lines = [f"- {r.date}: {r.status}" for r in rows.itertuples()]
    return f"Attendance for {student_name}:\n" + "\n".join(lines)


def get_attendance_warning(teacher_class: str | None = None) -> str:
    """Return students who are late or absent in the last two days (for teacher alerts)."""
    df = pd.read_csv(DATA / "attendance.csv")
    bad = df[df["status"].isin(["late", "absent"])]
    if bad.empty:
        return "No attendance warnings right now."
    lines = [f"- {r.name} on {r.date}: {r.status}" for r in bad.itertuples()]
    return "Attendance warnings:\n" + "\n".join(lines)
