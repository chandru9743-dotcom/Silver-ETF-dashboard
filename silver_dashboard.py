# ==========================================
# SILVER TERMINAL v5 (BULLETPROOF EDITION)
# NEVER CRASHES • ALWAYS RUNS • CLOUD SAFE
# ==========================================

import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")

# ----------------------------------
# AUTO REFRESH 10s
# ----------------------------------
st.markdown("""
<script>
setTimeout(function(){
   window.location.reload();
}, 10000);
</script>
""", unsafe_allow_html=True)

st.title("🥈 Silver ETF Trading Terminal")


# ----------------------------------
# SAFE DOWNLOAD
# ----------------------------------
def safe_price(ticker):

    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)

        if df is None or df.empty or "Close" not in df:
            return 0.0, pd.DataFrame()

        return float(df["Close"].dropna().iloc[-1]), df

    except:
        return 0.0, pd.DataFrame()


# ----------------------------------
# GET DATA (daily only → MOST STABLE)
# ----------------------------------
etf_now, etf_df = safe_price("TATASILVETF.NS")
silver_now, silver_df = safe_price("SI=F")
usd_now, usd_df = safe_price("INR=X")


# ----------------------------------
# IF STILL ZERO → SHOW MESSAGE
# ----------------------------------
if etf_now == 0 or silver_now == 0 or usd_now == 0:
    st.warning("Data temporarily unavailable. Yahoo blocked request. Try refresh.")
    st.stop()


# ----------------------------------
# FAIR VALUE
# ----------------------------------
fair_value = silver_now * usd_now / 10
deviation = ((etf_now - fair_value) / fair_value) * 100


# ----------------------------------
# SIGNAL
# ----------------------------------
if deviation <= -3:
    signal = "🟢 BUY"
    color = "green"
elif deviation >= 3:
    signal = "🔴 SELL"
    color = "red"
else:
    signal = "🟡 HOLD"
    color = "orange"


# ----------------------------------
# METRICS
# ----------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("TATA ETF", f"₹ {etf_now:.2f}")
c2.metric("COMEX Silver", f"$ {silver_now:.2f}")
c3.metric("USD/INR", f"{usd_now:.2f}")
c4.metric("Fair Value", f"₹ {fair_value:.2f}")


# ----------------------------------
# SIGNAL DISPLAY
# ----------------------------------
st.markdown(
    f"<h1 style='text-align:center;color:{color};'>{signal}</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<h4 style='text-align:center;'>Deviation: {deviation:.2f}%</h4>",
    unsafe_allow_html=True
)


# ----------------------------------
# SIMPLE CHART
# ----------------------------------
if not etf_df.empty:
    st.subheader("📈 Last 5 Days ETF Trend")
    st.line_chart(etf_df["Close"])


# ----------------------------------
# FOOTER
# ----------------------------------
st.caption("Stable daily data • No crash mode • Built by Aditya 🚀")
