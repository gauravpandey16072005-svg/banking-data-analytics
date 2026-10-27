# Banking Customer & Transaction Analytics

An end-to-end portfolio project using synthetic banking data to demonstrate data quality checks, exploratory analysis, MySQL business queries, baseline loan-default classification, and a Tableau dashboard build plan.

> **Data note:** All data is synthetic and the results are not actual bank performance. In the generator, loan statuses are randomly assigned; the model is a workflow demonstration, not a valid credit-risk model.

## Dataset

| Dataset | Rows (expected) | Main use |
|---|---:|---|
| Customers | 10,000 | Customer demographics and segmentation |
| Accounts | 20,012 | Balances, account types and status |
| Transactions | 383,242 | Transaction behavior, channels and trends |
| Loans | 4,789 | Loan portfolio and default-status exploration |

CSV files are in `data/raw/`. A cleaned customer file is in `data/cleaned/`. Treat row counts as the expected project dataset sizes; verify them after regenerating or replacing data.

## What is included

- **Data preparation:** generators for customers, accounts, transactions and loans.
- **Cleaning and validation:** `python/clean_data.py` and `python/validate_data.py`.
- **EDA and charts:** `python/eda.py`; existing PNG charts are included.
- **Loan-default baseline:** `python/loan_default_model.py` trains Logistic Regression, uses a stratified train/test split and preprocessing pipeline, and reports accuracy, precision, recall, F1, ROC-AUC and a confusion matrix.
- **MySQL analysis:** `sql/banking_analysis.sql` includes joins, aggregation, date trends, KPI queries, subqueries and referential-integrity checks.
- **Tableau:** `docs/TABLEAU_DASHBOARD_GUIDE.md` gives a reproducible dashboard plan. A Tableau workbook is not currently included; create and validate it in Tableau before claiming a completed workbook.

## Repository structure

```text
banking-data-analytics/
├── data/
│   ├── raw/                 # customers, accounts, transactions, loans
│   └── cleaned/             # cleaned customer data
├── docs/
│   └── TABLEAU_DASHBOARD_GUIDE.md
├── outputs/                 # model metrics/predictions generated at runtime
├── python/
│   ├── clean_data.py
│   ├── eda.py
│   ├── generate_data.py
│   ├── generate_accounts.py
│   ├── generate_transactions.py
│   ├── generate_loans.py
│   ├── inspect_data.py
│   ├── validate_data.py
│   └── loan_default_model.py
├── sql/
│   └── banking_analysis.sql
├── monthly_transaction_trend.png
├── transaction_channel.png
├── requirements.txt
└── README.md
```

## Setup (macOS/Linux)

Run commands from the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run the analysis

```bash
python python/clean_data.py
python python/validate_data.py
python python/eda.py
python python/loan_default_model.py
```

The model script writes a fitted model, test predictions, and evaluation metrics under `outputs/`. It requires `data/raw/loans.csv`; customer age is included only when a compatible customer file is available.

## MySQL analysis

1. Create a database, for example `banking_analytics`.
2. Import each CSV into a table with its matching column names: `customers`, `accounts`, `transactions`, and `loans`.
3. Open `sql/banking_analysis.sql` and run queries in MySQL Workbench or the MySQL client.
4. Compare query results with Python EDA results. The SQL file assumes MySQL 8+ and the column names documented in the project.

## Tableau dashboard

Follow `docs/TABLEAU_DASHBOARD_GUIDE.md` to build a Banking Portfolio Overview with KPI cards, monthly transaction trends, channel analysis, account status, loan portfolio and top customers. Validate the workbook's totals against SQL before publishing. The guide is not a substitute for a finished Tableau workbook.

## Model limitations

The target is `loan_status == 'Defaulted'`. The synthetic generator assigns loan statuses randomly, independently of the loan features. Consequently, predictive metrics should **not** be presented as evidence of real credit-risk performance. A meaningful model requires realistic historical outcomes and features available before the default event, plus careful leakage checks and time-based validation.

## Next improvements

- Add unit tests and a repeatable automated validation command.
- Replace random loan labels with a realistic, documented synthetic risk process or an appropriately licensed real dataset.
- Build and commit a validated Tableau workbook.
- Add a database schema/import script and automated SQL-vs-Python KPI reconciliation.

## Author

Anand Pandey · B.Tech, Electronics & Communication Engineering · MNIT Jaipur
