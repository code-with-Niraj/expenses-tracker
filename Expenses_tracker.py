import json
import os
import tkinter as tk
from tkinter import messagebox

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "expenses.json")
BUDGET_FILE = os.path.join(BASE_DIR, "budget.txt")

expenses = []
budget = 0

# ---------------------------------------------------------
# DATA FUNCTIONS (same logic as your CLI version)
# ---------------------------------------------------------

def load_expenses():
    global expenses
    try:
        with open(DATA_FILE, "r") as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        expenses = []


def save_expenses():
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file)


def load_budget():
    global budget
    try:
        with open(BUDGET_FILE, "r") as file:
            budget = float(file.read())
    except (FileNotFoundError, ValueError):
        budget = 0


def save_budget():
    with open(BUDGET_FILE, "w") as file:
        file.write(str(budget))


def total_expenses():
    return sum(e["amount"] for e in expenses)


def category_summary():
    summary = {}
    for e in expenses:
        category = e["category"]
        summary[category] = summary.get(category, 0) + e["amount"]
    return summary


# ---------------------------------------------------------
# GUI ACTIONS (these connect buttons to the data functions)
# ---------------------------------------------------------

def refresh_list():
    listbox.delete(0, tk.END)
    for i, e in enumerate(expenses, 1):
        listbox.insert(tk.END, f"{i}. {e['category']} - Rs. {e['amount']} - {e['note']}")


def add_expense_gui():
    try:
        amount = float(entry_amount.get())
        category = entry_category.get().strip()
        note = entry_note.get().strip()

        if not category:
            messagebox.showerror("Error", "Category khaali nahi ho sakti")
            return

        expenses.append({"amount": amount, "category": category, "note": note})
        save_expenses()
        refresh_list()

        entry_amount.delete(0, tk.END)
        entry_category.delete(0, tk.END)
        entry_note.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Error", "Amount sirf number hona chahiye")


def delete_expense_gui():
    selection = listbox.curselection()
    if not selection:
        messagebox.showwarning("Warning", "Pehle ek expense select karo list me se")
        return

    index = selection[0]
    removed = expenses.pop(index)
    save_expenses()
    refresh_list()
    messagebox.showinfo("Removed", f"Removed: {removed['category']} - Rs. {removed['amount']}")


def show_summary_gui():
    total = total_expenses()
    summary = category_summary()

    lines = [f"Total Expense: Rs. {total}"]
    for cat, amt in summary.items():
        lines.append(f"{cat}: Rs. {amt}")

    if budget > 0:
        lines.append(f"\nBudget Set: Rs. {budget}")
        if total > budget:
            lines.append(f"Budget exceeded by Rs. {total - budget}!")
        else:
            lines.append(f"Remaining budget: Rs. {budget - total}")
    else:
        lines.append("\nNo budget set yet.")

    messagebox.showinfo("Summary", "\n".join(lines))


def set_budget_gui():
    global budget
    try:
        budget = float(entry_budget.get())
        save_budget()
        messagebox.showinfo("Budget Set", f"Budget set to Rs. {budget}")
        entry_budget.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Budget sirf number hona chahiye")


# ---------------------------------------------------------
# LOAD SAVED DATA BEFORE BUILDING THE WINDOW
# ---------------------------------------------------------

load_expenses()
load_budget()

# ---------------------------------------------------------
# BUILD THE WINDOW
# ---------------------------------------------------------

root = tk.Tk()
root.title("Expense Tracker")
root.geometry("450x520")
root.resizable(False, False)

# --- Add Expense Section ---
frame_add = tk.Frame(root, pady=10)
frame_add.pack(fill="x", padx=10)

tk.Label(frame_add, text="Amount:").grid(row=0, column=0, sticky="w", pady=2)
entry_amount = tk.Entry(frame_add, width=25)
entry_amount.grid(row=0, column=1, padx=5, pady=2)

tk.Label(frame_add, text="Category:").grid(row=1, column=0, sticky="w", pady=2)
entry_category = tk.Entry(frame_add, width=25)
entry_category.grid(row=1, column=1, padx=5, pady=2)

tk.Label(frame_add, text="Note:").grid(row=2, column=0, sticky="w", pady=2)
entry_note = tk.Entry(frame_add, width=25)
entry_note.grid(row=2, column=1, padx=5, pady=2)

tk.Button(frame_add, text="Add Expense", command=add_expense_gui).grid(
    row=3, column=0, columnspan=2, pady=8
)

# --- Expense List Section ---
frame_list = tk.Frame(root)
frame_list.pack(fill="both", expand=True, padx=10, pady=5)

scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side="right", fill="y")

listbox = tk.Listbox(frame_list, yscrollcommand=scrollbar.set)
listbox.pack(fill="both", expand=True)
scrollbar.config(command=listbox.yview)

tk.Button(root, text="Delete Selected", command=delete_expense_gui).pack(pady=5)

# --- Budget Section ---
frame_budget = tk.Frame(root, pady=10)
frame_budget.pack(fill="x", padx=10)

tk.Label(frame_budget, text="Set Budget:").grid(row=0, column=0, sticky="w")
entry_budget = tk.Entry(frame_budget, width=15)
entry_budget.grid(row=0, column=1, padx=5)
tk.Button(frame_budget, text="Set", command=set_budget_gui).grid(row=0, column=2, padx=5)

tk.Button(root, text="Show Summary", command=show_summary_gui).pack(pady=10)

refresh_list()

root.mainloop()