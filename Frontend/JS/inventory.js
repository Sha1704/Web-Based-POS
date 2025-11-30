// -----------------------------
// Load inventory items
// -----------------------------
async function loadInventory() {
    const res = await fetch("/inventory/get"); // hook to your backend
    const data = await res.json();
    renderInventory(data);
}

// -----------------------------
// Render inventory table rows
// -----------------------------
function renderInventory(items) {
    const tbody = document.getElementById("inventory-body");
    tbody.innerHTML = "";

    items.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${item.item_name}</td>
            <td>${item.quantity}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>${item.category || "—"}</td>
            <td>
                <button class="btn btn-sm btn-warning" onclick="editItem(${item.item_id})">Edit</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// -----------------------------
// Search Filter
// -----------------------------
document.getElementById("inventory-search").addEventListener("input", async function () {
    const query = this.value.toLowerCase();

    const res = await fetch("/inventory/get");
    const items = await res.json();

    const filtered = items.filter(i =>
        i.item_name.toLowerCase().includes(query)
    );

    renderInventory(filtered);
});

// -----------------------------
// Add product form toggle
// -----------------------------
document.getElementById("add-product-btn").addEventListener("click", () => {
    document.getElementById("add-product-form").classList.toggle("d-none");
});

// -----------------------------
// Add new product
// -----------------------------
document.getElementById("save-new-product").addEventListener("click", async () => {
    const name = document.getElementById("new-item-name").value;
    const qty = Number(document.getElementById("new-item-qty").value);
    const price = Number(document.getElementById("new-item-price").value);
    const category = document.getElementById("new-item-category").value;

    if (!name || price <= 0 || qty < 0) {
        alert("Please fill in all fields correctly.");
        return;
    }

    await fetch("/inventory/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, price, quantity: qty, category })
    });

    alert("Item added!");

    loadInventory();
});

// -----------------------------
// Edit item (open modal)
// -----------------------------
async function editItem(id) {
    const res = await fetch(`/inventory/get?id=${id}`);
    const item = await res.json();

    const newName = prompt("Item Name:", item.item_name);
    const newQty = prompt("Quantity:", item.quantity);
    const newPrice = prompt("Price:", item.price);
    const newCat = prompt("Category:", item.category);

    if (!newName || !newQty || !newPrice) return;

    await fetch("/inventory/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            product_name: newName,
            quantity: Number(newQty),
            price: Number(newPrice),
            category: newCat
        })
    });

    loadInventory();
}

// Initial load
loadInventory();
