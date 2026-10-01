"""MCP-style academics tools (schedule, grades, ...)."""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent.parent / "data"


def get_course_schedule(student_name: str, date: str | None = None) -> str:
    """Return a student's class schedule for a given date."""
    # resolve name -> student_id via attendance lookup
    att = pd.read_csv(DATA / "attendance.csv")
    ids = att.loc[att["name"] == student_name, "student_id"].unique()
    if not len(ids):
        return f"Unknown student: {student_name}"
    sid = ids[0]

    df = pd.read_csv(DATA / "courses.csv")
    rows = df[df["student_id"] == sid]
    if date:
        rows = rows[rows["day"] == date]
    if rows.empty:
        return f"No schedule found for {student_name} on {date or 'the given day'}."
    lines = [f"- Period {r.period}: {r.course} with {r.teacher} in room {r.room}"
             for r in rows.itertuples()]
    return f"Schedule for {student_name}:\n" + "\n".join(lines)
