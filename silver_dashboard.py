# ======================================
# SILVER TERMINAL v6 (STOOQ VERSION)
# NO YAHOO • NO BLOCK • ALWAYS WORKS
# ======================================

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

# --------------------------
# AUTO REFRESH 15s
# --------------------------
st.markdown("""
<script>
setTimeout(function(){
   window.location.reload();
}, 15000);
</script>
""", unsafe_allow_html=True)

st.title("🥈 Silver ETF Trading Terminal")


# --------------------------
# STOOQ FETCH (VERY STABLE)
# --------------------------
def get_price_stooq(url):
    try:
        df = pd.read_csv(url)
        df = df[::-1]
        return float(df["Close"].iloc[-1]), df
    except:
        return 0.0, pd.DataFrame()


# --------------------------
# DATA SOURCES
# --------------------------
etf_now, etf_df = get_price_stooq(
    "https://stooq.com/q/d/l/?s=tatasilvetf.ns&i=d"
)

silver_now, silver_df = get_price_stooq(
    "https://stooq.com/q/d/l/?s=si.f&i=d"
)

usd_now, usd_df = get_price_stooq(
    "https://stooq.com/q/d/l/?s=usdinr&i=d"
)


if etf_now == 0 or silver_now == 0 or usd_now == 0:
    st.error("Data source temporarily unavailable.")
    st.stop()


# --------------------------
# FAIR VALUE
# --------------------------
fair_value = silver_now * usd_now / 10
deviation = ((etf_now - fair_value) / fair_value) * 100


# --------------------------
# SIGNAL
# --------------------------
if deviation <= -3:
    signal = "🟢 BUY"
    color = "green"
elif deviation >= 3:
    signal = "🔴 SELL"
    color = "red"
else:
    signal = "🟡 HOLD"
    color = "orange"


# --------------------------
# METRICS
# --------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("TATA ETF", f"₹ {etf_now:.2f}")
c2.metric("Silver ($)", f"{silver_now:.2f}")
c3.metric("USD/INR", f"{usd_now:.2f}")
c4.metric("Fair Value", f"₹ {fair_value:.2f}")


st.markdown(
    f"<h1 style='text-align:center;color:{color};'>{signal}</h1>",
    unsafe_allow_html=True
)

st.markdown(
    f"<h4 style='text-align:center;'>Deviation: {deviation:.2f}%</h4>",
    unsafe_allow_html=True
)


# --------------------------
# CHART
# --------------------------
if not etf_df.empty:
    st.subheader("📈 ETF Trend")
    st.line_chart(etf_df["Close"])


st.caption("Powered by Stooq • Cloud safe • Built by Aditya 🚀")

