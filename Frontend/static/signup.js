document.addEventListener("DOMContentLoaded", () => {
    const step1Form = document.getElementById("signup-form-step1");
    const step2Form = document.getElementById("signup-form-step2");
    const step1Div = document.getElementById("part1");
    const step2Div = document.getElementById("part2");
    const message = document.getElementById("message");
    const home = document.getElementById("home-button");

    let signupInfo = {};

    // Home button
    home.addEventListener("click", () => {
        window.location.href = "../HTML/index.html";
    });

    //Password strength checker
    const pass = document.getElementById("password");
    const strengthMessage = document.getElementById("password-strength");

    pass.addEventListener("input", () => {
        const value = pass.value;
        let strength = 0;

        // Actual checks
        if (value.length >= 8) strength++;          // min 8 chars
        if (/[A-Z]/.test(value)) strength++;        // 1 upper
        if (/[a-z]/.test(value)) strength++;        // 1 lower
        if (/[0-9]/.test(value)) strength++;        // 1 num
        if (/[\W_]/.test(value)) strength++;        // 1 special char

        // Update message
        if (strength === 0) {
            strengthMessage.textContent = "";
        } else if (strength === 1 || strength === 2) {
            strengthMessage.textContent = "Weak password";
            strengthMessage.style.color = "red";
        }
        else if (strength === 3 || strength === 4) {
            strengthMessage.textContent = "Mid password";
            strengthMessage.style.color = "orange";
        } else if (strength === 5) {
            strengthMessage.textContent = "Strong password";
            strengthMessage.style.color = "green";
        } else {
            strengthMessage.textContent = "";
        }
    });

    step1Form.addEventListener("submit", async (e) => {
        e.preventDefault();
        message.textContent = "";

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        if (!email || !password || !confirmPassword) {
            message.style.color = "red";
            message.textContent = "Please fill in all fields.";
            return;
        }

        if (password !== confirmPassword) {
            message.style.color = "red";
            message.textContent = "Passwords do not match.";
            return;
        }

        //Page 1 Data
        signupInfo.email = email;
        signupInfo.password = password;

        step1Div.style.display = "none";
        step2Div.style.display = "block";
    });

    //Page 2
    step2Form.addEventListener("submit", async (e) => {
        e.preventDefault();
        message.textContent = "";

        signupInfo.user_type = document.getElementById("user-type").value;
        signupInfo.security_question = document.getElementById("security-question").value;
        signupInfo.security_answer = document.getElementById("security-answer").value.trim();

        if (!signupInfo.user_type || !signupInfo.security_question || !signupInfo.security_answer) {
            message.style.color = "red";
            message.textContent = "Please fill in all fields.";
            return;
        }

        //Sending to backend
        try {
            const response = await fetch("/signup", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(signupInfo),
            });

            const data = await response.json();

            if (response.ok) {
                message.style.color = "green";
                message.textContent = data.message || "Account created successfully!";
                setTimeout(() => window.location.href = "../HTML/login.html", 1000);
            } else {
                message.style.color = "red";
                message.textContent = data.error || "Signup failed.";
            }
        } catch (err) {
            message.style.color = "red";
            message.textContent = "Network error. Please try again.";
            console.error(err);
        }
    });
});
