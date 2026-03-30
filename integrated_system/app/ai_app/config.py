from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "lab8_adapted_model"
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "TinyLlama/TinyLlama-1.1B-Chat-v1.0")
LOCAL_BASE_MODEL_PATH = os.getenv("LOCAL_BASE_MODEL_PATH")
KNOWLEDGE_BASE_PATH = Path(
    os.getenv("KNOWLEDGE_BASE_PATH", BASE_DIR / "knowledge_base.json")
)
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE")
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", "3"))
