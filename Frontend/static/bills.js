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

    receipts.forEach(r => {
        const tr = document.createElement("tr");

        tr.innerHTML = `
            <td>${r[0]}</td>
            <td>${r[1] || ""}</td>
            <td>$${Number(r[2]).toFixed(2)}</td>
            <td>$${Number(r[3]).toFixed(2)}</td>
            <td>${r[4]}</td>
            <td>${r[5] || ""}</td>
        `;

        // Click row to open bill
        tr.style.cursor = "pointer";
        tr.onclick = () => window.location.href = `/bill?receipt_id=${r[0]}`;

        tbody.appendChild(tr);
    });
}


async function createNewBill() {
    const response = await fetch("/bill/create", { method: "POST" });
    const data = await response.json();
    window.location.href = `/bill?receipt_id=${data.receipt_id}`;
}

window.onload = function () {
    loadReceipts();
};
