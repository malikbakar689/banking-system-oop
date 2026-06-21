"""
Banking System Simulation
--------------------------
Demonstrates core Object-Oriented Programming concepts in Python:
encapsulation, inheritance, and polymorphism.

Author: Muhammad Abubakar Mustafa
"""


class BankAccount:
    """Base class representing a standard bank account."""

    def __init__(self, account_holder, account_number, balance=0.0):
        self.account_holder = account_holder
        self.account_number = account_number
        self._balance = balance  # protected attribute -> encapsulation

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self._balance += amount
        print(f"Deposited Rs.{amount:.2f}. New balance: Rs.{self._balance:.2f}")
        return self._balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self._balance:
            print("Withdrawal denied: insufficient funds.")
            return self._balance
        self._balance -= amount
        print(f"Withdrew Rs.{amount:.2f}. New balance: Rs.{self._balance:.2f}")
        return self._balance

    def get_balance(self):
        return self._balance

    def account_summary(self):
        return (f"Account Holder : {self.account_holder}\n"
                f"Account Number : {self.account_number}\n"
                f"Account Type   : {self.__class__.__name__}\n"
                f"Balance        : Rs.{self._balance:.2f}")

    def __str__(self):
        return self.account_summary()


class SavingsAccount(BankAccount):
    """Savings account with interest calculation. Demonstrates inheritance."""

    MINIMUM_BALANCE = 1000

    def __init__(self, account_holder, account_number, balance=0.0, interest_rate=0.05):
        super().__init__(account_holder, account_number, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        interest = self._balance * self.interest_rate
        self._balance += interest
        print(f"Interest applied: Rs.{interest:.2f}. New balance: Rs.{self._balance:.2f}")
        return self._balance

    def withdraw(self, amount):
        """Override: savings accounts must maintain a minimum balance (polymorphism)."""
        if amount > 0 and (self._balance - amount) < self.MINIMUM_BALANCE:
            print(f"Withdrawal denied: minimum balance of Rs.{self.MINIMUM_BALANCE} must be maintained.")
            return self._balance
        return super().withdraw(amount)

    def account_summary(self):
        return super().account_summary() + f"\nInterest Rate  : {self.interest_rate * 100:.1f}%"


class CurrentAccount(BankAccount):
    """Current account with overdraft facility. Further demonstrates polymorphism."""

    def __init__(self, account_holder, account_number, balance=0.0, overdraft_limit=5000):
        super().__init__(account_holder, account_number, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        """Override: current accounts may go negative up to the overdraft limit."""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if (self._balance - amount) < -self.overdraft_limit:
            print("Withdrawal denied: overdraft limit exceeded.")
            return self._balance
        self._balance -= amount
        print(f"Withdrew Rs.{amount:.2f}. New balance: Rs.{self._balance:.2f}")
        return self._balance

    def account_summary(self):
        return super().account_summary() + f"\nOverdraft Limit: Rs.{self.overdraft_limit:.2f}"


def main():
    print("=== Banking System Simulation ===\n")

    savings = SavingsAccount("Muhammad Abubakar Mustafa", "SA-1001", balance=5000, interest_rate=0.06)
    current = CurrentAccount("Muhammad Abubakar Mustafa", "CA-2001", balance=2000, overdraft_limit=3000)
    accounts = [savings, current]

    print("--- Initial Summaries ---")
    for acc in accounts:
        print(acc.account_summary())
        print("-" * 40)

    print("\n--- Transactions ---")
    savings.deposit(1500)
    savings.apply_interest()
    savings.withdraw(4000)   # respects minimum balance rule
    current.withdraw(4500)   # uses overdraft

    print("\n--- Final Summaries (same method, different behavior -> polymorphism) ---")
    for acc in accounts:
        print(acc.account_summary())
        print("-" * 40)


if __name__ == "__main__":
    main()
