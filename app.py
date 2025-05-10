import streamlit as st
import requests
import pandas as pd
import os
import time
from datetime import datetime

# ========== CONFIG ==========
API_KEY = os.getenv("FINNHUB_API_KEY") or "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"

# List of tickers to scan
SYMBOLS = ["AAPL", "TSLA", "AMZN", "NVDA", "MSFT", "META", "AMD", "NFLX"]

# === UI Header ===
st.set_page_config(page_title="Gap Scanner", layout="wide")
st.title("🚀 Warrior-Style Gap Scanner")

# === Fake Mode Toggle ===
use_fake_data = st.toggle("🧪 Enable Fake Test Mode", value=False)

# === Auto-refresh ===
REFRESH_INTERVAL = 60  # in seconds
countdown = st.empty()

# === Timestamp ===
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.caption(f"🕒 Last Updated: {timestamp} (auto-refresh every {REFRESH_INTERVAL}s)")

# === Fetch Data ===
def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    r = requests.get(url)
    return r.json()

# === Build Data Table ===
data = []

if use_fake_data:
    # 🧪 Fake data (static values)
    for symbol in SYMBOLS:
        data.append({
            "Symbol": symbol,
            "Last Price": 100 + len(symbol),
            "Open": 105 + len(symbol),
            "Prev Close": 95 + len(symbol),
            "Gap %": round(((105 + len(symbol)) - (95 + len(symbol))) / (95 + len(symbol)) * 100, 2),
            "Change %": round(((100 + len(symbol)) - (95 + len(symbol))) / (95 + len(symbol)) * 100, 2),
        })
else:
    for symbol in SYMBOLS:
        quote = get_quote(symbol)
        if "pc" not in quote or "o" not in quote or "c" not in quote:
            continue
        if quote["pc"] == 0:
            continue
        gap_pct = ((quote["o"] - quote["pc"]) / quote["pc"]) * 100
        change_pct = ((quote["c"] - quote["pc"]) / quote["pc"]) * 100
        data.append({
            "Symbol": symbol,
            "Last Price": quote["c"],
            "Open": quote["o"],
            "Prev Close": quote["pc"],
            "Gap %": round(gap_pct, 2),
            "Change %": round(change_pct, 2)
        })

# === Show Table ===
df = pd.DataFrame(data)

if not df.empty:
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data available. Check ticker symbols or wait for market hours.")

# === Countdown auto-refresh ===
import streamlit.runtime.scriptrunner.script_run_context as context
import threading

def rerun():
    ctx = context.get_script_run_ctx()
    threading.Thread(target=lambda: st._runtime._rerun(ctx)).start()

for i in range(REFRESH_INTERVAL, 0, -1):
    countdown.markdown(f"🔁 Refreshing in **{i} seconds**...")
    time.sleep(1)

rerun()
