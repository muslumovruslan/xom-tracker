import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime
import os

# Create docs folder if it does not exist
os.makedirs("docs", exist_ok=True)

# Download stock data
ticker = "XOM"

data = yf.download(
    ticker,
    period="3mo",
    interval="1d",
    auto_adjust=True
)

# Extract close prices correctly
close_prices = data["Close"].squeeze()

# Latest prices
latest_price = round(float(close_prices.iloc[-1]), 2)
previous_price = round(float(close_prices.iloc[-2]), 2)

change = round(latest_price - previous_price, 2)
percent = round((change / previous_price) * 100, 2)

# Trend analysis
trend = "Bullish 📈" if change > 0 else "Bearish 📉"

analysis = f"""
Latest Close Price: ${latest_price}

Daily Change: {change} ({percent}%)

Trend: {trend}

Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

# Create graph
plt.figure(figsize=(10, 5))

plt.plot(
    close_prices.index,
    close_prices.values,
    linewidth=2
)

plt.title("XOM Stock Price")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.grid(True)

# Save graph
plt.savefig("docs/xom_graph.png")
plt.close()

# Create webpage
html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>XOM Tracker</title>

    <style>
        body {{
            font-family: Arial;
            background: #f4f4f4;
            padding: 40px;
        }}

        .container {{
            background: white;
            max-width: 900px;
            margin: auto;
            padding: 30px;
            border-radius: 10px;
        }}

        img {{
            width: 100%;
            border-radius: 10px;
        }}

        .analysis {{
            margin-top: 20px;
            padding: 20px;
            background: #fafafa;
            border-left: 5px solid #007BFF;
            white-space: pre-line;
        }}
    </style>
</head>

<body>

<div class="container">

<h1>XOM Daily Tracker</h1>

<img src="xom_graph.png">

<div class="analysis">
{analysis}
</div>

</div>

</body>
</html>
"""

with open("docs/index.html", "w") as f:
    f.write(html)

print("Website generated successfully.")