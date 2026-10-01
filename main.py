"""Entrypoint: CLI chat loop, or FastAPI web service.

Run CLI:     python main.py
Run web:      uvicorn main:app --reload
"""
from fastapi import FastAPI
from pydantic import BaseModel
from agents.orchestrator import answer

app = FastAPI(title="Campus Multi-Agent Demo")


class Ask(BaseModel):
    question: str


@app.post("/ask")
def ask(body: Ask):
    return {"question": body.question, "answer": answer(body.question)}


@app.get("/")
def root():
    return {"ok": True, "service": "campus-multi-agent-demo",
            "docs": "/docs"}


def cli():
    print("Campus assistant demo. Type 'exit' to quit.")
    while True:
        q = input("\n> ").strip()
        if not q or q.lower() in {"exit", "quit"}:
            break
        try:
            print(answer(q))
        except Exception as e:
            print(f"[error] {e}")


if __name__ == "__main__":
    cli()
