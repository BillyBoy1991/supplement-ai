# Despliegue en VPS IONOS

> Este documento se completa en la Fase 2 cuando se creen los Dockerfiles de producción definitivos.

## Resumen del proceso (se detallará en Fase 2)

1. Conectar al VPS por SSH
2. Clonar el repositorio
3. Copiar `.env.example → .env` y rellenar con valores de producción
4. `docker compose -f docker-compose.prod.yml up -d --build`
5. Configurar Apache VirtualHost con `infra/apache/supplement.conf`
6. Obtener certificado SSL: `certbot --apache -d supplement.billytheboy.com`
7. Verificar que `https://supplement.billytheboy.com` responde correctamente

## Variables de entorno en producción

En producción, cambiar:
- `DATABASE_URL`: usar contraseña segura
- `JWT_SECRET`: secreto de al menos 32 bytes aleatorios
- `ALLOWED_ORIGINS`: solo `https://supplement.billytheboy.com`
- `ENVIRONMENT`: `production`
