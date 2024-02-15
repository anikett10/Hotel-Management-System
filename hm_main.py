import tkinter as tk
from tkinter import ttk
from datetime import datetime
from hm_functions import *

def main():
    window = tk.Tk()
    window.title("Billing System")
    w, h = window.winfo_screenwidth(), window.winfo_screenheight()
    window.geometry("%dx%d+0+0" % (w, h))

    def reset_values():
        menu_combobox.set("")  
        quantity_entry.delete(0, tk.END)  
        item_b.delete(0, tk.END)  
        item_c.delete(0, tk.END)  
        payment_options.set("")  
        cart_tree.delete(*cart_tree.get_children())  
        total_price.set(0.0)
        update_pie_chart([], pie_chart_frame)  


    title_frame = tk.Frame(window, bg="gray", bd=8)
    title_frame.pack(side=tk.TOP, fill="x")

    title_label = tk.Label(title_frame, text="Hotel Management System",
                           font=("Arial", 24, "bold"), bg="gray", fg="black", pady=10)
    title_label.pack()

    menu_frame = tk.Frame(window, bd=8, bg="lightgray", relief=tk.GROOVE)
    menu_frame.place(x=0, y=80, height=730, width=300)

    menu_label = tk.Label(menu_frame, text="Select Items from here",
                          font=("Arial", 18, "bold"), bg="gray", fg="black", pady=5)
    menu_label.pack(side=tk.TOP, fill="x")

    item_frame = tk.Frame(window, bd=8, bg="white", relief="groove")
    item_frame.place(x=300, y=80, height=730, width=1200)

    item_title_label = tk.Label(item_frame, text="Order Information",
                                font=("Arial", 18, "bold"), bg="gray", fg="black", pady=5)
    item_title_label.pack(side=tk.TOP, fill="x")

    create_database()
    dropdown_label = tk.Label(menu_frame, text="Menu Items", font=("Arial", 12))
    dropdown_label.pack(pady=15)

    menu_combobox = ttk.Combobox(menu_frame, state="readonly", width=40)
    menu_combobox.pack(pady=5)

    quantity_label = tk.Label(menu_frame, text="Quantity:")
    quantity_label.pack(pady=20)

    quantity_entry = ttk.Entry(menu_frame)
    quantity_entry.pack(pady=5)

    selected_items = []

    add_to_cart_button = ttk.Button(menu_frame, text="Add to Cart", command=lambda: add_to_cart(selected_items, menu_combobox, quantity_entry, cart_tree, total_price, pie_chart_frame))
    add_to_cart_button.pack(pady=20)

    item_frame2 = tk.Frame(item_frame, bg="gray",relief="groove")
    item_frame2.pack(fill="x", pady=10)

    item_date = tk.Label(item_frame2, text="Date:",
                         font=("Arial", 12, "bold"), bg="gray", fg="black")
    item_date.grid(row=0, column=0, pady=10, padx=10, sticky="w")

    current_date = datetime.now().strftime("%Y-%m-%d")

    item_a = ttk.Entry(item_frame2, font="Arial 12", width=65, style="TEntry")
    item_a.insert(0, current_date)
    item_a.grid(row=0, column=1, pady=10, padx=10, sticky="w")

    item_ID = tk.Label(item_frame2, text="Customer ID:",
                       font=("Arial", 12, "bold"), bg="gray", fg="black")
    item_ID.grid(row=1, column=0, pady=10, padx=10, sticky="w")

    item_b = ttk.Entry(item_frame2, font="Arial 12", width=65, style="TEntry")
    item_b.grid(row=1, column=1, pady=10, padx=10, sticky="w")

    item_no = tk.Label(item_frame2, text="Table Number:", font=("Arial", 12, "bold"), bg="gray", fg="black")
    item_no.grid(row=2, column=0, pady=10, padx=10, sticky="w")

    item_c = ttk.Entry(item_frame2, font="Arial 12", width=65, style="TEntry")
    item_c.grid(row=2, column=1, pady=10, padx=10, sticky="w")

    item_pay = tk.Label(item_frame2, text="Payment method:", font=("Arial", 12, "bold"), bg="gray", fg="black")
    item_pay.grid(row=3, column=0, pady=10, padx=10, sticky="w")

    payment_options = ttk.Combobox(item_frame2, values=["Cash", "UPI"], state="readonly")
    payment_options.grid(row=3, column=1, pady=10, padx=10, sticky="w")

    cart_tree = ttk.Treeview(item_frame, columns=("Name", "Price", "Quantity"), show="headings", selectmode="browse")
    cart_tree.heading("Name", text="Name")
    cart_tree.heading("Price", text="Price")
    cart_tree.heading("Quantity", text="Quantity")
    cart_tree.column("Name", width=500)
    cart_tree.column("Price", width=200)
    cart_tree.column("Quantity", width=150)

    cart_tree['height'] = 17
    cart_tree.pack()

    total_price_label = tk.Label(item_frame, text="Total Price:")
    total_price_label.pack()

    total_price = tk.DoubleVar(value=0.0)
    total_price_label = tk.Label(item_frame, textvariable=total_price)
    total_price_label.pack()

    pie_chart_frame = tk.Frame(menu_frame, bd=2, bg="white", relief=tk.GROOVE)
    pie_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    populate_menu_combobox(menu_combobox)

    remove_button = ttk.Button(item_frame, text="Update", command=lambda: [remove_from_cart(cart_tree, selected_items, total_price, pie_chart_frame), reset_values()], width=70)
    remove_button.pack()

    window.mainloop()

if __name__ == "__main__":
    main()
