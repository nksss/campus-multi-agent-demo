"""Fallback agent: safe, polite refusal for out-of-scope / off-topic questions."""


def run(question: str) -> str:
    return ("你好，我是校园助手，目前只能帮你查询考勤和课程安排相关的问题。"
            "其他问题我暂时无法回答，如需帮助请联系班主任或教务处老师。")
