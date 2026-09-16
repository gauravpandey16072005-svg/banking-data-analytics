import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LOAD DATA
# ============================================================

customers = pd.read_csv("data/cleaned/customers_cleaned.csv")
accounts = pd.read_csv("data/raw/accounts.csv")
transactions = pd.read_csv("data/raw/transactions.csv")
loans = pd.read_csv("data/raw/loans.csv")

print("=" * 60)
print("BANKING DATA - PYTHON EDA")
print("=" * 60)

# ============================================================
# 1. BASIC DATASET INFORMATION
# ============================================================

print("\nDATASET SIZES")
print("Customers:", len(customers))
print("Accounts:", len(accounts))
print("Transactions:", len(transactions))
print("Loans:", len(loans))

print("\nCUSTOMER COLUMNS")
print(customers.columns.tolist())

print("\nTRANSACTION COLUMNS")
print(transactions.columns.tolist())

# ============================================================
# 2. CUSTOMER ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMER ANALYSIS")
print("=" * 60)

print("\nCustomers by gender:")
print(customers["gender"].value_counts())

print("\nTop 10 cities by customers:")
print(customers["city"].value_counts().head(10))

# ============================================================
# 3. ACCOUNT ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("ACCOUNT ANALYSIS")
print("=" * 60)

print("\nAccounts by type:")
print(accounts["account_type"].value_counts())

print("\nAccounts by status:")
print(accounts["account_status"].value_counts())

print("\nAccount balance statistics:")
print(accounts["balance"].describe())

# ============================================================
# 4. TRANSACTION ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("TRANSACTION ANALYSIS")
print("=" * 60)

print("\nTransaction type:")
print(transactions["transaction_type"].value_counts())

print("\nTransaction channel:")
print(transactions["channel"].value_counts())

print("\nTransaction amount statistics:")
print(transactions["amount"].describe())

# ============================================================
# 5. TRANSACTION TYPE ANALYSIS
# ============================================================

transaction_summary = (
    transactions
    .groupby("transaction_type")["amount"]
    .agg(["count", "sum", "mean"])
)

print("\nTransaction summary:")
print(transaction_summary)

# ============================================================
# 6. MONTHLY TRANSACTION TREND
# ============================================================

transactions["transaction_date"] = pd.to_datetime(
    transactions["transaction_date"]
)

transactions["month"] = transactions["transaction_date"].dt.to_period("M")

monthly_transactions = (
    transactions
    .groupby("month")["amount"]
    .sum()
)

print("\nMonthly transaction value:")
print(monthly_transactions)

plt.figure(figsize=(10, 5))
monthly_transactions.plot(kind="line")
plt.title("Monthly Transaction Value Trend")
plt.xlabel("Month")
plt.ylabel("Total Transaction Value")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_transaction_trend.png")
plt.show()

# ============================================================
# 7. TRANSACTION CHANNEL ANALYSIS
# ============================================================

channel_summary = (
    transactions
    .groupby("channel")["amount"]
    .agg(["count", "sum", "mean"])
    .sort_values("sum", ascending=False)
)

print("\nChannel summary:")
print(channel_summary)

plt.figure(figsize=(8, 5))
channel_summary["sum"].plot(kind="bar")
plt.title("Transaction Value by Channel")
plt.xlabel("Channel")
plt.ylabel("Total Transaction Value")
plt.tight_layout()
plt.savefig("transaction_channel.png")
plt.show()

# ============================================================
# 8. BASIC OUTLIER ANALYSIS
# ============================================================

Q1 = transactions["amount"].quantile(0.25)
Q3 = transactions["amount"].quantile(0.75)

IQR = Q3 - Q1

lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

outliers = transactions[
    (transactions["amount"] < lower_limit) |
    (transactions["amount"] > upper_limit)
]

print("\n" + "=" * 60)
print("OUTLIER ANALYSIS")
print("=" * 60)

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower limit:", lower_limit)
print("Upper limit:", upper_limit)
print("Potential outliers:", len(outliers))

# ============================================================
# 9. LOAN ANALYSIS
# ============================================================

print("\n" + "=" * 60)
print("LOAN ANALYSIS")
print("=" * 60)

print("\nLoan types:")
print(loans["loan_type"].value_counts())

print("\nLoan status:")
print(loans["loan_status"].value_counts())

print("\nLoan amount statistics:")
print(loans["loan_amount"].describe())

# ============================================================
# 10. NUMPY STATISTICS
# ============================================================

print("\n" + "=" * 60)
print("BASIC STATISTICS")
print("=" * 60)

amounts = transactions["amount"]

print("Mean transaction:", np.mean(amounts))
print("Median transaction:", np.median(amounts))
print("Standard deviation:", np.std(amounts))
print("Minimum transaction:", np.min(amounts))
print("Maximum transaction:", np.max(amounts))

print("\nEDA COMPLETED")

# ============================================================
# BUSINESS KPIs
# ============================================================

print("\n" + "=" * 60)
print("BANKING BUSINESS KPIs")
print("=" * 60)

total_customers = len(customers)
total_accounts = len(accounts)
total_transactions = len(transactions)
total_loans = len(loans)

total_balance = accounts["balance"].sum()
average_balance = accounts["balance"].mean()

total_transaction_value = transactions["amount"].sum()
average_transaction_value = transactions["amount"].mean()

deposit_value = transactions.loc[
    transactions["transaction_type"] == "Deposit", "amount"
].sum()

withdrawal_value = transactions.loc[
    transactions["transaction_type"] == "Withdrawal", "amount"
].sum()

total_loan_value = loans["loan_amount"].sum()
average_loan_amount = loans["loan_amount"].mean()

defaulted_loans = (loans["loan_status"] == "Defaulted").sum()
default_rate = defaulted_loans / total_loans * 100

print("Total customers:", total_customers)
print("Total accounts:", total_accounts)
print("Total transactions:", total_transactions)
print("Total loans:", total_loans)

print("Total account balance:", total_balance)
print("Average account balance:", average_balance)

print("Total transaction value:", total_transaction_value)
print("Average transaction value:", average_transaction_value)

print("Deposit value:", deposit_value)
print("Withdrawal value:", withdrawal_value)

print("Total loan value:", total_loan_value)
print("Average loan amount:", average_loan_amount)

print("Defaulted loans:", defaulted_loans)
print("Loan default rate:", default_rate)

print("\nBUSINESS KPI ANALYSIS COMPLETED")

# ============================================================
# BUSINESS KPIs
# ============================================================

print("\n" + "=" * 60)
print("BANKING BUSINESS KPIs")
print("=" * 60)

total_customers = len(customers)
total_accounts = len(accounts)
total_transactions = len(transactions)
total_loans = len(loans)

total_balance = accounts["balance"].sum()
average_balance = accounts["balance"].mean()

total_transaction_value = transactions["amount"].sum()
average_transaction_value = transactions["amount"].mean()

deposit_value = transactions.loc[
    transactions["transaction_type"] == "Deposit", "amount"
].sum()

withdrawal_value = transactions.loc[
    transactions["transaction_type"] == "Withdrawal", "amount"
].sum()

total_loan_value = loans["loan_amount"].sum()
average_loan_amount = loans["loan_amount"].mean()

defaulted_loans = (loans["loan_status"] == "Defaulted").sum()
default_rate = defaulted_loans / total_loans * 100

print("Total customers:", total_customers)
print("Total accounts:", total_accounts)
print("Total transactions:", total_transactions)
print("Total loans:", total_loans)

print("Total account balance:", total_balance)
print("Average account balance:", average_balance)

print("Total transaction value:", total_transaction_value)
print("Average transaction value:", average_transaction_value)

print("Deposit value:", deposit_value)
print("Withdrawal value:", withdrawal_value)

print("Total loan value:", total_loan_value)
print("Average loan amount:", average_loan_amount)

print("Defaulted loans:", defaulted_loans)
print("Loan default rate:", default_rate)

print("\nBUSINESS KPI ANALYSIS COMPLETED")

# ============================================================
# BUSINESS KPIs
# ============================================================

print("\n" + "=" * 60)
print("BANKING BUSINESS KPIs")
print("=" * 60)

total_customers = len(customers)
total_accounts = len(accounts)
total_transactions = len(transactions)
total_loans = len(loans)

total_balance = accounts["balance"].sum()
average_balance = accounts["balance"].mean()

total_transaction_value = transactions["amount"].sum()
average_transaction_value = transactions["amount"].mean()

deposit_value = transactions.loc[
    transactions["transaction_type"] == "Deposit", "amount"
].sum()

withdrawal_value = transactions.loc[
    transactions["transaction_type"] == "Withdrawal", "amount"
].sum()

total_loan_value = loans["loan_amount"].sum()
average_loan_amount = loans["loan_amount"].mean()

defaulted_loans = (loans["loan_status"] == "Defaulted").sum()
default_rate = defaulted_loans / total_loans * 100

print("Total customers:", total_customers)
print("Total accounts:", total_accounts)
print("Total transactions:", total_transactions)
print("Total loans:", total_loans)

print("Total account balance:", total_balance)
print("Average account balance:", average_balance)

print("Total transaction value:", total_transaction_value)
print("Average transaction value:", average_transaction_value)

print("Deposit value:", deposit_value)
print("Withdrawal value:", withdrawal_value)

print("Total loan value:", total_loan_value)
print("Average loan amount:", average_loan_amount)

print("Defaulted loans:", defaulted_loans)
print("Loan default rate:", default_rate)

print("\nBUSINESS KPI ANALYSIS COMPLETED")
