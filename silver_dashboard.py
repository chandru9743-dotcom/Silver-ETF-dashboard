import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")

st.title("🥈 Silver ETF Master Dashboard")


# ---------------- SAFE PRICE FUNCTION ----------------
def last_price(ticker, period="1mo", interval="1d"):
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df.empty:
            return None, None
        return df, float(df["Close"].iloc[-1])
    except:
        return None, None


# ---------------- DAILY DATA (LOGIC) ----------------
silver_df, silver_now = last_price("SI=F")
usd_df, usd_now = last_price("INR=X")

c1, c2 = st.columns(2)
c1.metric("Silver ($)", silver_now if silver_now else "No Data")
c2.metric("USDINR", usd_now if usd_now else "No Data")

st.write("---")


# ---------------- ETF LIST ----------------
etfs = {
    "Tata": "TATASILVETF.NS",
    "HDFC": "HDFCSILVER.NS",
    "Nippon": "SILVERBEES.NS"
}


rows = []

for name, ticker in etfs.items():

    df, price_now = last_price(ticker)

    if df is None or silver_df is None:
        continue

    etf_prev = float(df["Close"].iloc[-2])
    silver_prev = float(silver_df["Close"].iloc[-2])

    silver_change = (silver_now - silver_prev) / silver_prev

    expected = etf_prev * (1 + silver_change)
    deviation = (price_now - expected) / expected * 100

    if deviation <= -3:
        signal = "BUY 🟢"
    elif deviation >= 3:
        signal = "SELL 🔴"
    else:
        signal = "HOLD ⚪"

    rows.append([name, price_now, expected, deviation, signal])


# ---------------- TABLE ----------------
if rows:

    table = pd.DataFrame(
        rows,
        columns=["ETF", "Current", "Expected", "Deviation %", "Signal"]
    )

    # highlight best opportunity
    best = table["Deviation %"].abs().idxmax()
    st.subheader("📊 Fair Value Comparison")

    st.dataframe(
        table.style.highlight_min(subset=["Deviation %"], color="lightgreen"),
        use_container_width=True
    )

else:
    st.warning("Data unavailable")


# ---------------- INTRADAY CHART ----------------
st.write("---")
st.subheader("📈 Intraday Chart (5-min)")

selected = st.selectbox("Select ETF", list(etfs.keys()))

chart = yf.download(etfs[selected], period="1d", interval="5m", progress=False)

if not chart.empty:
    st.line_chart(chart["Close"])
else:
    st.info("Intraday data unavailable (market closed)")


# ---------------- STATUS ----------------
st.write("Last refresh:", pd.Timestamp.now())


# ---------------- AUTO REFRESH ----------------
time.sleep(20)
st.rerun()

