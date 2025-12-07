// Bill vars
let billItems = [];
let discount = 0;
let tip = 0;

// Split payment type (default to equal)
let currentSplitType = "equal";

async function loadBill(receiptId) {
    const response = await fetch(`/bill/items?receipt_id=${receiptId}`);
    const items = await response.json();

    billItems = items.map(item => ({
        line_id: item[0],   // item_line_id
        id: item[1],        // item_id
        name: item[2],
        qty: item[3],
        price: Number(item[4])
    }));
    

    console.log("Loaded billItems:", billItems);

    renderBill();
}

function updateTotals() {
    let subtotal = 0;
    billItems.forEach(item => subtotal += item.qty * item.price);

    const total = subtotal;
    document.querySelector("#total-container div").innerText =
        `Total: $${total.toFixed(2)}`;
}

function populateItemSelect(items) {
    const select = document.getElementById("item-select");
    select.innerHTML = '<option value="">-- Select an item --</option>';

    items.forEach(item => {
        const option = document.createElement("option");
        option.value = item[0];    // item_id
        option.textContent = `${item[1]} - $${Number(item[3]).toFixed(2)}`;
        select.appendChild(option);
    });
}

async function fetchInventoryItems() {
    const response = await fetch("/inventory/items");
    const items = await response.json();
    console.log("Fetched inventory:", items);  // DEBUG LINE
    window.inventoryItems = items;
    populateItemSelect(items);
}

async function addItem() {
    const itemSelect = document.getElementById("item-select");
    const qty = parseInt(document.getElementById("item-qty").value);
    const receiptId = document.getElementById("receipt-id").value;

    if (!receiptId) return alert("Enter a receipt ID first.");
    if (!itemSelect.value) return alert("Select an item.");
    if (!qty || qty < 1) return alert("Enter a valid quantity.");

    const itemID = parseInt(itemSelect.value);

    // Find inventory row (array)
    const item = window.inventoryItems.find(f => f[0] === itemID);
    if (!item) return alert("Item not found.");

    const price = Number(item[3]);

    // --- SEND TO BACKEND ---
    const res = await fetch("/bill/add-item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            receipt_id: receiptId,
            item_id: itemID,
            qty: qty,
            price: price
        })
    });

    const data = await res.json();

    if (!data.success) {
        alert("Failed to add item to bill.");
        return;
    }

    // --- Reload from backend ---
    loadBill(receiptId);
}

// Tax
const TAX_RATE = 0.02;

function renderBill() {
    const tbody = document.querySelector("#bill-table tbody");
    tbody.innerHTML = "";

    let subtotal = 0;

    billItems.forEach((item, index) => {
        const row = document.createElement("tr");
        const itemTotal = item.qty * item.price;
        subtotal += itemTotal;

        const starRating = [1,2,3,4,5].map(star => `
            <span style="cursor:pointer;" onclick="rateBillItem(${index}, ${star})">⭐</span>
        `).join("");

        row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.qty}</td>
            <td>$${item.price.toFixed(2)}</td>
            <td>$${itemTotal.toFixed(2)}</td>
            <td>${starRating}</td>
            <td><button class="btn btn-danger btn-sm" onclick="removeItem(${index})">Remove</button></td>
        `;
        tbody.appendChild(row);
    });

    

    const tax = subtotal * TAX_RATE;
    const total = subtotal + tax + tip - discount;

    const summaryLines = [
        `<h3>Summary</h3>`,
        `<div>Subtotal: $${subtotal.toFixed(2)}</div>`,
        `<div>Tax (2%): $${tax.toFixed(2)}</div>`
    ];

    if (discount > 0) summaryLines.push(`<div>Discount: $${discount.toFixed(2)}</div>`);

    summaryLines.push(`<div>Tip: $${tip.toFixed(2)}</div>`);
    summaryLines.push(`<div><strong>Total: $${total.toFixed(2)}</strong></div>`);

    document.getElementById("total-container").innerHTML = summaryLines.join("");

    if (document.getElementById("enable-split").checked) generateSplitInputs();
}

function rateBillItem(itemIndex, rating) {
    if (!currentCustomerEmail) {
        alert("Please select a customer first.");
        return;
    }

    const itemName = billItems[itemIndex].name;

    if (!rating) return;

    fetch('/rate-item', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            customer_email: currentCustomerEmail,
            item_name: itemName,
            rating: parseInt(rating)
        })
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            alert(`You rated ${itemName} ${rating} star(s)!`);
        } else {
            alert(`Error: ${data.message}`);
        }
    })
    .catch(err => {
        console.error(err);
        alert("Failed to submit rating.");
    });
}

async function removeItem(index) {
    const receiptId = document.getElementById("receipt-id").value;
    const item = billItems[index];

    const res = await fetch("/bill/remove-item", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            receipt_id: Number(receiptId),
            item_line_id: item.line_id
        })
    });

    const data = await res.json();

    if (!data.success) {
        alert("Failed to remove item from bill.");
        console.error("Remove error:", data);
        return;
    }

    loadBill(receiptId);
}



function processRefund() {
    const receipt_id = document.getElementById("refund-receipt-id").value;
    const admin_email = document.getElementById("refund-admin-email").value;
    const admin_code = document.getElementById("refund-admin-code").value;
    const refund_amount = document.getElementById("refund-amount").value;
    const total_due = document.getElementById("total-container").innerText.match(/Total: \$(\d+\.\d+)/)[1];

    fetch("/bill/refund", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            admin_code,
            admin_email,
            total_due: parseFloat(total_due),
            refund_amount: parseFloat(refund_amount),
            receipt_id
        })
    })
    .then(res => res.json())
    .then(data => {
        if (!data.status || data.status === "fail") {
            alert("Could not process refund");
        } else {
            alert("Refund processed successfully");
        }
    });
}
// Tip & Discount
function updateBill() {
    tip = Number(document.getElementById("tip").value) || 0;
    const coupon = document.getElementById("coupon").value || "";

    discount = coupon === "SAVE10" ? 10 : 0;

    renderBill();
}

// Split payment toggle
function toggleSplit() {
    const enabled = document.getElementById("enable-split").checked;
    document.getElementById("split-container").style.display = enabled ? "block" : "none";
    if (enabled) generateSplitInputs();
}

// Split type buttons
function setSplitType(type) {
    currentSplitType = type;

    // Highlight active button
    const buttons = document.querySelectorAll("#split-buttons button");
    buttons.forEach(btn => btn.style.backgroundColor = "");
    document.querySelector(`#split-buttons button[onclick="setSplitType('${type}')"]`).style.backgroundColor = "#a0d2ff";

    generateSplitInputs();
}

// Generate split inputs
function generateSplitInputs() {
    const numPeople = Number(document.getElementById("num-people").value);

    let subtotal = 0;
    billItems.forEach(item => subtotal += item.qty * item.price);
    const tax = subtotal * TAX_RATE;
    const total = subtotal + tax + tip - discount;

    const splitInputsDiv = document.getElementById("split-inputs");
    splitInputsDiv.innerHTML = "";

    const inputs = [];

    for (let i = 1; i <= numPeople; i++) {
        const input = document.createElement("input");
        input.type = "number";
        input.min = 0;
        input.step = "0.01";
        input.placeholder = `Person ${i}`;
        input.id = `person-${i}`;

        if (currentSplitType === "equal") {
            input.value = (total / numPeople).toFixed(2);
        } else if (currentSplitType === "percent") {
            input.value = (100 / numPeople).toFixed(2);
        } else if (currentSplitType === "amount") {
            input.value = (total / numPeople).toFixed(2);
        }

        // Add event listener for percent type
        input.addEventListener("input", () => {
            if (currentSplitType === "percent") {
                redistributePercent(i - 1); // index starts at 0
            } else if (currentSplitType === "amount") {
                redistributeAmount(i - 1, total);
            }
        });

        splitInputsDiv.appendChild(input);
        splitInputsDiv.appendChild(document.createElement("br"));
        inputs.push(input);
    }
}

// Redistribute percentages
function redistributePercent(changedIndex) {
    const numPeople = Number(document.getElementById("num-people").value);
    const inputs = Array.from({ length: numPeople }, (_, i) => document.getElementById(`person-${i + 1}`));
    let changedValue = Number(inputs[changedIndex].value) || 0;
    changedValue = Math.min(changedValue, 100);
    inputs[changedIndex].value = changedValue;

    const remaining = 100 - changedValue;
    const others = inputs.filter((_, i) => i !== changedIndex);
    const sumOthers = others.reduce((sum, input) => sum + Number(input.value), 0);

    others.forEach(input => {
        input.value = ((Number(input.value) / sumOthers) * remaining || 0).toFixed(2);
    });
}

// Redistribute amounts
function redistributeAmount(changedIndex, total) {
    const numPeople = Number(document.getElementById("num-people").value);
    const inputs = Array.from({ length: numPeople }, (_, i) => document.getElementById(`person-${i + 1}`));
    let changedValue = Number(inputs[changedIndex].value) || 0;
    changedValue = Math.min(changedValue, total);
    inputs[changedIndex].value = changedValue.toFixed(2);

    const remaining = total - changedValue;
    const others = inputs.filter((_, i) => i !== changedIndex);
    const sumOthers = others.reduce((sum, input) => sum + Number(input.value), 0);

    others.forEach(input => {
        input.value = ((Number(input.value) / sumOthers) * remaining || 0).toFixed(2);
    });
}

// Complete payment
async function completePayment() {
    const receiptId = document.getElementById("receipt-id").value;
    const paymentType = document.getElementById("payment-method").value;
    const amount = parseFloat(document.getElementById("payment-amount").value);

    if (!receiptId || isNaN(amount) || amount <= 0) {
        alert("Enter a valid amount and receipt ID.");
        return;
    }

    const response = await fetch("/bill/pay", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            receipt_id: receiptId,
            payment_type: paymentType,
            amount: amount
        })
    });

    const data = await response.json();
    console.log("PAY RESPONSE:", data);

    if (data.success) {
        alert("Payment Successful!");

        // Reload bill totals
        loadBill(receiptId);

        if (data.new_due === 0) {
            // Redirect back to bills page
            window.location.href = "/bills";
        }
    } else {
        alert("Payment failed.");
    }
}

async function voidTransaction() {
    const receiptID = document.getElementById("void-receipt-id").value;
    const adminEmail = document.getElementById("admin-email").value;
    const adminCode = document.getElementById("admin-code").value;

    if (!receiptID || !adminEmail || !adminCode) {
        alert("Please fill out all fields.");
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/voidTransaction", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                receipt_id: receiptID,
                admin_email: adminEmail,
                admin_code: adminCode
            })
        });

        const result = await response.json();

        if (response.ok) {
            alert("Transaction voided successfully.");
        } else {
            alert("Failed to void transaction: " + result.error);
        }

    } catch (error) {
        console.error("Error:", error);
        alert("Server error while voiding transaction.");
    }
}

// Run on page load
window.onload = function () {
    fetchInventoryItems();
};