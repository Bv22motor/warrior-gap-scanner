import streamlit as st
import requests
import os
import time

# === CONFIG ===
API_KEY = os.getenv("FINNHUB_API_KEY") or "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"
SYMBOLS = ["ASTR", "CDNA", "QOCX", "APP", "AFRM", "RAMP", "DUOL"]  # Can edit anytime

st.set_page_config(page_title="📰 News Room", layout="wide")
st.title("🗞️ Warrior-Style News Room (Clickable Tickers)")

# === FETCH NEWS FOR SYMBOL ===
def fetch_news(symbol):
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-01-01&to={time.strftime('%Y-%m-%d')}&token={API_KEY}"
    try:
        res = requests.get(url)
        news_data = res.json()
        return news_data[:3]  # Show top 3
    except Exception as e:
        return []

# === DISPLAY ===
for sym in SYMBOLS:
    st.subheader(f"📌 {sym} — [View Chart](https://www.tradingview.com/symbols/{sym}/)")
    news = fetch_news(sym)
    
    if not news:
        st.info("No recent news.")
        continue

    for item in news:
        headline = item.get("headline", "")
        datetime = time.strftime('%Y-%m-%d %H:%M', time.localtime(item.get("datetime", 0)))
        url = item.get("url", "")
        st.markdown(f"- 🕒 **{datetime}** — [{headline}]({url})")

    st.markdown("---")

