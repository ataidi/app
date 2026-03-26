from abc import ABC, abstractmethod


# ======================
# Models
# ======================
class BankAccount(ABC):
    def __init__(self, name, balance=0):
        self.name = name
        self.__balance = balance

    @abstractmethod
    def account_type(self):
        pass

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited {amount}")
        else:
            print("Invalid amount")

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            print(f"Withdrew {amount}")
        else:
            print("Insufficient balance")

    def get_balance(self):
        return self.__balance


class SavingsAccount(BankAccount):
    def account_type(self):
        return "Savings Account"


class CurrentAccount(BankAccount):
    def account_type(self):
        return "Current Account"


# ======================
# Bank System (Database)
# ======================
class BankSystem:
    def __init__(self):
        self.accounts = {}

    def create_account(self):
        name = input("Enter name: ")
        acc_type = input("Enter account type (savings/current): ").lower()
        balance = float(input("Enter initial balance: "))

        if name in self.accounts:
            print("Account already exists!")
            return

        if acc_type == "savings":
            account = SavingsAccount(name, balance)
        else:
            account = CurrentAccount(name, balance)

        self.accounts[name] = account
        print(f"{acc_type.capitalize()} account created for {name}")

    def deposit(self):
        name = input("Enter name: ")
        amount = float(input("Enter amount: "))

        if name in self.accounts:
            self.accounts[name].deposit(amount)
        else:
            print("Account not found")

    def withdraw(self):
        name = input("Enter name: ")
        amount = float(input("Enter amount: "))

        if name in self.accounts:
            self.accounts[name].withdraw(amount)
        else:
            print("Account not found")

    def check_balance(self):
        name = input("Enter name: ")

        if name in self.accounts:
            balance = self.accounts[name].get_balance()
            print(f"Balance: {balance}")
        else:
            print("Account not found")


# ======================
# Main Program (Menu)
# ======================
def main():
    bank = BankSystem()

    while True:
        print("\n===== BANK SYSTEM =====")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            bank.create_account()
        elif choice == "2":
            bank.deposit()
        elif choice == "3":
            bank.withdraw()
        elif choice == "4":
            bank.check_balance()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()