// Example bill data (replace with SQL)
const bills = [
    { id: 1001, total: 23.45, date: "2025-01-16 2:15 PM" },
    { id: 1002, total: 58.90, date: "2025-01-16 2:45 PM" },
    { id: 1003, total: 12.10, date: "2025-01-16 3:10 PM" }
];

// CREATE A NEW BILL
function createNewBill() {
    // Generate a new ID (temporary logic)
    const newId = bills.length > 0 ? bills[bills.length - 1].id + 1 : 1001;

    // Mock new bill data
    const newBill = {
        id: newId,
        total: 0.00,
        date: new Date().toLocaleString("en-US", {
            year: "numeric",
            month: "2-digit",
            day: "2-digit",
            hour: "numeric",
            minute: "2-digit"
        })
    };

    // Add to list
    bills.push(newBill);

    // Refresh UI
    refreshBillList();

    // OPTIONAL: Open the bill immediately
    window.location.href = `bill.html?receipt=${newId}`;
}

// RELOADS UI WITHOUT REFRESHING PAGE
function refreshBillList() {
    const list = document.getElementById("bill-list");
    list.innerHTML = ""; // Clear existing items

    bills.forEach(bill => {
        const div = document.createElement("div");
        div.className = "p-3 border rounded hover:bg-gray-100 cursor-pointer";
        div.innerHTML = `
            <strong>Receipt #${bill.id}</strong>
            <br>
            Total: $${bill.total.toFixed(2)}
            <br>
            <span class="text-gray-600">${bill.date}</span>
        `;

        // CLICK → OPEN BILL PAGE
        div.addEventListener("click", () => {
            window.location.href = `bill.html?receipt=${bill.id}`;
        });

        list.appendChild(div);
    });
}

function loadBills() {
    const list = document.getElementById("bill-list");

    bills.forEach(bill => {
        const div = document.createElement("div");
        div.className = "p-3 border rounded hover:bg-gray-100 cursor-pointer";
        div.innerHTML = `
            <strong>Receipt #${bill.id}</strong>
            <br>
            Total: $${bill.total.toFixed(2)}
            <br>
            <span class="text-gray-600">${bill.date}</span>
        `;

        // CLICK BILL → OPEN bill.html WITH ID
        div.addEventListener("click", () => {
            window.location.href = `bill.html?receipt=${bill.id}`;
        });

        list.appendChild(div);
    });
}

function loadBills() {
    refreshBillList();
}
window.onload = loadBills;
