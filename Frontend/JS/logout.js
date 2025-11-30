document.addEventListener("DOMContentLoaded", () => {
    const logout = document.getElementById("logout-button");

    //Logout
    logout.addEventListener("click", () => {
        window.location.href = "../HTML/login.html";
    });
});
