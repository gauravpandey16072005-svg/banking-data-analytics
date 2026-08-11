import pandas as pd
import random
from datetime import timedelta

# ============================================================
# SETTINGS
# ============================================================

NUM_TRANSACTIONS = 400000

START_DATE = pd.Timestamp("2023-01-01")
END_DATE = pd.Timestamp("2025-12-31")

random.seed(42)


# ============================================================
# LOAD ACCOUNTS
# ============================================================

accounts = pd.read_csv(
    "data/raw/accounts.csv"
)

accounts["account_open_date"] = pd.to_datetime(
    accounts["account_open_date"]
)

accounts["balance"] = pd.to_numeric(
    accounts["balance"]
)

print("Accounts loaded:", len(accounts))


# ============================================================
# INITIAL BALANCE
# ============================================================

# We treat the existing balance as the starting balance
# for transaction generation.

accounts["starting_balance"] = accounts["balance"]

# This will be updated as transactions are generated.
accounts["current_balance"] = accounts["balance"]


# ============================================================
# GENERATE TRANSACTIONS
# ============================================================

transactions = []

transaction_id = 1

for _ in range(NUM_TRANSACTIONS):

    # --------------------------------------------------------
    # Select an account
    # --------------------------------------------------------

    account_index = random.randrange(len(accounts))

    account = accounts.iloc[account_index]

    account_id = account["account_id"]

    opening_date = account["account_open_date"]

    current_balance = accounts.at[
        account_index,
        "current_balance"
    ]


    # --------------------------------------------------------
    # VALID TRANSACTION DATE
    # --------------------------------------------------------

    earliest_date = max(
        opening_date,
        START_DATE
    )

    if earliest_date > END_DATE:
        continue

    days_available = (
        END_DATE - earliest_date
    ).days

    transaction_date = (
        earliest_date
        + timedelta(
            days=random.randint(
                0,
                days_available
            )
        )
    )


    # --------------------------------------------------------
    # TRANSACTION TYPE
    # --------------------------------------------------------

    transaction_type = random.choices(
        ["Deposit", "Withdrawal"],
        weights=[50, 50]
    )[0]


    # --------------------------------------------------------
    # TRANSACTION AMOUNT
    # --------------------------------------------------------

    if transaction_type == "Deposit":

        amount = round(
            random.uniform(
                500,
                100000
            ),
            2
        )

        new_balance = (
            current_balance + amount
        )

    else:

        # If balance is too low,
        # perform a deposit instead.

        if current_balance < 500:

            transaction_type = "Deposit"

            amount = round(
                random.uniform(
                    500,
                    100000
                ),
                2
            )

            new_balance = (
                current_balance + amount
            )

        else:

            # Never withdraw more than available balance.

            max_withdrawal = min(
                current_balance,
                100000
            )

            amount = round(
                random.uniform(
                    100,
                    max_withdrawal
                ),
                2
            )

            new_balance = (
                current_balance - amount
            )


    # --------------------------------------------------------
    # CHANNEL
    # --------------------------------------------------------

    channel = random.choice(
        [
            "ATM",
            "Branch",
            "Online",
            "UPI"
        ]
    )


    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    category = random.choice(
        [
            "Food",
            "Shopping",
            "Bills",
            "Investment",
            "Cash",
            "Other"
        ]
    )


    # --------------------------------------------------------
    # STORE TRANSACTION
    # --------------------------------------------------------

    transactions.append(
        {
            "transaction_id":
                f"T{transaction_id:08d}",

            "account_id":
                account_id,

            "transaction_date":
                transaction_date,

            "transaction_type":
                transaction_type,

            "amount":
                amount,

            "channel":
                channel,

            "category":
                category
        }
    )


    # --------------------------------------------------------
    # UPDATE BALANCE
    # --------------------------------------------------------

    accounts.at[
        account_index,
        "current_balance"
    ] = new_balance

    transaction_id += 1


# ============================================================
# CREATE DATAFRAME
# ============================================================

transactions = pd.DataFrame(
    transactions
)


# ============================================================
# SORT
# ============================================================

transactions = transactions.sort_values(
    [
        "account_id",
        "transaction_date"
    ]
).reset_index(drop=True)


# ============================================================
# VALIDATION
# ============================================================

print("\n================================")
print("TRANSACTION VALIDATION")
print("================================")

print(
    "\nTotal transactions:",
    len(transactions)
)


# ------------------------------------------------------------
# UNIQUE TRANSACTION IDs
# ------------------------------------------------------------

duplicate_ids = (
    transactions["transaction_id"]
    .duplicated()
    .sum()
)

print(
    "Duplicate transaction IDs:",
    duplicate_ids
)


# ------------------------------------------------------------
# MISSING VALUES
# ------------------------------------------------------------

missing_values = (
    transactions.isnull()
    .sum()
    .sum()
)

print(
    "Total missing values:",
    missing_values
)


# ------------------------------------------------------------
# VALID ACCOUNT IDs
# ------------------------------------------------------------

invalid_accounts = ~transactions[
    "account_id"
].isin(
    accounts["account_id"]
)

print(
    "Transactions with invalid account:",
    invalid_accounts.sum()
)


# ------------------------------------------------------------
# VALID DATE RANGE
# ------------------------------------------------------------

invalid_dates = (
    transactions["transaction_date"]
    < START_DATE
) | (
    transactions["transaction_date"]
    > END_DATE
)

print(
    "Transactions outside project date range:",
    invalid_dates.sum()
)


# ------------------------------------------------------------
# TRANSACTION TYPES
# ------------------------------------------------------------

print("\nTransaction types:")

print(
    transactions[
        "transaction_type"
    ].value_counts()
)


# ------------------------------------------------------------
# CHANNELS
# ------------------------------------------------------------

print("\nTransaction channels:")

print(
    transactions[
        "channel"
    ].value_counts()
)


# ------------------------------------------------------------
# AMOUNT STATISTICS
# ------------------------------------------------------------

print("\nAmount statistics:")

print(
    transactions[
        "amount"
    ].describe()
)


# ============================================================
# UPDATE ACCOUNT BALANCES
# ============================================================

accounts["balance"] = (
    accounts["current_balance"]
)

accounts = accounts.drop(
    columns=[
        "starting_balance",
        "current_balance"
    ]
)


# ============================================================
# SAVE FILES
# ============================================================

transactions.to_csv(
    "data/raw/transactions.csv",
    index=False
)

accounts.to_csv(
    "data/raw/accounts.csv",
    index=False
)


print(
    "\nTransactions saved successfully!"
)

print(
    "Accounts balances updated successfully!"
)