import os
import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import hmac
import hashlib
import requests

app = FastAPI()

attendees = {}
SECRET_KEY = "solstice_secret_key"

# Locate absolute paths for static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class ScanRequest(BaseModel):
    attendee_id: str
    callback_url: str

async def process_print_queue(attendee_id: str, callback_url: str):
    await asyncio.sleep(3)
    attendees[attendee_id] = "checked_in"
    payload = f"{attendee_id}:checked_in"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    try:
        requests.post(
            callback_url,
            json={"attendee_id": attendee_id, "status": "checked_in"},
            headers={"X-Signature": signature},
            timeout=5
        )
    except Exception as e:
        print(f"Webhook delivery failed: {e}")

@app.post("/api/scan")
async def handle_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    current_status = attendees.get(request.attendee_id)
    if current_status in ["pending", "checked_in"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Scan blocked: Attendee {request.attendee_id} is already {current_status}."
        )

    attendees[request.attendee_id] = "pending"
    background_tasks.add_task(process_print_queue, request.attendee_id, request.callback_url)
    return {"status": "pending", "message": "Print job queued. Awaiting webhook confirmation."}

@app.post("/api/webhook")
async def handle_webhook(data: dict):
    return {"status": "received", "data": data}

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
