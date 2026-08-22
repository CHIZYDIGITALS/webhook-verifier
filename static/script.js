document.addEventListener("DOMContentLoaded", () => {
  fetchAttendees();
  setInterval(fetchAttendees, 1000);
});

async function fetchAttendees() {
  try {
    const response = await fetch("/api/attendees");
    if (!response.ok) return;
    const attendees = await response.json();
    updateUI(attendees);
  } catch (e) {
    console.error("Polling error:", e);
  }
}

function updateUI(attendees) {
  Object.keys(attendees).forEach((id) => {
    const card = document.querySelector(`[data-id="${id}"]`);
    if (!card) return;

    const statusBadge = card.querySelector(".status-badge");
    const status = attendees[id];

    if (statusBadge) {
      statusBadge.textContent = formatStatus(status);
      statusBadge.className = `status-badge ${status}`;
    }
  });
}

function formatStatus(status) {
  if (status === "not_checked_in") return "Not Checked In";
  if (status === "pending") return "Pending...";
  if (status === "checked_in") return "Checked In";
  return status;
}

async function scanBadge(attendeeId) {
  logActivity(`Initiating scan for ${attendeeId}...`);

  try {
    const response = await fetch("/api/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ attendee_id: attendeeId }),
    });

    const data = await response.json();

    if (!response.ok) {
      const errorMsg = data.detail || data.message || "Scan blocked";
      logActivity(`BLOCKED: ${errorMsg}`);
      showNotification(errorMsg, "error");
      return;
    }

    logActivity(`Scan queued for ${attendeeId}. Printing badge...`);
    showNotification(`Scan initiated for ${attendeeId}`, "success");
    fetchAttendees();
  } catch (error) {
    logActivity(`ERROR: ${error.message}`);
    showNotification("An error occurred during scan.", "error");
  }
}

function logActivity(message) {
  const log = document.getElementById("activity-log");
  if (!log) return;
  const time = new Date().toLocaleTimeString();
  const entry = document.createElement("p");
  entry.textContent = `[${time}] ${message}`;
  log.prepend(entry);
}

function showNotification(message, type) {
  const alertBox = document.getElementById("notification");
  if (!alertBox) return;
  alertBox.textContent = message;
  alertBox.className = `notification ${type}`;
  alertBox.style.display = "block";
  setTimeout(() => {
    alertBox.style.display = "none";
  }, 4000);
}
