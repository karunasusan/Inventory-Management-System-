# 🧾 Inventory Management System

This is a simple, **web-based Inventory Management System** built with **Flask** and **SQLite**.  
It allows users to manage products, track inventory, handle sales through a billing interface, and generate detailed sales reports.

---

### 📊 Dashboard
At-a-glance view of key metrics, including total **Quantity in Hand** and **Low Stock** item count.

### 📦 Product Management (CRUD)
**Create:** Add new products to the inventory.  
**Read:** View all products, filter by category, and see low-stock items.  
**Update:** Edit existing product details (name, category, quantity, price).  
**Delete:** Remove products from the inventory.

### 💳 Billing / Point-of-Sale (POS)
Simple interface to search for products and add them to a bill.

### ⚙️ Automatic Stock Control
When a sale is completed via checkout, the system automatically deducts the sold quantity from the products table.

### 📈 Sales Tracking
All completed transactions are recorded in a separate sales table.

### 🧾 Reporting
View comprehensive sales reports directly in the app.  
Filter reports by product category.  
Download complete sales reports as a **PDF**.

---

## 🧰 Technologies Used
**Backend:** Python (Flask)  
**Database:** SQLite 3  
**Frontend:** HTML, CSS, Vanilla JavaScript  
**PDF Generation:** ReportLab  
**Icons:** Lucide Icons  

---

## ⚙️ Setup and Installation

### 1️⃣ Clone the repository
bash
git clone <your-repository-url>
cd <repository-folder>
### 2️⃣ Create and activate a virtual environment

#### Windows
python -m venv venv
venv\Scripts\activate
#### macOS / Linux
python3 -m venv venv
source venv/bin/activate
###  3️⃣ Install dependencies
bash
Copy code
pip install -r requirements.txt
### 4️⃣ Run the application
python app.py
The app will automatically create the inventory.db file and the necessary products and sales tables if they don't exist.

### 5️⃣ Access the application
Open your browser and go to:
👉
http://127.0.0.1:5000