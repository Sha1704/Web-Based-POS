// Load inventory items
async function loadInventory() {
    const res = await fetch("/inventory/items");
    const data = await res.json();
    renderInventory(data);
}

// Render inventory table rows
function renderInventory(items) {
    const tbody = document.getElementById("inventory-body");
    tbody.innerHTML = "";

    items.forEach(item => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
        <td>${item[1]}</td>
        <td>${item[2]}</td>
        <td>${item[3]}</td>
        <td>${item[4]}</td>
        <td>
            <button class="btn btn-sm btn-warning" onclick="editItem(${item[0]})">Edit</button>
            <button class="btn btn-sm btn-danger" onclick="deleteItem(${item[0]})">Delete</button>
        </td>
    `;
        tbody.appendChild(tr);
    });
}

// Search Filter
document.getElementById("inventory-search").addEventListener("input", async function () {
    const query = this.value.toLowerCase();

    const res = await fetch("/inventory/items");
    const items = await res.json();

    const filtered = items.filter(i => {
        const name = i[1].toLowerCase();
        const category = i[4].toLowerCase();
        return name.includes(query) || category.includes(query);
    });

    renderInventory(filtered);
});

// Add product form toggle
document.getElementById("add-product-btn").addEventListener("click", () => {
    document.getElementById("add-product-form").classList.toggle("d-none");
});

// Add new product
document.getElementById("save-new-product").addEventListener("click", async () => {
    const item_name = document.getElementById("new-item-name").value;
    const qty = Number(document.getElementById("new-item-qty").value);
    const price = Number(document.getElementById("new-item-price").value);
    const category = document.getElementById("new-item-category").value;

    if (!item_name || price <= 0 || qty < 0 || !category) {
        alert("Please fill in all fields correctly.");
        return;
    }

    const res = await fetch("/inventory/add", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ item_name, price, quantity: qty, category_id: category })
    });

    if (!res.ok) {
        const errText = await res.text();
        console.error("Add item failed:", errText);
        alert("Item addition failed");
        return;
    }

    alert("Item added!");
    loadInventory();
});

// Load categories into the dropdown
async function loadCategories() {
    const res = await fetch("/inventory/categories");
    const categories = await res.json();

    const select = document.getElementById("new-item-category");
    select.innerHTML = '<option value="">Please Select Category</option>';
    categories.forEach(cat => {
        const opt = document.createElement("option");
        opt.value = cat[0];
        opt.textContent = cat[1];
        select.appendChild(opt);
    });

    const listDiv = document.getElementById("category-list");
    if (!listDiv) return;
    listDiv.innerHTML = "";
    categories.forEach(cat => {
        const div = document.createElement("div");
        div.className = "d-flex justify-content-between align-items-center mb-1";
        div.innerHTML = `
            <span>${cat[1]}</span>
            <button class="btn btn-sm btn-danger" onclick="deleteCategory(${cat[0]}, '${cat[1]}')">Delete</button>
        `;
        listDiv.appendChild(div);
    });
}


// Add new category
document.getElementById("add-category-btn").addEventListener("click", async () => {
    const categoryInput = document.getElementById("new-category-name");
    const categoryValue = categoryInput.value.trim();

    if (!categoryValue) {
        alert("Please enter a category name.");
        return;
    }

    try {
        const res = await fetch("/inventory/category", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ category_name: categoryValue })
        });

        const data = await res.json();

        if (res.ok && data.status === "success") {
            await loadCategories();
            categoryInput.value = "";
            alert(`Category "${categoryValue}" added.`);
        } else {
            alert(`Failed to add category: ${data.message}`);
        }
    } catch (err) {
        console.error(err);
        alert("Error adding category");
    }
});

// Delete category
async function deleteCategory(categoryId, categoryName) {
    if (!confirm(`Are you sure you want to delete category "${categoryName}"?`)) return;

    try {
        const res = await fetch("/inventory/category/delete", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ category_id: categoryId })
        });

        const data = await res.json();

        if (res.ok && data.status === "success") {
            alert(`Category "${categoryName}" deleted.`);
            await loadCategories();
            loadInventory();
        } else {
            alert(`Failed to delete category: ${data.message}`);
        }
    } catch (err) {
        console.error(err);
        alert("Error deleting category");
    }
}

// Edit item 
async function editItem(id) {
    const res = await fetch(`/inventory/get?id=${id}`);
    const item = await res.json();

    document.getElementById("edit-item-id").value = item.item_id;
    document.getElementById("edit-item-name").value = item.item_name;
    document.getElementById("edit-item-qty").value = item.quantity;
    document.getElementById("edit-item-price").value = item.price;

    const categorySelect = document.getElementById("edit-item-category");
    categorySelect.innerHTML = ""; 

    const categoriesRes = await fetch("/inventory/categories");
    const categories = await categoriesRes.json();

    categories.forEach(cat => {
        const option = document.createElement("option");
        option.value = cat[0]; 
        option.textContent = cat[1];
        if (cat[1] === item.category) option.selected = true;
        categorySelect.appendChild(option);
    });

    document.getElementById("edit-product-form").classList.remove("d-none");
}

// Save edits
document.getElementById("save-edit-product").addEventListener("click", async () => {
    const id = document.getElementById("edit-item-id").value;
    const name = document.getElementById("edit-item-name").value.trim();
    const qty = Number(document.getElementById("edit-item-qty").value);
    const price = Number(document.getElementById("edit-item-price").value);
    const category = document.getElementById("edit-item-category").value;

    if (!name || price <= 0 || qty < 0 || !category) {
        alert("Please fill all fields correctly.");
        return;
    }

    const res = await fetch("/inventory/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            id: id,
            product_name: name,
            quantity: qty,
            price: price,
            category
        })
    });

    const data = await res.json();
    if (res.ok && data.status === "success") {
        loadInventory();
        document.getElementById("edit-product-form").classList.add("d-none");
    } else {
        alert(`Failed to update product: ${data.message}`);
    }
});


// Cancel edits
document.getElementById("cancel-edit").addEventListener("click", () => {
    document.getElementById("edit-product-form").classList.add("d-none");
});

// Manage Categories
document.getElementById("toggle-category-list").addEventListener("click", () => {
    const listDiv = document.getElementById("category-list");
    listDiv.classList.toggle("d-none");
});

// Delete item 
async function deleteItem(id) {
    if (!confirm("Are you sure you want to delete this item?")) return;

    await fetch(`/inventory/delete?id=${id}`, { method: "POST" });
    loadInventory();
}

// Initial load
window.onload = function () {
    loadInventory();
    loadCategories();
};
