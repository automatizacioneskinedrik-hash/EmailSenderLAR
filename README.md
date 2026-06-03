# Atnova Email Service

Microservicio en Python para recibir eventos desde el CRM, renderizar plantillas con Jinja2, generar certificados PDF personalizados y enviar correos por SMTP.

## Stack

- FastAPI para la API HTTP.
- Pydantic para validacion de entrada.
- Jinja2 para plantillas HTML.
- WeasyPrint para generar certificados PDF desde HTML/CSS.
- aiosmtplib para envio SMTP.
- Cloud Run como runtime recomendado.
- Cloud Tasks o Pub/Sub para procesamiento asincrono cuando el volumen crezca.

## Flujo

1. El CRM llama `POST /webhooks/crm-campus-result`.
2. El servicio valida `X-Secret-Token`.
3. Si el evento es exitoso, genera el certificado PDF y envia bienvenida al usuario.
4. Si el evento llega con error, envia una alerta al equipo interno de gestion.

## Instalacion local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8080
```

## Ejemplo curl exitoso

```bash
curl -X POST http://localhost:8080/webhooks/crm-campus-result ^
  -H "Content-Type: application/json" ^
  -H "X-Secret-Token: change-me" ^
  -d "{\"event_id\":\"crm-123\",\"status\":\"success\",\"user\":{\"name\":\"Carlos Perez\",\"email\":\"carlos@example.com\",\"document\":\"123456789\"},\"convocatoria\":{\"id\":\"conv-001\",\"name\":\"Diplomado Seguridad\"},\"campus\":{\"user_created\":true,\"associated\":true,\"response_id\":\"atnova-789\",\"username\":\"carlos.perez\",\"password\":\"Temporal123\",\"platform_url\":\"https://campus.example.com\",\"enrollment_certificate_url\":\"https://docs.example.com/matricula.pdf\",\"educational_services_contract_url\":\"https://docs.example.com/contrato.pdf\"}}"
```

## Ejemplo curl con error

```bash
curl -X POST http://localhost:8080/webhooks/crm-campus-result ^
  -H "Content-Type: application/json" ^
  -H "X-Secret-Token: change-me" ^
  -d "{\"event_id\":\"crm-124\",\"status\":\"error\",\"user\":{\"name\":\"Carlos Perez\",\"email\":\"carlos@example.com\",\"document\":\"123456789\"},\"convocatoria\":{\"id\":\"conv-001\",\"name\":\"Diplomado Seguridad\"},\"error\":{\"code\":\"ATNOVA_ASSOCIATION_FAILED\",\"message\":\"No fue posible asociar el usuario a la convocatoria\"}}"
```

## Variables importantes

Configura `.env` con las credenciales SMTP reales antes de probar envios.

Nunca subas `.env` al repositorio.
