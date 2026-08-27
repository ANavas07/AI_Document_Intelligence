import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

# Place for storing all reusable project settings in one place
@dataclass(frozen=True)
class AppSettings:
    project_root: Path
    raw_data_dir: Path
    processed_data_dir: Path
    output_data_dir: Path
    ai_api_key: str | None
    embedding_model: str
    chat_model: str
    retrieval_distance_threshold: float
    ai_url: str | None

# Load AppSettings
def load_settings() -> AppSettings:
    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")

    return AppSettings(
        project_root=project_root,
        raw_data_dir=project_root / "data" / "raw",
        processed_data_dir=project_root / "data" / "processed",
        output_data_dir=project_root / "data" / "output",
        ai_api_key=os.getenv("AI_API_KEY"),
        embedding_model=os.getenv("AI_EMBEDDING_MODEL", "google/embeddinggemma-300m"),
        chat_model=os.getenv("AI_CHAT_MODEL", "Qwen3.5-4B"),
        retrieval_distance_threshold=float(
            os.getenv("RETRIEVAL_DISTANCE_THRESHOLD", "1.25")
        ),
        ai_url =os.getenv("AI_URL")
    )

# Validate Open AI Settings
def validate_ai_settings(settings: AppSettings) -> bool:
    return bool(settings.ai_api_key)