"""
Explicaciones personalizadas vía LLM (OpenRouter) con RAG sobre pgvector.

El LLM SOLO redacta texto para una recomendación ya decidida por el motor
determinista. No decide qué recomendar ni si incluir el disclaimer. Antes de
redactar se recuperan fragmentos de evidencia por similitud coseno; si esa
búsqueda falla (sin pgvector, sin embeddings, error de DB) se degrada a la
llamada sin contexto de la Fase 2a. Cualquier fallo del LLM deja la
explicación en None: la recomendación determinista siempre llega al usuario.
"""
import logging
import time

import httpx
from sqlalchemy.orm import Session

from core.config import settings
from engine.embeddings import get_embedding
from engine.safety import DISCLAIMER
from models.db import EvidenceChunk

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 10.0
RATE_LIMIT_RETRY_DELAY = 2.0
EVIDENCE_LIMIT = 3


def _top_needs(need_scores: dict) -> list[tuple[str, float]]:
    return sorted(need_scores.items(), key=lambda kv: -kv[1])[:3]


def _retrieve_evidence(db: Session, supplement, need_scores: dict) -> list[EvidenceChunk]:
    needs = ", ".join(cat for cat, _ in _top_needs(need_scores))
    query_embedding = get_embedding(f"{supplement.name}: {needs}")
    return (
        db.query(EvidenceChunk)
        .filter(EvidenceChunk.supplement_slug == supplement.slug)
        .order_by(EvidenceChunk.embedding.cosine_distance(query_embedding))
        .limit(EVIDENCE_LIMIT)
        .all()
    )


def _system_prompt(evidence: list[EvidenceChunk]) -> str:
    evidence_block = ""
    if evidence:
        lines = "\n".join(f"- {chunk.content} [{chunk.source}]" for chunk in evidence)
        evidence_block = (
        "Apóyate ÚNICAMENTE en esta evidencia científica. "
        "Cuando uses información de un fragmento, cítalo inline con exactamente "
        "el texto entre corchetes que aparece al final de ese fragmento, "
        "por ejemplo: [PubMed 2021 · PMID:34883514]. "
        "No inventes datos ni afirmaciones que no estén en la evidencia:\n"
        f"Evidencia relevante:\n{lines}\n"
        )
    return (
        "Eres un asistente de bienestar que redacta explicaciones breves y empáticas "
        "sobre por qué un suplemento concreto encaja con el perfil de una persona. "
        "La recomendación YA ha sido decidida por un motor determinista; tu única tarea "
        "es redactar 2-3 frases en español, cercanas y claras, conectando el suplemento "
        "con las necesidades del perfil. No diagnostiques, no prometas resultados médicos, "
        "no sugieras dosis y no contradigas ni cuestiones la recomendación. "
        f"{evidence_block}"
        f"Ten siempre presente este aviso, que enmarca tu respuesta: {DISCLAIMER}"
    )


def _user_prompt(need_scores: dict, supplement, score_breakdown: dict) -> str:
    needs_txt = ", ".join(f"{cat} ({val})" for cat, val in _top_needs(need_scores)) or "sin necesidades destacadas"
    contributions = score_breakdown.get("category_contributions", {})
    contrib_txt = ", ".join(contributions.keys()) or "—"
    mechanisms = ", ".join(getattr(supplement, "mechanisms", []) or []) or "n/d"
    return (
        f"Perfil del usuario — necesidades principales: {needs_txt}.\n"
        f"Suplemento recomendado: {supplement.name} (categoría: {supplement.category}).\n"
        f"Mecanismos: {mechanisms}.\n"
        f"Encaja por estas categorías de necesidad: {contrib_txt}.\n"
        "Redacta la explicación personalizada."
    )


def generate_explanation(user_profile: dict, supplement, score_breakdown: dict, db: Session) -> str | None:
    """Devuelve una explicación de 2-3 frases, o None si la llamada al LLM falla.

    Ante un 429 (rate limit del tier :free) reintenta UNA vez tras una pausa.
    """
    try:
        evidence = _retrieve_evidence(db, supplement, user_profile)
    except Exception as exc:  # degradación elegante: sin evidencia, prompt de Fase 2a
        logger.warning("Evidencia RAG no disponible para %s: %s", getattr(supplement, "slug", "?"), exc)
        evidence = []

    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": _system_prompt(evidence)},
            {"role": "user", "content": _user_prompt(user_profile, supplement, score_breakdown)},
        ],
    }

    def _post() -> httpx.Response:
        return httpx.post(
            f"{settings.openrouter_base_url}/chat/completions",
            timeout=TIMEOUT_SECONDS,
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
            json=payload,
        )

    try:
        response = _post()
        if response.status_code == 429:
            logger.warning("OpenRouter 429 (rate limit) para %s; reintento en %.0fs",
                           getattr(supplement, "slug", "?"), RATE_LIMIT_RETRY_DELAY)
            time.sleep(RATE_LIMIT_RETRY_DELAY)
            response = _post()
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"].strip()
        return content or None
    except Exception as exc:  # robustez: la recomendación nunca se rompe por el LLM
        logger.warning("Explicación LLM no disponible para %s: %s", getattr(supplement, "slug", "?"), exc)
        return None
