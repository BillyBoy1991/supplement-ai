# Supplement AI - Chatbot de Recomendación de Suplementos

## Stack
- Backend: Python + FastAPI + LangGraph
- Frontend: React + Tailwind
- AI: Anthropic Claude API
- DB: SQLite (desarrollo) → PostgreSQL (producción)

## Arquitectura de agentes
- OrchestratorAgent: recibe respuestas del usuario y enruta al agente correcto
- ProfileAgent: gestiona el perfil del usuario (15 preguntas)
- RecommendationAgent: genera recomendaciones de suplementos
- SafetyAgent: valida recomendaciones contra reglas de seguridad médica

## Reglas de código
- Python limpio y mínimo, sin queries raw
- Proponer cambios antes de ejecutar
- Respuestas lo más cortas posible pero correctas
- Siempre usar entorno virtual .venv

## Aspectos legales
- Nunca hacer diagnósticos médicos
- Siempre incluir disclaimers en recomendaciones
- Cumplimiento GDPR