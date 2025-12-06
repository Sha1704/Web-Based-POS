// Fetch and display sales report
async function loadSalesReport() {
    try {
        const response = await fetch("/sales/report");
        const sales = await response.json();
        renderSalesReport(sales);
    } catch (err) {
        console.error("Failed to fetch sales report", err);
    }
}

function renderSalesReport(sales) {
    const tbody = document.getElementById("sales-body");
    tbody.innerHTML = "";
    sales.forEach(sale => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${sale.receipt_id}</td>
            <td>${sale.customer_email}</td>
            <td>$${sale.total_amount.toFixed(2)}</td>
            <td>${sale.created_at}</td>
        `;
        tbody.appendChild(tr);
    });
}

window.onload = function () {
    loadSalesReport();
};
