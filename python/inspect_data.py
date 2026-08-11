import pandas as pd

# Load the CSV file
customers = pd.read_csv("data/raw/customers.csv")

print("FIRST 5 ROWS")
print(customers.head())

print("\nSHAPE")
print(customers.shape)

print("\nCOLUMN NAMES")
print(customers.columns)

print("\nDATA INFORMATION")
customers.info()

print("\nSTATISTICAL SUMMARY")
print(customers.describe())