//bills.js - FIXED AND IMPROVED
let bills = [
    { id: 1001, total: 23.45, date: "2025-01-16 2:15 PM" },
    { id: 1002, total: 58.90, date: "2025-01-16 2:45 PM" },
    { id: 1003, total: 12.10, date: "2025-01-16 3:10 PM" }
];

// Optional: Load from localStorage 
function loadBillsFromStorage() {
    const saved = localStorage.getItem('pos_bills');
    if (saved) {
        bills = JSON.parse(saved);
    }
}
loadBillsFromStorage();

// Save to localStorage whenever bills change
function saveBills() {
    localStorage.setItem('pos_bills', JSON.stringify(bills));
}

function createNewBill() {
    const newId = bills.length > 0 ? Math.max(...bills.map(b => b.id)) + 1 : 1001;

    const now = new Date();
    const date = now.toLocaleDateString("en-US", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
    }) + " " + now.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
        hour12: true
    });

    const newBill = {
        id: newId,
        total: 0.00,
        date: date  // Now properly shows "1:23 PM"
    };

    bills.push(newBill);
    saveBills();           // ← persist across refresh
    refreshBillList();
    window.location.href = `bill.html?receipt=${newId}`;
}

function refreshBillList() {
    const list = document.getElementById("bill-list");
    if (!list) {
        console.error("bill-list element not found!");
        return;
    }
    list.innerHTML = "";

    // Sort newest first
    [...bills].sort((a, b) => b.id - a.id).forEach(bill => {
        const div = document.createElement("div");
        div.className = "p-4 border rounded-lg hover:bg-gray-50 cursor-pointer transition-shadow hover:shadow-md";
        div.innerHTML = `
            <div class="flex justify-between items-start">
                <div>
                    <strong class="text-lg">Receipt #${bill.id}</strong><br>
                    <span class="text-2xl font-bold text-blue-600">$${bill.total.toFixed(2)}</span>
                </div>
                <div class="text-right text-sm text-gray-600">
                    ${bill.date}
                </div>
            </div>
        `;
        div.onclick = () => window.location.href = `bill.html?receipt=${bill.id}`;
        list.appendChild(div);
    });
}

// Load on page start
window.onload = () => {
    refreshBillList();
};
