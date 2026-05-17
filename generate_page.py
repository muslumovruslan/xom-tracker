import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime
import os

# Create docs folder
os.makedirs("docs", exist_ok=True)

# Stock ticker
ticker = "XOM"

# Download stock data
data = yf.download(
    ticker,
    period="6mo",
    interval="1d",
    auto_adjust=True
)

# Extract close prices
close_prices = data["Close"].squeeze()

# Latest values
latest_price = round(float(close_prices.iloc[-1]), 2)
previous_price = round(float(close_prices.iloc[-2]), 2)

change = round(latest_price - previous_price, 2)
percent = round((change / previous_price) * 100, 2)

# Trend
trend = "Bullish 📈" if change > 0 else "Bearish 📉"

# Analysis text
analysis = f"""
Latest Close Price: ${latest_price}

Daily Change: {change} ({percent}%)

Trend: {trend}

Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""

# Create interactive graph
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=close_prices.index,
        y=close_prices.values,
        mode='lines',
        name='XOM Price',
        line=dict(width=3),

        hovertemplate=
        '<b>Date:</b> %{x}<br>' +
        '<b>Price:</b> $%{y:.2f}<extra></extra>'
    )
)

# Layout
fig.update_layout(
    title="Interactive XOM Stock Price",
    xaxis_title="Date",
    yaxis_title="Price ($)",

    template="plotly_white",

    hovermode="x unified",

    height=650,

    xaxis=dict(
        rangeslider=dict(visible=True),
        type="date"
    )
)

# Convert graph to HTML
graph_html = fig.to_html(
    full_html=False,
    include_plotlyjs='cdn'
)

# Create webpage
html = f"""
<!DOCTYPE html>
<html>

<head>

<title>XOM Interactive Tracker</title>

<style>

body {{
    font-family: Arial;
    background: #f4f4f4;
    padding: 40px;
}}

.container {{
    background: white;
    max-width: 1200px;
    margin: auto;
    padding: 30px;
    border-radius: 12px;
}}

.analysis {{
    margin-top: 30px;
    padding: 20px;
    background: #fafafa;
    border-left: 5px solid #007BFF;
    white-space: pre-line;
    font-size: 18px;
}}

h1 {{
    text-align: center;
}}

</style>

</head>

<body>

<div class="container">

<h1>XOM Interactive Daily Tracker</h1>

{graph_html}

<div class="analysis">
{analysis}
</div>

</div>

</body>

</html>
"""

# Save webpage
with open("docs/index.html", "w") as f:
    f.write(html)

print("Interactive website generated successfully.")