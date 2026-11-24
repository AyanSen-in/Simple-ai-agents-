"""
AI Research Assistant Agent
An intelligent agent that gathers web and Wikipedia data, saves findings, and outputs structured research summaries.
"""
import os
import sys
import re
import json
from pathlib import Path
from typing import List, Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# LangChain Agents & Prompts
try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
except ImportError:
    from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

# Tools
from tools import ALL_TOOLS


class ResearchResponse(BaseModel):
    """Structured response schema for research queries."""
    topic: str = Field(description="The primary subject or topic researched")
    summary: str = Field(description="A comprehensive, factual multi-paragraph summary of findings")
    sources: List[str] = Field(default_factory=list, description="List of URLs, articles, or reference sources gathered")
    tools_used: List[str] = Field(default_factory=list, description="Names of tools used during the research process")


def get_llm():
    """Initializes and returns an LLM based on configured environment variables."""
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("GOOGLE_API_KEY", "").strip()
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    # 1. Check for OpenAI
    if openai_key:
        try:
            from langchain_openai import ChatOpenAI
            print("🤖 Using LLM Provider: OpenAI (gpt-4o-mini)")
            return ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=openai_key)
        except Exception as e:
            print(f"[!] Failed to initialize OpenAI: {e}")

    # 2. Check for Google Gemini
    if gemini_key:
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            print("🤖 Using LLM Provider: Google Gemini (gemini-1.5-flash)")
            return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=gemini_key)
        except Exception as e:
            print(f"[!] Failed to initialize Gemini: {e}")

    # 3. Check for Anthropic Claude
    if anthropic_key:
        try:
            from langchain_anthropic import ChatAnthropic
            print("🤖 Using LLM Provider: Anthropic (claude-3-5-sonnet)")
            return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.2, api_key=anthropic_key)
        except Exception as e:
            print(f"[!] Failed to initialize Anthropic: {e}")

    # If no keys configured, prompt interactively
    print("\n" + "=" * 60)
    print("⚠️  No API Key detected in .env!")
    print("=" * 60)
    print("Please choose an LLM provider to configure:")
    print("  1. OpenAI (requires OPENAI_API_KEY)")
    print("  2. Google Gemini (requires GEMINI_API_KEY)")
    print("  3. Anthropic Claude (requires ANTHROPIC_API_KEY)")
    print("  4. Exit")

    choice = input("\nEnter choice (1-4): ").strip()
    if choice == "1":
        key = input("Paste your OPENAI_API_KEY: ").strip()
        if key:
            save_key_to_env("OPENAI_API_KEY", key)
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=key)
    elif choice == "2":
        key = input("Paste your GEMINI_API_KEY: ").strip()
        if key:
            save_key_to_env("GEMINI_API_KEY", key)
            from langchain_google_genai import ChatGoogleGenerativeAI
            return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=key)
    elif choice == "3":
        key = input("Paste your ANTHROPIC_API_KEY: ").strip()
        if key:
            save_key_to_env("ANTHROPIC_API_KEY", key)
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.2, api_key=key)

    print("\nExiting. Please update your .env file with a valid API key and run again.")
    sys.exit(1)


def save_key_to_env(key_name: str, key_val: str):
    """Saves a provided API key to the local .env file."""
    lines = []
    found = False
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    lines.append(f"{key_name}=\"{key_val}\"\n")
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f"{key_name}=\"{key_val}\"\n")

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    os.environ[key_name] = key_val
    print(f"✅ Saved {key_name} to {env_path.name}!")


def extract_json_payload(raw_text: str) -> dict:
    """Extracts and parses JSON object from LLM response text."""
    text = raw_text.strip()
    # Check for markdown code fences
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1)
    else:
        # Fall back to finding matching outer curly braces
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            text = text[start:end + 1]

    return json.loads(text)


def parse_research_response(raw_output, default_topic: str) -> ResearchResponse:
    """Safely converts raw agent output into a ResearchResponse model."""
    # Handle list or dict output formats from different LangChain variants
    if isinstance(raw_output, list) and len(raw_output) > 0:
        if isinstance(raw_output[0], dict) and "text" in raw_output[0]:
            raw_text = raw_output[0]["text"]
        else:
            raw_text = str(raw_output[0])
    elif isinstance(raw_output, dict):
        raw_text = raw_output.get("output", str(raw_output))
    else:
        raw_text = str(raw_output)

    try:
        data = extract_json_payload(raw_text)
        return ResearchResponse(**data)
    except Exception:
        # Graceful fallback: construct model from plain text output
        return ResearchResponse(
            topic=default_topic,
            summary=raw_text.strip(),
            sources=["Direct LLM & Web Synthesis"],
            tools_used=["web_search", "wikipedia_search"]
        )


def display_research_card(result: ResearchResponse):
    """Renders a formatted card of the research output to the terminal."""
    print("\n" + "=" * 65)
    print(f"📑 RESEARCH REPORT: {result.topic.upper()}")
    print("=" * 65)
    print("\n📝 SUMMARY:")
    print("-" * 65)
    print(result.summary)
    print("-" * 65)

    if result.sources:
        print("\n🌐 REFERENCE SOURCES:")
        for idx, src in enumerate(result.sources, 1):
            print(f"  [{idx}] {src}")

    if result.tools_used:
        print("\n🔧 TOOLS UTILIZED:")
        print(f"  {', '.join(result.tools_used)}")

    print("=" * 65 + "\n")


def build_agent(llm):
    """Builds and returns the LangChain Tool-Calling AgentExecutor."""
    parser = PydanticOutputParser(pydantic_object=ResearchResponse)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert AI Research Assistant. Your mission is to gather comprehensive, accurate, and objective information on the user's research topic.

Instructions:
1. Use 'web_search' for current news, fresh developments, or specific queries.
2. Use 'wikipedia_search' for deep encyclopedic, historical, or scientific context.
3. Use 'save_text_to_file' to automatically record your final comprehensive summary to disk.
4. Always formulate your final answer strictly adhering to the JSON schema provided below. Do not include markdown preamble or postscript outside the JSON structure.

{format_instructions}
""",
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]
    ).partial(format_instructions=parser.get_format_instructions())

    agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=ALL_TOOLS)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )
    return agent_executor


def main():
    print("\n" + "=" * 60)
    print("          🔍 AI RESEARCH ASSISTANT AGENT")
    print("=" * 60)

    llm = get_llm()
    agent_executor = build_agent(llm)

    print("\nAgent initialized and ready! (Type 'exit' or 'quit' to end session)\n")

    while True:
        try:
            query = input("💡 What topic or question would you like to research? ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting session. Goodbye!")
            break

        if not query:
            continue
        if query.lower() in ("exit", "quit", "q"):
            print("Exiting AI Research Assistant. Happy learning!")
            break

        print(f"\n🚀 Initiating research on: '{query}' ...\n")
        try:
            raw_response = agent_executor.invoke({"query": query})
            output_content = raw_response.get("output", "")
            structured = parse_research_response(output_content, default_topic=query)
            display_research_card(structured)
        except Exception as e:
            print(f"\n❌ Research process encountered an error: {e}")


if __name__ == "__main__":
    main()
