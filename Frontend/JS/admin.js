// ../JS/admin.js
const ADMIN_CODE = "1234";   // ← change this

// Run AFTER the full page (DOM) is ready → this is the key!
document.addEventListener("DOMContentLoaded", () => {
    const unlocked = localStorage.getItem("adminUnlocked") === "true";

    // Now the elements definitely exist
    document.querySelectorAll(".admin-locked").forEach(el => {
        unlocked ? el.classList.remove("d-none") : el.classList.add("d-none");
    });

    const logoutBtn = document.getElementById("admin-logout-btn");
    if (logoutBtn) logoutBtn.classList.toggle("d-none", !unlocked);

    const successMsg = document.getElementById("admin-success");
    if (successMsg) successMsg.style.display = unlocked ? "block" : "none";
});

// Unlock button
window.submitAdminCodeFromPage = function () {
    const input   = document.getElementById("admin-code-input");
    const error   = document.getElementById("admin-error");
    const success = document.getElementById("admin-success");

    if (input && input.value.trim() === ADMIN_CODE) {
        localStorage.setItem("adminUnlocked", "true");
        document.querySelectorAll(".admin-locked").forEach(el => el.classList.remove("d-none"));
        document.getElementById("admin-logout-btn")?.classList.remove("d-none");
        if (error)   error.style.display = "none";
        if (success) success.style.display = "block";
        input.value = "";
    } else {
        if (error) error.style.display = "block";
    }
};

// Revoke button
window.clearAdminAccess = function () {
    localStorage.removeItem("adminUnlocked");
    document.querySelectorAll(".admin-locked").forEach(el => el.classList.add("d-none"));
    document.getElementById("admin-logout-btn")?.classList.add("d-none");
    const success = document.getElementById("admin-success");
    if (success) success.style.display = "none";
};