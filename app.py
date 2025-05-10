import streamlit as st
import pandas as pd
from datetime import datetime
import time

# ======= FAKE TEST MODE =======
st.set_page_config(page_title="Top Gappers Scanner", layout="wide")
st.sidebar.markdown("🧪 **Enable Fake Test Mode**")
use_fake = st.sidebar.toggle("Enable Fake Test Mode", value=False)

# ======= SIMULATED DATA =======
def get_fake_data():
    return [
        {
            "Symbol": "ASTR", "Price": 2.5, "Volume": 8180000, "Float": 15.74,
            "Relative Vol (Daily Rate)": 2876.08, "Relative Vol (5 Min %)": 500720.16,
            "Change From Close (%)": 83.78, "Short Interest": 1830000, "Short Ratio": 3.48,
            "Prev Close": 1.36
        },
        {
            "Symbol": "CDNA", "Price": 70.68, "Volume": 2145000, "Float": 213.03,
            "Relative Vol (Daily Rate)": 0.48, "Relative Vol (5 Min %)": 29.13,
            "Change From Close (%)": 26.46, "Short Interest": 0, "Short Ratio": 0.0,
            "Prev Close": 55.9
        },
        {
            "Symbol": "QOCX", "Price": 1.36, "Volume": 10779000, "Float": 59.76,
            "Relative Vol (Daily Rate)": 140.7, "Relative Vol (5 Min %)": 6215.56,
            "Change From Close (%)": 14.51, "Short Interest": 1980000, "Short Ratio": 1.28,
            "Prev Close": 1.19
        },
        {
            "Symbol": "APP", "Price": 45.45, "Volume": 84550000, "Float": 183.98,
            "Relative Vol (Daily Rate)": 20.28, "Relative Vol (5 Min %)": 1943.8,
            "Change From Close (%)": 13.29, "Short Interest": 17480000, "Short Ratio": 8.97,
            "Prev Close": 40.14
        },
        {
            "Symbol": "AFRM", "Price": 24.65, "Volume": 56714000, "Float": 220.94,
            "Relative Vol (Daily Rate)": 4.09, "Relative Vol (5 Min %)": 415.51,
            "Change From Close (%)": 13.08, "Short Interest": 44590000, "Short Ratio": 3.52,
            "Prev Close": 21.81
        },
        {
            "Symbol": "RAMP", "Price": 33.91, "Volume": 5700000, "Float": 64.25,
            "Relative Vol (Daily Rate)": 237.5, "Relative Vol (5 Min %)": 686666.67,
            "Change From Close (%)": 12.37, "Short Interest": 1260000, "Short Ratio": 3.52,
            "Prev Close": 30.17
        },
        {
            "Symbol": "DUOL", "Price": 185.99, "Volume": 13670000, "Float": 37.39,
            "Relative Vol (Daily Rate)": 14.93, "Relative Vol (5 Min %)": 3044.47,
            "Change From Close (%)": 11.19, "Short Interest": 2360000, "Short Ratio": 4.11,
            "Prev Close": 167.27
        },
    ]

# ======= DATA HANDLING =======
data = get_fake_data() if use_fake else []

if data:
    df = pd.DataFrame(data)

    # Calculate Gap %
    df["Gap %"] = ((df["Price"] - df["Prev Close"]) / df["Prev Close"]) * 100
    df["Gap %"] = df["Gap %"].round(2)

    # Reorder columns so Gap % comes first
    cols = ["Gap %"] + [col for col in df.columns if col != "Gap %"]
    df = df[cols]

    # Sort by Gap % descending
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)

    # Remove internal 'Prev Close' column if not needed in view
    df.drop(columns=["Prev Close"], inplace=True)

# ======= UI DISPLAY =======
st.markdown("## 🚀 Warrior-Style Gap Scanner")
st.markdown(f"⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")
st.markdown("---")

if data:
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data available. Please enable Fake Test Mode.")

# ======= AUTO REFRESH =======
st.experimental_rerun = lambda: None  # override to silence warnings
time.sleep(60)
st.experimental_rerun()
