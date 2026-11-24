# 🤖 Autonomous AI Research Assistant Agent

An intelligent, multi-provider autonomous research agent built using **LangChain**, **Tool-Calling Architecture**, and **Pydantic** structured schema validation. The agent plans research steps, searches the live internet, queries Wikipedia for in-depth technical and historical foundations, logs comprehensive reports to disk, and presents structured findings in an interactive terminal session.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-v0.2%2B-green.svg)](https://www.langchain.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🎯 What the Agent Can Do

This agent is designed to function as an autonomous researcher that bridges broad internet retrieval with structured synthesis. Specifically, the agent can:

### 1. 🔍 Autonomous Research Decision Making
* Understands natural language research prompts, ambiguous questions, and technical topics.
* Automatically decides **which tools to call**, **in what sequence**, and **what search queries to formulate**.

### 2. 🌐 Real-Time Web Exploration (`web_search`)
* Uses DuckDuckGo (`ddgs`) to retrieve up-to-the-minute news, recent technical announcements, benchmarks, and live web sources without requiring commercial search API keys.

### 3. 📚 Deep Encyclopedic Fact-Finding (`wikipedia_search`)
* Connects directly to Wikipedia's knowledge base to extract high-density background overviews (up to 2,500 characters of clean context per entity) on science, history, engineering, and mathematics.

### 4. 📝 Factual Synthesis & Source Attribution
* Synthesizes multiple disparate search results into a clean, multi-paragraph factual summary.
* Captures and enumerates all reference URLs, publications, and sources used.

### 5. 💾 Automatic Persistent Report Generation (`save_text_to_file`)
* Automatically records full research findings into a local text log ([research_output.txt](file:///C:/Users/USER/Desktop/AI%20AGENT/AI-assistent/research_output.txt)) with timestamps, separating entries cleanly for offline archiving.

### 6. 🛡️ Schema-Enforced Pydantic Output
* Formulates output strictly adhering to a strongly typed schema:
  * `topic`: Name of the topic investigated.
  * `summary`: Comprehensive, multi-paragraph synthesis.
  * `sources`: Extracted list of links and publications.
  * `tools_used`: Audit trail of which tools were invoked.
* Resilient extraction logic cleans markdown backticks (````json ... ````) and prevents JSON parsing crashes.

### 7. 🔌 Multi-Provider LLM Flexibility
* Supports all leading model providers with automatic discovery:
  * **OpenAI ChatGPT** (`gpt-4o-mini`, `gpt-4o`)
  * **Google Gemini** (`gemini-1.5-flash`, `gemini-2.0-flash`)
  * **Anthropic Claude** (`claude-3-5-sonnet`)
* If no key is configured in `.env`, the assistant interactively prompts you to choose your provider and paste your key on startup.

### 8. 🔁 Continuous Interactive Exploration
* Features an interactive REPL loop allowing you to research question after question without restarting the program.

---

## 📂 Proper Project Structure

```text
AI AGENT/
├── run.py                       # Root launcher for the entire project
├── requirements.txt             # Project-wide dependency specification
├── README.md                    # Main portfolio documentation
├── .gitignore                   # Excludes virtual environments, .env, and caches
└── AI-assistent/
    ├── main.py                  # Agent core, prompt logic & interactive CLI loop
    ├── tools.py                 # Tool wrappers (web_search, wikipedia_search, save_text_to_file)
    ├── .env                     # Your local API credentials (never committed)
    ├── .env.example             # Template for API keys
    ├── requirements.txt         # Module requirements
    ├── research_output.txt      # Automated output log of research reports
    └── venv/                    # Python virtual environment
```

---

## 🛠️ Integrated Research Tools

| Tool Name | Underlying Engine | Responsibility |
| :--- | :--- | :--- |
| **`web_search`** | DuckDuckGo (`ddgs`) | Searches live internet queries for current news, blog posts, documentation, and web sources. |
| **`wikipedia_search`** | Wikipedia API Wrapper | Queries encyclopedic articles (2,500 chars/article, top 2 results) for deep conceptual context. |
| **`save_text_to_file`** | Local File Storage | Writes formatted and timestamped research findings into `research_output.txt`. |

---

## 🚀 Getting Started

### 1. Prerequisites
Ensure Python 3.10+ is installed. The repository already includes a pre-configured virtual environment located in `AI-assistent/venv`.

### 2. Configure Your API Key
Open [AI-assistent/.env](file:///C:/Users/USER/Desktop/AI%20AGENT/AI-assistent/.env) and insert **at least one** of your API keys:

```env
# Option 1: OpenAI
OPENAI_API_KEY="sk-proj-..."

# Option 2: Google Gemini
GEMINI_API_KEY="AIzaSy..."

# Option 3: Anthropic Claude
ANTHROPIC_API_KEY="sk-ant-..."
```

*(Note: If left empty, the assistant will display an interactive menu on launch to let you paste your key and save it automatically).*

---

## 💻 How to Run

Open **PowerShell** or any terminal:

### Method 1: Root Launcher (Recommended)
```powershell
cd "C:\Users\USER\Desktop\AI AGENT"
.\AI-assistent\venv\Scripts\python.exe run.py
```

### Method 2: From the `AI-assistent` Directory
```powershell
cd "C:\Users\USER\Desktop\AI AGENT\AI-assistent"
.\venv\Scripts\python.exe main.py
```

---

## 📋 Example Terminal Output

```text
=================================================================
📑 RESEARCH REPORT: RETRIEVAL-AUGMENTED GENERATION (RAG)
=================================================================

📝 SUMMARY:
-----------------------------------------------------------------
Retrieval-Augmented Generation (RAG) is an architectural framework 
that optimizes the output of large language models by referencing an 
external, authoritative knowledge base before generating a response. 
By combining vector embedding search with neural generation, RAG models 
significantly reduce hallucinations, maintain domain specificity, and 
allow organizations to update facts without retraining model weights...
-----------------------------------------------------------------

🌐 REFERENCE SOURCES:
  [1] https://en.wikipedia.org/wiki/Retrieval-augmented_generation
  [2] https://research.ibm.com/blog/retrieval-augmented-generation-RAG

🔧 TOOLS UTILIZED:
  web_search, wikipedia_search, save_text_to_file
=================================================================
```

---

## 👤 Author
**Ayan Sen**  
* GitHub: [@AyanSen-in](https://github.com/AyanSen-in)
