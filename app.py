import streamlit as st
import requests
import pandas as pd
import os

# ========== CONFIG ==========
API_KEY = os.getenv("FINNHUB_API_KEY") or "d0fhdhbr01qsy9ehhli0d0fhdhbr01qsy9ehhlig"

SYMBOLS = ["NVDA", "META", "MSFT", "AMD", "NFLX", "GME", "SPY"]

st.set_page_config(page_title="Gap Scanner", layout="wide")
st.title("🚀 Warrior-Style Gap Scanner")

def get_quote(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
    r = requests.get(url)
    return r.json()

data = []

for symbol in SYMBOLS:
    quote = get_quote(symbol)
    if "pc" not in quote or quote["pc"] == 0:
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

df = pd.DataFrame(data)

if not df.empty:
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data available. Check ticker symbols or wait for market hours.")
