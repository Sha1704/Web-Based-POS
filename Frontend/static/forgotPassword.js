// forgotPassword.js
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("forgotForm");
    const modal = new bootstrap.Modal(document.getElementById("codeModal"));
    const verifyBtn = document.getElementById("verifyBtn");
    const codeInput = document.getElementById("verificationCode");

    let email = "";
    let securityQuestion = "";

    // Get Security Question
    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        email = form.querySelector("input[type='email']").value.trim();

        if (!email) {
            alert("Please enter your email.");
            return;
        }

        try {
            const response = await fetch("/get-security-question", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email }),
            });

            const data = await response.json();

            if (response.ok && data.question) {
                securityQuestion = data.question;
                document.querySelector("#codeModalLabel").textContent = securityQuestion;
                modal.show();
            } else {
                alert(data.error || "Email not found.");
            }
        } catch (err) {
            alert("Network error. Please try again.");
            console.error(err);
        }
    });

    // Verify Answer & Redirect
    verifyBtn.addEventListener("click", async () => {
        const answer = codeInput.value.trim();
        if (!answer) {
            alert("Please enter your answer.");
            return;
        }

        localStorage.setItem("resetEmail", email);
        localStorage.setItem("securityAnswer", answer);

        modal.hide();
        window.location.href = "../HTML/resetPassword.html";
    });
});
