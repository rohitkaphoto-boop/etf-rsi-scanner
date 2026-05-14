import streamlit as st
import yfinance as yf
import pandas as pd
from ta.momentum import RSIIndicator
from datetime import datetime
import time

# PAGE SETTINGS
st.set_page_config(
    page_title="NSE ETF RSI Scanner",
    layout="wide"
)

st.title("📈 NSE ETF RSI Scanner")
st.write("Low RSI Buying Opportunity Scanner")

# ETF LIST
etfs = {
    "NIFTYBEES": "NIFTYBEES.NS",
    "BANKBEES": "BANKBEES.NS",
    "GOLDBEES": "GOLDBEES.NS",
    "SILVERBEES": "SILVERBEES.NS",
    "ITBEES": "ITBEES.NS",
    "CPSEETF": "CPSEETF.NS",
    "AUTOBEES": "AUTOBEES.NS",
    "PSUBNKBEES": "PSUBNKBEES.NS",
    "ICICIB22": "ICICIB22.NS",
    "SETFNIF50": "SETFNIF50.NS"
}

results = []

# DOWNLOAD DATA
for name, symbol in etfs.items():

    try:
        ticker = yf.Ticker(symbol)

        data = ticker.history(period="3mo")

        # SKIP EMPTY
        if data.empty:
            continue

        close_prices = data["Close"]

        # RSI
        rsi = RSIIndicator(close_prices).rsi()

        latest_price = round(close_prices.iloc[-1], 2)
        latest_rsi = round(rsi.iloc[-1], 2)

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
            "ETF": name,
            "Price": latest_price,
            "RSI": latest_rsi,
            "Signal": signal
        })

        # SMALL DELAY
        time.sleep(1)

    except Exception as e:
        st.warning(f"Could not load {name}")

# DATAFRAME
df = pd.DataFrame(results)

# CHECK DATA
if not df.empty:

    # SORT
    df = df.sort_values(by="RSI")

    # TIME
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

    # STYLE
    styled_df = df.style.applymap(
        color_signal,
        subset=["Signal"]
    )

    # DISPLAY
    st.dataframe(
        styled_df,
        use_container_width=True
    )

else:
    st.error("ETF data could not be loaded from Yahoo Finance.")

# REFRESH BUTTON
if st.button("🔄 Refresh Scanner"):
    st.rerun()
