'''
🔹 Problem 4 — Merge / Join (very common)
🧩 Problem

You have:

transactions
    customer_id | txn_date | amount
customers
    customer_id | city
Task
    Join both tables
    Compute total amount per city
'''

import pandas as pd

txn_data = [
    [1, "2026-04-01", 100],
    [1, "2026-04-03", 250],
    [2, "2026-04-02", 300],
    [2, "2026-04-05", 120],
    [3, "2026-04-01", 500],
]

df_txn = pd.DataFrame(txn_data, columns=["customer_id", "txn_date", "amount"])
df_txn["txn_date"] = pd.to_datetime(df_txn["txn_date"])


cust_data = [
    [1, "Dallas"],
    [2, "Houston"],
    [3, "Austin"],
]

df_cust = pd.DataFrame(cust_data, columns=["customer_id", "city"])



#  merging
df = df_txn.merge(df_cust, on="customer_id", how="left")

print(df)

df = df.groupby("city")["amount"].sum().reset_index(name="total_amount")

print(df)
