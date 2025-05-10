import streamlit as st
import requests
import os
import time

# === CONFIG ===
API_KEY = os.getenv("FINNHUB_API_KEY") or "your_finnhub_api_key"
SYMBOLS = ["ASTR", "CDNA", "QOCX", "APP", "AFRM", "RAMP", "DUOL"]

st.set_page_config(page_title="News Room", layout="wide")
st.title("📰 Warrior-Style News Room (Clickable Tickers)")

# === FETCH NEWS FOR SYMBOL ===
def fetch_news(symbol):
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-01-01&to={time.strftime('%Y-%m-%d')}&token={API_KEY}"
    try:
        res = requests.get(url)
        news = res.json()
        return news[:3]  # return top 3 only
    except:
        return []

# === DISPLAY ===
for sym in SYMBOLS:
    st.subheader(f"📌 {sym} — [Chart](https://www.tradingview.com/symbols/{sym}/)")
    news_list = fetch_news(sym)

    if not news_list:
        st.info("📭 No recent news found for this symbol.")
        continue

    for item in news_list:
        timestamp = time.strftime('%H:%M', time.localtime(item.get("datetime", 0)))
        st.markdown(f"**[{timestamp}]** {item.get('headline', '')}")
