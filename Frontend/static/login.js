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

});
