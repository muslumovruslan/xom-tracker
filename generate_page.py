import yfinance as yf
import pandas as pd
import json
import os
from datetime import datetime

# Create folders
os.makedirs("docs/data", exist_ok=True)
os.makedirs("docs/saved", exist_ok=True)

# Stock symbol
symbol = "XOM"

# Timeframes
TIMEFRAMES = {
    "1D": {"period": "1d", "interval": "5m"},
    "3D": {"period": "3d", "interval": "15m"},
    "1W": {"period": "7d", "interval": "30m"},
    "1M": {"period": "1mo", "interval": "1d"},
    "6M": {"period": "6mo", "interval": "1d"},
    "1Y": {"period": "1y", "interval": "1d"},
}

all_data = {}

# Download data for each timeframe
for tf, config in TIMEFRAMES.items():

    data = yf.download(
        symbol,
        period=config["period"],
        interval=config["interval"],
        auto_adjust=True,
        progress=False
    )

    data = data.reset_index()

    records = []

    for _, row in data.iterrows():

        records.append({

            "Date": str(row.iloc[0]),

            "Open": float(row["Open"].item()),

            "High": float(row["High"].item()),

            "Low": float(row["Low"].item()),

            "Close": float(row["Close"].item())

        })

    all_data[tf] = records

# Save latest dataset
with open("docs/data/latest.json", "w") as f:

    json.dump(all_data, f)

# Save archive copy
save_name = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

with open(f"docs/saved/{save_name}.json", "w") as f:

    json.dump(all_data, f)

print("Dashboard data generated successfully.")