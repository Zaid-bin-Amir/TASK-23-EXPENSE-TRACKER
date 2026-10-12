import csv
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
FIELDS = ["date", "category", "description", "amount"]


def load_expenses(path=DATA_FILE):
    if not os.path.exists(path):
        return []
    expenses = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            expenses.append(
                {
                    "date": row["date"],
                    "category": row["category"],
                    "description": row["description"],
                    "amount": float(row["amount"]),
                }
            )
    return expenses


def save_expenses(expenses, path=DATA_FILE):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(expenses)


def parse_amount(text):
    try:
        value = float(text)
    except ValueError:
        raise ValueError("Amount must be a number.")
    if value <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(value, 2)


def parse_date(text):
    text = text.strip()
    if not text:
        return datetime.now().strftime("%Y-%m-%d")
    try:
        return datetime.strptime(text, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Date must be in YYYY-MM-DD format.")


def clean_text(text, field_name):
    text = text.strip()
    if not text:
        raise ValueError(f"{field_name} cannot be empty.")
    return text


def create_expense(date, category, description, amount):
    return {
        "date": parse_date(date),
        "category": clean_text(category, "Category").title(),
        "description": clean_text(description, "Description"),
        "amount": parse_amount(amount),
    }


def total_spending(expenses):
    return round(sum(e["amount"] for e in expenses), 2)


def spending_by_category(expenses):
    totals = {}
    for e in expenses:
        totals[e["category"]] = totals.get(e["category"], 0) + e["amount"]
    return {k: round(v, 2) for k, v in totals.items()}


def spending_by_month(expenses):
    totals = {}
    for e in expenses:
        month = e["date"][:7]
        totals[month] = totals.get(month, 0) + e["amount"]
    return {k: round(v, 2) for k, v in sorted(totals.items())}


def filter_by_category(expenses, category):
    return [e for e in expenses if e["category"].lower() == category.lower()]


def print_expenses(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    print(f"\n{'#':<4}{'Date':<12}{'Category':<15}{'Description':<25}{'Amount':>10}")
    print("-" * 66)
    for i, e in enumerate(expenses, start=1):
        print(
            f"{i:<4}{e['date']:<12}{e['category']:<15}"
            f"{e['description'][:24]:<25}{e['amount']:>10.2f}"
        )


def print_category_summary(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    totals = spending_by_category(expenses)
    grand_total = total_spending(expenses)
    print(f"\n{'Category':<20}{'Total':>12}{'Share':>10}")
    print("-" * 42)
    for category, amount in sorted(totals.items(), key=lambda x: x[1], reverse=True):
        share = amount / grand_total * 100
        print(f"{category:<20}{amount:>12.2f}{share:>9.1f}%")


def print_total_report(expenses):
    if not expenses:
        print("\nNo expenses recorded yet.")
        return
    totals = spending_by_category(expenses)
    top_category = max(totals, key=totals.get)
    biggest = max(expenses, key=lambda e: e["amount"])
    print("\n===== TOTAL SPENDING REPORT =====")
    print(f"Number of expenses : {len(expenses)}")
    print(f"Total spent        : {total_spending(expenses):.2f}")
    print(f"Average per expense: {total_spending(expenses) / len(expenses):.2f}")
    print(f"Top category       : {top_category} ({totals[top_category]:.2f})")
    print(
        f"Largest expense    : {biggest['description']} "
        f"({biggest['amount']:.2f} on {biggest['date']})"
    )
    print("\nMonthly spending:")
    for month, amount in spending_by_month(expenses).items():
        print(f"  {month}: {amount:.2f}")


def add_expense_flow(expenses):
    print("\n--- Add New Expense ---")
    try:
        expense = create_expense(
            input("Date (YYYY-MM-DD, Enter for today): "),
            input("Category (e.g. Food, Transport): "),
            input("Description: "),
            input("Amount: "),
        )
    except ValueError as error:
        print(f"Invalid input: {error}")
        return
    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved successfully.")


def delete_expense_flow(expenses):
    print_expenses(expenses)
    if not expenses:
        return
    choice = input("\nEnter the number to delete (Enter to cancel): ").strip()
    if not choice:
        return
    if not choice.isdigit() or not 1 <= int(choice) <= len(expenses):
        print("Invalid number.")
        return
    removed = expenses.pop(int(choice) - 1)
    save_expenses(expenses)
    print(f"Deleted: {removed['description']} ({removed['amount']:.2f})")


def filter_flow(expenses):
    category = input("\nCategory to filter by: ").strip()
    if not category:
        print("Category cannot be empty.")
        return
    matches = filter_by_category(expenses, category)
    print_expenses(matches)
    if matches:
        print(f"\nTotal for {category.title()}: {total_spending(matches):.2f}")


MENU = """
===== EXPENSE TRACKER =====
1. Add expense
2. View all expenses
3. Category-wise summary
4. Total spending report
5. Filter by category
6. Delete an expense
7. Exit
"""


def main():
    expenses = load_expenses()
    actions = {
        "1": lambda: add_expense_flow(expenses),
        "2": lambda: print_expenses(expenses),
        "3": lambda: print_category_summary(expenses),
        "4": lambda: print_total_report(expenses),
        "5": lambda: filter_flow(expenses),
        "6": lambda: delete_expense_flow(expenses),
    }
    while True:
        print(MENU)
        choice = input("Choose an option (1-7): ").strip()
        if choice == "7":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Please choose a number between 1 and 7.")


if __name__ == "__main__":
    main()