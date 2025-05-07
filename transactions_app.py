import os
import requests
from flask import Flask, request, jsonify
from bank_auth_sdk import BankAuth

app = Flask(__name__)
auth = BankAuth("transactions")

@app.route('/transfer', methods=['POST'])
def transfer():
    # Paso 1: Verificar token entrante
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({
            "error": "Token faltante o malformado en el header Authorization. Se espera 'Bearer <token>'"
        }), 401

    token = auth_header.replace('Bearer ', '')

    try:
        auth.verify_token(token)
    except ValueError as e:
        return jsonify({"error": f"Token inválido o expirado: {str(e)}"}), 403
    except Exception as e:
        return jsonify({"error": f"Error interno al verificar el token: {str(e)}"}), 500

    # Paso 2: Leer datos del cuerpo de la request
    body = request.get_json()
    monto = body.get("amount", 0)

    # Paso 3: Generar token firmado por esta API para uso interno
    internal_token = auth.generate_token()

    # Paso 4: Llamar a la API de accounts para obtener el balance
    accounts_api_url = os.getenv("ACCOUNTS_API_URL", "http://localhost:5001")
    try:
        accounts_response = requests.get(
            f"{accounts_api_url}/balance",
            headers={"Authorization": f"Bearer {internal_token}"}
        )

        if accounts_response.status_code != 200:
            return jsonify({"error": "No se pudo obtener el balance de cuentas", "status_code_accounts_api": accounts_response.status_code, "response_accounts_api": accounts_response.json()}), 502

        data = accounts_response.json()
        balance = data["balance"]["available"]

        if monto > balance:
            return jsonify({"error": "Fondos insuficientes"}), 400

    except Exception as e:
        return jsonify({"error": f"Error al consultar el balance: {str(e)}"}), 500

    # Paso 5: Si hay fondos, procesar la transferencia
    return jsonify({
        "status": "success",
        "message": "Transferencia realizada",
        "monto": monto
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
