# Supplement AI

## Stack
- Backend: Python 3.13 + FastAPI + LangGraph (Fase 1)
- Frontend: Next.js 14 (App Router) + Tailwind
- LLM: OpenRouter free tier (base_url: https://openrouter.ai/api/v1)
- DB: PostgreSQL 16 (sin Redis — estado de sesión en JSONB)
- Auth: JWT propio en FastAPI (passlib + python-jose)
- Infra: Docker Compose + Apache reverse proxy (VPS IONOS)

## Entorno de desarrollo
- Siempre usar el venv: `.venv/` (Python 3.14)
- Driver PostgreSQL: `psycopg` v3 (no psycopg2)
- DATABASE_URL debe usar prefijo `postgresql+psycopg://`
- Arrancar con: `docker compose up`

## Reglas de código
- Python limpio y mínimo, sin queries SQL raw
- Proponer cambios antes de ejecutar
- Sin comentarios obvios; solo los que explican el "por qué"
- Imports relativos al directorio `backend/` (se ejecuta desde allí en Docker)

## Contexto del proyecto
- Demo de prácticas — Ticmatic. No va a producción real.
- Todo el aparato legal pesado está documentado en `docs/out-of-scope.md`
- Catálogo y reglas de seguridad son ficticios para la demo
- Ver `docs/decisions.md` para el registro de decisiones (D-1 a D-8)

## Disclaimers
- Nunca hacer diagnósticos médicos
- Disclaimer inyectado en system prompt del LLM (no delegado al modelo)
- Si el usuario reporta medicación → aviso "consulta a un profesional"
