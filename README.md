# 🛍️ Online Shopping System (Python + Tkinter)

## 🗓️ Project Info

**This is the third project submitted on 20/9/2025**
Part of the **Samsung Innovation Campus – Chapter 6**.

---

## 📘 Project Overview

This project is a **Graphical User Interface (GUI)**-based **Online Shopping System** built using **Python and Tkinter**.
It allows users to register, log in, browse product categories, add items to their cart, and calculate totals with delivery fees.
Administrators have special access to manage categories, add or delete items, and apply discounts.

---

## ⚙️ Features

### 👤 User

* **Login / Register** with validation (email, phone, age, and national ID).
* View product **categories** (Electronics, Fashion, Books, Sports, Home Appliances).
* **Search** for products by name.
* **Sort** products by price (ascending/descending) or by year.
* Add products to a **cart** and remove items if needed.
* **Calculate total** (including delivery fees based on governorate).

### 🛠️ Admin

* Login using fixed credentials:

  * Email: `admin@gmail.com`
  * Password: `admin123`
* Manage categories (add, delete, apply discounts).
* View all registered users.

---

## 📂 Project Structure

```
Online-Shopping-System/
│
├── main.py                # Main application file
├── users.json             # Stores registered user data
├── images/                # Folder containing category images
│   ├── electronics.png
│   ├── fashion.png
│   ├── books.png
│   ├── sports.png
│   └── home_appliances.png
└── README.md              # Project documentation
```

---

## 🧠 Algorithms Used

* **Quicksort** → Used for sorting items by price or year.
* **Binary Search** → Used for searching items by name (O(log n) complexity).
* **Recursive Total Calculation** → Calculates total cart price without using loops.

---

## 🗺️ Delivery Fee

| Governorate | Fee (EGP) |
| ----------- | --------- |
| Cairo       | 50        |
| Giza        | 100       |
| Alexandria  | 200       |
| Aswan       | 300       |

---

## 🧾 Requirements

Install the following package before running:

```bash
pip install pillow
```

Python version: **3.8+**

---

## 🖼️ UI Overview

* **Login Page** → First screen with Login & Register options.
* **Register Page** → Collects user info (name, phone, gender, governorate, etc.).
* **Home Page** → Displays product categories with images.
* **Category Page** → Lists items, allows sorting, searching, and adding to cart.
* **Cart Page** → Displays all selected items and calculates total price + delivery.

---

## 👩‍💻 Team & Collaboration

This project was proudly developed by:

* **Maria Akmal**
* **Ahmed Wael**
* **Youssef Kamel**

As a team, we worked with strong communication, mutual respect, and shared goals.
We divided responsibilities effectively, helped one another through technical challenges,
and ensured that every part of the project reflected teamwork and dedication.

It was a valuable learning experience that taught us the power of collaboration
and how teamwork transforms ideas into real success. 💫
