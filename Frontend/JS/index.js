document.addEventListener("DOMContentLoaded", function () {
  // ===== Sidebar Navigation =====
  const links = document.querySelectorAll(".sidebar a");
  const screens = document.querySelectorAll(".screen");

  links.forEach(link => {
    link.addEventListener("click", e => {
      e.preventDefault();
      links.forEach(l => l.classList.remove("active"));
      link.classList.add("active");

      const target = link.textContent.trim().toLowerCase();
      screens.forEach(screen => {
        screen.classList.toggle("d-none", screen.id !== `${target}-screen`);
      });
    });
  });
  { // === INVENTORY ===
    // inventory loader
    async function loadInventoryHTML() {
      const container = document.getElementById("inventory-content");
      if (!container) return;

      try {
        const response = await fetch("inventory.html");
        const html = await response.text();
        container.innerHTML = html;
      } catch (err) {
        container.innerHTML = "<p style='color:red'>Failed to load inventory.</p>";
        console.error(err);
      }
    }

    window.showInventoryScreen = function (e) {
      e.preventDefault();

      // Remove active class from all sidebar links
      document.querySelectorAll(".sidebar a").forEach(l => l.classList.remove("active"));
      e.currentTarget.classList.add("active");

      // Hide all screens
      document.querySelectorAll(".screen").forEach(s => s.classList.add("d-none"));

      // Show inventory screen
      const inventoryScreen = document.getElementById("inventory-screen");
      inventoryScreen.classList.remove("d-none");

      // Load inventory HTML dynamically
      loadInventoryHTML();
    };

    // Search bar
    document.addEventListener("input", function (e) {
      if (e.target.id === "inventory-search") {
        let searchValue = e.target.value.toLowerCase();

        document.querySelectorAll("#inventory-body tr").forEach(row => {
          let nameText = row.children[0]?.textContent.toLowerCase() || "";
          let categoryText = row.children[3]?.textContent.toLowerCase() || "";

          // Show row if search matches name OR category
          row.style.display =
            nameText.includes(searchValue) ||
              categoryText.includes(searchValue)
              ? "" : "none";
        });
      }
    });



    // Button for form toggle
    document.addEventListener("click", function (e) {
      if (e.target.id === "add-product-btn") {
        const form = document.getElementById("add-product-form");
        if (form) form.classList.toggle("d-none");
      }
    });

    // Save New Product to Table
    document.addEventListener("click", function (e) {
      if (e.target.id === "save-new-product") {

        const name = document.getElementById("new-item-name").value.trim();
        const qty = document.getElementById("new-item-qty").value;
        const price = document.getElementById("new-item-price").value;
        const category = document.getElementById("new-item-category").value;

        if (!name || qty === "" || price === "" || !category) {
          alert("Fill out all fields");
          return;
        }

        const row = `
        <tr>
          <td>${name}</td>
          <td>${qty}</td>
          <td>$${parseFloat(price).toFixed(2)}</td>
          <td>${category}</td>
          <td>
          <button class="btn btn-sm btn-warning edit-item">Edit</button>
          <button class="btn btn-danger btn-sm delete-item">X</button>
          </td>
        </tr>
      `;
        document.getElementById("inventory-body").insertAdjacentHTML("beforeend", row);

        // Clear inputs after save
        document.getElementById("new-item-name").value = "";
        document.getElementById("new-item-qty").value = "";
        document.getElementById("new-item-price").value = "";
        document.getElementById("new-item-category").value = "";
      }
    });

    //Category changer and creator
    let categories = ["Electronics", "Clothing", "Food"];

    // Add new category
    document.addEventListener("click", function (e) {
      if (e.target.id === "add-category-btn") {
        e.preventDefault();
        const newCatInput = document.getElementById("new-category-name");
        const select = document.getElementById("new-item-category");
        const newCategory = newCatInput.value.trim();

        if (!newCategory) return alert("Enter a category name.");

        if (!categories.includes(newCategory)) {
          categories.push(newCategory);

          // Add to dropdown
          const option = document.createElement("option");
          option.value = newCategory;
          option.textContent = newCategory;
          select.appendChild(option);
        }

        // Clear input
        newCatInput.value = "";
        select.value = newCategory;
      }
    });

    // Edit inventory
    document.addEventListener("click", function (e) {
      if (e.target.classList.contains("edit-item")) {
        const row = e.target.closest("tr");
        const cells = row.children;

        // If currently in edit mode, save the changes
        if (e.target.textContent === "Save") {
          // Grab updated values
          const newName = cells[0].querySelector("input").value.trim();
          const newQty = cells[1].querySelector("input").value;
          const newPrice = cells[2].querySelector("input").value;

          if (!newName || newQty === "" || newPrice === "") {
            alert("All fields must be filled!");
            return;
          }

          // Update row display
          cells[0].textContent = newName;
          cells[1].textContent = newQty;
          cells[2].textContent = `$${parseFloat(newPrice).toFixed(2)}`;

          // Restore buttons
          e.target.textContent = "Edit";
        } else {
          // Turn cells into input fields
          cells[0].innerHTML = `<input type="text" class="form-control" value="${cells[0].textContent}">`;
          cells[1].innerHTML = `<input type="number" class="form-control" min="0" value="${cells[1].textContent}">`;
          cells[2].innerHTML = `<input type="number" class="form-control" min="0" step="0.01" value="${cells[2].textContent.replace("$", "")}">`;

          // Change button to "Save"
          e.target.textContent = "Save";
        }
      }
    });


    // Delete Inventory Row
    document.addEventListener("click", function (e) {
      if (e.target.classList.contains("delete-item")) {
        e.target.closest("tr").remove();
      }
    });
  }
  // ===== Bill System =====
  const billList = document.getElementById("bill-list");
  const billItemsTable = document.querySelector("#bill-items tbody");
  const billNumberSpan = document.getElementById("bill-number");
  const newBillBtn = document.getElementById("new-bill-btn");

  const itemNameInput = document.getElementById("item-name");
  const itemQtyInput = document.getElementById("item-qty");
  const itemPriceInput = document.getElementById("item-price");

  let bills = {};
  let currentBill = null;

  function renderBillItems() {
    billItemsTable.innerHTML = "";

    if (!currentBill) {
      billNumberSpan.textContent = "—";
      return;
    }

    billNumberSpan.textContent = currentBill.id;

    currentBill.items.forEach((item, i) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.qty}</td>
        <td>$${item.price.toFixed(2)}</td>
        <td>$${(item.qty * item.price).toFixed(2)}</td>
        <td><button class="btn btn-sm btn-danger" data-index="${i}">X</button></td>
      `;
      billItemsTable.appendChild(row);
    });

    // handle delete buttons
    billItemsTable.querySelectorAll(".btn-danger").forEach(btn => {
      btn.addEventListener("click", e => {
        const index = e.target.getAttribute("data-index");
        currentBill.items.splice(index, 1);
        renderBillItems();
      });
    });
  }

  function addNewBill() {
    const newId = Object.keys(bills).length + 1;
    bills[newId] = { id: newId, items: [] };

    const newBillItem = document.createElement("li");
    newBillItem.classList.add("list-group-item", "bill-item");
    newBillItem.setAttribute("data-bill", newId);
    newBillItem.textContent = `Bill #${newId}`;
    billList.insertBefore(newBillItem, newBillBtn);

    newBillItem.addEventListener("click", () => selectBill(newId, newBillItem));
    newBillItem.click();
  }

  function selectBill(id, element) {
    document.querySelectorAll(".bill-item").forEach(item => item.classList.remove("active"));
    element.classList.add("active");
    currentBill = bills[id];
    renderBillItems();
  }

  function addItem() {
    if (!currentBill) {
      alert("Please select or create a bill first!");
      return;
    }

    const name = itemNameInput.value.trim();
    const qty = parseInt(itemQtyInput.value);
    const price = parseFloat(itemPriceInput.value);

    if (!name || qty <= 0 || isNaN(price)) {
      alert("Please enter valid item details.");
      return;
    }

    currentBill.items.push({ name, qty, price });
    itemNameInput.value = "";
    itemQtyInput.value = 1;
    itemPriceInput.value = "";

    renderBillItems();
  }

  function approveTransaction() {
    if (!currentBill) return alert("No bill selected.");
    const confirmApprove = confirm(`Approve transaction for Bill #${currentBill.id}?`);
    if (!confirmApprove) return;

    removeBill(currentBill.id);
    alert(`Bill #${currentBill.id} approved successfully.`);
  }

  function voidTransaction() {
    if (!currentBill) return alert("No bill selected.");
    const confirmVoid = confirm(`Void Bill #${currentBill.id}?`);
    if (!confirmVoid) return;

    removeBill(currentBill.id);
    alert(`Bill #${currentBill.id} has been voided.`);
  }

  function removeBill(id) {
    // Remove from data
    delete bills[id];

    // Remove from DOM
    const billElement = billList.querySelector(`[data-bill="${id}"]`);
    if (billElement) billElement.remove();

    // Clear current bill view
    currentBill = null;
    renderBillItems();
  }

  // ====== Event Listeners ======
  if (newBillBtn) newBillBtn.addEventListener("click", addNewBill);
  window.addItem = addItem;
  window.approveTransaction = approveTransaction;
  window.voidTransaction = voidTransaction;
});
