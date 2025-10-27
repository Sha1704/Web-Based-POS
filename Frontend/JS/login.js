document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("login-form");
    const message = document.getElementById("message");
    const home = document.getElementById("home-button");

    // Redirect to homepage
    home.addEventListener("click", () => {
        window.location.href = "../HTML/index.html";
    });

    //Test for no backend
    form.addEventListener("submit", (e) => {
        e.preventDefault();
        message.textContent = "";

        const username = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;

        // Fake server response
        setTimeout(() => {
            if (username === "test" && password === "123") {
                message.style.color = "green";
                message.textContent = "Login successful!";
                // Redirect
                setTimeout(() => {
                     window.location.href = "../HTML/index.html";
                 }, 1000);
            } else {
                message.style.color = "red";
                message.textContent = "Invalid username or password.";
            }
        }, 300);
    });

    // When Backend is finished vv

    // form.addEventListener("submit", async (e) => {
    //     e.preventDefault();

    //     message.textContent = ""; // Clear old messages

    //     const email = document.getElementById("email").value.trim();
    //     const password = document.getElementById("password").value;

    //     if (!email || !password) {
    //         message.textContent = "Please enter both email and password.";
    //         return;
    //     }

    //     try {
    //         const response = await fetch("/login", {
    //             method: "POST",
    //             headers: { "Content-Type": "application/json" },
    //             body: JSON.stringify({ email, password }),
    //         });

    //         const data = await response.json();

    //         if (response.ok) {
    //             message.style.color = "green";
    //             message.textContent = "Login successful!";
    //             setTimeout(() => {
    //                 window.location.href = "home.html";
    //             }, 1000);
    //         } else {
    //             message.style.color = "red";
    //             message.textContent = data.error || "Invalid email or password.";
    //         }
    //     } catch (err) {
    //         message.style.color = "red";
    //         message.textContent = "Network error. Please try again.";
    //         console.error(err);
    //     }
    // });
});
