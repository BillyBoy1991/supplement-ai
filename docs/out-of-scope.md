# Fuera de alcance (demo → producción real)

Este documento lista lo que se implementaría antes de poner la plataforma en producción con datos reales de usuarios.

## Legal / GDPR

- **Registro de actividades de tratamiento (Art. 30 GDPR):** documento formal que describe qué datos se procesan, con qué finalidad, base jurídica y tiempo de retención.
- **DPO (Delegado de Protección de Datos):** designación obligatoria para procesamiento de datos de categoría especial (salud) a escala.
- **DPA firmado con el proveedor LLM:** Anthropic tiene DPA disponible. El proveedor LLM no puede procesar datos de salud sin este acuerdo.
- **Consentimiento explícito granular (Art. 9):** pantalla de consentimiento diferenciada para datos de salud, marketing y terceros.
- **Derecho al olvido:** endpoint `DELETE /users/me` con pipeline de borrado hard a los 7 días.
- **Portabilidad:** endpoint `GET /users/me/export` con todos los datos del usuario en JSON.
- **Consent log y audit log:** tablas de auditoría para todas las acciones sobre datos sensibles.

## Seguridad de datos

- **Cifrado en reposo de datos de salud:** columnas cifradas con pgcrypto o tablespace cifrado para `questionnaire_sessions` y `user_profiles`.
- **Pseudonimización:** usar hashes de ID en logs, no identificadores directos.

## Catálogo y evidencia médica

- **Revisión por profesional de salud:** el catálogo de suplementos y las reglas de seguridad deben ser validados y firmados por un nutricionista o médico antes de su uso en producción.
- **Fuente de interacciones medicamento-suplemento:** integración con DrugBank API o base de datos equivalente con cobertura sistemática.
- **Base de evidencia para RAG:** artículos científicos reales indexados con DOI, con revisión periódica.

## Infraestructura de producción

- **Backups automáticos de PostgreSQL:** política de backup y restore probada.
- **Monitorización y alertas:** métricas de la API, tasa de error, latencia del LLM.
- **Rate limiting** en endpoints de recomendación para controlar costes de API LLM.
- **HTTPS forzado en CORS:** `ALLOWED_ORIGINS` solo con dominios HTTPS en producción.
