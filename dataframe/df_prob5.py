'''
🔹 Problem 5 — Date grouping (very common)
🧩 Problem

Given:
    customer_id | txn_date | amount
Task
    Compute monthly total amount per customer
'''

import pandas as pd

txn_data = [
    [1, "2026-04-01", 100],
    [1, "2026-04-03", 250],
    [2, "2026-04-02", 300],
    [2, "2026-04-05", 120],
    [3, "2026-04-01", 500],
]

df = pd.DataFrame(txn_data, columns=["customer_id", "txn_date", "amount"])
df["txn_date"] = pd.to_datetime(df["txn_date"])
df["month"] = df["txn_date"].dt.month   # mixes different years (April 2025 vs April 2026)
df["month"] = df["txn_date"].dt.to_period("M")

print(df)

df = df.groupby(["customer_id","month"])["amount"].sum().reset_index(name="total_amount")

print(df)



