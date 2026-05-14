import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from datetime import datetime

# PAGE SETTING
st.set_page_config(page_title="ETF RSI Scanner", layout="wide")

st.title("📈 NSE ETF RSI Scanner")
st.write("Low RSI Buying Opportunity Scanner")

# ETF LIST
etfs = [
    "NIFTYBEES.NS",
    "BANKBEES.NS",
    "GOLDBEES.NS",
    "SILVERBEES.NS",
    "ITBEES.NS",
    "CPSEETF.NS",
    "AUTOBEES.NS",
    "PSUBNKBEES.NS",
    "ICICIB22.NS",
    "SETFNIF50.NS"
]

results = []

# DOWNLOAD DATA
for etf in etfs:

    try:
        data = yf.download(
            etf,
            period="3mo",
            interval="1d",
            auto_adjust=True,
            progress=False
        )

        # SKIP EMPTY DATA
        if data.empty:
            continue

        close_prices = data['Close']

        # RSI CALCULATION
        rsi = RSIIndicator(close_prices).rsi()

        latest_price = round(float(close_prices.iloc[-1]), 2)
        latest_rsi = round(float(rsi.iloc[-1]), 2)

        # SIGNALS
        if latest_rsi < 30:
            signal = "STRONG BUY"
        elif latest_rsi < 40:
            signal = "BUY ZONE"
        elif latest_rsi < 50:
            signal = "WATCH"
        else:
            signal = "AVOID"

        results.append({
            "ETF": etf.replace(".NS", ""),
            "Price": latest_price,
            "RSI": latest_rsi,
            "Signal": signal
        })

    except Exception as e:
        st.warning(f"Error loading {etf}")

# CREATE DATAFRAME
df = pd.DataFrame(results)

# CHECK IF DATA EXISTS
if len(df) > 0:

    # SORT
    df = df.sort_values(by="RSI")

    # REFRESH TIME
    refresh_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    st.write(f"Last Refresh: {refresh_time}")

    # COLOR FUNCTION
    def color_signal(val):

        if val == "STRONG BUY":
            return "background-color: green; color: white;"

        elif val == "BUY ZONE":
            return "background-color: lightgreen;"

        elif val == "WATCH":
            return "background-color: yellow;"

        else:
            return "background-color: pink;"

    # APPLY COLORS
    styled_df = df.style.applymap(
        color_signal,
        subset=['Signal']
    )

    # SHOW TABLE
    st.dataframe(
        styled_df,
        use_container_width=True
    )

    # REFRESH BUTTON
    if st.button("🔄 Refresh Scanner"):
        st.rerun()

else:
    st.error("ETF data not loaded. Please refresh again later.")
