# Testing

> Este documento se completa en la Fase 1 junto con los tests del motor de recomendación.

## Tests unitarios (por escribir en Fase 1)

```bash
cd backend
../.venv/bin/pytest tests/ -v
```

Los tests cubrirán principalmente:
- Motor de puntuación: `engine/scoring.py`
- Reglas de seguridad: `engine/safety.py`
- Endpoints de auth: `api/auth.py`

## Flujo manual

Con los servicios corriendo (`docker compose up`):

1. Registro: `POST http://localhost:8000/api/auth/register`
2. Login: `POST http://localhost:8000/api/auth/login`
3. API docs interactiva: `http://localhost:8000/docs`
4. Frontend: `http://localhost:3000`
