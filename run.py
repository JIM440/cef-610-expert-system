import os
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

env = os.environ.copy()
env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")

subprocess.run(
    [sys.executable, "-m", "streamlit", "run", str(ROOT / "app" / "ui" / "streamlit_app.py")],
    cwd=ROOT,
    env=env,
    check=False,
)
