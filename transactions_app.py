from flask import Flask, request, jsonify
from bank_auth_sdk import BankAuth

app = Flask(__name__)
auth = BankAuth("transactions")  

@app.route('/transfer', methods=['POST'])
def transfer():
    auth_header = request.headers.get('Authorization', '')
    
    if not auth_header.startswith('Bearer '):
        return jsonify({"error": "Token faltante o malformado en el header Authorization. Se espera 'Bearer <token>'"}), 401

    token = auth_header.replace('Bearer ', '')

    try:
        auth.verify_token(token)
        return jsonify({"status": "success"})
    except ValueError as e:
        return jsonify({"error": f"Token inválido o expirado: {str(e)}"}), 403
    except Exception as e:
        return jsonify({"error": f"Error interno al verificar el token: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
