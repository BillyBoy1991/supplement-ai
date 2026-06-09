"""
Explicaciones personalizadas vía LLM (OpenRouter).

El LLM SOLO redacta texto para una recomendación ya decidida por el motor
determinista. No decide qué recomendar ni si incluir el disclaimer. Cualquier
fallo de la llamada deja la explicación en None: la recomendación determinista
siempre llega al usuario.
"""
import logging
import time

import httpx

from core.config import settings
from engine.safety import DISCLAIMER

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 10.0
RATE_LIMIT_RETRY_DELAY = 2.0


def _system_prompt() -> str:
    return (
        "Eres un asistente de bienestar que redacta explicaciones breves y empáticas "
        "sobre por qué un suplemento concreto encaja con el perfil de una persona. "
        "La recomendación YA ha sido decidida por un motor determinista; tu única tarea "
        "es redactar 2-3 frases en español, cercanas y claras, conectando el suplemento "
        "con las necesidades del perfil. No diagnostiques, no prometas resultados médicos, "
        "no sugieras dosis y no contradigas ni cuestiones la recomendación. "
        f"Ten siempre presente este aviso, que enmarca tu respuesta: {DISCLAIMER}"
    )


def _user_prompt(need_scores: dict, supplement, score_breakdown: dict) -> str:
    top_needs = sorted(need_scores.items(), key=lambda kv: -kv[1])[:3]
    needs_txt = ", ".join(f"{cat} ({val})" for cat, val in top_needs) or "sin necesidades destacadas"
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


def generate_explanation(user_profile: dict, supplement, score_breakdown: dict) -> str | None:
    """Devuelve una explicación de 2-3 frases, o None si la llamada al LLM falla.

    Ante un 429 (rate limit del tier :free) reintenta UNA vez tras una pausa.
    """
    payload = {
        "model": settings.openrouter_model,
        "messages": [
            {"role": "system", "content": _system_prompt()},
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
