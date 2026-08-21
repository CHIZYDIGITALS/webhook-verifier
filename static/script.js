let pollInterval = null;

// Helper to append log messages
function log(message) {
  const logList = document.getElementById("log-list");
  const timestamp = new Date().toLocaleTimeString();
  const entry = document.createElement("div");
  entry.className = "log-entry";
  entry.textContent = `[${timestamp}] ${message}`;
  logList.prepend(entry);
}

// Display error alert banner
function showAlert(message) {
  const banner = document.getElementById("alert-banner");
  banner.textContent = message;
  banner.className = "alert-banner error";
  setTimeout(() => {
    banner.className = "alert-banner hidden";
  }, 4000);
}

// Fetch current attendee states from server
async function updateAttendeeStates() {
  try {
    const response = await fetch("/api/attendees");
    if (!response.ok) return;

    const attendees = await response.json();

    for (const [id, data] of Object.entries(attendees)) {
      const badge = document.getElementById(`badge-${id}`);
      const btn = document.getElementById(`btn-${id}`);

      if (badge && btn) {
        if (data.status === "not_checked_in") {
          badge.textContent = "Not Checked In";
          badge.className = "status-badge status-not_checked_in";
          btn.disabled = false;
        } else if (data.status === "pending") {
          badge.textContent = "Printing Badge...";
          badge.className = "status-badge status-pending";
          btn.disabled = true;
        } else if (data.status === "checked_in") {
          badge.textContent = "Checked In";
          badge.className = "status-badge status-checked_in";
          btn.disabled = true;
        }
      }
    }
  } catch (e) {
    console.error("Failed to fetch attendees", e);
  }
}

// Trigger scan request
async function scanBadge(attendeeId) {
  log(`Initiating scan for ${attendeeId}...`);

  try {
    const response = await fetch("/api/checkin", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ attendee_id: attendeeId }),
    });

    const data = await response.json();

    if (response.status === 202) {
      log(
        `Success: Print job queued for ${attendeeId} (Status set to Pending).`,
      );
      updateAttendeeStates();
    } else if (response.status === 400) {
      log(`BLOCKED: ${data.message}`);
      showAlert(data.message);
    } else {
      showAlert(data.error || "An error occurred.");
    }
  } catch (e) {
    log(`Error communicating with backend server.`);
  }
}

// Automatically refresh status every 1 second to capture background webhook updates
pollInterval = setInterval(updateAttendeeStates, 1000);
updateAttendeeStates();
