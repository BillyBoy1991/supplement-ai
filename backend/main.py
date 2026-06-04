from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent.graph import setup_checkpointer
from api import auth, questionnaire, recommendations
from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_checkpointer()
    yield


app = FastAPI(title="Supplement AI API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(questionnaire.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")


@app.get("/api/health")
def health():
    return {"status": "ok"}
