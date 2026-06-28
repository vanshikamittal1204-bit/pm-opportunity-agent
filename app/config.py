"""Configuration management for the PM Opportunity Agent."""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application configuration loaded from environment variables."""

    GEMINI_API_KEY: str
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_CHAT_ID: str
    GOOGLE_SHEETS_ID: str
    SQLITE_DATABASE_PATH: str
    JOB_MATCH_THRESHOLD: int


def _require(name: str) -> str:
    """Load a required environment variable, raising ValueError if absent or empty."""
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(
            f"Required environment variable '{name}' is missing or empty. "
            "Add it to your .env file before starting the application."
        )
    return value


def _optional_str(name: str, default: str) -> str:
    """Load an optional string environment variable, returning default if absent or empty."""
    value = os.environ.get(name, "").strip()
    return value if value else default


def _optional_int(
    name: str,
    default: int,
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    """Load an optional integer environment variable, returning default if absent.

    Raises ValueError if the value cannot be parsed as an integer or falls
    outside the allowed range.
    """
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default

    try:
        value = int(raw)
    except ValueError:
        raise ValueError(
            f"Environment variable '{name}' must be an integer. "
            "Check your .env file and correct the value."
        )

    if min_value is not None and value < min_value:
        raise ValueError(
            f"Environment variable '{name}' must be at least {min_value}. Got {value}."
        )

    if max_value is not None and value > max_value:
        raise ValueError(
            f"Environment variable '{name}' must be at most {max_value}. Got {value}."
        )

    return value


def _build_settings() -> Settings:
    """Load and validate all configuration from environment variables."""
    return Settings(
        GEMINI_API_KEY=_require("GEMINI_API_KEY"),
        TELEGRAM_BOT_TOKEN=_require("TELEGRAM_BOT_TOKEN"),
        TELEGRAM_CHAT_ID=_require("TELEGRAM_CHAT_ID"),
        GOOGLE_SHEETS_ID=_require("GOOGLE_SHEETS_ID"),
        SQLITE_DATABASE_PATH=_optional_str("SQLITE_DATABASE_PATH", "data/jobs.db"),
        JOB_MATCH_THRESHOLD=_optional_int("JOB_MATCH_THRESHOLD", default=75, min_value=0, max_value=100),
    )


settings: Settings = _build_settings()
