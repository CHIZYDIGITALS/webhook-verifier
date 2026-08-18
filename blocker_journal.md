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
