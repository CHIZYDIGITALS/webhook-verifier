import os
import asyncio
from typing import Optional
from fastapi import FastAPI, BackgroundTasks, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import hmac
import hashlib
import requests

app = FastAPI()

attendees = {}
SECRET_KEY = "solstice_secret_key"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class ScanRequest(BaseModel):
    attendee_id: str
    callback_url: Optional[str] = None

async def process_print_queue(attendee_id: str, callback_url: str):
    await asyncio.sleep(3)
    attendees[attendee_id] = "checked_in"
    payload = f"{attendee_id}:checked_in"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    
    if callback_url and callback_url.startswith("http"):
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
async def handle_scan(request_data: ScanRequest, http_request: Request, background_tasks: BackgroundTasks):
    attendee_id = request_data.attendee_id
    current_status = attendees.get(attendee_id)
    
    if current_status in ["pending", "checked_in"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Scan blocked: Attendee {attendee_id} is already {current_status}."
        )

    attendees[attendee_id] = "pending"
    
    # Auto-resolve callback URL if missing or relative
    callback_url = request_data.callback_url
    if not callback_url or not callback_url.startswith("http"):
        base_url = str(http_request.base_url).rstrip("/")
        callback_url = f"{base_url}/api/webhook"
    
    background_tasks.add_task(process_print_queue, attendee_id, callback_url)
    return {"status": "pending", "message": "Print job queued. Awaiting webhook confirmation."}

@app.post("/api/webhook")
async def handle_webhook(data: dict):
    return {"status": "received", "data": data}

@app.get("/")
async def read_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))
