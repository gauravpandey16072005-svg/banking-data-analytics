# Tableau Dashboard Build Guide

This repository does **not** currently contain a Tableau workbook (.twb/.twbx). Use this guide to build a real dashboard from the project's CSVs.

## Connect data
1. Open Tableau Desktop/Public and connect to Text File.
2. Import `data/raw/customers.csv`, `accounts.csv`, `transactions.csv`, and `loans.csv`.
3. Relate tables using the keys documented in README: customers.customer_id → accounts.customer_id; accounts.account_id → transactions.account_id; customers.customer_id → loans.customer_id; accounts.account_id → loans.account_id.
4. Check that date columns are Date and amount/balance fields are numeric. Avoid joining transactions directly to loans in a single physical join because it can multiply rows.

## Suggested dashboard: Banking Portfolio Overview
Create KPI cards for customer count, account count, transaction count, total deposits, total withdrawals, total account balance, loan portfolio value, and loan default rate.

Suggested sheets:
- Monthly Transaction Value: MONTH(transaction_date) vs SUM(amount), line chart.
- Transactions by Channel: channel vs SUM(amount), bar chart.
- Deposit vs Withdrawal: transaction_type vs SUM(amount).
- Loan Portfolio: loan_type vs SUM(loan_amount), stacked by loan_status.
- Account Status: account_status vs COUNT(account_id).
- Top 10 Customers: customer name vs SUM(balance), sorted descending.

Add filters for transaction date, channel, transaction type, city, account type, and loan status where applicable. Validate KPI totals against the SQL queries before publishing.

## Important
The repository contains synthetic data. Label the dashboard accordingly. Save your finished workbook as `tableau/banking_analytics.twbx` only after you create it in Tableau; this guide is not itself a Tableau workbook.
