import streamlit as st
import yfinance as yf
import pandas as pd
import altair as alt

st.title("Tesla Stock History (TSLA)")

# 1. Pull data
tsla = yf.Ticker("TSLA")
data = tsla.history(period="max")  # all available daily data

# Prep data
data = data.reset_index()  # Date becomes a column
data["Return"] = data["Close"].pct_change()
data["RollingVolatility"] = data["Return"].rolling(window=30).std()

# 2. Allow the user to choose a date range
min_date = data["Date"].min()
max_date = data["Date"].max()

start_date, end_date = st.slider(
    "Select date range",
    min_value=min_date.to_pydatetime(),
    max_value=max_date.to_pydatetime(),
    value=(min_date.to_pydatetime(), max_date.to_pydatetime())
)

mask = (data["Date"] >= pd.to_datetime(start_date)) & (data["Date"] <= pd.to_datetime(end_date))
filtered = data[mask]

# 3. Price chart
price_chart = (
    alt.Chart(filtered)
    .mark_line()
    .encode(
        x="Date:T",
        y=alt.Y("Close:Q", title="Close Price (USD)"),
        tooltip=["Date:T", "Close:Q"]
    )
    .properties(
        width=800,
        height=300,
        title="TSLA Closing Price Over Time"
    )
)

st.altair_chart(price_chart, use_container_width=True)

# 4. Volume chart
volume_chart = (
    alt.Chart(filtered)
    .mark_bar()
    .encode(
        x="Date:T",
        y=alt.Y("Volume:Q", title="Trading Volume"),
        tooltip=["Date:T", "Volume:Q"]
    )
    .properties(
        width=800,
        height=550,
        title="Daily Trading Volume"
    )
)

st.altair_chart(volume_chart, use_container_width=True)

# 5. Volatility line (optional but good for your "risk" task)
vol_chart = (
    alt.Chart(filtered)
    .mark_line()
    .encode(
        x="Date:T",
        y=alt.Y("RollingVolatility:Q", title="30-Day Rolling Volatility"),
        tooltip=["Date:T", "RollingVolatility:Q"]
    )
    .properties(
        width=800,
        height=400,
        title="Rolling Volatility (Risk Signal)"
    )
)

st.altair_chart(vol_chart, use_container_width=True)

# 6. Little descriptive text for non-experts
st.markdown("""
**How to read this dashboard:**
- Big upward slope in price = rapid growth period.
- Sharp downward slope = crash / scary period.
- High volume bars = a lot of people trading (attention, excitement, panic).
- Higher volatility line = more chaotic, stressful to hold.
""")
