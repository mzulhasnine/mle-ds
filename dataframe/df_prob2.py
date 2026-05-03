'''
Problem 2 — doc style

You are given a dataframe df with columns:

customer_id | txn_date | amount | txn_type

Where:

txn_type is either "debit" or "credit"
Task

For each customer_id:
- Sort by txn_date
- Compute a running balance
    - credit adds to balance
    - debit subtracts from balance
- Compute previous transaction amount as prev_amount
- Flag a transaction as suspicious if:
    - it is a debit and amount > 1.5 * customer_avg_debit
Return
customer_id | txn_date | amount | txn_type | running_balance | prev_amount | is_suspicious.
'''

import pandas as pd
import numpy as np

data = [
    [1, "2026-04-01", 1000, "credit"],
    [1, "2026-04-02", 200, "debit"],
    [1, "2026-04-03", 250, "debit"],
    [1, "2026-04-04", 1200, "credit"],
    [1, "2026-04-05", 700, "debit"],

    [2, "2026-04-01", 500, "credit"],
    [2, "2026-04-02", 100, "debit"],
    [2, "2026-04-03", 600, "credit"],
    [2, "2026-04-04", 50, "debit"],
    [2, "2026-04-05", 300, "debit"],

    [3, "2026-04-03", 400, "credit"],
    [3, "2026-04-01", 100, "debit"],
    [3, "2026-04-02", 200, "credit"],
]

df = pd.DataFrame(data, columns=["customer_id", "txn_date", "amount", "txn_type"])



# Solution

df["txn_date"] = pd.to_datetime(df["txn_date"])
df = df.sort_values(["customer_id", "txn_date"])
df = df.dropna() # dropna() too aggressive, use subset


# df["amount_adj"] = df.apply(lambda x: x["amount"] if x["txn_type"]=="credit" else -x["amount"], axis=1)
df["amount_adj"] = np.where(df["txn_type"]=="credit", df["amount"], -df["amount"])
df["running_balance"] = df.groupby("customer_id")["amount_adj"].cumsum()


df["prev_amount"] = df.groupby("customer_id")["amount"].shift(1)
# df["prev_amount"] = df["prev_amount"].fillna(0)


# df["customer_avg_debit"] = df[df["txn_type"]=="debit"].groupby("customer_id")["amount"].transform("mean")
# df["customer_avg_debit"] = df["customer_avg_debit"].fillna(0)


debit_avg_map = df[df["txn_type"]=="debit"].groupby("customer_id")["amount"].mean()
df["customer_avg_debit"] = df["customer_id"].map(debit_avg_map)

print(df)

df["is_suspicious"] = (df["txn_type"] == "debit") & (df["amount"] > 1.5 * df["customer_avg_debit"])

print(df)