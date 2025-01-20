import json
from abc import ABC, abstractmethod

class AbstractExpenseTracker(ABC):
    @abstractmethod
    def add_expense(self):
        pass

    @abstractmethod
    def delete_expense(self):
        pass

    @abstractmethod
    def edit_expense(self):
        pass

    @abstractmethod
    def display_summary(self):
        pass

    @abstractmethod
    def display_expenses(self):
        pass

    @abstractmethod
    def convert_to_rupees(self):
        pass


class ExpenseTracker(AbstractExpenseTracker):
    def __init__(self):
        self.expenses = self.load_expenses()

    def load_expenses(self):
        try:
            with open('expenses.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_expenses(self):
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file, indent=4)

    def add_expense(self):
        category = input("Enter expense category (e.g., Food, Travel, Shopping, Bill payments, etc): ")
        try:
            amount = float(input("Enter the amount in USD: "))
        except ValueError:
            print("Invalid amount. Please enter a numeric value.")
            return
        expense = {'category': category, 'amount': amount}
        self.expenses.append(expense)
        print(f"Expense of ${amount} added under category '{category}'.")

    def delete_expense(self):
        if not self.expenses:
            print("No expenses to delete.")
            return
        self.display_expenses()
        try:
            index = int(input("Enter the number of the expense to delete: ")) - 1
            if 0 <= index < len(self.expenses):
                removed = self.expenses.pop(index)
                print(f"Deleted expense: {removed['category']} - ${removed['amount']}")
            else:
                print("Invalid number. No expense deleted.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def edit_expense(self):
        if not self.expenses:
            print("No expenses to edit.")
            return
        self.display_expenses()
        try:
            index = int(input("Enter the number of the expense to edit: ")) - 1
            if 0 <= index < len(self.expenses):
                print("Editing expense:")
                category = input(f"New category (current: {self.expenses[index]['category']}): ") or self.expenses[index]['category']
                try:
                    amount = input(f"New amount (current: ${self.expenses[index]['amount']}): ")
                    amount = float(amount) if amount else self.expenses[index]['amount']
                except ValueError:
                    print("Invalid amount. Edit canceled.")
                    return
                self.expenses[index] = {'category': category, 'amount': amount}
                print("Expense updated.")
            else:
                print("Invalid number. No expense edited.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    def display_summary(self):
        if not self.expenses:
            print("No expenses to summarize.")
            return
        print("\n--- Expense Summary ---")
        total = 0
        category_totals = {}
        for expense in self.expenses:
            total += expense['amount']
            category_totals[expense['category']] = category_totals.get(expense['category'], 0) + expense['amount']
        for category, amount in category_totals.items():
            print(f"{category}: ${amount}")
        print(f"\nTotal Expenses: ${total}")

    def display_expenses(self):
        if not self.expenses:
            print("No expenses to display.")
            return
        print("\n--- Expenses ---")
        total = 0
        for idx, expense in enumerate(self.expenses, start=1):
            print(f"{idx}. {expense['category']}: ${expense['amount']}")
            total += expense['amount']
        print(f"\nTotal Expenses: ${total}")

    def convert_to_rupees(self):
        try:
            exchange_rate = float(input("Enter the current USD to INR exchange rate: "))
        except ValueError:
            print("Invalid exchange rate. Please enter a numeric value.")
            return

        if not self.expenses:
            print("No expenses to convert.")
            return

        print("\n--- Expenses in INR ---")
        total_inr = 0
        for expense in self.expenses:
            amount_inr = expense['amount'] * exchange_rate
            total_inr += amount_inr
            print(f"{expense['category']}: ₹{amount_inr:.2f}")
        print(f"\nTotal Expenses in INR: ₹{total_inr:.2f}")


def main():
    tracker = ExpenseTracker()

    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Delete Expense")
        print("4. Edit Expense")
        print("5. View Summary")
        print("6. Convert Expenses to INR")
        print("7. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            tracker.add_expense()
            tracker.save_expenses()
        elif choice == '2':
            tracker.display_expenses()
        elif choice == '3':
            tracker.delete_expense()
            tracker.save_expenses()
        elif choice == '4':
            tracker.edit_expense()
            tracker.save_expenses()
        elif choice == '5':
            tracker.display_summary()
        elif choice == '6':
            tracker.convert_to_rupees()
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please try again.")


if __name__ == "__main__":
    main()
