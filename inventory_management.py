import sqlite3
from tkinter import *
from tkinter import messagebox

# Database Setup
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()

# Drop the products table if it exists (This will remove any existing data in the products table)
cursor.execute('''DROP TABLE IF EXISTS products''')

# Create User and Product tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL, stock INTEGER)''')
conn.commit()

# Check if admin user exists
cursor.execute("SELECT * FROM users WHERE username = ?", ('admin',))
admin_user = cursor.fetchone()

# Insert admin user only if it doesn't already exist
if not admin_user:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'password123'))
    conn.commit()

# GUI Application
root = Tk()
root.title("Inventory Management System")
root.geometry("600x400")

# Login Function
def login():
    username = username_entry.get()
    password = password_entry.get()
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo("Login Success", "Welcome to Inventory Management System!")
        open_inventory_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Inventory Window
def open_inventory_window():
    inventory_window = Toplevel(root)
    inventory_window.title("Inventory Management")
    inventory_window.geometry("600x400")

    def add_product():
        name = name_entry.get()
        price = float(price_entry.get())
        stock = int(stock_entry.get())
        
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        messagebox.showinfo("Success", "Product added successfully!")
        display_inventory()

    def delete_product():
        selected_product = product_listbox.get(ACTIVE)
        if selected_product:
            product_id = selected_product.split()[0]
            cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
            conn.commit()
            messagebox.showinfo("Success", "Product deleted successfully!")
            display_inventory()

    def display_inventory():
        product_listbox.delete(0, END)
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        for product in products:
            product_listbox.insert(END, f"{product[0]} - {product[1]}, Price: {product[2]}, Stock: {product[3]}")

    def generate_report():
        low_stock_products = []
        cursor.execute("SELECT * FROM products WHERE stock < 5")
        low_stock_products = cursor.fetchall()
        
        if low_stock_products:
            messagebox.showwarning("Low Stock", f"Products with low stock: {low_stock_products}")
        else:
            messagebox.showinfo("Report", "All products are sufficiently stocked!")

    # Inventory Management Layout
    Label(inventory_window, text="Product Name:").grid(row=0, column=0)
    Label(inventory_window, text="Price:").grid(row=1, column=0)
    Label(inventory_window, text="Stock:").grid(row=2, column=0)
    
    name_entry = Entry(inventory_window)
    price_entry = Entry(inventory_window)
    stock_entry = Entry(inventory_window)
    
    name_entry.grid(row=0, column=1)
    price_entry.grid(row=1, column=1)
    stock_entry.grid(row=2, column=1)
    
    Button(inventory_window, text="Add Product", command=add_product).grid(row=3, column=0)
    Button(inventory_window, text="Delete Product", command=delete_product).grid(row=3, column=1)
    Button(inventory_window, text="Generate Report", command=generate_report).grid(row=4, column=0, columnspan=2)
    
    product_listbox = Listbox(inventory_window, width=50)
    product_listbox.grid(row=5, column=0, columnspan=2)

    display_inventory()

# Login Layout
Label(root, text="Username:").grid(row=0, column=0)
Label(root, text="Password:").grid(row=1, column=0)

username_entry = Entry(root)
password_entry = Entry(root, show="*")

username_entry.grid(row=0, column=1)
password_entry.grid(row=1, column=1)

Button(root, text="Login", command=login).grid(row=2, column=0, columnspan=2)

root.mainloop()

# Close DB connection when done
conn.close()
