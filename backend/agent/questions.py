"""
Definición fija del cuestionario de 15 preguntas.

Cada opción de respuesta lleva sus contribuciones a las categorías de necesidad
(`needs`), que ya son el producto peso_pregunta × valor_respuesta. El motor de
puntuación solo tiene que sumarlas. Las categorías coinciden con las claves de
`need_weights` del catálogo de suplementos.
"""

NEGATIVE_ANSWERS = {"", "no", "ninguna", "ninguno", "nada", "n/a", "na", "-"}


def has_meaningful_text(value: object) -> bool:
    """True si un campo de texto libre aporta información (no vacío ni negación)."""
    if not isinstance(value, str):
        return bool(value)
    return value.strip().lower() not in NEGATIVE_ANSWERS


QUESTIONS: list[dict] = [
    {
        "id": "age",
        "prompt": "¿Cuántos años tienes?",
        "type": "number",
    },
    {
        "id": "sex",
        "prompt": "¿Cuál es tu sexo biológico?",
        "type": "single_choice",
        "options": [
            {"label": "Hombre", "value": "male", "needs": {"muscle": 0.2, "hormonal": 0.2}},
            {"label": "Mujer", "value": "female", "needs": {"hormonal": 0.3, "bone_health": 0.2}},
            {"label": "Prefiero no decirlo", "value": "other", "needs": {}},
        ],
    },
    {
        "id": "main_goal",
        "prompt": "¿Cuál es tu objetivo principal ahora mismo?",
        "type": "single_choice",
        "options": [
            {"label": "Perder grasa", "value": "fat_loss", "needs": {"fat_loss": 1.0, "energy": 0.3}},
            {"label": "Ganar músculo", "value": "muscle", "needs": {"muscle": 1.0, "energy": 0.3}},
            {"label": "Más energía", "value": "energy", "needs": {"energy": 1.0}},
            {"label": "Longevidad y bienestar", "value": "longevity", "needs": {"longevity": 1.0, "heart": 0.3}},
            {"label": "Claridad mental / foco", "value": "focus", "needs": {"cognitive": 1.0}},
        ],
    },
    {
        "id": "activity_level",
        "prompt": "¿Cuál es tu nivel de actividad física?",
        "type": "single_choice",
        "options": [
            {"label": "Sedentario", "value": "sedentary", "needs": {"fat_loss": 0.3, "energy": 0.2}},
            {"label": "Ligero", "value": "light", "needs": {"energy": 0.2}},
            {"label": "Moderado", "value": "moderate", "needs": {"muscle": 0.3, "energy": 0.2}},
            {"label": "Intenso", "value": "intense", "needs": {"muscle": 0.6, "energy": 0.4, "heart": 0.2}},
        ],
    },
    {
        "id": "sleep_quality",
        "prompt": "¿Cómo calificarías la calidad de tu sueño?",
        "type": "single_choice",
        "options": [
            {"label": "Muy mala", "value": "very_poor", "needs": {"sleep": 1.0, "stress": 0.4, "energy": 0.3}},
            {"label": "Mala", "value": "poor", "needs": {"sleep": 0.7, "stress": 0.3}},
            {"label": "Aceptable", "value": "fair", "needs": {"sleep": 0.4}},
            {"label": "Buena", "value": "good", "needs": {}},
        ],
    },
    {
        "id": "stress_level",
        "prompt": "¿Cómo describirías tu nivel de estrés habitual?",
        "type": "single_choice",
        "options": [
            {"label": "Bajo", "value": "low", "needs": {}},
            {"label": "Moderado", "value": "moderate", "needs": {"stress": 0.5}},
            {"label": "Alto", "value": "high", "needs": {"stress": 1.0, "sleep": 0.3, "mood": 0.3}},
            {"label": "Muy alto", "value": "very_high", "needs": {"stress": 1.0, "sleep": 0.5, "mood": 0.5}},
        ],
    },
    {
        "id": "diet_quality",
        "prompt": "¿Cómo es tu alimentación actual en general?",
        "type": "single_choice",
        "options": [
            {"label": "Pobre / desordenada", "value": "poor", "needs": {"energy": 0.4, "gut": 0.3, "immune": 0.3}},
            {"label": "Mejorable", "value": "average", "needs": {"energy": 0.2, "immune": 0.2}},
            {"label": "Equilibrada", "value": "good", "needs": {}},
        ],
    },
    {
        "id": "dietary_restrictions",
        "prompt": "¿Tienes alguna restricción alimentaria?",
        "type": "multi_choice",
        "options": [
            {"label": "Vegana", "value": "vegan", "needs": {"energy": 0.5, "cognitive": 0.4, "heart": 0.3}},
            {"label": "Vegetariana", "value": "vegetarian", "needs": {"energy": 0.3, "muscle": 0.2}},
            {"label": "Sin lactosa", "value": "lactose_free", "needs": {"bone_health": 0.3, "gut": 0.2}},
            {"label": "Sin gluten", "value": "gluten_free", "needs": {"gut": 0.3}},
            {"label": "Ninguna", "value": "none", "needs": {}},
        ],
    },
    {
        "id": "supplement_history",
        "prompt": "¿Has usado suplementos antes?",
        "type": "single_choice",
        "options": [
            {"label": "Nunca", "value": "never", "needs": {}},
            {"label": "Ocasionalmente", "value": "occasionally", "needs": {}},
            {"label": "Habitualmente", "value": "regularly", "needs": {}},
        ],
    },
    {
        "id": "medication",
        "prompt": "¿Tomas alguna medicación actualmente? Si es así, indícala. Si no, escribe «ninguna».",
        "type": "text",
    },
    {
        "id": "digestive_symptoms",
        "prompt": "¿Tienes síntomas digestivos con frecuencia (hinchazón, gases, malestar)?",
        "type": "single_choice",
        "options": [
            {"label": "Nunca", "value": "none", "needs": {}},
            {"label": "A veces", "value": "mild", "needs": {"gut": 0.5}},
            {"label": "Frecuentemente", "value": "frequent", "needs": {"gut": 1.0, "immune": 0.3}},
        ],
    },
    {
        "id": "hormonal_health",
        "prompt": "¿Notas alteraciones hormonales (libido, ciclo, fatiga inexplicada)?",
        "type": "single_choice",
        "options": [
            {"label": "No", "value": "no_issues", "needs": {}},
            {"label": "Algunas", "value": "some_concerns", "needs": {"hormonal": 0.6}},
            {"label": "Significativas", "value": "significant", "needs": {"hormonal": 1.0, "energy": 0.3}},
        ],
    },
    {
        "id": "hydration",
        "prompt": "¿Cómo es tu hidratación diaria?",
        "type": "single_choice",
        "options": [
            {"label": "Baja (<1L)", "value": "low", "needs": {"energy": 0.3, "cognitive": 0.2}},
            {"label": "Adecuada", "value": "adequate", "needs": {}},
            {"label": "Alta", "value": "high", "needs": {}},
        ],
    },
    {
        "id": "mood",
        "prompt": "¿Cómo describirías tu estado de ánimo en las últimas semanas?",
        "type": "single_choice",
        "options": [
            {"label": "Bajo / decaído", "value": "low", "needs": {"mood": 1.0, "stress": 0.3, "cognitive": 0.2}},
            {"label": "Neutro", "value": "neutral", "needs": {"mood": 0.3}},
            {"label": "Bueno", "value": "good", "needs": {}},
        ],
    },
    {
        "id": "other_treatments",
        "prompt": "¿Sigues otro tratamiento médico en curso? Si no, escribe «ninguno».",
        "type": "text",
    },
]

QUESTION_BY_ID: dict[str, dict] = {q["id"]: q for q in QUESTIONS}
ORDER: list[str] = [q["id"] for q in QUESTIONS]


def payload(question_id: str) -> dict:
    """Versión de la pregunta que se envía al cliente (sin las contribuciones internas)."""
    q = QUESTION_BY_ID[question_id]
    out = {"id": q["id"], "prompt": q["prompt"], "type": q["type"]}
    if "options" in q:
        out["options"] = [{"label": o["label"], "value": o["value"]} for o in q["options"]]
    return out


def needs_for(question_id: str, answer: object) -> dict[str, float]:
    """Contribuciones a las categorías de necesidad para la respuesta dada."""
    q = QUESTION_BY_ID.get(question_id)
    if not q or "options" not in q:
        return {}
    selected = answer if isinstance(answer, list) else [answer]
    totals: dict[str, float] = {}
    for opt in q["options"]:
        if opt["value"] in selected:
            for cat, val in opt.get("needs", {}).items():
                totals[cat] = totals.get(cat, 0.0) + val
    return totals
