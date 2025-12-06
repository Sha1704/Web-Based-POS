// sales.js

// Format ISO datetime to readable string (simple)
function formatDate(iso) {
    try {
        const d = new Date(iso);
        return d.toLocaleString();
    } catch {
        return iso;
    }
}

async function loadSalesReport() {
    try {
        const response = await fetch("/sales/report");
        if (!response.ok) {
            console.error("sales report fetch failed:", response.status);
            return;
        }
        const sales = await response.json();
        renderSalesReport(sales || []);
    } catch (err) {
        console.error("Failed to fetch sales report", err);
    }
}

function renderSalesReport(sales) {
    const tbody = document.getElementById("sales-body");
    if (!tbody) {
        console.error("No #sales-body found in DOM");
        return;
    }
    tbody.innerHTML = "";

    let totalSales = 0;
    let totalOrders = sales.length;

    sales.forEach(sale => {
        totalSales += Number(sale.total_amount) || 0;
        const tr = document.createElement("tr");
        tr.innerHTML = `
            <td>${sale.receipt_id}</td>
            <td>${sale.customer_email || "—"}</td>
            <td>$${(Number(sale.total_amount) || 0).toFixed(2)}</td>
            <td>${formatDate(sale.created_at)}</td>
        `;
        tbody.appendChild(tr);
    });

    // Update summary cards
    const avg = totalOrders > 0 ? (totalSales / totalOrders) : 0;
    const totalEl = document.getElementById("sales-total");
    const ordersEl = document.getElementById("sales-orders");
    const avgEl = document.getElementById("sales-average");

    if (totalEl) totalEl.textContent = `$${totalSales.toFixed(2)}`;
    if (ordersEl) ordersEl.textContent = `${totalOrders}`;
    if (avgEl) avgEl.textContent = `$${avg.toFixed(2)}`;
}

// load on page open
window.addEventListener("DOMContentLoaded", loadSalesReport);
