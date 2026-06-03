# Registro de decisiones

## D-1: Stack principal
**Elegido:** FastAPI + LangGraph + OpenRouter (free tier) + Next.js 14 + JWT propio en FastAPI.

LangGraph se eligió sobre una FSM manual porque el cuestionario tiene bifurcaciones condicionales reales (ej. medicación → preguntas de seguimiento) y el roadmap apunta a un agente con memoria longitudinal. OpenRouter free tier cubre perfectamente las necesidades de demo.

**Demo vs producción:** en producción, OpenRouter se sustituiría por Anthropic Claude API con DPA firmado para datos de salud.

## D-2: Monorepo
**Elegido:** monorepo en `supplement-ai/`.

Equipo pequeño, una sola plataforma en fase inicial. La separación en repos añadiría overhead de CI/CD sin ganancia real.

## D-3: Evidencia médica
**Fuera de alcance.** El catálogo (`data/supplements/catalog.json`) y las reglas de seguridad (`data/rules/safety_rules.json`) son datos de demo creados para mostrar el flujo completo, no validados por un profesional de salud.

**En producción:** el catálogo requeriría revisión y firma por un nutricionista o médico titulado antes de servir recomendaciones reales.

## D-4: Interacciones medicamento-suplemento
**Elegido:** reglas conservadoras manuales en `data/rules/safety_rules.json`.

Si el usuario reporta medicación → disclaimer genérico "consulta a un profesional". No hay cross-check automático con bases de datos externas (DrugBank, NIH).

**En producción:** se integraría DrugBank API o equivalente.

## D-5: DPO / aparato legal GDPR
**Fuera de alcance.** Proyecto de demo sin datos reales ni lanzamiento. Ver `docs/out-of-scope.md`.

## D-6: Mercado objetivo
**Demo en España.** HIPAA fuera de alcance. GDPR solo a nivel de disclaimer visible en la UI.

## D-7: Sin Redis
**Elegido:** el estado de sesión del cuestionario (LangGraph checkpointing) se persiste en la columna `graph_state` (JSONB) en PostgreSQL. Ahorra RAM en el VPS pequeño de IONOS.

## D-8: Apache como reverse proxy
**Elegido:** Apache (ya instalado en el VPS IONOS). No se añade nginx. Certbot gestiona el certificado SSL para `supplement.billytheboy.com`.
