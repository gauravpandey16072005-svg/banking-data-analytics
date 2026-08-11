import pandas as pd

# ============================================================
# LOAD DATA
# ============================================================

customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
accounts = pd.read_csv("data/raw/accounts.csv")
transactions = pd.read_csv("data/raw/transactions.csv")
loans = pd.read_csv("data/raw/loans.csv")


# ============================================================
# BASIC INFORMATION
# ============================================================

print("=" * 60)
print("BANKING DATA QUALITY VALIDATION")
print("=" * 60)

print("\nDATASET SIZES")
print("-" * 60)

print(f"Customers     : {len(customers)}")
print(f"Accounts      : {len(accounts)}")
print(f"Transactions  : {len(transactions)}")
print(f"Loans         : {len(loans)}")


# ============================================================
# DUPLICATE ID VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE ID VALIDATION")
print("=" * 60)

duplicate_customer_ids = customers["customer_id"].duplicated().sum()
duplicate_account_ids = accounts["account_id"].duplicated().sum()
duplicate_transaction_ids = transactions["transaction_id"].duplicated().sum()
duplicate_loan_ids = loans["loan_id"].duplicated().sum()

print(f"Duplicate customer IDs     : {duplicate_customer_ids}")
print(f"Duplicate account IDs      : {duplicate_account_ids}")
print(f"Duplicate transaction IDs  : {duplicate_transaction_ids}")
print(f"Duplicate loan IDs         : {duplicate_loan_ids}")


# ============================================================
# MISSING VALUE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUE VALIDATION")
print("=" * 60)

customer_missing = customers.isnull().sum().sum()
account_missing = accounts.isnull().sum().sum()
transaction_missing = transactions.isnull().sum().sum()
loan_missing = loans.isnull().sum().sum()

print(f"Customer missing values     : {customer_missing}")
print(f"Account missing values      : {account_missing}")
print(f"Transaction missing values  : {transaction_missing}")
print(f"Loan missing values         : {loan_missing}")

print("\nMissing values by dataset:")
print("-" * 60)

print("\nCustomers:")
print(customers.isnull().sum())

print("\nAccounts:")
print(accounts.isnull().sum())

print("\nTransactions:")
print(transactions.isnull().sum())

print("\nLoans:")
print(loans.isnull().sum())


# ============================================================
# REFERENTIAL INTEGRITY VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("REFERENTIAL INTEGRITY VALIDATION")
print("=" * 60)

# Transactions should reference existing accounts
invalid_transaction_accounts = (
    ~transactions["account_id"].isin(accounts["account_id"])
).sum()

# Loans should reference existing customers
invalid_loan_customers = (
    ~loans["customer_id"].isin(customers["customer_id"])
).sum()

# Loans should reference existing accounts
invalid_loan_accounts = (
    ~loans["account_id"].isin(accounts["account_id"])
).sum()

print(
    f"Transactions with invalid account IDs : "
    f"{invalid_transaction_accounts}"
)

print(
    f"Loans with invalid customer IDs       : "
    f"{invalid_loan_customers}"
)

print(
    f"Loans with invalid account IDs        : "
    f"{invalid_loan_accounts}"
)


# ============================================================
# ACCOUNT DATA VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("ACCOUNT DATA VALIDATION")
print("=" * 60)

# IMPORTANT:
# Active, Closed and Dormant are all valid statuses
valid_account_statuses = [
    "Active",
    "Closed",
    "Dormant"
]

invalid_account_statuses = (
    ~accounts["account_status"].isin(valid_account_statuses)
).sum()

# Valid account types
valid_account_types = [
    "Savings",
    "Current"
]

invalid_account_types = (
    ~accounts["account_type"].isin(valid_account_types)
).sum()

# Account balance should not be negative
negative_balances = (
    accounts["balance"] < 0
).sum()

print(f"Invalid account statuses : {invalid_account_statuses}")
print(f"Invalid account types    : {invalid_account_types}")
print(f"Negative balances        : {negative_balances}")


# ============================================================
# TRANSACTION DATA VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION DATA VALIDATION")
print("=" * 60)

# Valid transaction types
valid_transaction_types = [
    "Deposit",
    "Withdrawal"
]

invalid_transaction_types = (
    ~transactions["transaction_type"].isin(valid_transaction_types)
).sum()

# Valid transaction channels
valid_transaction_channels = [
    "ATM",
    "Online",
    "Branch",
    "UPI"
]

invalid_transaction_channels = (
    ~transactions["channel"].isin(valid_transaction_channels)
).sum()

# Transaction amount should not be negative
negative_transaction_amounts = (
    transactions["amount"] < 0
).sum()

print(f"Invalid transaction types    : {invalid_transaction_types}")
print(f"Invalid transaction channels : {invalid_transaction_channels}")
print(f"Negative transaction amounts : {negative_transaction_amounts}")


# ============================================================
# LOAN DATA VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("LOAN DATA VALIDATION")
print("=" * 60)

# Valid loan types
valid_loan_types = [
    "Personal",
    "Vehicle",
    "Home",
    "Education",
    "Business"
]

invalid_loan_types = (
    ~loans["loan_type"].isin(valid_loan_types)
).sum()

# Valid loan statuses
valid_loan_statuses = [
    "Active",
    "Closed",
    "Defaulted"
]

invalid_loan_statuses = (
    ~loans["loan_status"].isin(valid_loan_statuses)
).sum()

# Loan amount should be positive
invalid_loan_amounts = (
    loans["loan_amount"] <= 0
).sum()

# Interest rate should be positive
invalid_interest_rates = (
    loans["interest_rate"] <= 0
).sum()

# Loan term should be positive
invalid_loan_terms = (
    loans["loan_term_months"] <= 0
).sum()

print(f"Invalid loan types       : {invalid_loan_types}")
print(f"Invalid loan statuses    : {invalid_loan_statuses}")
print(f"Invalid loan amounts     : {invalid_loan_amounts}")
print(f"Invalid interest rates   : {invalid_interest_rates}")
print(f"Invalid loan terms       : {invalid_loan_terms}")


# ============================================================
# DATE VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("DATE VALIDATION")
print("=" * 60)

# Convert dates to datetime
accounts["account_open_date"] = pd.to_datetime(
    accounts["account_open_date"],
    errors="coerce"
)

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"],
    errors="coerce"
)

loans["loan_start_date"] = pd.to_datetime(
    loans["loan_start_date"],
    errors="coerce"
)

loans["loan_end_date"] = pd.to_datetime(
    loans["loan_end_date"],
    errors="coerce"
)

# Count dates that failed conversion
invalid_account_dates = (
    accounts["account_open_date"].isna()
).sum()

invalid_transaction_dates = (
    transactions["transaction_date"].isna()
).sum()

invalid_loan_start_dates = (
    loans["loan_start_date"].isna()
).sum()

invalid_loan_end_dates = (
    loans["loan_end_date"].isna()
).sum()

print(f"Invalid account dates     : {invalid_account_dates}")
print(f"Invalid transaction dates : {invalid_transaction_dates}")
print(f"Invalid loan start dates  : {invalid_loan_start_dates}")
print(f"Invalid loan end dates    : {invalid_loan_end_dates}")


# ============================================================
# LOAN DATE LOGIC VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("LOAN DATE LOGIC VALIDATION")
print("=" * 60)

# Loan end date should never be before loan start date

invalid_loan_date_logic = (
    loans["loan_end_date"] < loans["loan_start_date"]
).sum()

print(
    f"Loans where end date is before start date : "
    f"{invalid_loan_date_logic}"
)


# ============================================================
# TRANSACTION DATE RANGE
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION DATE RANGE")
print("=" * 60)

earliest_transaction = transactions["transaction_date"].min()
latest_transaction = transactions["transaction_date"].max()

print(f"Earliest transaction : {earliest_transaction}")
print(f"Latest transaction   : {latest_transaction}")


# ============================================================
# PROJECT DATE RANGE VALIDATION
# ============================================================

project_start_date = pd.Timestamp("2023-01-01")
project_end_date = pd.Timestamp("2025-12-31")

transactions_outside_project_range = (
    (transactions["transaction_date"] < project_start_date)
    |
    (transactions["transaction_date"] > project_end_date)
).sum()

print(
    f"\nTransactions outside project date range : "
    f"{transactions_outside_project_range}"
)


# ============================================================
# TRANSACTION AMOUNT STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION AMOUNT STATISTICS")
print("=" * 60)

print(transactions["amount"].describe())


# ============================================================
# ACCOUNT STATUS DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("ACCOUNT STATUS DISTRIBUTION")
print("=" * 60)

print(accounts["account_status"].value_counts())


# ============================================================
# TRANSACTION TYPE DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION TYPE DISTRIBUTION")
print("=" * 60)

print(transactions["transaction_type"].value_counts())


# ============================================================
# TRANSACTION CHANNEL DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION CHANNEL DISTRIBUTION")
print("=" * 60)

print(transactions["channel"].value_counts())


# ============================================================
# LOAN TYPE DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("LOAN TYPE DISTRIBUTION")
print("=" * 60)

print(loans["loan_type"].value_counts())


# ============================================================
# LOAN STATUS DISTRIBUTION
# ============================================================

print("\n" + "=" * 60)
print("LOAN STATUS DISTRIBUTION")
print("=" * 60)

print(loans["loan_status"].value_counts())


# ============================================================
# FINAL STATUS
# ============================================================

print("\n" + "=" * 60)
print("FINAL VALIDATION STATUS")
print("=" * 60)

total_issues = (
    duplicate_customer_ids
    + duplicate_account_ids
    + duplicate_transaction_ids
    + duplicate_loan_ids

    + customer_missing
    + account_missing
    + transaction_missing
    + loan_missing

    + invalid_transaction_accounts
    + invalid_loan_customers
    + invalid_loan_accounts

    + invalid_account_statuses
    + invalid_account_types
    + negative_balances

    + invalid_transaction_types
    + invalid_transaction_channels
    + negative_transaction_amounts

    + invalid_loan_types
    + invalid_loan_statuses
    + invalid_loan_amounts
    + invalid_interest_rates
    + invalid_loan_terms

    + invalid_account_dates
    + invalid_transaction_dates
    + invalid_loan_start_dates
    + invalid_loan_end_dates

    + invalid_loan_date_logic
    + transactions_outside_project_range
)

if total_issues == 0:
    print("STATUS : PASSED")
    print("All data quality checks passed successfully!")
else:
    print("STATUS : REVIEW REQUIRED")
    print(f"Total data quality issues detected : {total_issues}")