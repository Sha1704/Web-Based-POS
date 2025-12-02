// Fetch and display all receipts
async function loadReceipts() {
    try {
        const response = await fetch("/bills/all");
        const receipts = await response.json();
        renderReceipts(receipts);
    } catch (err) {
        console.error("Failed to fetch receipts", err);
    }
}

function renderReceipts(receipts) {
    const tbody = document.getElementById("bills-body");
    tbody.innerHTML = "";
    receipts.forEach(receipt => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${receipt.receipt_id}</td>
            <td>${receipt.customer_email}</td>
            <td>$${receipt.total_amount.toFixed(2)}</td>
            <td>$${receipt.amount_due.toFixed(2)}</td>
            <td>${receipt.created_at}</td>
            <td>${receipt.note || ""}</td>
        `;
        tbody.appendChild(tr);
    });
}

window.onload = function () {
    loadReceipts();
};
