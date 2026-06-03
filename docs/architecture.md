# Arquitectura

## Topología general

```
Usuario
  │
  ▼
Next.js (puerto 3000)
  │  llamadas a /api/*
  ▼
FastAPI (puerto 8000)
  ├── /api/auth          → autenticación JWT
  ├── /api/questionnaire → agente LangGraph (Fase 1)
  └── /api/recommendations → motor de recomendación
        │
        ├── Motor determinista (puntuación + reglas de seguridad)
        │   └── Lee: data/rules/safety_rules.json
        │
        └── LLM (Fase 2): OpenRouter → explicación personalizada
              └── RAG sobre PostgreSQL + pgvector (Fase 2)
  │
  ▼
PostgreSQL 16
```

En producción, Apache actúa como reverse proxy delante de ambos servicios.

## Estructura de carpetas

```
backend/
├── api/        # Routers FastAPI (auth, questionnaire, recommendations)
├── agent/      # Grafo LangGraph — cuestionario conversacional (Fase 1)
├── engine/     # Motor de puntuación y reglas de seguridad (Fase 1)
├── models/     # Modelos SQLAlchemy + esquemas Pydantic
└── core/       # Config (Pydantic Settings), JWT, logging
```

## Por qué motor determinista + LLM solo redacta

El motor de puntuación y las reglas de seguridad son 100% deterministas:
- No pueden alucinar ni sugerir un suplemento contraindicado
- Son auditables y reproducibles
- Las reglas de interacciones medicamentosas se verifican antes de cualquier llamada LLM

El LLM solo redacta la explicación en lenguaje natural. No decide qué recomendar ni aplica reglas de seguridad. El disclaimer se inyecta en el system prompt, no en el mensaje del usuario, por lo que el LLM no puede omitirlo.

## Sin Redis

El estado de sesión del cuestionario (LangGraph) se persiste en la columna `graph_state` (JSONB) de `questionnaire_sessions`. Esto evita una dependencia extra en un VPS pequeño.

## Configuración

Todas las variables de entorno pasan por `backend/core/config.py` (Pydantic Settings). El servidor falla al arrancar si falta alguna variable obligatoria.
