import time
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.deps import get_current_user, get_db
from engine.explanations import generate_explanation
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

    existing = db.query(Recommendation).filter(Recommendation.session_id == session_id).all()
    if existing:
        explanations = {r.supplement_id: r.llm_explanation for r in existing}
    else:
        explanations = {}
        db.add(UserProfile(
            user_id=user.id,
            session_id=session_id,
            need_scores=result.need_scores,
            risk_flags=result.safety.risk_flags(),
        ))
        # Solo las top 3 reciben explicación IA, secuencialmente y con pausa entre
        # llamadas, para no saturar el rate limit del modelo :free de OpenRouter.
        for i, item in enumerate(result.items):
            if i < 3:
                if i > 0:
                    time.sleep(0.6)
                explanation = generate_explanation(result.need_scores, item.supplement, item.breakdown, db)
            else:
                explanation = None
            explanations[item.supplement.id] = explanation
            db.add(Recommendation(
                user_id=user.id,
                session_id=session_id,
                supplement_id=item.supplement.id,
                score=item.score,
                score_breakdown=item.breakdown,
                llm_explanation=explanation,
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
                "llm_explanation": explanations.get(item.supplement.id),
            }
            for item in result.items
        ],
    }
