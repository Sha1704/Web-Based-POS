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


  
  // === BILL SCREEN INTERACTIVITY ===
  document.addEventListener("DOMContentLoaded", function () {
    const billList = document.getElementById("bill-list");
    const billDetails = document.getElementById("bill-details");
  
    // Example bill data (you can replace this with data from backend later)
    const bills = {
      1: {
        customer: "John Doe",
        items: [
          { name: "Latte", qty: 2, price: 4.5 },
          { name: "Bagel", qty: 1, price: 3.0 },
          { name: "Muffin", qty: 2, price: 2.5 },
        ],
      },
      2: {
        customer: "Sarah Smith",
        items: [
          { name: "Espresso", qty: 1, price: 3.0 },
          { name: "Croissant", qty: 2, price: 2.5 },
        ],
      },
      3: {
        customer: "David Jones",
        items: [
          { name: "Cappuccino", qty: 1, price: 4.0 },
          { name: "Donut", qty: 3, price: 1.5 },
        ],
      },
    };
  
    // When clicking on a bill
    billList.addEventListener("click", (e) => {
      const billItem = e.target.closest(".bill-item");
      if (!billItem) return;
  
      const billId = billItem.getAttribute("data-bill");
      const bill = bills[billId];
  
      if (!bill) return;
  
      // Highlight selected bill
      document.querySelectorAll(".bill-item").forEach(item => item.classList.remove("active"));
      billItem.classList.add("active");
  
      // Build bill detail table
      const total = bill.items.reduce((sum, item) => sum + item.qty * item.price, 0);
  
      billDetails.innerHTML = `
        <h5>Customer: ${bill.customer}</h5>
        <table class="table table-striped mt-3">
          <thead>
            <tr>
              <th>Item</th>
              <th>Qty</th>
              <th>Price</th>
              <th>Subtotal</th>
            </tr>
          </thead>
          <tbody>
            ${bill.items
              .map(
                (item) => `
              <tr>
                <td>${item.name}</td>
                <td>${item.qty}</td>
                <td>$${item.price.toFixed(2)}</td>
                <td>$${(item.qty * item.price).toFixed(2)}</td>
              </tr>`
              )
              .join("")}
          </tbody>
        </table>
        <h5 class="mt-3">Total: $${total.toFixed(2)}</h5>
        <button class="btn btn-success mt-3">Proceed to Payment</button>
      `;
    });
  });