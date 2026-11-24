# 🤖 AI Research Assistant Agent (AI-assistent)

An autonomous LangChain tool-calling agent that performs web and encyclopedic research, saves timestamped reports to disk, and returns structured Pydantic models.

---

## 🚀 Execution Guide

Run from this folder:
```powershell
.\venv\Scripts\python.exe main.py
```

### Key Files
- `main.py`: Interactive CLI, multi-provider LLM loader (OpenAI, Gemini, Claude), Pydantic parsing.
- `tools.py`: Live DuckDuckGo search, Wikipedia lookup (2500 chars), and file writer.
- `.env`: Environment variables (`OPENAI_API_KEY`, `GEMINI_API_KEY`, or `ANTHROPIC_API_KEY`).
- `research_output.txt`: Generated research logs and full reports.
