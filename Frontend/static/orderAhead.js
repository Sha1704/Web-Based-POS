const OA_TAX_RATE = 0.02; // frontend display only
let backendItems = []; // fetched from backend
let oaItems = [];      // current order items

// ---------------------------
// Populate item dropdown
// ---------------------------
function oa_populateDropdown() {
    const select = document.getElementById("oa-item-select");
    select.innerHTML = `<option value="">-- Select an item --</option>`;

    oaDB.forEach(item => {
        const opt = document.createElement("option");

        // IMPORTANT: backend expects item_name
        opt.value = item.name;
        opt.textContent = `${item.name} - $${item.price.toFixed(2)}`;

        select.appendChild(opt);
    });
}

// ---------------------------
// Populate item dropdown
// ---------------------------
function oa_populateDropdown(items) {
    const select = document.getElementById("oa-item-select");
    select.innerHTML = `<option value="">-- Select an item --</option>`;

    items.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item[0]; // id
        const price = parseFloat(item[3]) || 0; // convert string to number
        opt.textContent = `${item[1]} - $${price.toFixed(2)}`;
        select.appendChild(opt);
    });
}

// Fetch available items for order ahead
async function fetchOrderItems() {
    try {
        const response = await fetch("/inventory/items");
        const items = await response.json();
        backendItems = items;
        oa_populateDropdown(backendItems);
    } catch (err) {
        console.error("Failed to fetch order ahead items", err);
    }
}

window.onload = function () {
    fetchOrderItems();
    // ...existing code...
};

// ---------------------------
// Add item to order
// ---------------------------
function oa_addItem() {
    const itemId = document.getElementById("oa-item-select").value;
    const qty = Number(document.getElementById("oa-qty").value);

    if (!itemId || qty <= 0) {
        alert("Choose an item and quantity.");
        return;
    }

    // const item = oaDB.find(f => f.name === itemName);
    const item = backendItems.find(f => f[0] == itemId);
    if (!item) return alert("Item not found.");

    oaItems.push({
        item_name: item[1],
        quantity: qty,
        price: parseFloat(item[3]) || 0  // convert string to number
    });

    oa_renderOrder();
}

// ---------------------------
// Render table + summary
// ---------------------------
function oa_renderOrder() {
    const tbody = document.querySelector("#oa-table tbody");
    tbody.innerHTML = "";

    let subtotal = 0;

    oaItems.forEach(item => {
        const row = document.createElement("tr");
        const total = item.quantity * item.price;
        subtotal += total;

        row.innerHTML = `
            <td>${item.item_name}</td>
            <td>${item.quantity}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>$${total.toFixed(2)}</td>
             <td>
                <div class="item-rating" data-item="${item.item_name}">
                    <i class="fa-regular fa-star" data-value="1"></i>
                    <i class="fa-regular fa-star" data-value="2"></i>
                    <i class="fa-regular fa-star" data-value="3"></i>
                    <i class="fa-regular fa-star" data-value="4"></i>
                    <i class="fa-regular fa-star" data-value="5"></i>
                </div>
            </td>
        `;

        tbody.appendChild(row);
        attachStarListeners(row);
    });

    const tax = subtotal * OA_TAX_RATE;
    const finalTotal = subtotal + tax;

    document.getElementById("oa-summary").innerHTML = `
        <div>Subtotal: $${subtotal.toFixed(2)}</div>
        <div>Tax (2%): $${tax.toFixed(2)}</div>
        <div><strong>Total: $${finalTotal.toFixed(2)}</strong></div>
    `;
}

// ---------------------------
// Listeners for the stars
// ---------------------------
function attachStarListeners(row) {
    const stars = row.querySelectorAll('.item-rating i');
    const itemName = row.querySelector('.item-rating').dataset.item;
    
    let selectedRating = 0;

    stars.forEach(star => {
        const value = parseInt(star.dataset.value);

        // ----- Hover in -----
        star.addEventListener('mouseenter', () => {
            stars.forEach(s => {
                s.className = parseInt(s.dataset.value) <= value ? 'fa-solid fa-star' : 'fa-regular fa-star';
            });
        });

        // ----- Hover out -----
        star.addEventListener('mouseleave', () => {
            stars.forEach(s => {
                s.className = parseInt(s.dataset.value) <= selectedRating ? 'fa-solid fa-star' : 'fa-regular fa-star';
            });
        });

        // ----- Click -----
        star.addEventListener('click', async () => {
            selectedRating = value;

            const customerEmail = prompt("Enter your email to rate this item:");
            if (!customerEmail) return alert("Email required to rate item.");

            try {
                const response = await fetch("http://127.0.0.1:5000/rate", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        customer_email: customerEmail,
                        item_name: itemName,
                        rating: selectedRating
                    })
                });

                const result = await response.json();
                alert(result.message);
            } catch (err) {
                alert("Failed to submit rating.");
                console.error(err);
            }
        });
    });
}


// ---------------------------
// Visually show stars
// ---------------------------
function updateStarsUI(container, rating) {
    container.querySelectorAll('i').forEach(star => {
        star.className = (parseInt(star.dataset.value) <= rating)
            ? 'fa-solid fa-star'
            : 'fa-regular fa-star';
    });
}


// ---------------------------
// Submit order to backend
// ---------------------------
async function oa_submitOrder() {
    if (oaItems.length === 0) {
        alert("No items in order.");
        return;
    }

    const pickupTime = document.getElementById("oa-pickup-time").value;

    // Build request body EXACTLY how backend expects
    const bodyData = {
        customer_email: "test@example.com", // later replace with logged-in user
        items: oaItems.map(i => ({
            item_name: i.item_name,
            quantity: i.quantity
        })),
        tip: 0,
        note: pickupTime ? `Pickup at ${pickupTime}` : null
    };

    try {
        const response = await fetch("http://127.0.0.1:5000/orderAhead", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(bodyData)
        });

        const result = await response.json();

        if (result.success) {
            alert(`Order placed successfully! Receipt #${result.receipt_id}`);

            // Clear UI
            oaItems = [];
            oa_renderOrder();
        } else {
            alert(result.message);
        }
    } catch (err) {
        alert("Failed to submit order. Server error.");
        console.error(err);
    }
}
