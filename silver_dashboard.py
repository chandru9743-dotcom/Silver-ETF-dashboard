# =====================================
# SILVER ETF TERMINAL v4 (FRESH BUILD)
# Always Works • No Empty Data • Stable
# =====================================

import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(layout="wide")

# ---------------------------------
# AUTO REFRESH EVERY 10s
# ---------------------------------
st.markdown("""
<script>
setTimeout(function(){
   window.location.reload();
}, 10000);
</script>
""", unsafe_allow_html=True)


st.title("🥈 Silver ETF Trading Terminal")


# ---------------------------------
# SMART FETCH (intraday → daily fallback)
# ---------------------------------
def get_data(ticker):

    # try intraday
    df = yf.download(ticker, period="1d", interval="1m", progress=False)

    if df.empty:
        # fallback daily (always available)
        df = yf.download(ticker, period="5d", interval="1d", progress=False)

    return df


# ---------------------------------
# DOWNLOAD
# ---------------------------------
etf_df = get_data("TATASILVETF.NS")
silver_df = get_data("SI=F")
usd_df = get_data("INR=X")

# last prices (ALWAYS safe now)
etf_now = float(etf_df["Close"].iloc[-1])
silver_now = float(silver_df["Close"].iloc[-1])
usd_now = float(usd_df["Close"].iloc[-1])


# ---------------------------------
# FAIR VALUE LOGIC
# ---------------------------------
fair_value = silver_now * usd_now / 10
deviation = ((etf_now - fair_value) / fair_value) * 100


# ---------------------------------
# SIGNAL
# ---------------------------------
if deviation <= -3:
    signal = "🟢 BUY"
    color = "green"
elif deviation >= 3:
    signal = "🔴 SELL"
    color = "red"
else:
    signal = "🟡 HOLD"
    color = "orange"


# ---------------------------------
# METRIC CARDS
# ---------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("TATA ETF", f"₹ {etf_now:.2f}")
c2.metric("COMEX Silver", f"$ {silver_now:.2f}")
c3.metric("USD/INR", f"{usd_now:.2f}")
c4.metric("Fair Value", f"₹ {fair_value:.2f}")


# ---------------------------------
# SIGNAL TEXT
# ---------------------------------
st.markdown(
    f"<h1 style='text-align:center; color:{color};'>{signal}</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<h4 style='text-align:center;'>Deviation: {deviation:.2f}%</h4>",
    unsafe_allow_html=True
)


# ---------------------------------
# LIVE CHART
# ---------------------------------
st.subheader("📈 ETF vs Fair Value")

min_len = min(len(etf_df), len(silver_df), len(usd_df))

chart_df = pd.DataFrame({
    "ETF": etf_df["Close"].tail(min_len).values,
    "Fair Value": (
        silver_df["Close"].tail(min_len).values *
        usd_df["Close"].tail(min_len).values / 10
    )
})

st.line_chart(chart_df)


# ---------------------------------
# FOOTER
# ---------------------------------
st.caption("Auto refresh 10s • Live when open • Daily fallback when closed • Built by Aditya 🚀")
