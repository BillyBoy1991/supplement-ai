import os
import sys
from pathlib import Path

# Variables mínimas para que core.config.Settings cargue sin un .env real.
os.environ.setdefault("DATABASE_URL", "postgresql+psycopg://u:p@db:5432/x")
os.environ.setdefault("JWT_SECRET", "test-secret")
os.environ.setdefault("OPENROUTER_API_KEY", "test-key")

# backend/ en el path para imports absolutos (core, engine, agent).
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
