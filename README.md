# TASK-23-EXPENSE-TRACKER# Simple Expense Tracker

A command-line expense tracker built with Python. It records the date, category, description and amount of every expense, saves them to a CSV file, and generates spending summaries.

## Features

- Add expenses with date, category, description and amount
- Persistent storage in `expenses.csv` (data is kept between runs)
- View all recorded expenses in a clean table
- Category-wise spending summary with percentage share
- Total spending report (total, average, top category, largest expense, monthly breakdown)
- Filter expenses by category
- Delete an expense
- Input validation for dates and amounts

## Requirements

- Python 3.8 or newer
- No external libraries (uses only the standard library: `csv`, `os`, `datetime`)

## How to Run

```bash
python expense_tracker.py
```

## Usage

When the program starts, a menu is shown:

```
===== EXPENSE TRACKER =====
1. Add expense
2. View all expenses
3. Category-wise summary
4. Total spending report
5. Filter by category
6. Delete an expense
7. Exit
```

### Adding an expense

```
Date (YYYY-MM-DD, Enter for today): 2026-10-12
Category (e.g. Food, Transport): food
Description: Lunch at cafe
Amount: 450
```

- Press Enter on the date to use today's date.
- Category names are stored in title case, so `food` and `Food` are treated as the same category.
- The amount must be a number greater than zero.

### Sample category summary

```
Category                  Total     Share
------------------------------------------
Food                    1250.00     52.1%
Transport                700.00     29.2%
Shopping                 450.00     18.7%
```

## Project Structure

```
expense_tracker.py   Main program
expenses.csv         Data file (created automatically on first save)
README.md            Project documentation
```

## Design Notes

The code is organised so that data storage, calculations and user interaction are kept separate:

| Part | Functions |
|------|-----------|
| Storage | `load_expenses`, `save_expenses` |
| Validation | `parse_amount`, `parse_date`, `clean_text`, `create_expense` |
| Calculations | `total_spending`, `spending_by_category`, `spending_by_month`, `filter_by_category` |
| Display | `print_expenses`, `print_category_summary`, `print_total_report` |
| User flow | `add_expense_flow`, `delete_expense_flow`, `filter_flow`, `main` |

Each expense is a dictionary:

```python
{"date": "2026-10-12", "category": "Food", "description": "Lunch at cafe", "amount": 450.0}
```

All expenses are kept in a list, and that list is written to a CSV file after every change.

## Interview Questions

**How would you store expense records?**
Each expense is a dictionary with date, category, description and amount. All dictionaries are collected in a list, and the list is saved to a CSV file so the data survives after the program closes.

**Why should application data be stored separately from calculations?**
Keeping storage and calculation logic apart makes the code easier to test, maintain and change. For example, the CSV file could be replaced with JSON or a database without touching the summary functions.

**Why validate expense amounts?**
Invalid values such as text, zero or negative numbers would break the totals and make reports wrong. Validating at the point of input keeps the saved data clean.

## Possible Improvements

- Edit an existing expense
- Filter by date range
- Export reports to a text or PDF file
- Set monthly budgets with overspending warnings

## Author

Zaid — Python Programming Track, Level 1, Day 23
