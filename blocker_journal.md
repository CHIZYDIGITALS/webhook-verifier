# Learning & Blocker Journal — Week 2 (Assignment 1)

- **Learner Name:** Eze Assumpta Chimzurum
- **Assigned Tool:** Webhook Verification (HMAC-SHA256)
- **Start Time:** Aug 18, 2026

---

### Entry #1 — Environment & Setup Issues

- **1. Goal / Action:** Install Python, Flask, and set up project files.
- **2. Error Message / Behavior:** Encountered network resolution errors (`getaddrinfo failed`) during `pip install`.
- **3. Initial Hypothesis:** Command prompt lacked active network connection to PyPI.
- **4. What I Tried:** Verified internet connection and installed via `python -m pip install --user flask`.
- **5. Outcome / Fix:** Flask 3.1.3 installed successfully.

---

### Entry #2 — Server Execution & CLI Alias Blockers

- **1. Goal / Action:** Run local Flask server and test `/webhook/payment` endpoint using cURL.
- **2. Error Message / Behavior:** Received `Invoke-WebRequest` parameter errors when running cURL in PowerShell.
- **3. Initial Hypothesis:** PowerShell aliased `curl` and required strict case syntax.
- **4. What I Tried:** Switched VS Code terminal to Command Prompt (`cmd`) and ran standard cURL commands.
- **5. Outcome / Fix:** Received expected `400` status with `"Missing X-Signature header"`.

---

### Entry #3 — Signature Validation Verification

- **1. Goal / Action:** Validate handling of incorrect webhook signatures.
- **2. Error Message / Behavior:** Tested request with `-H "X-Signature: fake_signature_123"`.
- **3. Initial Hypothesis:** Server should reject invalid HMAC-SHA256 digests with a `401 Unauthorized`.
- **4. What I Tried:** Sent POST request with custom header via cURL.
- **5. Outcome / Fix:** Server correctly returned `401` status with `"Invalid signature!"`.

## Day 3: Individual Refactoring & Retrospective

### Trade-Off Decisions

- **Verification vs. Complexity:** Focused on solidifying single-file HMAC-SHA256 request verification using Flask over complex multi-file modules to maintain lightweight, readable code for rapid testing.
- **Shell Formatting Handling:** Worked around Windows `cmd` quote-escaping differences during payload testing by using raw string payload hashes directly for HMAC validation.

### Self-Retrospective

- **Start:** Testing API endpoints using direct header signatures and automated post-processing scripts to avoid manual hashing errors.
- **Stop:** Troubleshooting Windows CMD quote escaping manually without verifying raw incoming request bytes in Flask first.
- **Continue:** Keeping real-time terminal output logs inside `blocker_journal.md` to document verification evidence clearly.

## Day 4 Pivot: Solstice Events Co. Asynchronous Re-architecture

### Architectural Shift

- **Pre-Pivot Model:** Synchronous REST calls to badge printer vendor[span_1](start_span)[span_1](end_span).
- **Post-Pivot Model:** Asynchronous event-driven queue with HMAC-SHA256 verified webhook callback[span_2](start_span)[span_2](end_span).

### Deprecation Strategy

- Marked pre-pivot synchronous endpoints (`/webhook/payment`) with explicit deprecation docstrings and configured them to return `HTTP 410 Gone` to prevent accidental parallel execution[span_3](start_span)[span_3](end_span).

### Verification & Test Results

- **Attendee Check-in (`202 Accepted`):** Scanned attendee transitions immediately to `Pending` state while print job is pushed to message queue[span_4](start_span)[span_4](end_span).
- **Webhook Callback (`200 OK`):** Background worker signs payload with HMAC-SHA256 and calls `/webhook/print-complete` to update state to `Checked In`[span_5](start_span)[span_5](end_span).
- **Duplicate Protection (`400 Bad Request`):** Re-scanning `pending` or `checked_in` attendees blocks second print job creation[span_6](start_span)[span_6](end_span).

---

## Summary of Autonomous Learning

- **Total Time Spent:** ~3.5 Hours
- **Primary Documentation Used:** Python `hmac`, `hashlib`, `urllib.request` documentation, Flask request processing guide, and asynchronous threading patterns.
- **Key Takeaway:** Pivoting from synchronous API calls to an asynchronous, event-driven model requires decoupling status tracking (using `Pending` states) and validating background callbacks via signature verification to prevent duplicate requests[span_7](start_span)[span_7](end_span).
