# 🧾 Modern Inventory Management System

A lightweight, full-stack **inventory and sales management system** built with **Flask** and **SQLite**.  
This project provides a complete solution for tracking products, managing stock, processing sales, and generating reports — all wrapped in a **clean and responsive frontend** inspired by **Google's Material 3 Expressive Design**.

---

<!--
TODO: Replace this placeholder with a screenshot of your beautiful new UI!
I've used your new color palette for the placeholder.
-->

---

## 🚀 Core Features

### 📊 Dashboard

A sleek homepage showing key metrics like:

- Total items in stock
- Count of low-stock products

---

### 📦 Full Product Management (CRUD)

**Create:** Add new products with details like name, category, quantity, and price.  
**Read:** View the entire inventory, with filters for _Low Stock_ and dynamic category buttons.  
**Update:** Edit any existing product’s details.  
**Delete:** Remove products from the inventory easily.

---

### 💵 Billing / Point-of-Sale (POS)

- A fast, minimal billing interface with live search.
- Add products to the cart dynamically.
- Automatically deducts sold quantities from the products table when a sale is completed.

---

### 📈 Sales Tracking

- Every completed transaction is logged in a dedicated **sales table**.
- Perfect for auditing and performance tracking.

---

### 📊 Dynamic Reporting

- View a complete, filterable history of all sales.
- Filter reports by **product category**.
- **Export to PDF**: Generate print-ready reports on demand using ReportLab.

---

## 🛠️ Tech Stack

### Backend

- **Python 3**
- **Flask** – Lightweight web framework for server-side logic & APIs
- **SQLite 3** – File-based database for products and sales

### Frontend

- **HTML5** (with **Jinja2** templating)
- **CSS3** – Modern, unified stylesheet inspired by **Material 3 Design**
- **Vanilla JavaScript (ES6+)** – Powers dynamic UI interactions
- **Lucide Icons** – Open-source, clean, and minimal icon set

### PDF Generation

- **ReportLab** – Python library for creating high-quality PDF reports

---

## ⚙️ Setup and Installation

Follow these steps to get the app running locally 👇

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

## 2️⃣ Create and Activate a Virtual Environment

### 🖥️ macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 💻 Windows

```bash
python -m venv venv
.\venv\Scripts\activate
```

## 3️⃣ Install Dependencies

Install all required packages from `requirement.txt`:

```bash
pip install -r requirement.txt
```

## 4️⃣ Run the Application

The app will automatically create the `inventory.db` database and its tables (`products`, `sales`) on first launch.

```bash
python app.py
```

## 5️⃣ Access the App

Open your browser and navigate to:

[http://127.0.0.1:5000](http://127.0.0.1:5000)
