#  ShopEasy – Full Stack E-Commerce Web App (Django + Tailwind)

ShopEasy is a modern mini E-commerce application built using **Django**, **Tailwind CSS**, and **SQLite/MySQL**.  
It allows users to browse products, add them to a cart, and place orders securely.  
Admins can manage products, view orders, and track revenue via a powerful admin dashboard.

---

# Features

# User Side
- User authentication (Register, Login, Logout)
- Browse products by category (Electronics, Fashion, Beauty)
- Add to Cart, View Cart, Remove Items
- Checkout with two payment methods:
  - 💵 Cash on Delivery (COD)
  - 💳 Fake Card Payment (for demo)
- Order success page with summary
- Cart and checkout protected behind login

# Admin Side
- Manage Products (Add / Edit / Delete)
- Admin Dashboard with total revenue, pending orders & product stats
- Export orders to CSV
- Manage order status and admin notes

---

# Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | Django 4.2 |
| Frontend | Tailwind CSS |
| Database | SQLite / MySQL |
| Auth | Django Auth System |
| Deployment Ready | Whitenoise, dotenv support |
| Version Control | Git & GitHub |

---

# Setup Instructions

# Clone the Repository
```bash
git clone https://github.com/Mprem028/ShopEasy.git
cd ShopEasy
