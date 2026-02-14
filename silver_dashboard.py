# ======================================================
# 🥈 SILVER QUANT TERMINAL PRO+
# Fair Value Line + Prediction Added
# ======================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from streamlit_autorefresh import st_autorefresh
from plyer import notification

st.set_page_config(layout="wide")

# ======================================================
# AUTO REFRESH
# ======================================================

st_autorefresh(interval=15000, key="refresh")

# ======================================================
# DARK THEME
# ======================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0b0f14,#141e30,#1c2833);
}

html, body, [class*="css"], p, div, span, label {
    color: white !important;
}

[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 16px;
}

h1,h2,h3 { color:#00ffd5 !important; }

/* bigger % change */
[data-testid="stMetricDelta"] {
    font-size: 26px !important;
    font-weight: 800 !important;
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# ALERT
# ======================================================

def alert(title,msg):
    try:
        notification.notify(title=title,message=msg,timeout=4)
    except:
        pass

# ======================================================
# FETCH
# ======================================================

def fetch(ticker):
    df = yf.download(ticker, period="3mo", interval="1d", progress=False)

    if df.empty:
        return None, 0, pd.DataFrame()

    close = df["Close"].dropna()

    now = float(close.iloc[-1])
    prev = float(close.iloc[-2]) if len(close)>1 else now
    chg = ((now-prev)/prev)*100

    return now, chg, df


# ======================================================
# DATA
# ======================================================

etf_now, etf_chg, etf_df = fetch("TATSILV.NS")
comex_now, comex_chg, comex_df = fetch("SI=F")
usd_now, usd_chg, usd_df = fetch("INR=X")

# ======================================================
# HEADER
# ======================================================

st.title("🥈 Silver Quant Trading Terminal PRO+")

india = datetime.now()
est = datetime.now(pytz.timezone("US/Eastern"))

c1,c2,c3,c4 = st.columns(4)

c1.metric("Tata Silver ETF", f"₹{etf_now:.2f}" if etf_now else "No data", f"{etf_chg:.2f}%")
c2.metric("COMEX Silver", f"${comex_now:.2f}" if comex_now else "No data", f"{comex_chg:.2f}%")
c3.metric("USD/INR", f"{usd_now:.2f}" if usd_now else "No data", f"{usd_chg:.2f}%")
c4.metric("Time (IST | EST)", f"{india:%H:%M:%S} | {est:%H:%M:%S}")

st.divider()

# ======================================================
# FAIR VALUE + PREDICTION
# ======================================================

if not etf_df.empty:

    hist = pd.concat([
        etf_df["Close"],
        comex_df["Close"],
        usd_df["Close"]
    ], axis=1).dropna()

    hist.columns = ["ETF","COMEX","USD"]

    X = hist[["COMEX","USD"]].values
    y = hist["ETF"].values

    A = np.column_stack([X, np.ones(len(X))])
    a,b,c = np.linalg.lstsq(A,y,rcond=None)[0]

    # FAIR VALUE SERIES
    hist["Fair"] = a*hist["COMEX"] + b*hist["USD"] + c

    fair_now = a*comex_now + b*usd_now + c
    deviation = ((etf_now-fair_now)/fair_now)*100

    # PREDICTION (next day)
    pred_price = fair_now

    signal="🟡 HOLD"
    if deviation < -3:
        signal="🟢 BUY"
        alert("BUY Signal", f"Dev {deviation:.2f}%")
    elif deviation > 3:
        signal="🔴 SELL"
        alert("SELL Signal", f"Dev {deviation:.2f}%")

    c5,c6,c7 = st.columns(3)

    c5.metric("Fair Price", f"₹{fair_now:.2f}")
    c6.metric("Deviation", f"{deviation:.2f}%")
    c7.metric("Next Day Estimate", f"₹{pred_price:.2f}")

    st.subheader(f"Signal → {signal}")

    st.divider()

    # ======================================================
    # CHART WITH FAIR VALUE LINE
    # ======================================================

    chart = hist[["ETF","Fair","COMEX","USD"]]

    st.subheader("📈 ETF vs Fair Value vs COMEX vs USDINR")
    st.line_chart(chart)


# ======================================================
# FOOTER
# ======================================================

st.caption("Auto refresh every 15s • Fair Value Model • Prediction Enabled")



