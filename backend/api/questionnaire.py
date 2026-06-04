import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from agent import graph
from api.deps import get_current_user, get_db
from models.db import QuestionnaireSession, User

router = APIRouter(prefix="/questionnaire", tags=["questionnaire"])


class AnswerRequest(BaseModel):
    session_id: uuid.UUID
    answer: object


class StepResponse(BaseModel):
    session_id: uuid.UUID
    finished: bool
    question: dict | None


def _load_session(session_id: uuid.UUID, user: User, db: Session) -> QuestionnaireSession:
    session = db.get(QuestionnaireSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return session


@router.post("/start", response_model=StepResponse, status_code=status.HTTP_201_CREATED)
def start(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = QuestionnaireSession(user_id=user.id)
    db.add(session)
    db.commit()
    db.refresh(session)

    step = graph.start_session(session.id)
    session.responses = step["responses"]
    db.commit()
    return StepResponse(session_id=session.id, finished=step["finished"], question=step["question"])


@router.post("/answer", response_model=StepResponse)
def answer(body: AnswerRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    session = _load_session(body.session_id, user, db)
    if session.completed_at:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Questionnaire already completed")

    step = graph.submit_answer(session.id, body.answer)
    session.responses = step["responses"]
    if step["finished"]:
        session.completed_at = datetime.utcnow()
    db.commit()
    return StepResponse(session_id=session.id, finished=step["finished"], question=step["question"])
