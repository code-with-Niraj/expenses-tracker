import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "expenses.json")
BUDGET_FILE = os.path.join(BASE_DIR, "budget.txt")

expenses = []
budget = 0

# Add Expenses
def add_expenses():
    try:
        amount = float(input("Amount : "))
        category = input("Category : ")
        note = input("Note: ")
        expenses.append({"amount": amount, "category": category, "note": note})
        print("Added successfully")
        save_expenses()
        
    except ValueError:
        print("Enter only numbers")

# View Expenses
def view_expenses():
    if not expenses:
        print("No expenses added yet")
        
    else:
        for i, e in enumerate(expenses, 1):
            print(f"{i}. {e['category']} - Rs. {e['amount']} - Note: {e['note']}")
            
# Delete Expenses
def delete_expenses():
    if not expenses:
        print("No expenses to delete")
        return

    view_expenses()
    try:
        user_choice = int(input("Choose a number: "))

        if user_choice < 1 or user_choice > len(expenses):
            print("Invalid number, please choose from the list range")
            return

        delete = user_choice - 1
        removed = expenses.pop(delete)
        print("Removed:", removed)
        save_expenses()
        
    except ValueError:
        print("Enter a valid number")
        
# save expenses       
def save_expenses():
    with open(DATA_FILE, "w") as file:
        json.dump(expenses, file)
        
def load_expenses():
    global expenses
    try:
        with open(DATA_FILE, "r") as file:
            expenses = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        print("There is no existing file here; a new file is being created.")
        
load_expenses()

# total expenses
def total_expenses():
    total = sum([e['amount'] for e in expenses])
    return total 
 
# category summary
def category_summary():
    summary = {}
    for e in expenses:
        category = e["category"]
        summary[category] = summary.get(category , 0) + e['amount']
    return summary

# show summary
def show_summary():
    total = total_expenses()
    print(f"Total expenses is {total}.")
    summary = category_summary()
    for category, amount in summary.items():
        print(f"{category} : Rs. {amount}")

    if budget > 0:
        print(f"Budget Set: Rs. {budget}")
        if total > budget:
            print(f"Budget exceeded by Rs. {total - budget}!")
        else:
            print(f"Remaining budget: Rs. {budget - total}")
    else:
        print("No budget set yet.")
       
def set_budget(): 
    global budget      
    budget = float(input("Set your Budget.: "))
    with open (BUDGET_FILE, "w") as file:
        file.write(str(budget))
        

def load_budget():
    global budget
    try:
        with open(BUDGET_FILE, "r") as file:
            budget = float(file.read())
    except (FileNotFoundError, ValueError):
        budget = 0
        
load_budget()
    

while True:
    try:
        print("1. Add Expenses")
        print("2. View Expenses")
        print("3. Delete Expenses")
        print("4. Set Budget")
        print("5. Summary")
        print("6. Exit")
        
        while True:
            try:
                choice = int(input("Choose an option: "))
                if 1 <= choice <= 6:
                    break
                else:
                    print("Invailed option.")
            except:
                print("Invailed option.")
        if choice == 1:
            add_expenses()
            
        elif choice == 2:
            view_expenses()
            
        elif choice == 3:
            delete_expenses()
            
        elif choice == 4:
            set_budget()
            
        elif choice == 5:
            show_summary()
            
        elif choice == 6:
            break
        else:
            print("Wrong choice, choose only 1-6")
        
    except ValueError:
        print("Enter only numbers")