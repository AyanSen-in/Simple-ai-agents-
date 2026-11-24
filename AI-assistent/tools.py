"""
Research Tools Module for AI Assistant Agent
Provides Web Search (DuckDuckGo), Knowledge Base Lookup (Wikipedia), and Persistent File Saving.
"""
from datetime import datetime
from pathlib import Path
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_core.tools import Tool


def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    """Appends formatted research data to a local text file with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    target_path = Path(filename)
    if not target_path.is_absolute():
        target_path = Path(__file__).parent / filename

    formatted_text = (
        f"{'=' * 60}\n"
        f"Research Report - Generated: {timestamp}\n"
        f"{'=' * 60}\n\n"
        f"{data.strip()}\n\n"
    )

    try:
        with open(target_path, "a", encoding="utf-8") as f:
            f.write(formatted_text)
        return f"Research successfully saved to {target_path.resolve()}"
    except Exception as e:
        return f"Failed to save data: {e}"


# Tool 1: File Storage Tool
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research summary, findings, or notes to a text file for future reference. Input should be the text content to save.",
)

# Tool 2: DuckDuckGo Live Web Search Tool
search_engine = DuckDuckGoSearchRun()
search_tool = Tool(
    name="web_search",
    func=search_engine.run,
    description="Search the live web for up-to-date facts, current news, technology developments, and specific details.",
)

# Tool 3: Wikipedia In-Depth Encyclopedic Knowledge Tool
wiki_wrapper = WikipediaAPIWrapper(
    top_k_results=2,
    doc_content_chars_max=2500
)
wiki_tool = WikipediaQueryRun(
    name="wikipedia_search",
    description="Search Wikipedia for detailed historical, scientific, conceptual, and encyclopedic overviews.",
    api_wrapper=wiki_wrapper
)

ALL_TOOLS = [search_tool, wiki_tool, save_tool]
