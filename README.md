# Campus Multi-Agent AI Assistant — Demo

A minimal, runnable reconstruction of a production multi-agent assistant I built for a K-12
smart-campus platform (serving teachers, students, and parents). This repo strips out all
private data and internal systems to show the **architecture and engineering decisions**, not
the business logic.

## What this demo shows

- **Orchestrator + sub-agent pattern**: one main agent owns intent classification, task
  planning and final answer synthesis; specialized sub-agents handle a single domain.
- **MCP-style tool layer**: business-semantic tools only (`query_student_attendance`,
  `get_course_schedule`, ...) — no arbitrary SQL surface. Swap the underlying LLM without
  touching the tools.
- **Safety & degradation**: per-task retry caps, timeouts, and a fallback agent for
  failures / out-of-scope / off-topic questions.
- **Eval-friendly**: a small golden-case file you can extend.

> This is a demo. The production system also had: Redis short-term memory, Milvus long-term
> user profiles, shadow-mode → staged rollout, full-trace monitoring, and on-prem DeepSeek
> deployment for PII compliance. Those are described in `docs/ARCHITURE.md` but not wired up
> here to keep the demo ~300 lines.

## Architecture

```
                    ┌─────────────────────────┐
   user query ───▶ │   Orchestrator Agent      │
                    │  (intent + planning)     │
                    └──────┬──────────┬───────┘
                           │          │
              ┌────────────▼─┐    ┌───▼─────────────┐
              │ Attendance   │    │  Academics      │
              │ Sub-agent    │    │  Sub-agent      │
              └────┬─────────┘    └───┬─────────────┘
                   │                  │
              ┌────▼──────────────────▼────┐
              │  MCP-style Tools            │
              │  (mock CSV data sources)   │
              └─────────────────────────────┘
                           │
                   fallback agent if anything fails / off-topic
```

## Quick start

```bash
python -m venv .venv && . .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env     # then edit .env and put your DeepSeek API key in
python main.py
```

Then ask questions:

```
> 张三今天考勤怎么样？
> 明天下午第二节是什么课？
> 帮我写一首诗
```

The third one should be refused by the fallback agent — that's the 10% "must-refuse" path.

You can also run it as a web service:

```bash
uvicorn main:app --reload
# open http://localhost:8000/docs for a Swagger UI
```

## Layout

```
agents/
  orchestrator.py     # main agent: routes intent, calls sub-agents, synthesizes answer
  attendance_agent.py # attendance domain
  query_agent.py      # academics domain (schedule, grades)
  fallback.py         # safe refusal / degradation
tools/
  attendance_tools.py # MCP-style tools backed by mock CSV
  academics_tools.py
data/
  attendance.csv      # mock attendance records
  courses.csv         # mock schedule
eval/
  golden_cases.md     # example end-to-end test cases
main.py               # FastAPI + CLI entrypoint
```

## Design notes (the stuff clients actually ask about)

**Why multi-agent instead of one big prompt?**
When the system grows, a single prompt either hallucinates tool calls or loops. The
orchestrator pattern keeps each sub-agent's tool surface small and auditable, and makes
the failure modes explicit.

**Why not expose a generic "run SQL" tool?**
Two reasons: (1) the model will eventually generate something destructive, and (2) you lose
the ability to change the underlying data store. Every tool has a narrow, named signature —
the LLM picks the tool, our code executes it.

**What happens when a sub-agent loops?**
Production had a 3-retry cap + 10s per-call timeout + 60s overall timeout. On timeout, the
orchestrator looks at partial results: if they contain valid answer-bearing fields it
converges, otherwise it falls back to a canned message and logs the failure for eval.

## Stack

- Python 3.11+
- LangChain
- DeepSeek Chat (OpenAI-compatible API)
- FastAPI (optional web layer)
- Mock CSV data (no real DB required)
