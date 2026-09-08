import utils.transport
import utils.session
def load_balance() -> float:
    """
    Load the account balance from balance.txt.

    Returns:
        float: The saved balance, or 0.0 if no balance file exists or it
        contains invalid data.
    """
    try:
        with open("balance.txt", "r") as file:
            return float(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0.0


def save_balance(balance: float) -> None:
    """
    Persist the account balance to balance.txt.

    Args:
        balance (float): The current account balance.
    """
    with open("balance.txt", "w") as file:
        file.write(f"{balance:,.2f}")


def record_transaction(transaction_type: str, amount: float, balance: float) -> None:
    """
    Append a transaction entry to transactions.txt.

    Args:
        transaction_type (str): Either "deposit" or "withdrawal".
        amount (float): The amount of the transaction.
        balance (float): The account balance after the transaction.
    """
    import datetime

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} | {transaction_type} | ${amount:,.2f} | Balance: ${balance:,.2f}\n"
    with open("transactions.txt", "a") as file:
        file.write(entry)


def show_balance(balance: float) -> str:
    """
    Format the account balance as a currency string.

    Args:
        balance (float): The current account balance.

    Returns:
        str: The balance formatted as a dollar amount with two decimal places
             and thousands separators.
    """
    return f" ${balance:,.2f}"


def withdraw(balance: float, amount: float):
    """
    Withdraw a specified amount from the account balance.

    Validates the withdrawal amount and returns a message describing the result.

    Args:
        balance (float): The current account balance.
        amount (float): The amount to withdraw.

    Returns:
        tuple[float, str]: A tuple containing:
            - The updated balance (unchanged if the withdrawal is invalid).
            - A status message describing the outcome.
    """
    # Reject withdrawals larger than the available balance.
    if amount > balance:
        return balance, f"Insufficient funds"
    # Reject zero or negative amounts.
    elif amount <= 0:
        return balance, "Invalid amount, please enter a positive number"
    # Perform the withdrawal and confirm the transaction.
    else:
        balance -= amount
        record_transaction("withdrawal", amount, balance)
        save_balance(balance)
        return balance, f"You withdrew ${amount:,.2f}"


def deposit(balance: float, amount: float):
    """
    Deposit a specified amount into the account balance.

    Only positive amounts are accepted; non-positive amounts are rejected.

    Args:
        balance (float): The current account balance.
        amount (float): The amount to deposit.

    Returns:
        tuple[float, str]: A tuple containing:
            - The updated balance (unchanged if the deposit is invalid).
            - A status message describing the outcome.
    """
    # Accept only positive deposits and update the balance.
    if amount > 0:
        balance += amount
        record_transaction("deposit", amount, balance)
        save_balance(balance)
        return balance, f"You deposited ${amount} to your account"
    # Reject zero or negative deposit attempts.
    else:
        return balance, f"You cannot deposit ${amount} to your account"


def print_transactions() -> None:
    """
    Display the full transaction history from transactions.txt.

    If no transaction file exists, a message indicating an empty history is
    printed instead.
    """
    try:
        with open("transactions.txt", "r") as file:
            content = file.read()
        if content.strip():
            print("\n*********************")
            print("-- Transaction History --")
            print("*********************\n")
            print(content)
        else:
            print("\nNo transactions yet.\n")
    except FileNotFoundError:
        print("\nNo transactions yet.\n")


def main():
    """
    Run the interactive command-line banking application.

    Presents a menu loop allowing the user to withdraw, deposit, check their
    balance, view transaction history, or exit. Input is validated, and
    non-numeric entries produce a friendly error message without crashing.
    The balance and transaction history persist across sessions via files.
    """
    # Load the saved balance from file, or start at zero.
    balance = load_balance()

    # Display the application banner.
    print("\n*********************")
    print("-- Simple Bank --")
    print("*********************\n")
    # Main interaction loop: keep showing the menu until the user exits.
    while True:
        # Print the menu header and available options.
        print("\n*********************")
        print("select your option")
        print("1. Withdraw")
        print("2. Deposit")
        print("3. Account Balance")
        print("4. Transaction History")
        print("5. Exit")
        print("*********************\n")
        try:
            # Read the user's menu selection as an integer.
            choice = int(input("Enter your choice: "))
            # Option 5: exit the application gracefully.
            if choice == 5:
                print("\n*********************")
                print("\nclosing banking app, goodbye!\n")
                break
            # Option 1: handle a withdrawal request.
            if choice == 1:
                try:
                    amount = float(input("Enter amount to withdraw: "))
                    balance, message = withdraw(balance, amount)
                    print(f"{message}\nYour current balance is: {show_balance(balance)}")
                except ValueError:
                    # Handle non-numeric input for the withdrawal amount.
                    print("Please enter a numeric value")
            # Option 2: handle a deposit request.
            if choice == 2:
                try:
                    amount = float(input("Enter amount to deposit: "))
                    balance, message = deposit(balance, amount)
                    print(f"{message}\n Your current balance is: {show_balance(balance)}")
                except ValueError:
                    # Handle non-numeric input for the deposit amount.
                    print("Please enter a numeric value")
            # Option 3: display the current account balance.
            if choice == 3:
                print("\n********************")
                print(f"\nyour current balance is: {show_balance(balance)}\n")
            # Option 4: display the transaction history.
            if choice == 4:
                print_transactions()
        except ValueError:
            # Handle non-numeric input for the menu choice.
            print("Please enter a numeric value")


if __name__ == "__main__":
    main()
