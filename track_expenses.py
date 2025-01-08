import os
import datetime
import calendar

# Define the Expense class
class Expense:
    def __init__(self, name, amount, category):
        self.name = name
        self.amount = amount
        self.category = category

    def __str__(self):
        return f"{self.name}, ${self.amount:.2f}, {self.category}"

# Function to get user input for an expense
def get_user_expense():
    print("🎯 Getting User Expense")
    expense_name = input("Enter expense name: ")
    while True:
        try:
            expense_amount = float(input("Enter expense amount: "))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

    categories = {
        1: "🍔 Food",
        2: "🏠 Home",
        3: "💼 Work",
        4: "🎉 Fun",
        5: "✨ Misc",
    }
    print("Select a category:")
    for num, category in categories.items():
        print(f"  {num}. {category}")

    while True:
        try:
            category_number = int(input("Enter a category number [1 - 5]: "))
            expense_category = categories[category_number]
            break
        except (ValueError, KeyError):
            print("Invalid category. Please select a valid number from 1 to 5.")

    return Expense(expense_name, expense_amount, expense_category)

# Function to save the expense to a CSV file
def save_expense_to_file(expense, file_path):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")
    print(f"🎯 Saving User Expense: {expense} to {file_path}")

# Function to summarize expenses from the CSV file
def summarize_expenses(file_path, budget):
    print(f"🎯 Summarizing User Expense")
    expenses = []

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

        for line in lines:
            parts = line.strip().split(",")
            if len(parts) != 3:  # Check for malformed lines
                print(f"⚠️ Skipping malformed line: {line.strip()}")
                continue

            expense_name, expense_amount, expense_category = parts
            try:
                line_expense = Expense(
                    name=expense_name,
                    amount=float(expense_amount),
                    category=expense_category,
                )
                expenses.append(line_expense)
            except ValueError:
                print(f"⚠️ Error processing line: {line.strip()}")
                continue

    # Summarize expenses by category
    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount

    print("Expenses By Category 📈:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")

    total_spent = sum([x.amount for x in expenses])
    print(f"💵 Total Spent: ${total_spent:.2f}")

    remaining_budget = budget - total_spent
    print(f"✅ Budget Remaining: ${remaining_budget:.2f}")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = days_in_month - now.day

    daily_budget = remaining_budget / remaining_days if remaining_days > 0 else 0
    print(f"👉 Budget Per Day: ${daily_budget:.2f}")

# Main function to run the expense tracker
def main():
    print("🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = 1000.00  # Example monthly budget

    # Create the file if it doesn't exist
    if not os.path.exists(expense_file_path):
        with open(expense_file_path, "w", encoding="utf-8") as f:
            f.write("")

    expense = get_user_expense()
    save_expense_to_file(expense, expense_file_path)
    summarize_expenses(expense_file_path, budget)

if __name__ == "__main__":
    main()

