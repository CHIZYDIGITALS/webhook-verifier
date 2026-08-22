import time
import threading
import json
import urllib.request
import hmac
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = b"solstice_vendor_secret_key"

# In-memory database for test attendees
# States: "not_checked_in", "pending", "checked_in"
ATTENDEES = {
    "ATT_001": {"name": "Alice Johnson", "status": "not_checked_in"},
    "ATT_002": {"name": "Bob Smith", "status": "not_checked_in"},
    "ATT_003": {"name": "Charlie Davis", "status": "not_checked_in"}
}

# ==============================================================================
# DEPRECATED ENDPOINT (PRE-PIVOT SYNCHRONOUS MODEL)
# ==============================================================================
@app.route("/webhook/payment", methods=["POST"])
@app.route("/api/v1/sync-print", methods=["POST"])
def deprecated_sync_printer():
    """
    [DEPRECATED / OBSOLETE]
    Pre-pivot synchronous badge printing endpoint.
    Deprecated because vendor retired synchronous print API.
    """
    return jsonify({
        "status": "Gone",
        "error": "410 Gone - Deprecated API",
        "message": "The synchronous printing API has been deprecated. Use /api/checkin for asynchronous queue processing."
    }), 410

# ==============================================================================
# NEW ASYNCHRONOUS EVENT-DRIVEN MODEL (DAY 4 PIVOT)
# ==============================================================================

def process_print_queue_async(attendee_id, callback_url):
    """Simulates vendor message queue delay and triggers webhook callback using urllib."""
    time.sleep(3)  # Simulate queue processing delay
    
    payload_data = json.dumps({"attendee_id": attendee_id, "status": "SUCCESS"}).encode('utf-8')
    signature = hmac.new(SECRET_KEY, payload_data, hashlib.sha256).hexdigest()
    
    req = urllib.request.Request(
        callback_url,
        data=payload_data,
        headers={
            'Content-Type': 'application/json',
            'X-Signature': signature
        },
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            pass
    except Exception as e:
        print(f"Callback delivery failed: {e}")

@app.route("/api/attendees", methods=["GET"])
def get_attendees():
    """Returns current attendee check-in statuses."""
    return jsonify(ATTENDEES), 200

@app.route("/api/checkin", methods=["POST"])
def initiate_checkin():
    """Kiosk Endpoint: Sets state to 'Pending' immediately and pushes to Queue."""
    data = request.json or {}
    attendee_id = data.get("attendee_id")
    
    if attendee_id not in ATTENDEES:
        return jsonify({"error": "Invalid attendee ID"}), 404
        
    current_status = ATTENDEES[attendee_id]["status"]
    
    # Duplicate scan protection (handles pending or already checked_in)
    if current_status in ["pending", "checked_in"]:
        return jsonify({
            "status": "Blocked",
            "message": f"Duplicate scan blocked! Attendee status is already '{current_status}'."
        }), 400
        
    # 1. Update state to Pending
    ATTENDEES[attendee_id]["status"] = "pending"
    
    # 2. Publish print job to message queue
    callback_url = "http://127.0.0.1:5000/webhook/print-complete"
    threading.Thread(target=process_print_queue_async, args=(attendee_id, callback_url)).start()
    
    return jsonify({
        "status": "Pending",
        "message": "Print job queued. State set to Pending."
    }), 202

@app.route("/webhook/print-complete", methods=["POST"])
def webhook_print_complete():
    """Vendor Callback Webhook: Updates attendee status to 'Checked In' after signature check."""
    provided_signature = request.headers.get("X-Signature")
    computed_signature = hmac.new(SECRET_KEY, request.data, hashlib.sha256).hexdigest()
    
    if not provided_signature or not hmac.compare_digest(computed_signature, provided_signature):
        return jsonify({"status": "Unauthorized", "message": "Invalid HMAC signature"}), 401
        
    data = request.json
    attendee_id = data.get("attendee_id")
    
    if attendee_id in ATTENDEES:
        ATTENDEES[attendee_id]["status"] = "checked_in"
        print(f"\n[ASYNC EVENT COMPLETE] {attendee_id} is now Checked In!\n")
        return jsonify({"status": "Success", "message": f"{attendee_id} successfully Checked In!"}), 200
        
    return jsonify({"error": "Attendee not found"}), 404

if __name__ == "__main__":
    app.run(port=5000, debug=True)

