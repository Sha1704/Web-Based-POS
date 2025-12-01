// Placeholder sales data — replace later with backend fetch
const salesData = [
    { id: 101, date: "2025-11-01", total: 22.50, items: 3 },
    { id: 102, date: "2025-11-01", total: 12.99, items: 1 },
    { id: 103, date: "2025-11-02", total: 45.20, items: 5 },
    { id: 104, date: "2025-11-03", total: 18.75, items: 2 }
];

function loadSalesOverview() {
    const tbody = document.querySelector("#sales-table tbody");
    tbody.innerHTML = "";

    let totalSales = 0;

    salesData.forEach(order => {
        totalSales += order.total;

        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${order.id}</td>
            <td>${order.date}</td>
            <td>$${order.total.toFixed(2)}</td>
            <td>${order.items}</td>
        `;
        tbody.appendChild(row);
    });

    const numOrders = salesData.length;
    const avgOrderValue = numOrders > 0 ? totalSales / numOrders : 0;

    // Update summary cards
    document.getElementById("sales-total").textContent = `$${totalSales.toFixed(2)}`;
    document.getElementById("sales-orders").textContent = numOrders;
    document.getElementById("sales-average").textContent = `$${avgOrderValue.toFixed(2)}`;
}

// Initialize page
loadSalesOverview();
