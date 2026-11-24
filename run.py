"""
AI AGENT Root Launcher
Allows running the AI Assistant Agent directly from the project root directory.
"""
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
AGENT_DIR = ROOT_DIR / "AI-assistent"
MAIN_SCRIPT = AGENT_DIR / "main.py"

# Detect Python virtual environment in either root or submodule
VENV_CANDIDATES = [
    ROOT_DIR / "venv" / "Scripts" / "python.exe",
    AGENT_DIR / "venv" / "Scripts" / "python.exe",
]


def find_python_executable() -> str:
    for candidate in VENV_CANDIDATES:
        if candidate.is_file():
            return str(candidate)
    return sys.executable


def main():
    python_exec = find_python_executable()
    print(f"Starting AI Research Assistant via {python_exec} ...\n")
    try:
        subprocess.run([python_exec, str(MAIN_SCRIPT)], cwd=str(AGENT_DIR))
    except KeyboardInterrupt:
        print("\nSession ended.")


if __name__ == "__main__":
    main()
