import pandas as pd

# 1. Load raw data
customers = pd.read_csv("data/raw/customers.csv")

print("Original data shape:")
print(customers.shape)


# 2. Check missing values
print("\nMissing values:")
print(customers.isnull().sum())


# 3. Check duplicate rows
print("\nDuplicate rows:")
print(customers.duplicated().sum())


# 4. Convert date column to datetime
customers["account_open_date"] = pd.to_datetime(
    customers["account_open_date"]
)


# 5. Check data types after conversion
print("\nData types after cleaning:")
print(customers.dtypes)


# 6. Save cleaned data
customers.to_csv(
    "data/cleaned/customers_cleaned.csv",
    index=False
)

print("\nCleaned data saved successfully!")