async function fetchData(endpoint) {
    const response = await fetch(endpoint);
    const data = await response.json();
    return data;
}

async function loadSalesReport() {
    const salesData = await fetchData('/api/sales-report');
    populateTable(salesData);
}

async function loadCategories() {
    const categories = await fetchData('/api/sales-categories');
    const categoryContainer = document.getElementById('categoryCarousel');
    categoryContainer.innerHTML = '';
    categories.forEach(category => {
        const button = document.createElement('button');
        button.className = 'category-btn';
        button.textContent = category;
        button.onclick = () => filterByCategory(category);
        categoryContainer.appendChild(button);
    });
}

async function filterByCategory(category) {
    const filteredSales = await fetchData(`/api/sales-report/${category}`);
    populateTable(filteredSales);
}

function populateTable(data) {
    const table = document.getElementById('sales-report');
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    data.forEach(sale => {
        const row = `<tr>
            <td>${sale.id}</td>
            <td>${sale.name}</td>
            <td>${sale.category}</td>
            <td>${sale.quantity_sold}</td>
            <td>₹${sale.total_price}</td>
            <td>${sale.date}</td>
        </tr>`;
        tbody.innerHTML += row;
    });
}

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    loadSalesReport();
    loadCategories();
});