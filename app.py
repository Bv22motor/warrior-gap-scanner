import streamlit as st
import requests
import pandas as pd
import time
import random
import os

# ======== CONFIG =========
API_KEY = os.getenv("FINNHUB_API_KEY") or "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"
SYMBOLS = ["ASTR", "CDNA", "QOCX", "APP", "AFRM", "RAMP", "DUOL"]

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

# ======== CLEANER FORMAT =========
def safe_val(val, decimals=2):
    if val is None or val == 0:
        return "--"
    return round(val, decimals) if isinstance(val, (float, int)) else val

# ======== REAL DATA FETCHER =========
def fetch_real_data(symbol):
    base_url = "https://finnhub.io/api/v1/"
    try:
        quote = requests.get(f"{base_url}quote?symbol={symbol}&token={API_KEY}").json()
        stats = requests.get(f"{base_url}stock/metric?symbol={symbol}&metric=all&token={API_KEY}").json()
        news = requests.get(f"{base_url}company-news?symbol={symbol}&from=2024-01-01&to=2025-12-31&token={API_KEY}").json()

        prev_close = quote.get("pc", 0)
        open_price = quote.get("o", 0)
        current = quote.get("c", 0)

        gap = ((open_price - prev_close) / prev_close * 100) if prev_close else 0
        change = ((current - prev_close) / prev_close * 100) if prev_close else 0

        headline = "No recent news"
        if isinstance(news, list) and news:
            headline = f"[{news[0].get('datetime', '')}] {news[0].get('headline', '')[:80]}"

        return {
            "Gap %": safe_val(gap),
            "Symbol": symbol,
            "Price": safe_val(current),
            "Volume": safe_val(stats.get("metric", {}).get("volume", 0), 0),
            "Float (M)": safe_val(stats.get("metric", {}).get("sharesFloat", 0) / 1_000_000),
            "Relative Vol (Daily Rate)": safe_val(stats.get("metric", {}).get("10DayAverageTradingVolume", 0)),
            "Relative Vol (5 Min %)": safe_val(stats.get("metric", {}).get("52WeekHigh", 0)),
            "Change From Close (%)": safe_val(change),
            "Short Interest": safe_val(stats.get("metric", {}).get("shortInterest", 0), 0),
            "Short Ratio": safe_val(stats.get("metric", {}).get("shortRatio", 0)),
            "News": headline
        }
    except Exception as e:
        return None

# ======== GET DATA =========
data = get_fake_data() if use_fake else list(filter(None, [fetch_real_data(s) for s in SYMBOLS]))

# ======== DISPLAY =========
if data:
    df = pd.DataFrame(data)
    df = df.sort_values(by="Gap %", ascending=False, key=lambda x: pd.to_numeric(x, errors='coerce')).reset_index(drop=True)
    st.markdown(f"🕒 Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data to show. Check tickers or API usage.")

# ======== AUTO REFRESH =========
if auto_refresh:
    time.sleep(60)
    st.rerun()
