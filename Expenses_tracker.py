expenses = []

def add_expenses():
    try:
        amount = float(input("Amount : "))
        category = input("Category : ")
        note = input("Note: ")
        expenses.append({"amount": amount, "category": category, "note": note})
        print("Added successfully")
        
    except ValueError:
        print("Enter only numbers")

def view_expenses():
    if not expenses:
        print("No expenses added yet")
        
    else:
        for i, e in enumerate(expenses, 1):
            print(f"{i}. {e['category']} - Rs. {e['amount']} - Note: {e['note']}")

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
        
    except ValueError:
        print("Enter a valid number")

while True:
    try:
        print("1. Add Expenses")
        print("2. View Expenses")
        print("3. Delete Expenses")
        print("4. Exit")
        
        choice = int(input("Choose an option: "))
        
        if choice == 1:
            add_expenses()
            
        elif choice == 2:
            view_expenses()
            
        elif choice == 3:
            delete_expenses()
            
        elif choice == 4:
            break
        else:
            print("Wrong choice, choose only 1-4")
        
    except ValueError:
        print("Enter only numbers")