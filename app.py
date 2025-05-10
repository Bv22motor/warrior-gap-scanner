import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# ========== CONFIG ==========
st.set_page_config(page_title="Gap Scanner", layout="wide")

API_KEY = "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"  # ← Replace with your actual Finnhub key
SYMBOLS = ["AAPL", "TSLA", "AMZN", "META", "MSFT", "NVDA", "AMD", "NFLX"]

# ========== OPTIONS ==========
st.markdown("## 🚀 Warrior-Style Gap Scanner")
fake_mode = st.toggle("🌟 Enable Fake Test Mode")
auto_refresh = st.checkbox("🔁 Refreshing in 60 seconds...")

# Timestamp
st.markdown(
    f"🕒 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)"
)

# ========== FETCH DATA ==========
def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    try:
        r = requests.get(url)
        return r.json()
    except:
        return {}

data = []

if fake_mode:
    for sym in SYMBOLS:
        data.append({
            "Symbol": sym,
            "Last Price": 104,
            "Open": 104,
            "Prev Close": 109,
            "Gap %": -4.59,
            "Change %": -4.59,
            "Float (M)": 200,
            "Avg Vol (M)": 50,
            "Short Float %": 5.1
        })
else:
    for sym in SYMBOLS:
        q = get_quote(sym)
        try:
            if q["pc"] == 0:
                continue
            gap = ((q["o"] - q["pc"]) / q["pc"]) * 100
            change = ((q["c"] - q["pc"]) / q["pc"]) * 100
            data.append({
                "Symbol": sym,
                "Last Price": q["c"],
                "Open": q["o"],
                "Prev Close": q["pc"],
                "Gap %": round(gap, 2),
                "Change %": round(change, 2),
                "Float (M)": 200,
                "Avg Vol (M)": 50,
                "Short Float %": 5.1
            })
        except:
            continue

df = pd.DataFrame(data)

# Only sort if the column exists and has data
if not df.empty and "Gap %" in df.columns:
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)

# Show table
st.dataframe(df, use_container_width=True)

# ========== AUTO REFRESH ==========
if auto_refresh:
    time.sleep(60)
    st.rerun()
