import streamlit as st
import pandas as pd
import time

# ===================== CONFIG =====================
st.set_page_config(page_title="Top Gappers Scanner", layout="wide")

# Fake/test mode switch
use_fake_data = st.sidebar.toggle("💡 Enable Fake Test Mode", value=True)

# Auto-refresh every 60 seconds
refresh_interval = 60
countdown_placeholder = st.empty()
timestamp_placeholder = st.empty()

# ========== FAKE DATA (for testing only) ==========
@st.cache_data
def load_fake_data():
    data = [
        ["ASTR", 2.50, 8180000, 15.74, 2876.08, 500720.16, 83.78, 1830000, 3.48],
        ["CDNA", 70.68, 21450000, 213.03, 0.48, 29.13, 26.46, 0, 0.0],
        ["QOCX", 1.36, 10779000, 59.76, 140.70, 6215.56, 14.51, 1980000, 1.28],
        ["APP", 45.45, 84550000, 183.98, 20.28, 1943.80, 13.29, 17480000, 8.97],
        ["AFRM", 24.65, 56714000, 220.94, 4.09, 415.51, 13.08, 44590000, 3.52],
        ["RAMP", 33.91, 5700000, 64.25, 237.50, 686666.67, 12.37, 1260000, 3.52],
        ["DUOL", 185.99, 13670000, 37.39, 14.93, 3044.47, 11.19, 2360000, 4.11],
    ]
    columns = [
        "Symbol", "Price", "Volume", "Float (M)", "Relative Vol (Daily Rate)",
        "Relative Vol (5 Min %)", "Change From Close (%)", "Short Interest", "Short Ratio"
    ]
    return pd.DataFrame(data, columns=columns)

# ========== LIVE DATA FETCHING PLACEHOLDER ==========
def get_live_data():
    # Placeholder function; integrate your API logic here
    return load_fake_data()

# ===================== MAIN =====================
# Timer
def countdown(seconds):
    for remaining in range(seconds, 0, -1):
        countdown_placeholder.markdown(f"\u23F3 Refreshing in **{remaining} seconds**...")
        time.sleep(1)

# Data selection based on toggle
df = load_fake_data() if use_fake_data else get_live_data()

# Timestamp update
timestamp_placeholder.markdown(
    f"\u23F0 Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every {refresh_interval}s)"
)

# Sort and display table
df_sorted = df.sort_values(by="Change From Close (%)", ascending=False).reset_index(drop=True)
st.dataframe(df_sorted, use_container_width=True)

# Auto-refresh loop if live mode is used
if not use_fake_data:
    countdown(refresh_interval)
    st.rerun()

