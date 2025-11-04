document.addEventListener("DOMContentLoaded", function () {
    const links = document.querySelectorAll(".sidebar a");
    const screens = document.querySelectorAll(".screen");
  
    // When you click a nav item
    links.forEach(link => {
      link.addEventListener("click", e => {
        e.preventDefault();
  
        // Remove "active" class from all
        links.forEach(l => l.classList.remove("active"));
        link.classList.add("active");
  
        // Find which screen to show
        const target = link.textContent.trim().toLowerCase();
  
        screens.forEach(screen => {
          if (screen.id === `${target}-screen`) {
            screen.classList.remove("d-none");
          } else {
            screen.classList.add("d-none");
          }
        });
      });
    });
  });
  