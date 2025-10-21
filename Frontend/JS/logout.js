document.addEventListener("DOMContentLoaded", () => {
    const logout = document.getElementById("logout-button");
});

    //Logout
    logout.addEventListener("click", () => {
        
        //Refresh homepage after logout
        window.location.href = "../HTML/index.html";
    })