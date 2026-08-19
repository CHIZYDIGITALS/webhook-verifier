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

---

## Summary of Autonomous Learning

- **Total Time Spent:** ~1.5 Hours
- **Primary Documentation Used:** Python `hmac` & `hashlib` documentation, Flask request processing guide.
- **Key Takeaway:** HMAC verification requires comparing raw request bytes against a computed SHA256 digest using a shared secret key.
