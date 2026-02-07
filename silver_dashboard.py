import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.set_page_config(layout="wide")

# -----------------------
# AUTO REFRESH (10 sec)
# -----------------------
st.markdown(
    """
    <script>
    setTimeout(function(){
        window.location.reload();
    }, 10000);
    </script>
    """,
    unsafe_allow_html=True
)

st.title("🥈 Silver ETF Master Dashboard")

# -----------------------
# FETCH DATA
# -----------------------
def safe_last(series):
    if series is None or len(series) == 0:
        return None
    return float(series.iloc[-1])


try:
    etf_data = yf.download("TATASILVETF.NS", period="1d", interval="1m")
    usd_data = yf.download("INR=X", period="1d", interval="1m")
    silver_data = yf.download("SI=F", period="1d", interval="1m")

    etf_now = safe_last(etf_data["Close"])
    usd_now = safe_last(usd_data["Close"])
    silver_now = safe_last(silver_data["Close"])

except:
    st.error("Data fetch failed. Market might be closed.")
    st.stop()

# -----------------------
# FAIR VALUE LOGIC
# -----------------------
if None in (etf_now, usd_now, silver_now):
    st.warning("Waiting for live market data...")
    st.stop()

fair_value = silver_now * usd_now / 10
deviation = ((etf_now - fair_value) / fair_value) * 100


# -----------------------
# SIGNAL
# -----------------------
if deviation <= -3:
    signal = "🟢 BUY"
elif deviation >= 3:
    signal = "🔴 SELL"
else:
    signal = "🟡 HOLD"

# -----------------------
# DYNAMIC CARDS
# -----------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("TATA ETF", round(etf_now, 2))
c2.metric("COMEX Silver", round(silver_now, 2))
c3.metric("USD/INR", round(usd_now, 2))
c4.metric("Fair Value", round(fair_value, 2))

st.markdown(f"## Signal: {signal} | Deviation: {round(deviation,2)}%")

# -----------------------
# LIVE CHART
# -----------------------
chart_df = pd.DataFrame({
    "ETF": etf_data["Close"],
})

fair_line = (silver_data["Close"] * usd_data["Close"] / 10)

chart_df["Fair Value"] = fair_line.values[:len(chart_df)]

st.subheader("Live Price vs Fair Value")
st.line_chart(chart_df)

# -----------------------
# FOOTER
# -----------------------
st.caption("Auto refresh every 10 seconds • Built by Aditya's Silver Terminal 🚀")


