# ======================================================
# 🥈 SILVER QUANT TERMINAL — FINAL PRO VERSION
# Stable • Dark • Auto Refresh • Alerts • Fair Value
# ======================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import pytz
from streamlit_autorefresh import st_autorefresh
from plyer import notification

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(layout="wide")

# ======================================================
# AUTO REFRESH (REAL — NO FLICKER)
# ======================================================

REFRESH_SECONDS = 15
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="refresh")

# ======================================================
# DARK THEME (PERMANENT + WHITE TEXT)
# ======================================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg,#0b0f14,#141e30,#1c2833);
}

/* force white text everywhere */
html, body, [class*="css"], p, div, span, label {
    color: white !important;
}

/* metric cards */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 16px;
    box-shadow: 0 0 16px rgba(0,0,0,0.7);
}

/* headings */
h1, h2, h3 {
    color: #00ffd5 !important;
}

/* sidebar */
section[data-testid="stSidebar"] {
    background: #0e1117 !important;
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* =========================================
   BIGGER % CHANGE (DELTA)
========================================= */

[data-testid="stMetricDelta"] {
    font-size: 28px !important;
    font-weight: 800 !important;
}

/* optional: slightly bigger price too */
[data-testid="stMetricValue"] {
    font-size: 26px !important;
}


</style>
""", unsafe_allow_html=True)


# ======================================================
# DESKTOP ALERT FUNCTION
# ======================================================

def send_alert(title, message):
    try:
        notification.notify(
            title=title,
            message=message,
            timeout=5
        )
    except:
        pass


# ======================================================
# SAFE FETCH FUNCTION
# ======================================================

def fetch(ticker):
    try:
        df = yf.download(ticker, period="2mo", interval="1d", progress=False)

        if df.empty:
            return None, 0, pd.DataFrame()

        close = df["Close"].dropna()

        price = float(close.iloc[-1])
        prev = float(close.iloc[-2]) if len(close) > 1 else price
        change = ((price - prev) / prev) * 100

        return price, change, df

    except:
        return None, 0, pd.DataFrame()


# ======================================================
# FETCH DATA
# ======================================================

etf_now, etf_chg, etf_df = fetch("TATSILV.NS")
comex_now, comex_chg, comex_df = fetch("SI=F")
usd_now, usd_chg, usd_df = fetch("INR=X")

# ======================================================
# HEADER
# ======================================================

st.title("🥈 Silver Quant Trading Terminal")

# ======================================================
# TIME (IST + EST)
# ======================================================

india_time = datetime.now()
est_time = datetime.now(pytz.timezone("US/Eastern"))

# ======================================================
# METRICS ROW
# ======================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Tata Silver ETF", f"₹{etf_now:.2f}" if etf_now else "No data", f"{etf_chg:.2f}%")
c2.metric("COMEX Silver", f"${comex_now:.2f}" if comex_now else "No data", f"{comex_chg:.2f}%")
c3.metric("USD/INR", f"{usd_now:.2f}" if usd_now else "No data", f"{usd_chg:.2f}%")
c4.metric("Time (IST | EST)", f"{india_time.strftime('%H:%M:%S')} | {est_time.strftime('%H:%M:%S')}")

st.divider()

# ======================================================
# REGRESSION FAIR VALUE MODEL
# ======================================================

if not etf_df.empty and not comex_df.empty and not usd_df.empty:

    e = etf_df["Close"]
    c = comex_df["Close"]
    u = usd_df["Close"]

    hist = pd.concat([e, c, u], axis=1).dropna()
    hist.columns = ["ETF", "COMEX", "USD"]

    if len(hist) > 5:

        X = hist[["COMEX", "USD"]].values
        y = hist["ETF"].values

        A = np.column_stack([X, np.ones(len(X))])
        a, b, c0 = np.linalg.lstsq(A, y, rcond=None)[0]

        fair = a * comex_now + b * usd_now + c0
        deviation = ((etf_now - fair) / fair) * 100

        signal = "🟡 HOLD"

        if deviation < -3:
            signal = "🟢 BUY"
            send_alert("BUY Signal 🚀", f"TATSILV undervalued\nDev {deviation:.2f}%")

        elif deviation > 3:
            signal = "🔴 SELL"
            send_alert("SELL Signal ⚠", f"TATSILV overvalued\nDev {deviation:.2f}%")

        c5, c6, c7 = st.columns(3)

        c5.metric("Fair ETF Price", f"₹{fair:.2f}")
        c6.metric("Deviation %", f"{deviation:.2f}%")
        c7.metric("Signal", signal)

        st.divider()

        st.subheader("📈 2 Month Price Comparison")
        st.line_chart(hist)

    else:
        st.warning("Not enough historical data for regression")

else:
    st.warning("Market data temporarily unavailable")

# ======================================================
# FOOTER
# ======================================================

st.caption(f"Auto refresh every {REFRESH_SECONDS} seconds • Stable Dark Mode")
