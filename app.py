import streamlit as st
import pandas as pd
import requests
import time
import random
from datetime import datetime

# ======================== CONFIG ========================
API_KEY = st.secrets["FINNHUB_API_KEY"] if "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig" in st.secrets else "your_fallback_key_here"
SYMBOLS = ["TSLA", "AAPL", "META", "AMZN", "MSFT", "AMD", "NVDA", "NFLX"]
REFRESH_INTERVAL = 60  # seconds

# ================ PAGE CONFIG =================
st.set_page_config(page_title="Gap Scanner", layout="wide")

# ================== UI ======================
st.title("🚀 Warrior-Style Gap Scanner")
fake_mode = st.sidebar.toggle("Enable Fake Test Mode")

st.caption(f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every {REFRESH_INTERVAL}s)")

# =================== FUNCTIONS ======================
def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    r = requests.get(url)
    return r.json() if r.status_code == 200 else {}

def get_float(symbol):
    url = f"https://finnhub.io/api/v1/stock/profile2?symbol={symbol}&token={API_KEY}"
    r = requests.get(url)
    return r.json().get("shareOutstanding", 0)

def get_volume(symbol):
    url = f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={API_KEY}"
    r = requests.get(url)
    return r.json().get("metric", {}).get("10DayAverageTradingVolume", 0)

# ==================== DATA =======================
data = []

for symbol in SYMBOLS:
    if fake_mode:
        last = round(random.uniform(100, 200), 2)
        open_ = round(last * random.uniform(0.98, 1.02), 2)
        prev = round(last * random.uniform(0.98, 1.02), 2)
        gap = round(((open_ - prev) / prev) * 100, 2)
        change = round(((last - prev) / prev) * 100, 2)
        float_m = round(random.uniform(5, 300), 2)
        avg_vol = round(random.uniform(1, 100), 2)
    else:
        quote = get_quote(symbol)
        if not quote or "pc" not in quote or quote["pc"] == 0:
            continue
        last = quote.get("c", 0)
        open_ = quote.get("o", 0)
        prev = quote.get("pc", 0)
        gap = round(((open_ - prev) / prev) * 100, 2)
        change = round(((last - prev) / prev) * 100, 2)
        float_m = round(get_float(symbol), 2)
        avg_vol = round(get_volume(symbol) / 1_000_000, 2)

    data.append({
        "Symbol": symbol,
        "Last Price": last,
        "Open": open_,
        "Prev Close": prev,
        "Gap %": gap,
        "Change %": change,
        "Float (M)": float_m,
        "Avg Vol (M)": avg_vol
    })

# ================== DISPLAY ========================
df = pd.DataFrame(data)
df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)
st.dataframe(df, use_container_width=True)

# ================== AUTO REFRESH =====================
if not fake_mode:
    st.experimental_rerun = st.experimental_rerun if hasattr(st, "experimental_rerun") else lambda: None
    st.caption(f"🔁 Refreshing in {REFRESH_INTERVAL} seconds...")
    time.sleep(REFRESH_INTERVAL)
    st.experimental_rerun()
