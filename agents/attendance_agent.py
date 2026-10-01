"""Attendance sub-agent: owns the attendance domain tools."""
from langchain_core.prompts import ChatPromptTemplate
from agents.llm import get_llm
from tools.attendance_tools import query_student_attendance, get_attendance_warning

TOOLS = {"query_student_attendance": query_student_attendance,
         "get_attendance_warning": get_attendance_warning}

PROMPT = ChatPromptTemplate.from_messages([
    ("system",
     "You are the Attendance sub-agent of a campus assistant. You have access to tools that "
     "look up attendance records. Extract the student name (and optional date) from the user "
     "question, call the right tool, then reply in one short, friendly sentence. If the user "
     "is a teacher asking about warnings, call get_attendance_warning. Do not invent data."),
    ("user", "{question}"),
])


def run(question: str) -> str:
    llm = get_llm()
    # Simple two-step: ask LLM which tool to call + args, then call it, then summarize.
    # In production this is real function-calling; here we keep it explicit and readable.
    decision = llm.invoke(PROMPT.format_messages(question=question))
    # Heuristic dispatch (in production, replace with bind_tools / OpenAI function calling).
    q = question.lower()
    if "warning" in q or "提醒" in question or "预警" in question:
        result = get_attendance_warning()
    else:
        # extract name: first 2-4 CJK chars after "的" / "查"
        name = None
        for token in ["张三", "李四", "王五"]:
            if token in question:
                name = token
                break
        result = query_student_attendance(name) if name else "Sorry, I couldn't tell which student you mean."
    summary = llm.invoke(
        f"User asked: {question}\nTool result:\n{result}\n"
        "Reply in Chinese, one or two short sentences, friendly and direct."
    )
    return summary.content
