# ==============================
# SILVER ETF MASTER DASHBOARD v3
# Stable + Safe + Dynamic
# ==============================

import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")

# -----------------------------
# AUTO REFRESH (10 seconds)
# -----------------------------
st.markdown(
    """
    <script>
        setTimeout(function(){
            window.location.reload();
        }, 10000);
    </script>
    """,
    unsafe_allow_html=True
)

st.title("🥈 Silver ETF Trading Terminal")

# -----------------------------
# SAFE FETCH FUNCTION
# -----------------------------
def fetch_price(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="1m", progress=False)

        if df is None or df.empty:
            return None, None

        return float(df["Close"].iloc[-1]), df

    except:
        return None, None


# -----------------------------
# DOWNLOAD DATA
# -----------------------------
etf_now, etf_df = fetch_price("TATASILVETF.NS")
silver_now, silver_df = fetch_price("SI=F")
usd_now, usd_df = fetch_price("INR=X")

# -----------------------------
# IF NO DATA → SAFE EXIT
# -----------------------------
if None in (etf_now, silver_now, usd_now):
    st.warning("⏳ Waiting for market data... (Yahoo returned empty)")
    st.stop()

# -----------------------------
# FAIR VALUE CALCULATION
# -----------------------------
fair_value = silver_now * usd_now / 10
deviation = ((etf_now - fair_value) / fair_value) * 100

# -----------------------------
# SIGNAL LOGIC
# -----------------------------
if deviation <= -3:
    signal = "BUY"
    color = "green"
elif deviation >= 3:
    signal = "SELL"
    color = "red"
else:
    signal = "HOLD"
    color = "orange"


# -----------------------------
# TOP METRIC CARDS
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("TATA Silver ETF", round(etf_now, 2))
c2.metric("COMEX Silver ($)", round(silver_now, 2))
c3.metric("USD/INR", round(usd_now, 2))
c4.metric("Fair Value (₹)", round(fair_value, 2))


# -----------------------------
# SIGNAL DISPLAY
# -----------------------------
st.markdown(
    f"""
    <h2 style='text-align:center; color:{color};'>
    {signal} | Deviation: {round(deviation,2)}%
    </h2>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# LIVE CHART
# -----------------------------
st.subheader("📈 Live ETF vs Fair Value")

min_len = min(len(etf_df), len(silver_df), len(usd_df))

