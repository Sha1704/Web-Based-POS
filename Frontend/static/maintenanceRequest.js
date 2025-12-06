// Display maintenance requests from database
function displayFeedback(feedbackList) {
    const feedbackContainer = document.getElementById('feedback-section');
    let feedbackHTML = '<h3>Previous Submissions:</h3><ul>';

    feedbackList.forEach((f, index) => {
        feedbackHTML += `
            <li>
                <strong>#${index + 1}:</strong> ${f[2]} <em>(${f[1]})</em>
                <button onclick="deleteFeedback(${f[0]})">Delete</button>
            </li>
        `;
    });

    feedbackHTML += '</ul>';

    // Remove old list if exists
    const oldList = document.getElementById('feedback-list');
    if (oldList) oldList.remove();

    const div = document.createElement('div');
    div.id = 'feedback-list';
    div.innerHTML = feedbackHTML;
    feedbackContainer.appendChild(div);
}

// Fetch maintenance requests from backend
async function fetchFeedback() {
    try {
        const response = await fetch('/maintenance');
        const data = await response.json();

        if (Array.isArray(data)) {
            displayFeedback(data);
        } else {
            console.error("Invalid response from server:", data);
        }
    } catch (err) {
        console.error("Failed to fetch maintenance requests:", err);
    }
}

// Submit new maintenance request
async function submitFeedback() {
    const feedbackInput = document.getElementById('feedbackInput').value.trim();

    if (!feedbackInput) {
        alert("Please enter a description of the problem.");
        return;
    }

    try {
        const response = await fetch('/maintenanceRequest', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: feedbackInput })
        });

        const data = await response.json();

        if (data.success) {
            // Clear input
            document.getElementById('feedbackInput').value = "";
            // Refresh the list
            fetchFeedback();
        } else {
            alert("Failed to submit request: " + data.message);
        }
    } catch (err) {
        console.error("Failed to submit feedback:", err);
        alert("Error submitting maintenance request. See console for details.");
    }
}

// Delete a maintenance request
async function deleteFeedback(id) {
    if (!confirm("Are you sure you want to delete this maintenance request?")) return;

    try {
        const response = await fetch(`/maintenance/delete/${id}`, { method: "DELETE" });
        const data = await response.json();

        if (data.success) {
            // Refresh list after deletion
            fetchFeedback();
        } else {
            alert("Failed to delete: " + data.message);
        }
    } catch (err) {
        console.error("Delete failed:", err);
        alert("Error deleting maintenance request. See console for details.");
    }
}

// Initialize on page load
window.onload = () => {
    fetchFeedback();
};
