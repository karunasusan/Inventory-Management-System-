let selectedItems = [];

function filterItems() {
    const search = document.getElementById('search-bar').value.toLowerCase();
    const items = document.getElementById('item-list').getElementsByTagName('li');
    Array.from(items).forEach(item => {
        const text = item.textContent.toLowerCase();
        item.style.display = text.includes(search) ? 'block' : 'none';
    });
    document.getElementById('item-list').classList.toggle('hidden', search === '');
}

function addItem(id, name, category, price) {
    if (selectedItems.some(item => item.id === id)) return;

    const item = { id, name, category, quantity: 1, price: parseFloat(price) };
    selectedItems.push(item);
    updateItemList();
    document.getElementById('search-bar').value = '';
    document.getElementById('item-list').classList.add('hidden');
}

function updateItemList() {
    const container = document.getElementById('selected-items');
    container.innerHTML = '';
    selectedItems.forEach(item => {
        const itemCard = document.createElement('div');
        itemCard.className = 'item-card';
        itemCard.innerHTML = `
            <div class="item-info">
                <h3>${item.name}</h3>
                <p>${item.category}</p>
            </div>
            <input type="number" value="${item.quantity}" min="1" class="quantity" onchange="updateQuantity('${item.id}', this.value)">
            <p class="price">₹${(item.quantity * item.price).toFixed(2)}</p>
            <button onclick="removeItem('${item.id}')" class="close-btn">&times;</button>
        `;
        container.appendChild(itemCard);
    });
    updateTotalPrice();
}

function updateQuantity(id, quantity) {
    const item = selectedItems.find(item => item.id === id);
    if (item) {
        item.quantity = parseInt(quantity);
        updateItemList();
    }
}

function removeItem(id) {
    selectedItems = selectedItems.filter(item => item.id !== id);
    updateItemList();
}

function updateTotalPrice() {
    const total = selectedItems.reduce((sum, item) => sum + item.quantity * item.price, 0);
    document.getElementById('total-price').textContent = `₹${total.toFixed(2)}`;
}

async function checkout() {
    const response = await fetch('/checkout', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(selectedItems)
    });

    if (response.ok) {
        alert('Checkout successful!');
        selectedItems = [];
        updateItemList();
    } else {
        alert('Checkout failed!');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
});
