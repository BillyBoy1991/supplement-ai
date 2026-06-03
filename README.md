# Supplement AI

Demo de plataforma de recomendaciones personalizadas de suplementos basada en IA.
Proyecto de prácticas — Ticmatic.

## Stack

| Capa | Tecnología |
|---|---|
| Backend | FastAPI + Python 3.13 |
| Agente conversacional | LangGraph (Fase 1) |
| LLM | OpenRouter (free tier) |
| Base de datos | PostgreSQL 16 |
| Frontend | Next.js 14 (App Router) + Tailwind |
| Auth | JWT propio en FastAPI |
| Infra | Docker Compose + Apache reverse proxy |

## Requisitos previos

- Docker y Docker Compose instalados
- Una API key de [OpenRouter](https://openrouter.ai) (gratuita)

## Getting Started

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd supplement-ai

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env: rellenar JWT_SECRET y OPENROUTER_API_KEY como mínimo

# 3. Arrancar todos los servicios
docker compose up --build

# 4. Aplicar migraciones y hacer seed del catálogo (primera vez)
docker compose exec backend alembic upgrade head
docker compose exec backend python seed.py

# 5. Abrir la aplicación
# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
```

## Estructura del proyecto

```
supplement-ai/
├── backend/          # FastAPI — API, agente LangGraph, motor de recomendación
├── frontend/         # Next.js 14 — UI web
├── data/
│   ├── supplements/  # Catálogo de suplementos (seed JSON)
│   └── rules/        # Reglas de seguridad (safety rules)
├── infra/
│   └── apache/       # Configuración del reverse proxy para el VPS
├── docs/             # Documentación del proyecto
├── docker-compose.yml       # Dev
└── docker-compose.prod.yml  # Producción (VPS IONOS)
```

## Documentación

- [Arquitectura](docs/architecture.md)
- [Decisiones de diseño](docs/decisions.md)
- [Fuera de alcance (producción real)](docs/out-of-scope.md)
- [Cómo ejecutar los tests](docs/testing.md)
- [Despliegue en VPS IONOS](docs/deployment.md)

## Variables de entorno

Ver `.env.example` para la lista completa con comentarios.
Las variables críticas para arrancar son `DATABASE_URL`, `JWT_SECRET` y `OPENROUTER_API_KEY`.
