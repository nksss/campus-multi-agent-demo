"""Orchestrator: intent classification -> dispatch to a sub-agent -> final answer.

In production this also owns:
- short-term memory (Redis, last 10 turns)
- global state across sub-agent calls
- retry caps + timeouts + degradation
- logging for trace monitoring

Here we show the dispatch loop only, to keep the demo readable.
"""
from agents.llm import get_llm
from agents import attendance_agent, query_agent, fallback

INTENT_PROMPT = (
    "You are routing a question for a campus assistant. Reply with EXACTLY ONE WORD: "
    "'attendance', 'schedule', or 'off_topic'.\n"
    "attendance = questions about check-in, late, absent, attendance warnings.\n"
    "schedule   = questions about class timetable, courses, teachers, rooms.\n"
    "off_topic  = anything else (poems, jokes, math homework, etc.).\n\n"
    "Question: {q}\nCategory:"
)


def route(question: str) -> str:
    llm = get_llm()
    resp = llm.invoke(INTENT_PROMPT.format(q=question))
    tag = resp.content.strip().lower()
    if "attendance" in tag:
        return "attendance"
    if "schedule" in tag:
        return "schedule"
    return "off_topic"


def answer(question: str) -> str:
    intent = route(question)
    if intent == "attendance":
        return attendance_agent.run(question)
    if intent == "schedule":
        return query_agent.run(question)
    return fallback.run(question)
