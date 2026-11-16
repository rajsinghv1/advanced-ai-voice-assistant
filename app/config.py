
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
APP_NAME = os.getenv("APP_NAME", "Advanced AI Voice Assistant")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY missing. Please configure your .env file."
    )
