// -----------------------------
// Load inventory items
// -----------------------------
async function loadInventory() {
    const res = await fetch("/inventory/get");
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
                <button class="btn btn-sm btn-danger" onclick="deleteItem(${item.item_id})">Delete</button>
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

    if (!name || price <= 0 || qty < 0 || !category) {
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
// Add new category
// -----------------------------
document.getElementById("add-category-btn").addEventListener("click", () => {
    const categoryInput = document.getElementById("new-category-name");
    const categoryValue = categoryInput.value.trim();

    if (!categoryValue) {
        alert("Please enter a category name.");
        return;
    }

    const select = document.getElementById("new-item-category");

    // Check if category already exists
    const exists = Array.from(select.options).some(opt => opt.value.toLowerCase() === categoryValue.toLowerCase());
    if (exists) {
        alert("This category already exists.");
        return;
    }

    // Create new option and append
    const newOption = document.createElement("option");
    newOption.value = categoryValue;
    newOption.textContent = categoryValue;
    select.appendChild(newOption);
    select.value = categoryValue;

    alert(`Category "${categoryValue}" added.`);
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

// -----------------------------
// Delete item (open modal)
// -----------------------------
async function deleteItem(id) {
    if (!confirm("Are you sure you want to delete this item?")) return;

    await fetch(`/inventory/delete?id=${id}`, { method: "POST" });
    loadInventory();
}


// Initial load
loadInventory();
