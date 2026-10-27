-- Banking Customer & Transaction Analytics (MySQL 8+)
-- Import the CSV files into tables named customers, accounts, transactions, loans.
-- Use matching column names from the README. Amounts are synthetic INR values.

-- 1. Dataset coverage
SELECT 'customers' AS entity, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'accounts', COUNT(*) FROM accounts
UNION ALL SELECT 'transactions', COUNT(*) FROM transactions
UNION ALL SELECT 'loans', COUNT(*) FROM loans;

-- 2. Account portfolio and status
SELECT account_type, account_status, COUNT(*) AS accounts,
       ROUND(SUM(balance), 2) AS total_balance,
       ROUND(AVG(balance), 2) AS average_balance
FROM accounts
GROUP BY account_type, account_status
ORDER BY total_balance DESC;

-- 3. Deposit and withdrawal KPIs
SELECT transaction_type, COUNT(*) AS transaction_count,
       ROUND(SUM(amount), 2) AS total_value,
       ROUND(AVG(amount), 2) AS average_value
FROM transactions
GROUP BY transaction_type
ORDER BY total_value DESC;

-- 4. Monthly transaction trend
SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS transaction_month,
       COUNT(*) AS transaction_count,
       ROUND(SUM(amount), 2) AS total_value
FROM transactions
GROUP BY DATE_FORMAT(transaction_date, '%Y-%m')
ORDER BY transaction_month;

-- 5. Channel performance
SELECT channel, COUNT(*) AS transaction_count,
       ROUND(SUM(amount), 2) AS total_value,
       ROUND(AVG(amount), 2) AS average_value
FROM transactions
GROUP BY channel
ORDER BY total_value DESC;

-- 6. Top customers by total account balance
SELECT c.customer_id, c.name, c.city,
       COUNT(a.account_id) AS account_count,
       ROUND(SUM(a.balance), 2) AS total_balance
FROM customers c
JOIN accounts a ON a.customer_id = c.customer_id
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_balance DESC
LIMIT 10;

-- 7. High-activity customers (transaction count and value)
SELECT a.customer_id, COUNT(t.transaction_id) AS transaction_count,
       ROUND(SUM(t.amount), 2) AS total_transaction_value
FROM accounts a
JOIN transactions t ON t.account_id = a.account_id
GROUP BY a.customer_id
ORDER BY transaction_count DESC
LIMIT 10;

-- 8. Loan portfolio by type and status
SELECT loan_type, loan_status, COUNT(*) AS loan_count,
       ROUND(SUM(loan_amount), 2) AS total_loan_value,
       ROUND(AVG(loan_amount), 2) AS average_loan_value
FROM loans
GROUP BY loan_type, loan_status
ORDER BY total_loan_value DESC;

-- 9. Default rate (loan-level, not customer-level)
SELECT COUNT(*) AS total_loans,
       SUM(loan_status = 'Defaulted') AS defaulted_loans,
       ROUND(100.0 * SUM(loan_status = 'Defaulted') / NULLIF(COUNT(*), 0), 2) AS default_rate_pct
FROM loans;

-- 10. Customers with loans above the portfolio average
SELECT l.loan_id, l.customer_id, l.loan_type, l.loan_amount, l.loan_status
FROM loans l
WHERE l.loan_amount > (SELECT AVG(loan_amount) FROM loans)
ORDER BY l.loan_amount DESC;

-- 11. Referential-integrity checks: each query should return zero
SELECT COUNT(*) AS transactions_without_account
FROM transactions t LEFT JOIN accounts a ON a.account_id = t.account_id
WHERE a.account_id IS NULL;

SELECT COUNT(*) AS loans_without_customer
FROM loans l LEFT JOIN customers c ON c.customer_id = l.customer_id
WHERE c.customer_id IS NULL;
