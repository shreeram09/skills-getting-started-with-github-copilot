import os
import sys

# Ensure the repository `src` directory is on sys.path during tests so imports
# like `from src.main import ...` work regardless of how pytest is invoked.
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
