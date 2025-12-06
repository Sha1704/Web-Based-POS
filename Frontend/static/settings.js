document.addEventListener("DOMContentLoaded", () => {
    const logout = document.getElementById("logout-button");
    const feedbackInput = document.getElementById("feedbackInput");
    const feedbackDisplay = document.getElementById("feedbackDisplay");

    // Logout
    logout.addEventListener("click", () => {
        const url = logout.dataset.logoutUrl;
        if (url) {
            window.location.href = url; // goes to /logout
        } else {
            console.error("Logout URL not found!");
        }
    });

    // Load feedback from backend
    async function loadFeedback() {
        try {
            const res = await fetch("/feedback/get");
            const data = await res.json();

            if (!data || data.length === 0) {
                feedbackDisplay.innerHTML = `<p class="text-muted">No feedback yet.</p>`;
                return;
            }
            feedbackDisplay.innerHTML = data.map((fb, index) => `
                <div class="card mb-2">
                    <div class="card-body p-2">
                        <strong>Feedback #${index + 1}:</strong> ${fb.feedback || fb.text}
                    </div>
                </div>
            `).join("");
        } catch (err) {
            console.error("Error loading feedback:", err);
            feedbackDisplay.innerHTML = `<p class="text-danger">Failed to load feedback.</p>`;
        }
    }

    loadFeedback();

    // Submit feedback
    window.submitFeedback = async function () {
        const feedbackText = feedbackInput.value.trim();
        if (!feedbackText) {
            alert("Please write some feedback before submitting.");
            return;
        }

        try {
            const res = await fetch("/feedback/add", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ feedback: feedbackText })
            });

            if (!res.ok) throw new Error("Failed to submit feedback");
            loadFeedback();

        } catch (err) {
            console.error(err);
            alert("Error submitting feedback. Please try again.");
        }
    }
});
