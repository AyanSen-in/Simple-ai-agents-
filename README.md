# 🤖 AI Research Assistant Agent

An autonomous research agent built with **LangChain**, **Tool-Calling Agents**, and **Pydantic** structured output validation. The agent dynamically searches the live web, queries Wikipedia for in-depth encyclopedic context, writes detailed reports to persistent storage, and returns structured findings.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-v0.2%2B-green.svg)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features

- **🌐 Live Web Search**: Uses DuckDuckGo (`ddgs`) to gather fresh, real-time web results and news without requiring search API keys.
- **📚 Wikipedia Knowledge Base**: Deep encyclopedic query wrapper retrieving up to 2,500 characters of high-density context per topic.
- **💾 Automatic Persistent Storage**: Automatically writes and timestamps full research findings to `research_output.txt`.
- **🎯 Multi-Provider Model Support**: Seamlessly works with:
  - **OpenAI** (`gpt-4o-mini`, `gpt-4o`)
  - **Google Gemini** (`gemini-1.5-flash`, `gemini-2.0-flash`)
  - **Anthropic Claude** (`claude-3-5-sonnet`)
- **🛡️ Robust Output Parsing**: Eliminates LLM formatting crashes by stripping markdown fences (` ```json `), extracting valid JSON, and parsing into validated Pydantic models.
- **🔁 Interactive Terminal Session**: Continuous research loop allowing you to explore multiple topics in a single run.

---

## 📂 Project Structure

```text
AI AGENT/
├── run.py                     # Root launcher script
├── requirements.txt           # Consolidated dependencies
├── README.md                  # Main documentation
└── AI-assistent/
    ├── main.py                # Agent core logic & CLI interface
    ├── tools.py               # Web search, Wikipedia & file storage tools
    ├── .env                   # API keys configuration (ignored by git)
    ├── .env.example           # Template for environment variables
    ├── requirements.txt       # Module dependencies
    ├── research_output.txt    # Saved research output file
    └── venv/                  # Python virtual environment
```

---

## 🚀 Quick Start

### 1. Prerequisites & Virtual Environment

Ensure you have Python 3.10+ installed. A virtual environment is already configured in `AI-assistent/venv`.

If setting up fresh:
```bash
# Navigate to the project folder
cd "C:\Users\USER\Desktop\AI AGENT"

# Activate the existing virtual environment (Windows PowerShell)
.\AI-assistent\venv\Scripts\Activate.ps1

# (Optional) Install dependencies
pip install -r requirements.txt
```

### 2. Configure Your API Key

Edit `AI-assistent\.env` (or copy from `.env.example`) and add your preferred provider's API key:

```env
# Choose at least ONE provider:
OPENAI_API_KEY="your-openai-api-key"
# or
GEMINI_API_KEY="your-gemini-api-key"
# or
ANTHROPIC_API_KEY="your-anthropic-api-key"
```

> **Note:** If no API key is pre-configured in `.env`, the assistant will prompt you interactively when launched and save your key automatically.

---

## 💻 How to Run

You can run the agent directly using any of these commands:

### Method A: Run with Root Launcher (Easiest)
```powershell
cd "C:\Users\USER\Desktop\AI AGENT"
.\AI-assistent\venv\Scripts\python.exe run.py
```

### Method B: Run directly from `AI-assistent`
```powershell
cd "C:\Users\USER\Desktop\AI AGENT\AI-assistent"
.\venv\Scripts\python.exe main.py
```

---

## 🛠️ Integrated Research Tools

| Tool | Purpose | Source |
| :--- | :--- | :--- |
| `web_search` | Real-time live web facts, current developments, and reference URLs | DuckDuckGo Search API (`ddgs`) |
| `wikipedia_search` | Deep encyclopedic context, background history, and definitions | Wikipedia API Wrapper |
| `save_text_to_file` | Records structured research reports directly to local disk | Local File System (`research_output.txt`) |

---

## 📊 Example Research Output

```text
=================================================================
📑 RESEARCH REPORT: QUANTUM COMPUTING IN DRUG DISCOVERY
=================================================================

📝 SUMMARY:
-----------------------------------------------------------------
Quantum computing leverages qubits and superposition to simulate 
molecular interactions at quantum mechanical accuracy. This 
exponentially accelerates lead optimization and binding affinity 
prediction compared to classical molecular dynamics simulations...
-----------------------------------------------------------------

🌐 REFERENCE SOURCES:
  [1] https://en.wikipedia.org/wiki/Quantum_computing
  [2] https://www.nature.com/articles/quantum-drug-design

🔧 TOOLS UTILIZED:
  web_search, wikipedia_search, save_text_to_file
=================================================================
```

---

## 👤 Author
**Ayan Sen**  
* GitHub: [@AyanSen-in](https://github.com/AyanSen-in)
