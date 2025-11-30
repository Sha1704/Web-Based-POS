// Your admin code
const ADMIN_CODE = "1234";  // Change this!

// When user clicks "Admin"
document.getElementById("admin-link").addEventListener("click", function (e) {
    e.preventDefault();
    showAdminModal();
});

// Show popup
function showAdminModal() {
    document.getElementById("admin-modal").style.display = "flex";
}

// Close popup
function closeAdminModal() {
    document.getElementById("admin-modal").style.display = "none";
    document.getElementById("admin-error").style.display = "none";
    document.getElementById("admin-input").value = "";
}

// Submit admin code
function submitAdminCode() {
    const input = document.getElementById("admin-input").value;

    if (input === ADMIN_CODE) {
        localStorage.setItem("adminUnlocked", "true");
        unlockAdminSections();
        closeAdminModal();
        alert("Admin access granted.");
    } else {
        document.getElementById("admin-error").style.display = "block";
    }
}

// Reveal hidden pages
function unlockAdminSections() {
    const lockedLinks = document.querySelectorAll(".admin-locked");
    lockedLinks.forEach(link => link.classList.remove("d-none"));
}
