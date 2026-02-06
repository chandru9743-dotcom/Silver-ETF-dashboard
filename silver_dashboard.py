import streamlit as st
import yfinance as yf
import time

st.title("Silver ETF Dashboard")

silver = yf.download("SI=F", period="1d", interval="1m")["Close"].iloc[-1]
usdinr = yf.download("INR=X", period="1d", interval="1m")["Close"].iloc[-1]
etf = yf.download("TATASILVETF.NS", period="1d", interval="1m")["Close"].iloc[-1]

st.write("COMEX Silver:", silver)
st.write("USDINR:", usdinr)
st.write("ETF Price:", etf)

time.sleep(5)
st.rerun()
