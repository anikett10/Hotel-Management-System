import sqlite3
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from datetime import datetime

def create_database():
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            item_name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM menu")
    count = cursor.fetchone()[0]

    if count == 0:
        default_menu_data = [
            ("VadaPav", 15), ("Maaza", 40), ("Lemonade", 20), ("Noodles", 50),
            ("Cold Coffee", 60), ("Mineral Water", 30),
            ("Ice cream", 60), ("Starbucks", 170),
            ("Samosa", 45), ("Fried Rice", 190), ("Chocolate Milkshake", 150),
        ]

        cursor.executemany("INSERT INTO menu (item_name, price) VALUES (?, ?)", default_menu_data)
        conn.commit()

    conn.close()
def populate_menu_combobox(menu_combobox):
    conn = sqlite3.connect("restaurant.db")
    cursor = conn.cursor()

    cursor.execute("SELECT item_name, price FROM menu")
    menu_data = cursor.fetchall()

    conn.close()

    menu_combobox['values'] = [f"{item[0]} - ${item[1]}" for item in menu_data]

def add_to_cart(selected_items, menu_combobox, quantity_entry, cart_tree, total_price_var, pie_chart_frame):
    selected_item = menu_combobox.get()
    quantity = quantity_entry.get()

    try:
        quantity = int(quantity)
    except ValueError:
        # Handle the case where quantity is not an integer
        return

    if selected_item and quantity > 0:
        item_name, _, price_str = selected_item.rpartition(" - $")
        price = float(price_str)
        total_item_price = price * quantity
        selected_items.append((item_name, price, quantity, total_item_price))

        cart_tree.insert("", tk.END, values=(item_name, price, quantity, total_item_price))
        total_price_var.set(round(sum(item[3] for item in selected_items), 2))
        update_pie_chart(selected_items, pie_chart_frame)


def update_pie_chart(selected_items, pie_chart_frame):
    for widget in pie_chart_frame.winfo_children():
        widget.destroy()

    if selected_items:
        pie_data = [item[2] for item in selected_items]
        colors = ['green', 'blue', 'red', 'purple', 'orange', 'yellow', 'pink', 'cyan', 'gray', 'brown']
        fig, ax = plt.subplots(figsize=(8, 6), dpi=100)

        ax.pie(pie_data, labels=[item[0] for item in selected_items],
               autopct='%1.1f%%', startangle=90, colors=colors)

        canvas = FigureCanvasTkAgg(fig, master=pie_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        canvas = canvas
        plt.close('all')


def remove_from_cart(cart_tree, selected_items, total_price_var, pie_chart_frame):
    selected_item = cart_tree.selection()

    if selected_item:
        item_id = selected_item[0]
        index_to_remove = cart_tree.index(item_id)

        removed_item = selected_items.pop(index_to_remove)
        cart_tree.delete(item_id)

        total_price_var.set(round(sum(item[3] for item in selected_items), 2))

        update_pie_chart(selected_items, pie_chart_frame)
