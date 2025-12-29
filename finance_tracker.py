import json
import os
from datetime import datetime
import requests

EXPENSE_FILE = "expenses.json"
INVEST_FILE = "investments.json"
DEFAULT_CURRENCY = "USD"
EXCHANGE_API = "https://api.exchangerate.host"


def load_data(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


def add_expense(category, amount, note, currency=DEFAULT_CURRENCY):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if not category or not isinstance(category, str):
        raise ValueError("Category must be a non-empty string")

    expense = {
        "category": category,
        "amount": float(amount),
        "currency": currency.upper() if currency else DEFAULT_CURRENCY,
        "note": note,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }

    data = load_data(EXPENSE_FILE)
    data.append(expense)
    save_data(EXPENSE_FILE, data)

    return expense


def add_investment(inv_type, amount, returns, note, currency=DEFAULT_CURRENCY):
    if amount < 0:
        raise ValueError("Amount cannot be negative")
    if not inv_type or not isinstance(inv_type, str):
        raise ValueError("Investment type must be a non-empty string")

    investment = {
        "type": inv_type,
        "amount": float(amount),
        "currency": currency.upper() if currency else DEFAULT_CURRENCY,
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
        summary += f"{item['date']} | {item['category']} | {item['amount']} {item.get('currency', DEFAULT_CURRENCY)} | {item['note']}\n"
    summary += f"\nTotal Spent: {total} {DEFAULT_CURRENCY}\n"
    return summary


def view_investments():
    data = load_data(INVEST_FILE)
    if not data:
        return "No investments recorded yet."

    total = sum(item["amount"] for item in data)
    summary = "\n--- Investment Summary ---\n"
    for item in data:
        summary += f"{item['date']} | {item['type']} | {item['amount']} {item.get('currency', DEFAULT_CURRENCY)} | {item['returns']} | {item['note']}\n"
    summary += f"\nTotal Invested: {total} {DEFAULT_CURRENCY}\n"
    return summary


def get_total_expenses(target_currency=None):
    data = load_data(EXPENSE_FILE)
    if not data:
        return 0
    if not target_currency:
        return sum(item["amount"] for item in data)
    total = 0
    for item in data:
        total += convert_amount(item["amount"], item.get("currency", DEFAULT_CURRENCY), target_currency)
    return total


def get_total_investments(target_currency=None):
    data = load_data(INVEST_FILE)
    if not data:
        return 0
    if not target_currency:
        return sum(item["amount"] for item in data)
    total = 0
    for item in data:
        total += convert_amount(item["amount"], item.get("currency", DEFAULT_CURRENCY), target_currency)
    return total


def get_supported_currencies():
    # Restrict supported currencies to the primary set requested by the user.
    # This avoids returning a very large list and keeps the UI focused.
    return ["PLN", "USD", "INR"]


def convert_amount(amount, from_currency, to_currency):
    from_currency = (from_currency or DEFAULT_CURRENCY).upper()
    to_currency = (to_currency or DEFAULT_CURRENCY).upper()
    if from_currency == to_currency:
        return float(amount)
    try:
        params = {"from": from_currency, "to": to_currency, "amount": amount}
        r = requests.get(f"{EXCHANGE_API}/convert", params=params, timeout=5)
        r.raise_for_status()
        data = r.json()
        return float(data.get("result", amount))
    except Exception:
        # on failure, return original amount (best-effort)
        return float(amount)


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
            currency = input("Currency (USD): ") or DEFAULT_CURRENCY
            note = input("Any note: ")
            add_expense(category, amount, note, currency)
            print("Expense added successfully!")
        elif choice == "2":
            inv_type = input("Investment type (stocks, crypto, mutual fund, etc): ")
            amount = float(input("Amount invested: "))
            currency = input("Currency (USD): ") or DEFAULT_CURRENCY
            returns = input("Expected returns or % (optional): ")
            note = input("Any note: ")
            add_investment(inv_type, amount, returns, note, currency)
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
