async function fetchData(endpoint) {
    const response = await fetch(endpoint);
    const data = await response.json();
    return data;
}

async function showRecentProducts() {
    const recentProducts = await fetchData('/api/recent-products');
    populateTable(recentProducts);
}

async function showLowStock() {
    const lowStock = await fetchData('/api/low-stock');
    populateTable(lowStock);
}

function populateTable(data) {
    const table = document.getElementById('info-table');
    const tbody = table.querySelector('tbody');
    tbody.innerHTML = '';
    data.forEach(item => {
        const row = `<tr>
            <td>${item.id}</td>
            <td>${item.name}</td>
            <td>${item.category}</td>
            <td>${item.quantity}</td>
            <td>${item.price}</td>
            <td>${item.date}</td>
        </tr>`;
        tbody.innerHTML += row;
    });
    table.classList.remove('hidden');
}

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
});
