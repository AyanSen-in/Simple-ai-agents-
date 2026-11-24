# 🤖 AI Research Assistant Agent (Core Module)

The core module powering the autonomous research assistant. Built on LangChain tool-calling agents with multi-provider model support (OpenAI ChatGPT, Google Gemini, Anthropic Claude).

---

## 🎯 Agent Capabilities
- **Autonomous Query Decomposition**: Determines whether queries require live internet data, encyclopedic background, or both.
- **Live Internet Scraping**: Uses `ddgs` to pull real-time web results.
- **Encyclopedic Retrieval**: Pulls comprehensive Wikipedia context.
- **Automatic Persistence**: Appends timestamped findings to `research_output.txt`.
- **Structured Schema Enforcer**: Validates outputs using `ResearchResponse` Pydantic models.

---

## 💻 Execution Command

```powershell
.\venv\Scripts\python.exe main.py
```

### Key Files
- [main.py](file:///C:/Users/USER/Desktop/AI%20AGENT/AI-assistent/main.py): Agent execution loop, prompt templates, and multi-model dispatch.
- [tools.py](file:///C:/Users/USER/Desktop/AI%20AGENT/AI-assistent/tools.py): Live web search, Wikipedia wrapper, and file storage functions.
- [.env](file:///C:/Users/USER/Desktop/AI%20AGENT/AI-assistent/.env): API keys storage (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `ANTHROPIC_API_KEY`).
- [research_output.txt](file:///C:/Users/USER/Desktop/AI%20AGENT/AI-assistent/research_output.txt): Auto-generated output records.
