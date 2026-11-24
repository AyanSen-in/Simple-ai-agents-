"""
AI AGENT Root Launcher
Allows running the AI Assistant Agent directly from the project root directory.
"""
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
AGENT_DIR = ROOT_DIR / "AI-assistent"
VENV_PYTHON = AGENT_DIR / "venv" / "Scripts" / "python.exe"
MAIN_SCRIPT = AGENT_DIR / "main.py"


def main():
    python_exec = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    print(f"Starting AI Research Assistant via {python_exec} ...\n")
    try:
        subprocess.run([python_exec, str(MAIN_SCRIPT)], cwd=str(AGENT_DIR))
    except KeyboardInterrupt:
        print("\nSession ended.")


if __name__ == "__main__":
    main()
