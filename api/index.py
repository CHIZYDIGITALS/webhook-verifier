import os
import asyncio
from fastapi import FastAPI, BackgroundTasks, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
import hmac
import hashlib
import requests

app = FastAPI()

attendees = {
    "ATT_001": "not_checked_in",
    "ATT_002": "not_checked_in",
    "ATT_003": "not_checked_in"
}
SECRET_KEY = "solstice_secret_key"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

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
            print(f"Webhook error: {e}")

@app.get("/api/attendees")
@app.get("/attendees")
async def get_attendees():
    return attendees

@app.get("/api/reset")
@app.get("/reset")
async def reset_attendees():
    global attendees
    attendees = {
        "ATT_001": "not_checked_in",
        "ATT_002": "not_checked_in",
        "ATT_003": "not_checked_in"
    }
    return {"status": "reset", "attendees": attendees}

async def process_scan(http_request: Request, background_tasks: BackgroundTasks):
    try:
        body = await http_request.json()
    except Exception:
        body = {}

    attendee_id = body.get("attendee_id") or body.get("attendeeId") or body.get("id")
    callback_url = body.get("callback_url") or body.get("callbackUrl")

    if not attendee_id:
        return JSONResponse(status_code=400, content={"status": "error", "message": "Missing attendee_id in request body"})

    current_status = attendees.get(attendee_id, "not_checked_in")
    
    if current_status in ["pending", "checked_in"]:
        return JSONResponse(
            status_code=400,
            content={
                "status": "blocked", 
                "detail": f"Scan blocked: Attendee {attendee_id} is already {current_status}.",
                "message": f"Scan blocked: Attendee {attendee_id} is already {current_status}."
            }
        )

    attendees[attendee_id] = "pending"
    
    if not callback_url or not callback_url.startswith("http"):
        base_url = str(http_request.base_url).rstrip("/")
        callback_url = f"{base_url}/api/webhook"
    
    background_tasks.add_task(process_print_queue, attendee_id, callback_url)
    return {"status": "pending", "message": f"Scan initiated for {attendee_id}. Badge printing..."}

@app.post("/api/scan")
@app.post("/scan")
async def handle_scan(http_request: Request, background_tasks: BackgroundTasks):
    return await process_scan(http_request, background_tasks)

@app.post("/api/checkin")
@app.post("/checkin")
async def handle_checkin(http_request: Request, background_tasks: BackgroundTasks):
    return await process_scan(http_request, background_tasks)

@app.post("/api/webhook")
@app.post("/webhook")
async def handle_webhook(data: dict):
    attendee_id = data.get("attendee_id")
    status = data.get("status")
    if attendee_id and status:
        attendees[attendee_id] = status
    return {"status": "received", "data": data}

@app.get("/")
async def read_index():
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse(content={"status": "API online"})
