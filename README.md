# 💰 Personal Expense Tracker

A command-line tool that reads a CSV of personal expenses, prints a categorised summary in the terminal, and saves a bar chart as a PNG.

Built with Python as a first data project — practising CSV handling, data analysis with pandas, and visualisation with matplotlib.

---

## What it does

- Reads `expenses.csv` (date, category, amount, description)
- Calculates total spent and breakdown by category
- Identifies the biggest single expense
- Prints a formatted summary with mini bar chart in the terminal
- Saves a clean PNG chart of spending by category

## Example output

```
============================================
       EXPENSE SUMMARY
============================================
  Period    : 03/01/2025 → 30/01/2025
  Entries   : 15
  Total     : R$ 593.10
--------------------------------------------
  BY CATEGORY
--------------------------------------------
  Food           R$  208.80  35.2%  ███████
  Health         R$  205.00  34.6%  ██████
  Entertainment  R$   74.90  12.6%  ██
  Transport      R$   54.50   9.2%  █
  Education      R$   49.90   8.4%  █
--------------------------------------------
  Biggest expense:
  R$ 120.00 — Dentist (25/01/2025)
============================================
```

## Setup

1. Clone the repo
```bash
git clone https://github.com/your-username/expense-tracker.git
cd expense-tracker
```

2. Install dependencies
```bash
pip install pandas matplotlib
```

3. Run
```bash
python tracker.py
```

## CSV format

Edit `expenses.csv` with your own data. The expected columns are:

| Column | Format | Example |
|---|---|---|
| date | YYYY-MM-DD | 2025-01-15 |
| category | text | Food |
| amount | number | 48.90 |
| description | text | Supermarket |

## Tech used

- Python 3
- pandas — data loading and aggregation
- matplotlib — chart generation

---

*First Python project — feedback welcome.*
