import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

st.set_page_config(page_title="Gap Scanner", layout="wide")

# ========== CONFIG ==========
API_KEY = st.secrets["FINNHUB_API_KEY"] if "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig" in st.secrets else "YOUR_BACKUP_API_KEY_HERE"

SYMBOLS = ["TSLA", "AAPL", "META", "AMZN", "MSFT", "AMD", "NVDA", "NFLX"]
FAKE_MODE = st.sidebar.toggle("🚀 Enable Fake Test Mode", value=False)
REFRESH_INTERVAL = 60


st.title("🚀 Warrior-Style Gap Scanner")

# ========== FETCH FUNCTIONS ==========
def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    r = requests.get(url)
    return r.json()

def get_metrics(symbol):
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={API_KEY}"
    r = requests.get(url)
    return r.json().get("metric", {})

# ========== MAIN TABLE BUILD ==========
data = []

for symbol in SYMBOLS:
    if FAKE_MODE:
        quote = {"c": 104, "o": 104, "pc": 109}
        metrics = {
            "sharesFloat": 200_000_000,
            "10DayAverageTradingVolume": 50_000_000,
            "shortPercentFloat": 5.1
        }
    else:
        quote = get_quote(symbol)
        if quote.get("pc") == 0 or quote.get("c") is None:
            continue
        metrics = get_metrics(symbol)

    gap_pct = ((quote["o"] - quote["pc"]) / quote["pc"]) * 100
    change_pct = ((quote["c"] - quote["pc"]) / quote["pc"]) * 100

    float_shares = metrics.get("sharesFloat", 0)
    avg_vol = metrics.get("10DayAverageTradingVolume", 0)
    short_float = metrics.get("shortPercentFloat", 0)

    data.append({
        "Symbol": symbol,
        "Last Price": quote["c"],
        "Open": quote["o"],
        "Prev Close": quote["pc"],
        "Gap %": round(gap_pct, 2),
        "Change %": round(change_pct, 2),
        "Float (M)": round(float_shares / 1e6, 2),
        "Avg Vol (M)": round(avg_vol / 1e6, 2),
        "Short Float %": round(short_float, 2)
    })

# ========== DISPLAY ==========
if data:
    df = pd.DataFrame(data)
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)
    st.markdown(f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every {REFRESH_INTERVAL}s)")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("⚠️ No data available. Check ticker symbols or wait for market hours.")

# ========== AUTO-REFRESH ==========
countdown = st.empty()
for i in range(REFRESH_INTERVAL, 0, -1):
    countdown.markdown(f"🔁 Refreshing in **{i} seconds**...")
    time.sleep(1)

st.rerun()
