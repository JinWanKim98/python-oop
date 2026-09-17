# Class to represent a bank customer who can have multiple accounts
class Customer:
    # Initialize customer info and create first account
    def __init__(self, customer_id, name, address, email, account_num, account_type, balance, created_date):
        self.__customer_id = customer_id
        self.__name = name
        self.__address = address
        self.__email = email
        self.__accounts = []

        self.add_bank_account(account_num, account_type, balance, created_date)

    # Create a new account for this customer
    def add_bank_account(self, account_num, account_type, balance, created_date):
        for account in self.__accounts:  # check account
            if account.get_account_number() == account_num:
                return False
        new_account = BankAccount(account_num, account_type, self.__customer_id, balance, created_date)
        self.__accounts.append(new_account)
        return True

    # Remove an account from customer's accounts list
    def remove_bank_account(self, account_num_to_remove):
        for i, account in enumerate(self.__accounts):
            if account.get_account_number() == account_num_to_remove:
                del self.__accounts[i]
                return True
        return False

    # Deposit money to account
    def deposit(self, account_num, amount):
        account = self.get_bank_account(account_num)
        if account:
            return account.deposit(amount)
        else:
            return False

    # Withdraw money from account
    def withdraw(self, account_num, amount):
        account = self.get_bank_account(account_num)
        if account:
            return account.withdraw(amount)
        else:
            return False

    # Find an account by account number
    def get_bank_account(self, account_num):
        for account in self.__accounts:
            if account.get_account_number() == account_num:
                return account
        return None

    # Calculate total balance of accounts
    def get_total_balance(self):
        total = 0.0
        for account in self.__accounts:
            total += account.get_balance()
        return total

    # Add interest to accounts
    def add_interest_to_accounts(self):
        for account in self.__accounts:
            account.add_interest()

    # Return customer information
    def get_customer_info(self):
        return f"ID: {self.__customer_id}, Name: {self.__name}, Address: {self.__address}, Email: {self.__email}"

    # String representation of customer with total balance
    def __str__(self):
        return f"Customer {self.__customer_id}: Total Balance = {self.get_total_balance()}"


#####################################################################

# Class to represent a bank account
class BankAccount:
    # Class variable for interest rate (shared by all accounts)
    interest_rate = 0.0

    # Initialize account details
    def __init__(self, account_num, account_type, customer_id, balance, created_date):
        self.__account_num = account_num
        self.__account_type = account_type
        self.__customer_id = customer_id
        self.__balance = balance
        self.__created_date = created_date

    # Add money to account
    def deposit(self, amount):
        if amount <= 0:
            return False
        self.__balance += amount
        return True

    # Remove money from account if the balance is enough
    def withdraw(self, amount):
        if amount <= 0:
            return False
        if amount > self.__balance:
            return False
        self.__balance -= amount
        return True

    # Get account number
    def get_account_number(self):
        return self.__account_num

    # Get current balance
    def get_balance(self):
        return self.__balance

    # Apply interest to account balance
    def add_interest(self):
        self.__balance = round(self.__balance * (1 + BankAccount.interest_rate / 100), 2)

    # Set interest rate for all accounts
    @classmethod
    def set_interest_rate(cls, rate):
        cls.interest_rate = rate

    # String representation of account
    def __str__(self):
        return f"Account {self.__account_num} ({self.__account_type}): ${self.__balance}, Created: {self.__created_date}"
