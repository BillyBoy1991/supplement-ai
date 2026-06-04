"""
Motor de puntuación determinista.

need_scores = Σ por cada respuesta de sus contribuciones de categoría.
score del suplemento = (Σ need_score[cat] × need_weight[cat]) × multiplicador_evidencia.
Cero LLM, reproducible.
"""
from dataclasses import dataclass

from agent.questions import ORDER, needs_for
from engine.safety import SafetyResult, evaluate

MODEL_VERSION = "1.0.0"
EVIDENCE_MULTIPLIER = {"A": 1.0, "B": 0.85, "C": 0.7, "D": 0.5}


def compute_need_scores(responses: dict) -> dict[str, float]:
    scores: dict[str, float] = {}
    for qid in ORDER:
        if qid not in responses:
            continue
        for cat, val in needs_for(qid, responses[qid]).items():
            scores[cat] = round(scores.get(cat, 0.0) + val, 4)
    return scores


def _score_supplement(need_scores: dict[str, float], supplement) -> tuple[float, dict]:
    weights = supplement.need_weights or {}
    contributions = {
        cat: round(need_scores[cat] * w, 4)
        for cat, w in weights.items()
        if need_scores.get(cat, 0.0) > 0
    }
    raw = sum(contributions.values())
    multiplier = EVIDENCE_MULTIPLIER.get(supplement.evidence_level, 0.7)
    breakdown = {
        "raw_score": round(raw, 4),
        "evidence_level": supplement.evidence_level,
        "evidence_multiplier": multiplier,
        "category_contributions": dict(sorted(contributions.items(), key=lambda kv: -kv[1])),
    }
    return round(raw * multiplier, 4), breakdown


@dataclass
class ScoredSupplement:
    supplement: object
    score: float
    breakdown: dict
    safety_flags: list[str]


@dataclass
class RecommendationResult:
    need_scores: dict[str, float]
    safety: SafetyResult
    items: list[ScoredSupplement]


def build_recommendations(responses: dict, supplements: list, top_n: int = 5) -> RecommendationResult:
    need_scores = compute_need_scores(responses)
    safety = evaluate(responses)

    scored: list[ScoredSupplement] = []
    for supp in supplements:
        if supp.slug in safety.blocked:
            continue
        score, breakdown = _score_supplement(need_scores, supp)
        if score <= 0:
            continue
        scored.append(ScoredSupplement(supp, score, breakdown, safety.warnings.get(supp.slug, [])))

    scored.sort(key=lambda s: s.score, reverse=True)
    return RecommendationResult(need_scores, safety, scored[:top_n])
