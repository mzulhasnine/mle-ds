'''
🧩 Problem 1 (VERY realistic)

You are given a dataframe df with columns:

user_id | date | amount
Task:
For each user:
compute 3-day rolling average of amount
Flag an anomaly:
amount > 2 * user_avg

Return:

user_id | date | amount | rolling_avg | is_anomaly
'''

import pandas as pd

data = [
    # user 1
    [1, "2026-04-01", 100],
    [1, "2026-04-02", 120],
    [1, "2026-04-03", 130],
    [1, "2026-04-04", 400],  # anomaly candidate
    [1, "2026-04-05", 110],

    # user 2
    [2, "2026-04-01", 200],
    [2, "2026-04-02", 210],
    [2, "2026-04-03", None],  # missing value
    [2, "2026-04-04", 220],
    [2, "2026-04-05", 230],

    # user 3 (unsorted intentionally)
    [3, "2026-04-03", 300],
    [3, "2026-04-01", 280],
    [3, "2026-04-02", 290],
]

df = pd.DataFrame(data, columns=["user_id", "date", "amount"])


# Convert date column to datetime
df["date"] = pd.to_datetime(df["date"])

# Cleaning data
df = df.dropna(subset=["user_id", "date", "amount"]) 

# sort data
df = df.sort_values(by=["user_id", "date"])

# rolling average
df["rolling_avg"] = df.groupby("user_id")["amount"].rolling(3).mean().reset_index(level=0, drop=True)

# anomally detection
df["user_avg"] = df.groupby("user_id")["amount"].transform("mean")
df["is_anomaly"] =  df["amount"] > 2*df["user_avg"]

print(df)

