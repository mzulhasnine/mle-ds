'''
Quick Top-K / Rank Problem

You are given a dataframe df with columns:

customer_id | txn_date | amount
Task

For each customer_id, return the top 2 highest transactions by amount.

Output
customer_id | txn_date | amount
'''


import pandas as pd

data = [
    [1, "2026-04-01", 100],
    [1, "2026-04-03", 250],
    [1, "2026-04-02", 180],
    [1, "2026-04-05", 250],

    [2, "2026-04-01", 90],
    [2, "2026-04-02", 300],
    [2, "2026-04-03", 120],

    [3, "2026-04-01", 500],
    [3, "2026-04-02", 200],
]
df = pd.DataFrame(data, columns=["customer_id", "txn_date", "amount"])



# Solution

df["txn_date"] = pd.to_datetime(df["txn_date"])

df = df.sort_values(["customer_id", "amount", "txn_date"], ascending=[True, False, True])

df = df.groupby("customer_id").head(2)

print(df)