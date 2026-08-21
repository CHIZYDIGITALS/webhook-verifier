import asyncio
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import hmac
import hashlib
import requests
import os

app = FastAPI()

# In-memory storage for demo state
attendees = {}  # { "attendee_id": "checked_in" | "pending" }
SECRET_KEY = "solstice_secret_key"

class ScanRequest(BaseModel):
    attendee_id: str
    callback_url: str

async def process_print_queue(attendee_id: str, callback_url: str):
    """Simulates asynchronous queue worker processing print job and firing webhook."""
    await asyncio.sleep(3)  # Simulate badge printing latency
    
    # Update status to completed
    attendees[attendee_id] = "checked_in"
    
    # Construct signature for webhook security
    payload = f"{attendee_id}:checked_in"
    signature = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    
    # Send async webhook notification
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
    # Duplicate-scan protection logic
    current_status = attendees.get(request.attendee_id)
    if current_status in ["pending", "checked_in"]:
        raise HTTPException(
            status_code=400, 
            detail=f"Scan blocked: Attendee {request.attendee_id} is already {current_status}."
        )

    # Set state to pending instantly
    attendees[request.attendee_id] = "pending"
    
    # Enqueue print job asynchronously
    background_tasks.add_task(process_print_queue, request.attendee_id, request.callback_url)
    
    return {"status": "pending", "message": "Print job queued. Awaiting webhook confirmation."}

@app.post("/api/webhook")
async def handle_webhook(data: dict):
    # Endpoint to simulate receiving webhook callbacks
    return {"status": "received", "data": data}

# Serve frontend static assets
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")
