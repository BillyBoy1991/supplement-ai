import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, get_db
from engine.safety import DISCLAIMER, DISCLAIMER_VERSION
from engine.scoring import MODEL_VERSION, build_recommendations
from models.db import QuestionnaireSession, Recommendation, Supplement, User, UserProfile

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.get("/{session_id}")
def get_recommendations(
    session_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.get(QuestionnaireSession, session_id)
    if not session or session.user_id != user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    if not session.completed_at:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Questionnaire not completed")

    supplements = db.query(Supplement).all()
    result = build_recommendations(session.responses, supplements)

    already_persisted = (
        db.query(Recommendation).filter(Recommendation.session_id == session_id).first() is not None
    )
    if not already_persisted:
        db.add(UserProfile(
            user_id=user.id,
            session_id=session_id,
            need_scores=result.need_scores,
            risk_flags=result.safety.risk_flags(),
        ))
        for item in result.items:
            db.add(Recommendation(
                user_id=user.id,
                session_id=session_id,
                supplement_id=item.supplement.id,
                score=item.score,
                score_breakdown=item.breakdown,
                disclaimer_version=DISCLAIMER_VERSION,
                model_version=MODEL_VERSION,
            ))
        db.commit()

    return {
        "session_id": session_id,
        "need_scores": result.need_scores,
        "disclaimer": DISCLAIMER,
        "disclaimer_version": DISCLAIMER_VERSION,
        "advisory": result.safety.advisory_message if result.safety.advisory else None,
        "recommendations": [
            {
                "slug": item.supplement.slug,
                "name": item.supplement.name,
                "category": item.supplement.category,
                "evidence_level": item.supplement.evidence_level,
                "standard_dose": item.supplement.standard_dose,
                "mechanisms": item.supplement.mechanisms,
                "score": item.score,
                "score_breakdown": item.breakdown,
                "safety_flags": item.safety_flags,
            }
            for item in result.items
        ],
    }
