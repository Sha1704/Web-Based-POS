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
