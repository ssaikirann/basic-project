import json
import os
from datetime import datetime

EXPENSE_FILE = "expenses.json"
INVEST_FILE = "investments.json"


def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def add_expense(category, amount, note):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if not category or not isinstance(category, str):
        raise ValueError("Category must be a non-empty string")
    
    expense = {
        "category": category,
        "amount": amount,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data = load_data(EXPENSE_FILE)
    data.append(expense)
    save_data(EXPENSE_FILE, data)

    return expense


def add_investment(inv_type, amount, returns, note):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if not inv_type or not isinstance(inv_type, str):
        raise ValueError("Investment type must be a non-empty string")
    
    investment = {
        "type": inv_type,
        "amount": amount,
        "returns": returns,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data = load_data(INVEST_FILE)
    data.append(investment)
    save_data(INVEST_FILE, data)

    return investment


def view_expenses():
    data = load_data(EXPENSE_FILE)
    if not data:
        return "No expenses recorded yet."

    total = sum(item["amount"] for item in data)
    summary = "\n--- Expense Summary ---\n"
    for item in data:
        summary += f"{item['date']} | {item['category']} | {item['amount']} | {item['note']}\n"
    summary += f"\nTotal Spent: {total}\n"
    return summary


def view_investments():
    data = load_data(INVEST_FILE)
    if not data:
        return "No investments recorded yet."

    total = sum(item["amount"] for item in data)
    summary = "\n--- Investment Summary ---\n"
    for item in data:
        summary += f"{item['date']} | {item['type']} | {item['amount']} | {item['returns']} | {item['note']}\n"
    summary += f"\nTotal Invested: {total}\n"
    return summary


def get_total_expenses():
    data = load_data(EXPENSE_FILE)
    return sum(item["amount"] for item in data) if data else 0


def get_total_investments():
    data = load_data(INVEST_FILE)
    return sum(item["amount"] for item in data) if data else 0


def interactive_mode():
    while True:
        print("\n--- Finance Tracker ---")
        print("1. Add Expense")
        print("2. Add Investment")
        print("3. View Expenses")
        print("4. View Investments")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            category = input("Enter category (food, rent, travel, etc): ")
            amount = float(input("Enter amount: "))
            note = input("Any note: ")
            add_expense(category, amount, note)
            print("Expense added successfully!")
        elif choice == "2":
            inv_type = input("Investment type (stocks, crypto, mutual fund, etc): ")
            amount = float(input("Amount invested: "))
            returns = input("Expected returns or % (optional): ")
            note = input("Any note: ")
            add_investment(inv_type, amount, returns, note)
            print("Investment added successfully!")
        elif choice == "3":
            print(view_expenses())
        elif choice == "4":
            print(view_investments())
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    interactive_mode()
