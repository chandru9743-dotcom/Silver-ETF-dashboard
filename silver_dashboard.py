import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("🥈 Silver ETF Dashboard (Stable Version)")


# -------- ALWAYS WORKING PRICE --------
def price(ticker):
    try:
        df = yf.download(ticker, period="1mo", interval="1d", progress=False)

        if df.empty:
            return None

        return float(df["Close"].iloc[-1])

    except:
        return None


silver = price("SI=F")
usd = price("INR=X")
tata = price("TATASILVETF.NS")


# -------- UI --------
c1, c2, c3 = st.columns(3)

c1.metric("Silver ($)", silver if silver else "No Data")
c2.metric("USDINR", usd if usd else "No Data")
c3.metric("Tata ETF", tata if tata else "No Data")

st.write("---")

st.write("Last updated:", pd.Timestamp.now())


if silver and tata:
    st.success("✅ Data loaded successfully")
else:
    st.warning("Market closed OR Yahoo temporarily unavailable")


time.sleep(30)
st.rerun()

