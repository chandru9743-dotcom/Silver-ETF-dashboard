import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("🥈 Silver ETF PRO Dashboard")


# ---------------- SAFE DOWNLOAD ----------------
def safe_download(ticker, period="1d", interval="5m"):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df.empty:
            return None
        return df
    except:
        return None


# ---------------- FETCH DATA ----------------
silver_df = safe_download("SI=F")
usd_df = safe_download("INR=X")

etf_list = {
    "Tata": "TATASILVETF.NS",
    "HDFC": "HDFCSILVER.NS",
    "Nippon": "SILVERBEES.NS"
}


def last_price(df):
    if df is None:
        return None
    return float(df["Close"].iloc[-1])


silver = last_price(silver_df)
usdinr = last_price(usd_df)


# ---------------- TOP METRICS ----------------
c1, c2 = st.columns(2)

c1.metric("COMEX Silver ($)", silver if silver else "No Data")
c2.metric("USDINR", usdinr if usdinr else "No Data")

st.write("---")


# ---------------- ETF TABLE ----------------
rows = []

for name, ticker in etf_list.items():

    df = safe_download(ticker)
    if df is None or silver_df is None:
        continue

    etf_now = df["Close"].iloc[-1]
    etf_prev = df["Close"].iloc[0]

    silver_now = silver_df["Close"].iloc[-1]
    silver_prev = silver_df["Close"].iloc[0]

    silver_change = (silver_now - silver_prev) / silver_prev

    expected = etf_prev * (1 + silver_change)

    deviation = (etf_now - expected) / expected * 100

    if deviation <= -3:
        signal = "BUY 🟢"
    elif deviation >= 3:
        signal = "SELL 🔴"
    else:
        signal = "HOLD ⚪"

    rows.append([name, round(etf_now, 2), round(expect_]()
