import pandas as pd
import numpy as np
from pathlib import Path


# --------------------------------------------------
# 1. LOAD EXISTING DATA
# --------------------------------------------------

customers = pd.read_csv("data/raw/customers.csv")
accounts = pd.read_csv("data/raw/accounts.csv")

print(f"Customers loaded: {len(customers)}")
print(f"Accounts loaded: {len(accounts)}")


# --------------------------------------------------
# 2. SET RANDOM SEED
# --------------------------------------------------

np.random.seed(42)


# --------------------------------------------------
# 3. SELECT ELIGIBLE ACCOUNTS
# --------------------------------------------------

# Only active accounts can receive new loans
eligible_accounts = accounts[
    accounts["account_status"] == "Active"
].copy()

print(f"Eligible active accounts: {len(eligible_accounts)}")


# --------------------------------------------------
# 4. NUMBER OF LOANS
# --------------------------------------------------

# Around 40% of eligible accounts will have a loan
num_loans = int(len(eligible_accounts) * 0.40)

selected_accounts = eligible_accounts.sample(
    n=num_loans,
    random_state=42
).reset_index(drop=True)


# --------------------------------------------------
# 5. GENERATE LOAN IDs
# --------------------------------------------------

loan_ids = [
    f"L{str(i).zfill(7)}"
    for i in range(1, num_loans + 1)
]


# --------------------------------------------------
# 6. LOAN TYPES
# --------------------------------------------------

loan_types = [
    "Personal",
    "Home",
    "Education",
    "Vehicle",
    "Business"
]

loan_type = np.random.choice(
    loan_types,
    size=num_loans,
    p=[0.35, 0.20, 0.15, 0.20, 0.10]
)


# --------------------------------------------------
# 7. LOAN AMOUNTS
# --------------------------------------------------

loan_amount = np.random.randint(
    50000,
    5000000,
    size=num_loans
).astype(float)

loan_amount = np.round(loan_amount, 2)


# --------------------------------------------------
# 8. INTEREST RATES
# --------------------------------------------------

interest_rate = np.round(
    np.random.uniform(7.0, 16.0, size=num_loans),
    2
)


# --------------------------------------------------
# 9. LOAN TERM
# --------------------------------------------------

loan_terms = [
    12,
    24,
    36,
    48,
    60,
    84,
    120,
    180,
    240
]

loan_term_months = np.random.choice(
    loan_terms,
    size=num_loans
)


# --------------------------------------------------
# 10. LOAN START DATE
# --------------------------------------------------

start_date = pd.Timestamp("2020-01-01")
end_date = pd.Timestamp("2025-12-31")

loan_start_date = pd.to_datetime(
    np.random.randint(
        start_date.value // 10**9,
        end_date.value // 10**9,
        size=num_loans
    ),
    unit="s"
)


# --------------------------------------------------
# 11. LOAN END DATE
# --------------------------------------------------

loan_end_date = (
    loan_start_date
    + pd.to_timedelta(loan_term_months * 30, unit="D")
)


# --------------------------------------------------
# 12. LOAN STATUS
# --------------------------------------------------

loan_status = np.random.choice(
    [
        "Active",
        "Closed",
        "Defaulted"
    ],
    size=num_loans,
    p=[0.65, 0.30, 0.05]
)


# --------------------------------------------------
# 13. MONTHLY PAYMENT
# --------------------------------------------------

monthly_rate = interest_rate / 100 / 12

monthly_payment = (
    loan_amount * monthly_rate *
    (1 + monthly_rate) ** loan_term_months
) / (
    (1 + monthly_rate) ** loan_term_months - 1
)

monthly_payment = np.round(monthly_payment, 2)


# --------------------------------------------------
# 14. CREATE LOAN DATAFRAME
# --------------------------------------------------

loans = pd.DataFrame({
    "loan_id": loan_ids,
    "customer_id": selected_accounts["customer_id"],
    "account_id": selected_accounts["account_id"],
    "loan_type": loan_type,
    "loan_amount": loan_amount,
    "interest_rate": interest_rate,
    "loan_term_months": loan_term_months,
    "loan_start_date": loan_start_date,
    "loan_end_date": loan_end_date,
    "loan_status": loan_status,
    "monthly_payment": monthly_payment
})


# --------------------------------------------------
# 15. VALIDATION
# --------------------------------------------------

print("\n" + "=" * 40)
print("LOAN DATA VALIDATION")
print("=" * 40)

print(f"\nTotal loans: {len(loans)}")

print(
    f"Duplicate loan IDs: "
    f"{loans['loan_id'].duplicated().sum()}"
)

print(
    f"Missing values: "
    f"{loans.isnull().sum().sum()}"
)

print(

    f"Invalid customer IDs: "
    f"{(~loans['customer_id'].isin(customers['customer_id'])).sum()}"
)

print(
    f"Invalid account IDs: "
    f"{(~loans['account_id'].isin(accounts['account_id'])).sum()}"
)


print("\nLoan types:")
print(loans["loan_type"].value_counts())

print("\nLoan statuses:")
print(loans["loan_status"].value_counts())

print("\nLoan amount statistics:")
print(loans["loan_amount"].describe())


# --------------------------------------------------
# 16. SAVE DATA
# --------------------------------------------------

output_path = Path("data/raw/loans.csv")

loans.to_csv(output_path, index=False)

print("\nLoans data saved successfully!")


# --------------------------------------------------
# 17. DISPLAY SAMPLE
# --------------------------------------------------

print("\nFIRST 10 LOANS")
print(loans.head(10).to_string(index=False))