"""Ensure project root is on sys.path for Streamlit page scripts."""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
root = str(PROJECT_ROOT)

if root in sys.path:
    sys.path.remove(root)
sys.path.insert(0, root)
