import streamlit as st
import pandas as pd
import finnhub
from datetime import datetime
import time

# === Finnhub API Setup ===
api_key = "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"
finnhub_client = finnhub.Client(api_key=api_key)

# === App UI ===
st.set_page_config(page_title="Warrior-Style Gap Scanner", layout="wide")
st.title("🚀 Warrior-Style Gap Scanner")

# Session Toggle
session = st.selectbox("Market Session", ["Pre-market", "Regular Market"])

# Refresh toggle
refresh_rate = 60
refresh_enabled = st.checkbox("Refreshing in 60 seconds...", value=True)
if refresh_enabled:
    st.experimental_rerun()

# Symbol List (replace with your screener logic or top gappers)
symbols = ["APP", "CDNA", "RAMP", "DUOL", "ASTR", "QOCX", "AFRM"]

# === Data Fetching Function ===
def get_gap_data(symbols, session_type):
    rows = []

    for sym in symbols:
        try:
            quote = finnhub_client.quote(sym)
            news = finnhub_client.company_news(sym, _from="2025-05-10", to="2025-05-11")
            latest_news = news[0]["headline"] if news else "No recent news"

            current_price = quote["c"]
            previous_close = quote["pc"]
            premarket_price = quote["dp"]  # Optional, if available from another source

            # Calculate Gap %
            if session_type == "Pre-market":
                gap_percent = quote["dp"]  # Use premarket % if available
            else:
                gap_percent = ((current_price - previous_close) / previous_close) * 100 if previous_close else 0

            rows.append({
                "Gap %": round(gap_percent, 2),
                "Symbol": sym,
                "Price": round(current_price, 2),
                "Volume": "--",  # Add later if needed
                "Float (M)": "--",
                "Relative Vol (Daily Rate)": "--",
                "Relative Vol (5 Min %)": "--",
                "Change From Close (%)": round(gap_percent, 2),
                "Short Interest": "--",
                "Short Ratio": "--",
                "News": latest_news
            })
        except Exception as e:
            print(f"Error fetching for {sym}: {e}")
    return pd.DataFrame(rows)

# === Display Table ===
data = get_gap_data(symbols, session)
st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")
st.dataframe(data, use_container_width=True)
