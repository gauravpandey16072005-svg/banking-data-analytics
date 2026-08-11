import pandas as pd
import random
from datetime import datetime, timedelta

# Number of customers
num_customers = 10000

# Lists used to generate realistic data
first_names = [
    "Rahul", "Priya", "Amit", "Neha", "Rohan",
    "Ananya", "Arjun", "Sneha", "Vikas", "Pooja"
]

last_names = [
    "Sharma", "Singh", "Kumar", "Gupta", "Verma",
    "Patel", "Mehta", "Joshi", "Agarwal", "Malhotra"
]

cities = [
    "Jaipur", "Delhi", "Mumbai", "Pune",
    "Bangalore", "Hyderabad", "Chennai",
    "Kolkata", "Ahmedabad", "Lucknow"
]

genders = ["Male", "Female"]

occupations = [
    "Engineer",
    "Teacher",
    "Doctor",
    "Business",
    "Analyst",
    "Student",
    "Government Employee",
    "Software Developer",
    "Accountant",
    "Designer"
]

# Generate customer data
customers = []

for i in range(1, num_customers + 1):

    customer_id = f"C{i:05d}"

    name = random.choice(first_names) + " " + random.choice(last_names)

    age = random.randint(18, 65)

    gender = random.choice(genders)

    city = random.choice(cities)

    occupation = random.choice(occupations)

    start_date = datetime(2015, 1, 1)
    end_date = datetime(2025, 12, 31)

    days_between = (end_date - start_date).days

    account_open_date = start_date + timedelta(
        days=random.randint(0, days_between)
    )

    customers.append({
        "customer_id": customer_id,
        "name": name,
        "age": age,
        "gender": gender,
        "city": city,
        "occupation": occupation,
        "account_open_date": account_open_date.date()
    })

# Convert list into DataFrame
customers = pd.DataFrame(customers)

# Display first 5 customers
print(customers.head())

# Display number of customers
print("\nTotal customers:", len(customers))

# Save as CSV
customers.to_csv(
    "data/raw/customers.csv",
    index=False
)

print("\nCustomers data saved successfully!")