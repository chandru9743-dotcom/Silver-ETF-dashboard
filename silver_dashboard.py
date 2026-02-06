import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("🥈 Silver ETF Live Dashboard")


# ---------- SAFE PRICE FUNCTION ----------
def last_price(ticker):
    try:
        data = yf.download(ticker, period="1d", interval="5m", progress=False)

        if data.empty:
            return None

        return float(data["Close"].iloc[-1])

    except:
        return None


# ---------- Fetch ----------
silver = last_price("SI=F")
usdinr = last_price("INR=X")
etf = last_price("TATASILVETF.NS")


# ---------- Display ----------
col1, col2, col3 = st.columns(3)

col1.metric("COMEX Silver ($)", silver if silver else "No Data")
col2.metric("USDINR", usdinr if usdinr else "No Data")
col3.metric("Tata Silver ETF (₹)", etf if etf else "No Data")


st.write("---")

if silver and etf:
    st.success("Data Live ✅")
else:
    st.warning("Market closed or data unavailable")


# ---------- Auto refresh ----------
time.sleep(10)
st.rerun()
