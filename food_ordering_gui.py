import tkinter as tk
from tkinter import messagebox, simpledialog

# Project Name: FruitShopManagementSystem
# GUI Library: Tkinter

FRUITS = {
    "Apple": 120,
    "Banana": 60,
    "Mango": 150,
    "Orange": 80,
    "Grapes": 90,
    "Watermelon": 50,
    "Pineapple": 70,
    "Papaya": 60,
    "Strawberry": 200
}

GST_RATE = 0.05
cart = {}

BUTTON_COLORS = {
    "Apple": "#ffb0b0",
    "Banana": "#ffff00",
    "Mango": "#ffc000",
    "Orange": "#00e5e5",
    "Grapes": "#ff00e8",
    "Watermelon": "#00ee00",
    "Pineapple": "#c0c0c0",
    "Papaya": "#ffff00",
    "Strawberry": "#ff0000"
}


def add_fruit(fruit_name):
    """Ask the customer for the quantity and add it to the cart."""
    quantity = simpledialog.askinteger(
        "Select Quantity",
        f"{fruit_name} costs Rs.{FRUITS[fruit_name]} per kg/item.\n"
        "Enter quantity (whole number):",
        parent=root,
        minvalue=1
    )

    if quantity is None:
        return

    if fruit_name in cart:
        cart[fruit_name] += quantity
    else:
        cart[fruit_name] = quantity

    messagebox.showinfo(
        "Fruit Added",
        f"{fruit_name} x {quantity} added to the bill."
    )


def generate_bill():
    """Generate the bill and show total, GST and final amount."""
    customer_name = name_entry.get().strip()
    mobile_number = mobile_entry.get().strip()

    if not customer_name:
        messagebox.showwarning("Missing Details", "Please enter customer name.")
        name_entry.focus_set()
        return

    if not mobile_number:
        messagebox.showwarning("Missing Details", "Please enter mobile number.")
        mobile_entry.focus_set()
        return

    if not mobile_number.isdigit() or len(mobile_number) != 10:
        messagebox.showwarning(
            "Invalid Mobile Number",
            "Please enter a valid 10-digit mobile number."
        )
        mobile_entry.focus_set()
        return

    if not cart:
        messagebox.showwarning(
            "No Fruits Selected",
            "Please select at least one fruit before generating the bill."
        )
        return

    total_amount = sum(FRUITS[fruit] * quantity for fruit, quantity in cart.items())
    gst_amount = total_amount * GST_RATE
    final_amount = total_amount + gst_amount

    bill_text = []
    bill_text.append("          FRUIT SHOP MANAGEMENT SYSTEM")
    bill_text.append("=" * 48)
    bill_text.append(f"Customer Name : {customer_name}")
    bill_text.append(f"Mobile Number : {mobile_number}")
    bill_text.append("")
    bill_text.append("============== PURCHASED ITEMS ==============")
    bill_text.append("Fruit              Quantity       Amount")
    bill_text.append("-" * 48)

    for fruit, quantity in cart.items():
        unit = "kg" if fruit != "Banana" else "dozen"
        amount = FRUITS[fruit] * quantity
        bill_text.append(
            f"{fruit:<18} {quantity:>4} {unit:<8} Rs. {amount:.2f}"
        )

    bill_text.append("-" * 48)
    bill_text.append(f"Total Amount : Rs. {total_amount:.2f}")
    bill_text.append(f"GST (5%)     : Rs. {gst_amount:.2f}")
    bill_text.append(f"Final Amount : Rs. {final_amount:.2f}")
    bill_text.append("")
    bill_text.append("Thank You For Visiting Fruit Shop!")

    bill_output.config(state="normal")
    bill_output.delete("1.0", tk.END)
    bill_output.insert(tk.END, "\n".join(bill_text))
    bill_output.config(state="disabled")


def clear_bill():
    """Clear selected fruits and the displayed bill."""
    if not cart and not bill_output.get("1.0", tk.END).strip():
        messagebox.showinfo("Clear Bill", "There is nothing to clear.")
        return

    if messagebox.askyesno("Clear Bill", "Clear the current order and bill?"):
        cart.clear()
        bill_output.config(state="normal")
        bill_output.delete("1.0", tk.END)
        bill_output.config(state="disabled")


# ---------------- Main Window ----------------
root = tk.Tk()
root.title("Fruit Shop Management System")
root.geometry("1200x760")
root.minsize(900, 650)
root.configure(bg="#f5deb3")

# Main heading
heading = tk.Label(
    root,
    text="FRUIT SHOP MANAGEMENT SYSTEM",
    font=("Arial", 26, "bold"),
    fg="red",
    bg="#f5deb3"
)
heading.pack(pady=(18, 28))

# Customer information section
customer_frame = tk.Frame(root, bg="#f5deb3")
customer_frame.pack(fill="x", padx=35, pady=8)

tk.Label(
    customer_frame, text="Customer Name:",
    font=("Arial", 12, "bold"), bg="#f5deb3"
).grid(row=0, column=0, padx=(5, 12), pady=5, sticky="w")

name_entry = tk.Entry(customer_frame, font=("Arial", 12), width=25)
name_entry.grid(row=0, column=1, padx=(0, 35), pady=5, ipady=5)
name_entry.insert(0, "")

tk.Label(
    customer_frame, text="Mobile Number:",
    font=("Arial", 12, "bold"), bg="#f5deb3"
).grid(row=0, column=2, padx=(5, 12), pady=5, sticky="w")

mobile_entry = tk.Entry(customer_frame, font=("Arial", 12), width=25)
mobile_entry.grid(row=0, column=3, padx=(0, 5), pady=5, ipady=5)

# Fruit buttons section
fruit_frame = tk.Frame(root, bg="#f5deb3")
fruit_frame.pack(fill="x", padx=25, pady=(32, 10))

for index, (fruit, price) in enumerate(FRUITS.items()):
    button = tk.Button(
        fruit_frame,
        text=f"{fruit} Rs.{price}",
        font=("Arial", 12, "bold"),
        bg=BUTTON_COLORS[fruit],
        fg="white" if fruit == "Strawberry" else "black",
        activebackground=BUTTON_COLORS[fruit],
        width=17,
        height=2,
        relief="raised",
        bd=1,
        command=lambda item=fruit: add_fruit(item)
    )

    # Four buttons per row; last row is centered.
    row = index // 4
    col = index % 4
    button.grid(row=row, column=col, padx=15, pady=12, ipadx=4, sticky="nsew")

for col in range(4):
    fruit_frame.grid_columnconfigure(col, weight=1)

# Action buttons
action_frame = tk.Frame(root, bg="#f5deb3")
action_frame.pack(pady=(8, 15))

tk.Button(
    action_frame,
    text="Generate Final Bill",
    font=("Arial", 16, "bold"),
    bg="black",
    fg="white",
    activebackground="#333333",
    activeforeground="white",
    width=22,
    height=2,
    command=generate_bill
).grid(row=0, column=0, padx=12)

tk.Button(
    action_frame,
    text="Clear Bill",
    font=("Arial", 12, "bold"),
    bg="#e0e0e0",
    width=12,
    height=2,
    command=clear_bill
).grid(row=0, column=1, padx=12)

# Bill display area with scrollbar
bill_frame = tk.Frame(root, bg="#f5deb3")
bill_frame.pack(fill="both", expand=True, padx=35, pady=(0, 20))

scrollbar = tk.Scrollbar(bill_frame)
scrollbar.pack(side="right", fill="y")

bill_output = tk.Text(
    bill_frame,
    font=("Courier New", 11),
    height=11,
    wrap="none",
    yscrollcommand=scrollbar.set,
    bg="white",
    fg="black",
    relief="sunken",
    bd=1
)
bill_output.pack(side="left", fill="both", expand=True)
scrollbar.config(command=bill_output.yview)
bill_output.config(state="disabled")

root.mainloop()
