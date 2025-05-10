import streamlit as st
import pandas as pd
from datetime import datetime

# ========== CONFIG ==========
st.set_page_config(page_title="Top Gappers Scanner", layout="wide")

# ========== TEST MODE ==========
fake_mode = st.sidebar.toggle("🚀 Enable Fake Test Mode")

# ========== FAKE DATA (For Test Mode) ==========
FAKE_DATA = [
    {"symbol": "ASTR", "price": 2.5, "volume": 8180000, "float": 15.74, "rel_vol_daily": 2876.08,
     "rel_vol_5min": 500720.16, "change": 83.78, "short_interest": 1830000, "short_ratio": 3.48, "short_float": 12.4, "prev_close": 1.36},
    {"symbol": "CDNA", "price": 70.68, "volume": 2145000, "float": 213.03, "rel_vol_daily": 0.48,
     "rel_vol_5min": 29.13, "change": 26.46, "short_interest": 0, "short_ratio": 0, "short_float": 3.2, "prev_close": 55.9},
    {"symbol": "QOCX", "price": 1.36, "volume": 10779000, "float": 59.76, "rel_vol_daily": 140.7,
     "rel_vol_5min": 6215.56, "change": 14.51, "short_interest": 1980000, "short_ratio": 1.28, "short_float": 8.9, "prev_close": 1.19},
    {"symbol": "APP", "price": 45.45, "volume": 84550000, "float": 183.98, "rel_vol_daily": 20.28,
     "rel_vol_5min": 1943.8, "change": 13.29, "short_interest": 17480000, "short_ratio": 8.97, "short_float": 5.1, "prev_close": 40.17},
    {"symbol": "AFRM", "price": 24.65, "volume": 56714000, "float": 220.94, "rel_vol_daily": 4.09,
     "rel_vol_5min": 415.51, "change": 13.08, "short_interest": 44590000, "short_ratio": 3.52, "short_float": 6.3, "prev_close": 21.8},
    {"symbol": "RAMP", "price": 33.91, "volume": 5700000, "float": 64.25, "rel_vol_daily": 237.5,
     "rel_vol_5min": 686666.67, "change": 12.37, "short_interest": 1260000, "short_ratio": 3.52, "short_float": 2.2, "prev_close": 30.2},
    {"symbol": "DUOL", "price": 185.99, "volume": 13670000, "float": 37.39, "rel_vol_daily": 14.93,
     "rel_vol_5min": 3044.47, "change": 11.19, "short_interest": 2360000, "short_ratio": 4.11, "short_float": 4.8, "prev_close": 167.3},
]

# ========== DATA FETCH ==========
data = []
if fake_mode:
    for d in FAKE_DATA:
        gap_pct = ((d["price"] - d["prev_close"]) / d["prev_close"]) * 100
        data.append({
            "Gap %": round(gap_pct, 2),
            "Symbol": d["symbol"],
            "Price": d["price"],
            "Volume": d["volume"],
            "Float (M)": d["float"],
            "Relative Vol (Daily Rate)": d["rel_vol_daily"],
            "Relative Vol (5 Min %)": d["rel_vol_5min"],
            "Change From Close (%)": d["change"],
            "Short Interest": d["short_interest"],
            "Short Ratio": d["short_ratio"],
            "Short Float %": d["short_float"]
        })
else:
    st.warning("Live mode not connected. Please enable Fake Test Mode for now.")

# ========== UI ==========
st.markdown("""<h1 style='font-size: 40px;'>🚀 Warrior-Style Gap Scanner</h1>""", unsafe_allow_html=True)
st.caption(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (auto-refresh every 60s)")

if data:
    df = pd.DataFrame(data)
    df = df.sort_values(by="Gap %", ascending=False).reset_index(drop=True)
    st.dataframe(df, use_container_width=True)
else:
    st.info("No data available.")
