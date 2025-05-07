# Transactions API

API de ejemplo que forma parte de una Prueba de Concepto (PoC) de autenticación segura y control de autorización entre microservicios usando AWS KMS y JWT.

## 🚀 ¿Qué hace?

Expone un endpoint `/transfer` (POST) que simula el procesamiento de una transferencia, **verificando el token del usuario** y **consultando el balance disponible en la API de Accounts antes de continuar**.

## 🧱 Rol en la PoC

- Esta API **actúa como iniciadora de operaciones sensibles** (por ejemplo, transferencias).
- Verifica que el token entrante esté firmado correctamente.
- Genera un nuevo token interno firmado con su propia clave KMS para consultar otra API (`accounts`).
- Valida si hay fondos suficientes antes de completar la operación.

## 🔧 Requisitos

- Python 3.8+
- AWS SDK (`boto3`)
- Flask
- PyJWT
- Acceso a Secret Manager de AWS y a la clave KMS correspondiente

## ⚙️ Variables de entorno necesarias

| Variable         | Descripción                                                |
|------------------|------------------------------------------------------------|
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | Credenciales para acceder a Secrets Manager y KMS |
| `AWS_SESSION_TOKEN`                           | Requerido si usás credenciales temporales         |
| `AWS_DEFAULT_REGION`                          | Región de AWS (ej: `us-east-1`)                  |
| `ACCOUNTS_API_URL`                            | URL de la API de Accounts (ej: `http://10.0.1.123:5001`) |


## 🛠 Cómo levantar la API

```bash
pip install -r requirements.txt
export ACCOUNTS_API_URL=http://10.0.1.123:5001
export FLASK_APP=transactions_api.py
flask run --host=0.0.0.0 --port=5000
```

## 🔐 Seguridad

La API espera un token JWT válido en cada request a /transfer:

```bash
Authorization: Bearer <token>
```
Internamente genera un nuevo token (firmado por esta misma API) para consumir accounts.

## 📥 Ejemplo de request

POST /transfer HTTP/1.1
Host: transactions.api.local
Authorization: Bearer <token-del-usuario>
Content-Type: application/json

{
  "from": "123",
  "to": "456",
  "amount": 10000
}

### 🧪 Posibles respuestas

✅ Fondos suficientes:

```json
{
  "status": "success",
  "message": "Transacción exitosa"
}
```

### ❌ Fondos insuficientes:

```json
{
  "status": "error",
  "message": "Fondos insuficientes"
}
```

### ❌ Token inválido:

```json
{
  "error": "Token inválido o expirado: ..."
}
```

## 🧩 Integración

Este servicio depende de que la API accounts esté accesible mediante ACCOUNTS_API_URL, y de que ambas APIs compartan el esquema de verificación de tokens por clave pública mediante KMS.

