// resetPassword.js
document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("resetPw");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const inputs = form.querySelectorAll("input[type='password']");
        const newPassword = inputs[0].value;
        const confirmPassword = inputs[1].value;

        const email = localStorage.getItem("resetEmail");
        const securityAnswer = localStorage.getItem("securityAnswer");

        if (!email || !securityAnswer) {
            alert("Session expired. Please restart password reset.");
            window.location.href = "/Frontend/HTML/forgotPassword.html";
            return;
        }

        if (!newPassword || !confirmPassword) {
            alert("Please fill in both password fields.");
            return;
        }

        if (newPassword !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        try {
            const response = await fetch("/password-reset", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    email,
                    new_password: newPassword,
                    security_answer: securityAnswer,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.message || "Password reset successful!");
                localStorage.removeItem("resetEmail");
                localStorage.removeItem("securityAnswer");
                window.location.href = "/Frontend/HTML/login.html";
            } else {
                alert(data.error || "Password reset failed.");
            }
        } catch (err) {
            alert("Network error. Please try again.");
            console.error(err);
        }
    });
});


