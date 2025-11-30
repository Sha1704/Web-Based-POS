// Temporary test menu (same idea as in bill.js)
const oaDB = [
    { id: 1, name: "Burger", price: 12.99 },
    { id: 2, name: "Fries", price: 4.99 },
    { id: 3, name: "Soda", price: 1.50 },
    { id: 4, name: "Pizza Slice", price: 5.00 },
    { id: 5, name: "Salad", price: 5.75 }
];

let oaItems = [];
const OA_TAX_RATE = 0.02;

// Populate dropdown
function oa_populateDropdown() {
    const select = document.getElementById("oa-item-select");
    select.innerHTML = `<option value="">-- Select an item --</option>`;

    oaDB.forEach(item => {
        const opt = document.createElement("option");
        opt.value = item.id;
        opt.textContent = `${item.name} - $${item.price.toFixed(2)}`;
        select.appendChild(opt);
    });
}

oa_populateDropdown();

// Add item to order
function oa_addItem() {
    const itemId = Number(document.getElementById("oa-item-select").value);
    const qty = Number(document.getElementById("oa-qty").value);

    if (!itemId || qty <= 0) {
        alert("Choose an item and quantity.");
        return;
    }

    const item = oaDB.find(f => f.id === itemId);

    oaItems.push({ name: item.name, qty, price: item.price });
    oa_renderOrder();
}

// Display table + summary
function oa_renderOrder() {
    const tbody = document.querySelector("#oa-table tbody");
    tbody.innerHTML = "";

    let subtotal = 0;

    oaItems.forEach(item => {
        const row = document.createElement("tr");
        const total = item.qty * item.price;
        subtotal += total;

        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.qty}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>$${total.toFixed(2)}</td>
        `;

        tbody.appendChild(row);
    });

    const tax = subtotal * OA_TAX_RATE;
    const finalTotal = subtotal + tax;

    document.getElementById("oa-summary").innerHTML = `
        <div>Subtotal: $${subtotal.toFixed(2)}</div>
        <div>Tax (2%): $${tax.toFixed(2())}</div>
        <div><strong>Total: $${finalTotal.toFixed(2)}</strong></div>
    `;
}

// Simulate placing order
function oa_submitOrder() {
    if (oaItems.length === 0) {
        alert("No items in order.");
        return;
    }

    const pickupTime = document.getElementById("oa-pickup-time").value;

    alert(
        pickupTime
            ? `Order placed! Pickup at ${pickupTime}.`
            : "Order placed! No pickup time selected."
    );

    // Clear UI after "placing" order
    oaItems = [];
    oa_renderOrder();
}
