import pandas as pd
import random
from datetime import timedelta

# --------------------------------------------------
# 1. Load cleaned customer data
# --------------------------------------------------

customers = pd.read_csv(
    "data/cleaned/customers_cleaned.csv",
    parse_dates=["account_open_date"]
)

# --------------------------------------------------
# 2. Set random seed
# --------------------------------------------------

random.seed(42)

# --------------------------------------------------
# 3. Possible values
# --------------------------------------------------

account_types = ["Savings", "Current"]

account_statuses = [
    "Active",
    "Active",
    "Active",
    "Dormant",
    "Closed"
]

# --------------------------------------------------
# 4. Generate accounts
# --------------------------------------------------

accounts = []

account_number = 1

for _, customer in customers.iterrows():

    customer_id = customer["customer_id"]
    customer_open_date = customer["account_open_date"]

    # Each customer gets 1 to 3 accounts
    number_of_accounts = random.randint(1, 3)

    for _ in range(number_of_accounts):

        account_id = f"A{account_number:06d}"

        account_type = random.choice(account_types)

        balance = round(
            random.uniform(1000, 500000),
            2
        )

        account_status = random.choice(account_statuses)

        # Account cannot be opened before customer's
        # main account/customer relationship date.
        account_open_date = customer_open_date + timedelta(
            days=random.randint(0, 365)
        )

        accounts.append({
            "account_id": account_id,
            "customer_id": customer_id,
            "account_type": account_type,
            "balance": balance,
            "account_status": account_status,
            "account_open_date": account_open_date
        })

        account_number += 1


# --------------------------------------------------
# 5. Convert list to DataFrame
# --------------------------------------------------

accounts_df = pd.DataFrame(accounts)

# --------------------------------------------------
# 6. Display sample
# --------------------------------------------------

print("\nFIRST 10 ACCOUNTS")
print(accounts_df.head(10))

print("\nSHAPE")
print(accounts_df.shape)

print("\nACCOUNTS PER CUSTOMER")
print(
    accounts_df["customer_id"]
    .value_counts()
    .value_counts()
    .sort_index()
)

# --------------------------------------------------
# 7. Save data
# --------------------------------------------------

accounts_df.to_csv(
    "data/raw/accounts.csv",
    index=False
)

print("\nAccounts data saved successfully!")