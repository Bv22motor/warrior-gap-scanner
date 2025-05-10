import streamlit as st
import requests
import pandas as pd
import time
import random
import os
from datetime import datetime

# ======== CONFIG =========
API_KEY = os.getenv("FINNHUB_API_KEY") or "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"
SYMBOLS = ["ASTR", "CDNA", "QOCX", "APP", "AFRM", "RAMP", "DUOL"]  # Manual ticker list

st.set_page_config(page_title="Gap Scanner", layout="wide")
st.title("🚀 Warrior-Style Gap Scanner")

# ======== OPTIONS =========
use_fake = st.sidebar.toggle("✨ Enable Fake Test Mode", value=False)
auto_refresh = st.sidebar.checkbox("🔁 Refreshing in 60 seconds...", value=True)

# ======== MOCK TEST DATA =========
def get_fake_data():
    return [
        {
            "Gap %": round(random.uniform(10, 90), 2),
            "Symbol": symbol,
            "Price": round(random.uniform(1, 300), 2),
            "Volume": random.randint(1_000_000, 90_000_000),
            "Float (M)": round(random.uniform(10, 300), 2),
            "Relative Vol (Daily Rate)": round(random.uniform(1, 3000), 2),
            "Relative Vol (5 Min %)": round(random.uniform(1, 900_000), 2),
            "Change From Close (%)": round(random.uniform(1, 80), 2),
            "Short Interest": random.randint(0, 50_000_000),
            "Short Ratio": round(random.uniform(0.1, 20), 2),
            "News": f"[{time.strftime('%H:%M')}] {symbol} reports strong earnings growth."
        }
        for symbol in SYMBOLS
    ]

# ======== NEWS FETCHER =========
def fetch_news(symbol):
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-01-01&to=2025-12-31&token={API_KEY}"
    try:
        news = requests.get(url).json()
        for item in news:
            if symbol in item.get("related", ""):
                ts = item.get("datetime", 0)
                dt = datetime.fromtimestamp(ts).strftime("%H:%M")
                headline = item.get("headline", "")
                return f"[{dt}] {headline}"
        return "No recent news"
    except:
        return "No recent news"

# ======== REAL DATA FETCHER =========
def fetch_real_data(symbol):
    base_url = f"https://finnhub.io/api/v1/"
    try:
        quote = requests.get(f"{base_url}quote?symbol={symbol}&token={API_KEY}").json()
        stats = requests.get(f"{base_url}stock/metric?symbol={symbol}&metric=all&token={API_KEY}").json()

        prev_close = quote.get("pc", 0)
        open_price = quote.get("o", 0)
        current = quote.get("c", 0)

        gap = ((open_price - prev_close) / prev_close * 100) if prev_close else 0
        change = ((current - prev_close) / prev_close * 100) if prev_close else 0

        def safe(val):
            return "--" if val == 0 else val

        return {
            "Gap %": round(gap, 2),
            "Symbol": symbol,
            "Price": round(current, 2),
            "Volume": safe(stats.get("metric", {}).get("volume", 0)),
            "Float (M)": safe(round(stats.get("metric", {}).get("sharesFloat", 0) / 1_000_000, 2)),
            "Relative Vol (Daily Rate)": safe(round(stats.get("metric", {}).get("10DayAverageTradingVolume", 0), 2)),
            "Relative Vol (5 Min %)": safe(round(stats.get("metric", {}).get("52WeekHigh", 0), 2)),  # Placeholder
            "Change From Close (%)": round(change, 2),
            "Short Interest": safe(int(stats.get("metric", {}).get("shortInterest", 0))),
            "Short Ratio": safe(round(stats.get("metric", {}).get("shortRatio", 0), 2)),
            "News": fetch_news(symbol)
        }
    except:
        return None

# ======== GET DATA =========
data = get_fake_data() if use_fake else list(filter(None, [fetch_real_data(s) for s in SYMBOLS]))

# ======== DISPLAY =========
if data:
    df = pd.DataFrame(data)
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)
    st.markdown(f"🕒 Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data to show. Check tickers or API usage.")

# ======== AUTO REFRESH =========
if auto_refresh:
    time.sleep(60)
    st.rerun()
