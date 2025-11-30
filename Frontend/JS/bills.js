// Example bill data (replace with SQL)
const bills = [
    { id: 1001, total: 23.45, date: "2025-01-16 2:15 PM" },
    { id: 1002, total: 58.90, date: "2025-01-16 2:45 PM" },
    { id: 1003, total: 12.10, date: "2025-01-16 3:10 PM" }
];

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

window.onload = loadBills;
