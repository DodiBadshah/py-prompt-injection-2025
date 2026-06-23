"""
Core configuration for py-prompt-injection-2025.
Loads settings from environment variables with sensible defaults.
"""

from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Config(BaseModel):
    anthropic_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    mlflow_tracking_uri: str = "sqlite:///mlflow.db"
    mlflow_experiment_name: str = "llm-probe-2025"
    reports_dir: Path = Path("reports")
    default_timeout: int = 180
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> Config:
        return cls(
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY", ""),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            mlflow_tracking_uri=os.getenv("MLFLOW_TRACKING_URI", "sqlite:///mlflow.db"),
            mlflow_experiment_name=os.getenv(
                "MLFLOW_EXPERIMENT_NAME", "llm-probe-2025"
            ),
            reports_dir=Path(os.getenv("REPORTS_DIR", "reports")),
            default_timeout=int(os.getenv("DEFAULT_TIMEOUT", "180")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


config = Config.from_env()
