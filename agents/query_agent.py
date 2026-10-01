"""Academics sub-agent: schedule, grades, etc."""
from agents.llm import get_llm
from tools.academics_tools import get_course_schedule


def run(question: str) -> str:
    name = None
    for token in ["张三", "李四", "王五"]:
        if token in question:
            name = token
            break
    if not name:
        return "Sorry, I couldn't tell which student you're asking about."
    result = get_course_schedule(name)
    llm = get_llm()
    summary = llm.invoke(
        f"User asked: {question}\nTool result:\n{result}\n"
        "Reply in Chinese, one or two short sentences, list the classes clearly."
    )
    return summary.content
