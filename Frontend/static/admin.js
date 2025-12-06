//Admin Access Logic 
// Zoe Steinkoenig 12-05-2025
document.addEventListener("DOMContentLoaded", () => {
    const unlocked = localStorage.getItem("adminUnlocked") === "true";

    document.querySelectorAll(".admin-locked").forEach(el => {
        unlocked ? el.classList.remove("d-none") : el.classList.add("d-none");
    });

    const logoutBtn = document.getElementById("admin-logout-btn");
    if (logoutBtn) logoutBtn.classList.toggle("d-none", !unlocked);

    const successMsg = document.getElementById("admin-success");
    if (successMsg) successMsg.style.display = unlocked ? "block" : "none";
});

// Unlock button — safe checks and error handling
window.submitAdminCodeFromPage = async function () {
    const emailInput = document.getElementById("admin-email-input");
    const input = document.getElementById("admin-code-input");
    const error = document.getElementById("admin-error");
    const success = document.getElementById("admin-success");

    // Basic client validation
    const email = emailInput ? emailInput.value.trim() : "";
    const code = input ? input.value.trim() : "";

    if (!code) {
        if (error) {
            error.textContent = "Please enter the admin code.";
            error.style.display = "block";
        }
        return;
    }

    // Optional: quick client-side fallback (still do server check)
    // if (code === ADMIN_CODE) { ... }  // not secure; server must authorize

    try {
        const response = await fetch("/api/check-admin", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, code })
        });

        // if server returns non-JSON or error, handle gracefully
        const result = await response.json().catch(() => ({}));

        // Accept either `success` or `Success` just in case
        const ok = result.success === true || result.Success === true;

        if (ok) {
            localStorage.setItem("adminUnlocked", "true");
            document.querySelectorAll(".admin-locked").forEach(el => el.classList.remove("d-none"));
            document.getElementById("admin-logout-btn")?.classList.remove("d-none");
            if (error) error.style.display = "none";
            if (success) {
                success.textContent = "Admin access granted! Sales & Inventory are now visible.";
                success.style.display = "block";
            }
        } else {
            if (error) {
                error.textContent = "Incorrect code or email.";
                error.style.display = "block";
            }
        }

    } catch (err) {
        console.error("Error checking admin:", err);
        if (error) {
            error.textContent = "Network/server error. Check console.";
            error.style.display = "block";
        }
    } finally {
        if (input) input.value = "";
    }
};

window.clearAdminAccess = function () {
    localStorage.removeItem("adminUnlocked");
    document.querySelectorAll(".admin-locked").forEach(el => el.classList.add("d-none"));
    document.getElementById("admin-logout-btn")?.classList.add("d-none");
    const success = document.getElementById("admin-success");
    if (success) success.style.display = "none";
};

// // Fetch and display all users
// async function loadUsers() {
//     try {
//         const response = await fetch("/admin/users");
//         const users = await response.json();
//         renderUsers(users);
//     } catch (err) {
//         console.error("Failed to fetch users", err);
//     }
// }

// function renderUsers(users) {
//     const tbody = document.getElementById("admin-users-body");
//     tbody.innerHTML = "";
//     users.forEach(user => {
//         const tr = document.createElement("tr");
//         tr.innerHTML = `
//             <td>${user.email}</td>
//             <td>${user.user_type}</td>
//             <td>${user.security_question}</td>
//             <td>${user.security_answer}</td>
//         `;
//         tbody.appendChild(tr);
//     });
// }

// window.onload = function () {
//     loadUsers();
// };
