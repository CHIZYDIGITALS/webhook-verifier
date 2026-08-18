import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Secret key shared between your app and the sender
SECRET_KEY = b"super_secret_webhook_key_123"

@app.route("/webhook/payment", methods=["POST"])
def verify_payment_webhook():
    # 1. Read signature from incoming request header
    provided_signature = request.headers.get("X-Signature")
    if not provided_signature:
        return jsonify({"status": "Error", "message": "Missing X-Signature header"}), 400

    # 2. Compute HMAC-SHA256 signature using secret key and request body
    computed_signature = hmac.new(
        SECRET_KEY, 
        request.data, 
        hashlib.sha256
    ).hexdigest()

    # 3. Compare computed hash with header string
    if hmac.compare_digest(computed_signature, provided_signature):
        return jsonify({"status": "Success", "message": "Webhook verified successfully!"}), 200
    else:
        return jsonify({"status": "Unauthorized", "message": "Invalid signature!"}), 401

if __name__ == "__main__":
    app.run(port=5000, debug=True)
