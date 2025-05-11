import streamlit as st
import pandas as pd
import finnhub
from datetime import datetime

# === Finnhub API Setup ===
api_key = "d0fhdbhr01qsv9ehhli0d0fhdbhr01qsv9ehhlig"  # 🔁 Replace this with your actual Finnhub API key
finnhub_client = finnhub.Client(api_key=api_key)

# === Streamlit Page Config ===
st.set_page_config(page_title="Warrior-Style Gap Scanner", layout="wide")
st.title("🚀 Warrior-Style Gap Scanner")

# === Session Toggle (Pre-market / Regular Market) ===
session_type = st.selectbox("Market Session", ["Pre-market", "Regular Market"])

# === Auto-refresh toggle ===
refresh = st.checkbox("Refreshing in 60 seconds...", value=True)
if refresh:
    st.experimental_rerun()

# === Simulated Symbol List (Can be replaced with live data feed)
symbols = ["APP", "CDNA", "RAMP", "DUOL", "ASTR", "QOCX", "AFRM"]

# === Gap Scanner Logic ===
def get_gap_data(symbols, session_type):
    data = []

    for symbol in symbols:
        try:
            quote = finnhub_client.quote(symbol)
            news = finnhub_client.company_news(symbol, _from="2025-05-10", to="2025-05-11")
            latest_news = news[0]["headline"] if news else "No recent news"

            current_price = quote.get("c", 0)
            previous_close = quote.get("pc", 0)

            # Calculate Gap %
            if session_type == "Pre-market":
                gap_percent = quote.get("dp", 0)  # Use premarket % if available
            else:
                gap_percent = ((current_price - previous_close) / previous_close * 100) if previous_close else 0

            data.append({
                "Gap %": round(gap_percent, 2),
                "Symbol": symbol,
                "Price": round(current_price, 2),
                "Volume": "--",  # Placeholder
                "Float (M)": "--",  # Placeholder
                "Relative Vol (Daily Rate)": "--",  # Placeholder
                "Relative Vol (5 Min %)": "--",  # Placeholder
                "Change From Close (%)": round(gap_percent, 2),
                "Short Interest": "--",  # Placeholder
                "Short Ratio": "--",  # Placeholder
                "News": latest_news
            })

        except Exception as e:
            data.append({
                "Gap %": "--",
                "Symbol": symbol,
                "Price": "--",
                "Volume": "--",
                "Float (M)": "--",
                "Relative Vol (Daily Rate)": "--",
                "Relative Vol (5 Min %)": "--",
                "Change From Close (%)": "--",
                "Short Interest": "--",
                "Short Ratio": "--",
                "News": f"Error: {str(e)}"
            })

    return pd.DataFrame(data)

# === Display Table ===
df = get_gap_data(symbols, session_type)
st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")
st.dataframe(df, use_container_width=True)
