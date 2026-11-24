"""
AI Research Assistant Agent
An autonomous research agent supporting OpenAI ChatGPT, Google Gemini, and Anthropic Claude.
Equipped with live Web Search, Wikipedia Encyclopedic lookup, and automatic local file logging.
"""
import os
import sys
import re
import json
from pathlib import Path
from typing import List, Any
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# LangChain Agents & LLMs
try:
    from langchain.agents import create_tool_calling_agent, AgentExecutor
except ImportError:
    from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

from langchain_core.language_models.chat_models import BaseChatModel
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


def save_key_to_env(key_name: str, key_val: str) -> None:
    """
    Saves an API key to the local .env file.
    
    Args:
        key_name: Name of the environment variable (e.g. 'OPENAI_API_KEY').
        key_val: The API key string.
    """
    lines = []
    found = False
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith(f"{key_name}="):
                    lines.append(f'{key_name}="{key_val}"\n')
                    found = True
                else:
                    lines.append(line)
    if not found:
        lines.append(f'{key_name}="{key_val}"\n')

    with open(env_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    os.environ[key_name] = key_val
    print(f"✅ Saved {key_name} to {env_path.name}!")


def init_llm(provider: str, api_key: str) -> BaseChatModel:
    """
    Instantiates and returns the chat model corresponding to the chosen provider.
    
    Args:
        provider: 'openai', 'gemini', or 'anthropic'.
        api_key: The valid API key string for that provider.
        
    Returns:
        BaseChatModel: Configured LangChain chat model.
    """
    provider_clean = provider.strip().lower()

    if provider_clean == "openai":
        from langchain_openai import ChatOpenAI
        print("🤖 Active Model: OpenAI ChatGPT (gpt-4o-mini)")
        return ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=api_key)

    elif provider_clean == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("🤖 Active Model: Google Gemini (gemini-1.5-flash)")
        return ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2, google_api_key=api_key)

    elif provider_clean == "anthropic":
        from langchain_anthropic import ChatAnthropic
        print("🤖 Active Model: Anthropic Claude (claude-3-5-sonnet)")
        return ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.2, api_key=api_key)

    raise ValueError(f"Unsupported provider '{provider}'. Must be 'openai', 'gemini', or 'anthropic'.")


def get_llm() -> BaseChatModel:
    """
    Discovers available credentials from environment or interactively prompts the user.
    
    Returns:
        BaseChatModel: Initialized LangChain chat model.
    """
    openai_key = os.getenv("OPENAI_API_KEY", "").strip()
    gemini_key = os.getenv("GEMINI_API_KEY", "").strip() or os.getenv("GOOGLE_API_KEY", "").strip()
    anthropic_key = os.getenv("ANTHROPIC_API_KEY", "").strip()

    # Priority 1: OpenAI
    if openai_key:
        return init_llm("openai", openai_key)

    # Priority 2: Gemini
    if gemini_key:
        return init_llm("gemini", gemini_key)

    # Priority 3: Anthropic
    if anthropic_key:
        return init_llm("anthropic", anthropic_key)

    # If no keys are configured in .env, prompt the user to choose
    print("\n" + "=" * 60)
    print("⚠️  No API Key detected in .env!")
    print("=" * 60)
    print("Please choose your preferred LLM provider:")
    print("  1. OpenAI ChatGPT (requires OPENAI_API_KEY)")
    print("  2. Google Gemini  (requires GEMINI_API_KEY)")
    print("  3. Anthropic Claude (requires ANTHROPIC_API_KEY)")
    print("  4. Exit")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        key = input("Paste your OPENAI_API_KEY: ").strip()
        if key:
            save_key_to_env("OPENAI_API_KEY", key)
            return init_llm("openai", key)

    elif choice == "2":
        key = input("Paste your GEMINI_API_KEY: ").strip()
        if key:
            save_key_to_env("GEMINI_API_KEY", key)
            return init_llm("gemini", key)

    elif choice == "3":
        key = input("Paste your ANTHROPIC_API_KEY: ").strip()
        if key:
            save_key_to_env("ANTHROPIC_API_KEY", key)
            return init_llm("anthropic", key)

    print("\nExiting. Please add an API key to your .env file and run again.")
    sys.exit(1)


def extract_json_payload(raw_text: str) -> dict:
    """
    Parses a JSON object from text, handling markdown code fences.
    
    Args:
        raw_text: The raw output string from the LLM.
        
    Returns:
        dict: Parsed JSON data.
    """
    text = raw_text.strip()
    # Check for markdown code fences: ```json ... ``` or ``` ... ```
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


def parse_research_response(raw_output: Any, default_topic: str) -> ResearchResponse:
    """
    Safely converts the raw agent output into a validated ResearchResponse model.
    
    Args:
        raw_output: Output from agent_executor.invoke().
        default_topic: Fallback topic name if parsing fails.
        
    Returns:
        ResearchResponse: Structured Pydantic model.
    """
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
        # Fallback to plain text summary if model returned freeform text
        return ResearchResponse(
            topic=default_topic,
            summary=raw_text.strip(),
            sources=["Direct LLM & Web Synthesis"],
            tools_used=["web_search", "wikipedia_search"]
        )


def display_research_card(result: ResearchResponse) -> None:
    """
    Renders the research report formatted cleanly in the terminal.
    
    Args:
        result: The validated ResearchResponse instance.
    """
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


def build_agent(llm: BaseChatModel) -> AgentExecutor:
    """
    Constructs the tool-calling LangChain agent executor.
    
    Args:
        llm: Initialized BaseChatModel.
        
    Returns:
        AgentExecutor: Ready-to-run agent pipeline.
    """
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
    return AgentExecutor(
        agent=agent,
        tools=ALL_TOOLS,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=10
    )


def main() -> None:
    """Interactive CLI execution loop."""
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
