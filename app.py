import streamlit as st
import requests
import pandas as pd
import time
import random
import os

# === CONFIG ===
API_KEY = os.getenv("FINNHUB_API_KEY") or "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"
SYMBOLS = ["ASTR", "CDNA", "QOCX", "APP", "AFRM", "RAMP", "DUOL"]

st.set_page_config(page_title="Warrior Dashboard", layout="wide")
st.title("🧭 Warrior-Style Trading Dashboard")

# === OPTIONS ===
tab1, tab2 = st.tabs(["📊 Gap Scanner", "📰 News Room"])
use_fake = st.sidebar.toggle("✨ Enable Fake Test Mode", value=False)
auto_refresh = st.sidebar.checkbox("🔁 Refreshing in 60 seconds...", value=True)

# === HELPERS ===
def null_guard(val, is_float=False):
    return round(val, 2) if isinstance(val, (int, float)) and val != 0 else "--" if is_float else "--"

def fetch_news(symbol):
    url = f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from=2024-01-01&to={time.strftime('%Y-%m-%d')}&token={API_KEY}"
    try:
        res = requests.get(url)
        news_data = res.json()
        return news_data[:3]  # Top 3
    except:
        return []

# === GAP SCANNER TAB ===
with tab1:
    st.header("📊 Warrior-Style Gap Scanner")
    
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

    def fetch_real_data(symbol):
        try:
            quote = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}").json()
            stats = requests.get(f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={API_KEY}").json()
            news = fetch_news(symbol)
            news_str = f"[{news[0]['datetime']}] {news[0]['headline']}" if news else "No recent news"

            prev_close = quote.get("pc", 0)
            open_price = quote.get("o", 0)
            current = quote.get("c", 0)
            gap = ((open_price - prev_close) / prev_close * 100) if prev_close else 0
            change = ((current - prev_close) / prev_close * 100) if prev_close else 0

            return {
                "Gap %": round(gap, 2),
                "Symbol": symbol,
                "Price": round(current, 2),
                "Volume": null_guard(stats.get("metric", {}).get("volume"), True),
                "Float (M)": null_guard(stats.get("metric", {}).get("sharesFloat") / 1_000_000, True),
                "Relative Vol (Daily Rate)": null_guard(stats.get("metric", {}).get("10DayAverageTradingVolume"), True),
                "Relative Vol (5 Min %)": null_guard(stats.get("metric", {}).get("52WeekHigh"), True),  # Placeholder
                "Change From Close (%)": round(change, 2),
                "Short Interest": null_guard(stats.get("metric", {}).get("shortInterest")),
                "Short Ratio": null_guard(stats.get("metric", {}).get("shortRatio"), True),
                "News": news_str
            }
        except:
            return None

    data = get_fake_data() if use_fake else list(filter(None, [fetch_real_data(s) for s in SYMBOLS]))

    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)
        st.markdown(f"🕒 Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("No data to show. Check tickers or API usage.")

# === AUTO REFRESH ===
if auto_refresh:
    time.sleep(60)
    st.rerun()

# === NEWS ROOM TAB ===
with tab2:
    st.header("📰 Warrior-Style News Room (Clickable Tickers)")
    for sym in SYMBOLS:
        st.subheader(f"🔎 {sym} — [View Chart](https://www.tradingview.com/symbols/{sym})")
        news_items = fetch_news(sym)
        if not news_items:
            st.info("No recent news.")
            continue
        for item in news_items:
            dt = time.strftime('%H:%M', time.localtime(item["datetime"]))
            st.markdown(f"**[{dt}] {item['headline']}**")

   
