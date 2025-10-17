async function fetchData(endpoint) {
    const response = await fetch(endpoint);
    const data = await response.json();
    return data;
}

async function showAllItems() {
    const allItems = await fetchData('/api/all-items');
    populateTable(allItems);
}

async function showLowStock() {
    const lowStock = await fetchData('/api/low-stock');
    populateTable(lowStock);
}

async function toggleCategory(category) {
    const categoryItems = await fetchData(`/api/category/${category}`);
    populateTable(categoryItems);
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
            <td>
                <button class="delete-btn" onclick="window.location.href='/edit_product/${item.id}'">
                    <i data-lucide="edit"></i>Edit
                </button>
                <button class="delete-btn" onclick="deleteItem('${item.id}')">
                    <i data-lucide="trash-2"></i>Delete
                </button>
            </td>
        </tr>`;
        tbody.innerHTML += row;
    });
    table.classList.remove('hidden');
}

function editItem(itemId) {
    console.log('Edit item with ID:', itemId);
}

function deleteItem(itemId) {
    if (confirm('Are you sure you want to delete this item?')) {
        fetch(`/delete_product/${itemId}`, { method: 'POST' })
            .then(() => showAllItems())
            .catch(err => console.error('Failed to delete item:', err));
    }
}

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    showAllItems();
});