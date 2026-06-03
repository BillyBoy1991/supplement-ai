from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import auth
from core.config import settings

app = FastAPI(title="Supplement AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
