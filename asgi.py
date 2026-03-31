import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "server"))

from main import app  # noqa: E402 — imports server/main.py

__all__ = ["app"]
