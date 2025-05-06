from flask import Flask, request, jsonify
from bank_auth_sdk import BankAuth

app = Flask(__name__)
auth = BankAuth("transactions")  # Usará SU key

@app.route('/transfer', methods=['POST'])
def transfer():
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        auth.verify_token(token)
        return jsonify({"status": "success", "api": "transactions"})
    except ValueError as e:
        return jsonify({"error": str(e)}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)