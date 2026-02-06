import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")
st.title("🥈 Silver ETF PRO Dashboard")


# -------- SAFE LAST PRICE ----------
def get_last_price(ticker):
    try:
        df = yf.download(ticker, period="1d", interval="5m", progress=False)

        if df.empty:
            return None

        return float(df["Close"].dropna().values[-1])

    except:
        return None


# -------- MAIN PRICES ----------
silver = get_last_price("SI=F")
usdinr = get_last_price("INR=X")

c1, c2 = st.columns(2)
c1.metric("COMEX Silver ($)", silver if silver else "No Data")
c2.metric("USDINR", usdinr if usdinr else "No Data")

st.write("---")


# -------- ETF LIST ----------
etf_list = {
    "Tata": "TATASILVETF.NS",
    "HDFC": "HDFCSILVER.NS",
    "Nippon": "SILVERBEES.NS"
}


rows = []

for name, ticker in etf_list.items():

    df = yf.download(ticker, period="1d", interval="5m", progress=False)

    if df.empty or silver is None:
        continue

    etf_now = float(df["Close"].dropna().values[-1])
    etf_prev = float(df["Close"].dropna().values[0])

    silver_df = yf.download("SI=F", period="1d", interval="5m", progress=False)
    silver_prev = float(silver_df["Close"].dropna().values[0])

    silver_change = (silver - silver_prev) / silver_prev

    expected = etf_prev * (1 + silver_change)

    deviation = float((etf_now - expected) / expected * 100)


    # -------- SIGNAL ----------
    if deviation <= -3:
        signal = "BUY 🟢"
    elif deviation >= 3:
        signal = "SELL 🔴"
    else:
        signal = "HOLD ⚪"

    rows.append([name, round(etf_now, 2), round(expected, 2), round(deviation, 2), signal])


# -------- TABLE ----------
if rows:
    table = pd.DataFrame(rows,
                         columns=["ETF", "Current", "Expected", "Deviation %", "Signal"])

    st.subheader("📊 ETF Fair Value Comparison")
    st.dataframe(table, use_container_width=True)
else:
    st.warning("Market closed or data unavailable")


# -------- CHART ----------
selected = st.selectbox("Chart ETF", list(etf_list.keys()))

chart = yf.download(etf_list[selected], period="1d", interval="5m", progress=False)

if not chart.empty:
    st.line_chart(chart["Close"])


# -------- AUTO REFRESH ----------
time.sleep(10)
st.rerun()
