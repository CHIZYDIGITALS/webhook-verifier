# Webhook Verification & Async Badge Kiosk System

An event-driven Flask microservice built for Solstice Events Co. to handle asynchronous badge printing with HMAC-SHA256 webhook security, pending UI state handling, and duplicate scan protection[span_1](start_span)[span_1](end_span).

## Architectural Pivot Overview (Day 4)

- **Pre-Pivot:** Direct synchronous calls to printer vendor REST API[span_2](start_span)[span_2](end_span).
- **Post-Pivot:** Asynchronous event-driven queue[span_3](start_span)[span_3](end_span). The kiosk sets attendee state to `Pending`, publishes a background job, and waits for an HMAC-signed webhook callback (`/webhook/print-complete`) to transition state to `Checked In`[span_4](start_span)[span_4](end_span).
- **Deprecation:** Legacy synchronous route (`/webhook/payment`) returns `HTTP 410 Gone`[span_5](start_span)[span_5](end_span).

---

## Setup & Running

1. **Install Dependencies:**
   ```cmd
   python -m pip install flask
   ```

Start the flask server:
python app.py

Testing Endpoints

1. 202 Accepted
   curl -X POST http://127.0.0.1:5000/api/checkin -H "Content-Type: application/json" -d "{\"attendee_id\":\"ATT_001\"}"

2. Dubplicate scan 400
   curl -X POST http://127.0.0.1:5000/api/checkin -H "Content-Type: application/json" -d "{\"attendee_id\":\"ATT_001\"}"

3. Test deprecated Route: (Gone 410)
   curl -X POST http://127.0.0.1:5000/webhook/payment
