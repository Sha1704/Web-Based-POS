document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const message = document.getElementById("message");
    const home = document.getElementById("home-button");

    // Redirect to homepage
    home.addEventListener("click", () => {
        window.location.href = "/";
    });


    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        message.textContent = "";

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        if (!email || !password) {
            message.style.color = "red";
            message.textContent = "Email and password are required.";
            return;
        }

        try {
            const response = await fetch("/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({ email, password })
            });

            if (response.redirected) {
                window.location.href = response.url;
                return;
            }

            const data = await response.json();

            if (data.status === "fail") {
                message.style.color = "red";
                message.textContent = data.message || "Login failed.";
            }
        } catch (err) {
            console.error("Login error:", err);
            message.style.color = "red";
            message.textContent = "Server error, please try again later.";
        }
    });
});
