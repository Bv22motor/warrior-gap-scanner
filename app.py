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

# ======== UTILS =========
def null_guard(val, is_float=False):
    return round(val, 2) if isinstance(val, (int, float)) and val != 0 else "--" if is_float else "--"

def format_news_tooltip(news):
    if not news:
        return "--"
    short = news[:57] + "..." if len(news) > 60 else news
    return f'<span title="{news}">{short}</span>'

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
            "Change From Close (%)": round(random.uniform(-20, 20), 2),
            "Short Interest": random.randint(0, 50_000_000),
            "Short Ratio": round(random.uniform(0.1, 20), 2),
            "News": f"[{time.strftime('%H:%M')}] {symbol} reports strong earnings growth."
        }
        for symbol in SYMBOLS
    ]

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

        # Get latest headline
        if news and isinstance(news, list) and len(news) > 0:
            headline = news[0].get("headline", "")
            ts = news[0].get("datetime", 0)
            news_time = time.strftime('%H:%M', time.localtime(ts))
            news_text = f"[{news_time}] {headline}"
        else:
            news_text = "No recent news"

        return {
            "Gap %": round(gap, 2),
            "Symbol": symbol,
            "Price": null_guard(current, True),
            "Volume": null_guard(stats.get("metric", {}).get("volume")),
            "Float (M)": null_guard(stats.get("metric", {}).get("sharesFloat") / 1_000_000 if stats.get("metric", {}).get("sharesFloat") else 0, True),
            "Relative Vol (Daily Rate)": null_guard(stats.get("metric", {}).get("10DayAverageTradingVolume")),
            "Relative Vol (5 Min %)": null_guard(stats.get("metric", {}).get("52WeekHigh")),  # Placeholder
            "Change From Close (%)": round(change, 2),
            "Short Interest": null_guard(stats.get("metric", {}).get("shortInterest")),
            "Short Ratio": null_guard(stats.get("metric", {}).get("shortRatio"), True),
            "News": format_news_tooltip(news_text)
        }
    except Exception as e:
        return None

# ======== GET DATA =========
data = get_fake_data() if use_fake else list(filter(None, [fetch_real_data(s) for s in SYMBOLS]))

# ======== DISPLAY =========
if data:
    df = pd.DataFrame(data)
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)

    st.markdown(f"🕒 Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")
    st.markdown("<style>table td span {cursor: help;}</style>", unsafe_allow_html=True)
    st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
else:
    st.warning("No data to show. Check tickers or API usage.")

# ======== AUTO REFRESH =========
if auto_refresh:
    time.sleep(60)
    st.rerun()
