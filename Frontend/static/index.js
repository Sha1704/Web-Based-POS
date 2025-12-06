// JS/index.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("Home page loaded");
      const link = document.querySelector(".sidebar a.active"); // adjust selector as needed
      if (!link) return;
      const target = link.textContent.trim().toLowerCase();
      const screens = document.querySelectorAll(".screen");
      screens.forEach(screen => {
        if (!screen.classList.contains("admin-locked")) {
          screen.classList.toggle("d-none", screen.id !== `${target}-screen`);
      }
      });
    });
