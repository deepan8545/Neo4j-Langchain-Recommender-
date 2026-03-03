import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()

def require_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {var_name}")
    return value
