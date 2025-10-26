import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import json
import re
from tkinter import ttk
adminMail = "admin@gmail.com"
adminPassword = "admin123"
current_governorate = None

with open("users.json", "r") as f:
    users = json.load(f)
def loadUsers():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except Exception:
        return {}

def saveUsers():
    try:
        with open("users.json", "w") as f:
            json.dump(users, f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save users: {e}")
def quicksort(items, key, ascending=True):
    if len(items) <= 1:
        return items
    pivot = items[len(items) // 2]
    left = [x for x in items if x[key] < pivot[key]]
    middle = [x for x in items if x[key] == pivot[key]]
    right = [x for x in items if x[key] > pivot[key]]
    result = quicksort(left, key, ascending) + middle + quicksort(right, key, ascending)
    return result if ascending else result[::-1]


def binary_search(items, key, target):
    left, right = 0, len(items) - 1
    while left <= right:
        mid = (left + right) // 2
        if items[mid][key] == target:
            return items[mid]
        elif items[mid][key] < target:
            left = mid + 1
        else:
            right = mid - 1
    return None

class UserSystem:
    def clearFrame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def __init__(self, root):
        self.root = root
        self.root.title("Online Shopping System")
        self.root.geometry("900x700")
        self.cart = []
        self.showLogin()

    def showLogin(self):
        self.clearFrame()
        tk.Label(self.root, text="Email:", font=("Arial", 12)).pack(pady=5)
        email_entry = tk.Entry(self.root, font=("Arial", 12))
        email_entry.pack(pady=5)
        tk.Label(self.root, text="Password:", font=("Arial", 12)).pack(pady=5)
        password_entry = tk.Entry(self.root, show="*", font=("Arial", 12))
        password_entry.pack(pady=5)

        def login():
            try:
                email = email_entry.get().strip()
                password = password_entry.get().strip()
                if email == adminMail and password == adminPassword:
                    messagebox.showinfo("Admin Login", "Welcome Admin!")
                    self.showAdmin()
                    return
                if email in users and users[email].get("password") == password:
                    messagebox.showinfo("Success", f"Welcome {users[email].get('name', 'User')}!")
                    global current_governorate
                    current_governorate = users[email].get("governorate", "Cairo").lower()
                    email_entry.delete(0, tk.END)
                    password_entry.delete(0, tk.END)
                    show_home(self.root)
                else:
                    messagebox.showerror("Error", "Invalid login!")
            except Exception as e:
                messagebox.showerror("Error", f"Login failed: {e}")

        tk.Button(self.root, text="Login", command=login, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.showRegister, font=("Arial", 12)).pack(pady=5)

    def showRegister(self):
        self.clearFrame()
        labels = ["Name", "Phone", "Email", "Password", "Gender", "Governorate", "Age", "National ID"]
        entries = {}

        for label in labels:
            tk.Label(self.root, text=label, font=("Arial", 12)).pack()
            if label == "Gender":
                entry = ttk.Combobox(self.root, values=["male", "female"], font=("Arial", 12), state="readonly")
                entry.pack(pady=5)
                entries[label.lower()] = entry
            elif label == "Governorate":
                entry = ttk.Combobox(self.root, values=list(delivery_prices.keys()), font=("Arial", 12),
                                     state="readonly")
                entry.pack(pady=5)
                entries[label.lower()] = entry
            else:
                entry = tk.Entry(self.root, font=("Arial", 12))
                entry.pack(pady=5)
                entries[label.lower()] = entry

        def register():
            try:
                email = entries["email"].get().strip()
                phone = entries["phone"].get().strip()
                age = entries["age"].get().strip()
                national_id = entries["national id"].get().strip()

                for key in entries:
                    if not entries[key].get().strip():
                        messagebox.showerror("Error", f"Please fill {key}.")
                        return

                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    messagebox.showerror("Error", "Invalid email format.")
                    return

                if not phone.isdigit() or len(phone) != 11:
                    messagebox.showerror("Error", "Invalid phone number.")
                    return

                if not age.isdigit() or int(age) <= 0:
                    messagebox.showerror("Error", "Age must be a positive number.")
                    return

                if not national_id.isdigit() or len(national_id) != 14:
                    messagebox.showerror("Error", "Invalid National ID.")
                    return

                if email == adminMail:
                    messagebox.showerror("Error", "You can't use this mail")
                    return
                if email in users:
                    messagebox.showerror("Error", "User already exists")
                    return

                users[email] = {
                    "name": entries["name"].get().strip(),
                    "phone": phone,
                    "email": email,
                    "gender": entries["gender"].get().strip(),
                    "governorate": entries["governorate"].get().strip().lower(),
                    "password": entries["password"].get().strip(),
                    "age": int(age),
                    "national_id": national_id
                }
                saveUsers()
                messagebox.showinfo("Success", "Registered successfully!")
                self.showLogin()

            except Exception as e:
                messagebox.showerror("Error", f"Registration failed: {e}")

        tk.Button(self.root, text="Register", command=register, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.showLogin, font=("Arial", 12)).pack(pady=5)

    def addItem(self, cat):
        self.clearFrame()
        tk.Label(self.root, text=f"Add Item to {cat}", font=("Arial", 16, "bold")).pack(pady=10)

        labels = ["Name", "Price", "Brand", "Year"]
        entries = {}

        for label in labels:
            tk.Label(self.root, text=label, font=("Arial", 12)).pack()
            entry = tk.Entry(self.root, font=("Arial", 12))
            entry.pack(pady=5)
            entries[label.lower()] = entry

        def save_item():
            try:
                name = entries["name"].get().strip()
                price = int(entries["price"].get().strip())
                brand = entries["brand"].get().strip()
                year = int(entries["year"].get().strip())

                if not name or not brand:
                    messagebox.showerror("Error", "Name and Brand are required!")
                    return

                categories[cat].append({
                    "name": name,
                    "price": price,
                    "brand": brand,
                    "year": year
                })

                messagebox.showinfo("Success", "Item added successfully!")
                self.manageItems(cat)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add item: {e}")

        tk.Button(self.root, text="Save", command=save_item, font=("Arial", 12)).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.manageItems(cat), font=("Arial", 12)).pack()

    def showAdmin(self):
        self.clearFrame()
        tk.Label(self.root, text="Admin Panel", font=("Arial", 16, "bold")).pack(pady=10)
        tk.Button(self.root, text="Manage Categories / Items", command=self.showAdminCategories,
                  font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="View All Users", command=self.showAllUsers, font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.showLogin, font=("Arial", 12)).pack(pady=10)
    def showAllUsers(self):
        try:
            win = tk.Toplevel(self.root)
            win.title("All Registered Users")
            text = tk.Text(win, width=80, height=20)
            text.pack()
            for email, info in users.items():
                text.insert(tk.END, f"Email: {email}\n")
                for k, v in info.items():
                    text.insert(tk.END, f"  {k}: {v}\n")
                text.insert(tk.END, "\n")
            tk.Button(win, text="Close", command=win.destroy).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to show users: {e}")



    def showAdminCategories(self):
        self.clearFrame()
        tk.Label(self.root, text="Manage Categories", font=("Arial", 16, "bold")).pack(pady=10)
        for cat in categories.keys():
            tk.Button(self.root, text=f"Manage {cat}", command=lambda c=cat: self.manageItems(c),
                      font=("Arial", 12)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.showAdmin, font=("Arial", 12)).pack(pady=10)
    def manageItems(self, cat):
        self.clearFrame()
        tk.Label(self.root, text=f"Manage {cat}", font=("Arial", 16, "bold")).pack(pady=10)
        try:
            for i, item in enumerate(categories[cat]):
                frame = tk.Frame(self.root)
                frame.pack(pady=5, fill="x")
                tk.Label(frame, text=f"{item['name']} | {item['brand']} | {item['year']} | EGP {item['price']}",
                         font=("Arial", 12)).pack(side=tk.LEFT)
                tk.Button(frame, text="Delete", command=lambda idx=i: self.deleteItem(cat, idx),
                          font=("Arial", 10), bg="red", fg="white").pack(side=tk.RIGHT, padx=5)
                tk.Button(frame, text="Discount 10%", command=lambda idx=i: self.applyDiscount(cat, idx, 10),
                          font=("Arial", 10), bg="green", fg="white").pack(side=tk.RIGHT, padx=5)
            tk.Button(self.root, text="Add Item", command=lambda: self.addItem(cat),
                      font=("Arial", 12), bg="blue", fg="white").pack(pady=10)
            tk.Button(self.root, text="Back", command=self.showAdminCategories,
                      font=("Arial", 12)).pack(pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to manage items: {e}")

    def deleteItem(self, cat, idx):
        try:
            del categories[cat][idx]
            messagebox.showinfo("Deleted", "Item deleted successfully!")
            self.manageItems(cat)
        except Exception as e:
            messagebox.showerror("Error", f"Delete failed: {e}")

    def applyDiscount(self, cat, idx, percent):
        try:
            categories[cat][idx]["price"] = int(categories[cat][idx]["price"] * (1 - percent / 100))
            messagebox.showinfo("Discount", f"{percent}% discount applied!")
            self.manageItems(cat)
        except Exception as e:
            messagebox.showerror("Error", f"Discount failed: {e}")



delivery_prices = {
    "cairo": 50,
    "giza": 100,
    "alexandria": 200,
    "aswan": 300
}


categories = {
    "Electronics": [
        {"name": "Laptop", "price": 15000, "brand": "Dell", "year": 2022},
        {"name": "Phone", "price": 10000, "brand": "Samsung", "year": 2023}
    ],
    "Fashion": [
        {"name": "T-Shirt", "price": 300, "brand": "Zara", "year": 2023},
        {"name": "Shoes", "price": 1200, "brand": "Nike", "year": 2022}
    ],
    "Books": [
        {"name": "Python Basics", "price": 250, "brand": "O'Reilly", "year": 2021},
        {"name": "Data Science", "price": 400, "brand": "Packt", "year": 2022}
    ],
    "Sports": [
        {"name": "Football", "price": 600, "brand": "Adidas", "year": 2023},
        {"name": "Basketball", "price": 800, "brand": "Nike", "year": 2022}
    ],
    "Home appliances": [
        {"name": "Refrigerator", "price": 12000, "brand": "LG", "year": 2022},
        {"name": "Microwave", "price": 4000, "brand": "Samsung", "year": 2021}
    ]
}


cart = []

def calculate_total(cart, i=0):
    if i == len(cart):
        return 0
    return cart[i]["price"] + calculate_total(cart, i+1)


def delivery_fee(governorate):
    return delivery_prices.get(governorate, 300)



def clear_frame(root):
    for widget in root.winfo_children():
        widget.destroy()


def show_cart(root, governorate="Cairo"):
    clear_frame(root)
    tk.Label(root, text="Your Cart", font=("Arial", 14)).pack(pady=10)

    if not cart:
        tk.Label(root, text="Cart is empty!").pack()
    else:
        listbox = tk.Listbox(root ,width=50, height=len(cart))
        for idx , item in enumerate(cart):
            listbox.insert(idx , f"{item['name']} {item['price']} EGP - {item['brand']} - {item['year']}")
        listbox.pack(pady=10)

        def remove_item():
            selected_index = listbox.curselection()
            if selected_index:
                removed = cart.pop(selected_index[0])
                messagebox.showinfo("Cart" ,f"Removed {removed['name']} from your cart.")
                show_cart(root)
            else:
                messagebox.showwarning("Cart","Please select an item to remove!.")
        tk.Button(root, text="Remove Item", command=remove_item).pack(pady=5)

        def calc():
            total = calculate_total(cart)
            delivery = delivery_fee(current_governorate or "Cairo")
            final_price = total + delivery
            messagebox.showinfo("Cart Summary",
                                f"Governorate: {current_governorate}\n"
                                f"Total: {total} EGP\n"
                                f"Delivery: {delivery} EGP\n"
                                f"Final Price: {final_price} EGP")
        tk.Button(root, text="Calculate Total", command=calc).pack(pady=10)

        tk.Button(root, text="Back to Home", command=lambda: show_home(root)).pack(pady=10)


def show_category(root, category_name):
    clear_frame(root)
    search_entry = tk.Entry(root, font=("Arial", 12))
    search_entry.pack(pady=5)
    def search_item(categories,search_entry):
        p = search_entry.get().strip().lower()
        found_items = []
        for i in categories:
            for j in range(len(categories[i])):
                if p.lower() in categories[i][j]["name"].lower():
                    found_items.append(f"{categories[i][j]['name']} - {categories[i][j]['price']} EGP")
        if found_items:
            messagebox.showinfo("Search Results", "\n".join(found_items))
        else:
            messagebox.showwarning("Search Results", "Item not found!")
    tk.Button(root, text="Search", command=lambda:search_item(categories,search_entry), font=("Arial", 12)).pack(pady=5)


    tk.Label(root, text=f"{category_name} Items", font=("Arial", 14)).pack(pady=10)
    items = categories[category_name]

    listbox = tk.Listbox(root, width=40, height=len(items))
    for idx, item in enumerate(items):
        listbox.insert(idx, f"{item['name']} - {item['price']} EGP")
    listbox.pack(pady=10)

    def add_selected():
        selected_index = listbox.curselection()
        if selected_index:
            item = items[selected_index[0]]
            cart.append(item)
            messagebox.showinfo("Cart", f"Added {item['name']} to cart!")
        else:
            messagebox.showwarning("Cart", "Please select an item first!")
    def display_items(items):
        listbox.delete(0, tk.END)
        for idx, item in enumerate(items):
            listbox.insert(idx, f"{item['name']} - {item['price']} EGP")
    def sort_by_price():
        sorted_items = sorted(items, key=lambda x: x['price'])  # Ascending
        display_items(sorted_items)
    def sort_by_price_descending():
        sorted_items = sorted(items, key=lambda x: x['price'], reverse=True)  # Descending
        display_items(sorted_items)
    def sort_by_year():
        sorted_items = sorted(items, key=lambda x: x['year'], reverse=True)  # أحدث الأول
        display_items(sorted_items)
    display_items(items)


    tk.Button(root, text="Add to Cart", command=add_selected).pack(pady=5)
    tk.Button(root, text="Go to Cart", command=lambda: show_cart(root)).pack(pady=5)
    tk.Button(root, text="Back to Home", command=lambda: show_home(root)).pack(pady=10)
    tk.Button(root, text="Sort by low to high", command=lambda: sort_by_price()).pack(pady=10)
    tk.Button(root, text="Sort by high to low", command=lambda: sort_by_price_descending()).pack(pady=10)
    tk.Button(root, text="Sort by year(from newer)", command=lambda: sort_by_year()).pack(pady=10)




def show_home(root):
    clear_frame(root)
    tk.Label(root, text="Choose a Category:", font=("Arial", 14, "bold")).pack(pady=10)

    img_folder = "images" 

    frame_all = tk.Frame(root)
    frame_all.pack(pady=20)

    col = 0
    row = 0

    for cat in categories.keys():
        frame = tk.Frame(frame_all, padx=10, pady=10)
        frame.grid(row=row, column=col)


        possible_names = [cat, cat.lower().replace(" ", "_")]

        img_path = None
        for name in possible_names:
            for ext in [".png", ".jpg", ".jpeg"]:
                test_path = os.path.join(img_folder, name + ext)
                if os.path.exists(test_path):
                    img_path = test_path
                    break
            if img_path:
                break

        if img_path:
            try:
                img = Image.open(img_path)
                img = img.resize((100, 100))
                photo = ImageTk.PhotoImage(img)

                btn = tk.Button(frame, image=photo, command=lambda c=cat: show_category(root, c))
                btn.image = photo
                btn.pack()
            except Exception as e:
                tk.Label(frame, text=f"[Image error for {cat}]").pack()

        tk.Label(frame, text=cat, font=("Arial", 12, "bold")).pack()

        col += 1
        if col > 2:
            col = 0
            row += 1

    tk.Button(root, text="Back", command=lambda: app.showLogin(), font=("Arial", 12)).pack(pady=20)


root = tk.Tk()
root.title("Shopping System")
root.geometry("500x400")

app = UserSystem(root)

root.mainloop()
