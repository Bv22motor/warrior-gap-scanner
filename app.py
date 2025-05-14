import streamlit as st
import pandas as pd
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# === Load API Key from .env ===
load_dotenv()
API_KEY = os.getenv("d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig")
REFRESH_INTERVAL = 60  # seconds

# === Sidebar toggle ===
st.sidebar.toggle("Enable Fake Test Mode", key="fake_mode", value=False)
fake_mode = st.session_state.fake_mode

# === Header ===
st.title("🚀 Warrior-Style Gap Scanner")
st.caption(f"📅 Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every {REFRESH_INTERVAL}s)")

# === Functions ===
def get_gappers():
    if fake_mode:
        return pd.read_csv("mock_data.csv")  # Optional CSV for offline testing

    # Get US symbols
    url = f"https://finnhub.io/api/v1/stock/symbol?exchange=US&token={API_KEY}"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("Failed to fetch stock symbols.")
        return pd.DataFrame()

    all_symbols = response.json()
    tickers = [item["symbol"] for item in all_symbols if item["type"] == "Common Stock"]

    data = []

    for symbol in tickers[:50]:  # limit for testing
        try:
            quote = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}").json()
            stats = requests.get(f"https://finnhub.io/api/v1/stock/metric?symbol={symbol}&metric=all&token={API_KEY}").json()
            news = requests.get(f"https://finnhub.io/api/v1/company-news?symbol={symbol}&from={datetime.now().strftime('%Y-%m-%d')}&to={datetime.now().strftime('%Y-%m-%d')}&token={API_KEY}").json()

            price = quote.get("c")
            prev_close = quote.get("pc")

            if not price or not prev_close:
                continue

            gap_pct = ((price - prev_close) / prev_close) * 100

            data.append({
                "Gap %": round(gap_pct, 2),
                "Symbol": symbol,
                "Price": round(price, 2),
                "Volume": stats.get("metric", {}).get("volume", "--"),
                "Float (M)": round(float(stats.get("metric", {}).get("float", 0)) / 1e6, 2) if stats.get("metric", {}).get("float") else "--",
                "Relative Vol (Daily Rate)": round(stats.get("metric", {}).get("10DayAvgVolume", 0) / stats.get("metric", {}).get("volume", 1), 2) if stats.get("metric", {}).get("volume") else "--",
                "Relative Vol (5 Min %)": round(stats.get("metric", {}).get("volatility", 0), 2) if stats.get("metric", {}).get("volatility") else "--",
                "Change From Close (%)": round((price - prev_close) / prev_close * 100, 2),
                "Short Interest": stats.get("metric", {}).get("shortInterest", "--"),
                "Short Ratio": stats.get("metric", {}).get("shortRatio", "--"),
                "News": news[0]["headline"] if news else "No recent news"
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")

    df = pd.DataFrame(data)
    df = df.sort_values(by="Gap %", ascending=False)
    return df

# === Main Display ===
with st.spinner("Fetching data..."):
    df = get_gappers()
    st.dataframe(df, use_container_width=True)

# === Auto refresh ===
st.experimental_rerun()
