import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Bond Investment & FX Hedge Tool", layout="centered")
st.title("🇮🇳 INR Bond Investment FX Hedge Calculator")

st.markdown("""
This app helps you simulate:
- Investing in Indian bonds using **USD**
- Hedging with **USDINR futures**
- Understanding how currency movement affects your returns
""")

st.sidebar.header("1️⃣ Investment Details")
inr_investment = st.sidebar.number_input("INR Bond Investment Amount", min_value=100000, value=10000000, step=100000)
usdinr_entry = st.sidebar.number_input("USDINR Rate at Entry", min_value=60.0, max_value=100.0, value=85.0, step=0.5)
usdinr_exit = st.sidebar.number_input("USDINR Rate at Exit", min_value=60.0, max_value=100.0, value=90.0, step=0.5)

st.sidebar.header("2️⃣ Futures Details")
lot_size = 1000
margin_per_lot = 2150
usd_exposure = inr_investment / usdinr_entry
lots_needed = int(np.round(usd_exposure / lot_size))

st.sidebar.write(f"USD Exposure: ${usd_exposure:,.2f}")
st.sidebar.write(f"Hedge Lots Required: {lots_needed} lots")
total_margin = lots_needed * margin_per_lot
st.sidebar.write(f"Margin Required: ₹{total_margin:,.0f}")

st.header("📈 Simulation Result")

# Unhedged return
usd_return_unhedged = inr_investment / usdinr_exit

# Hedged return calculation
futures_pnl_inr = (usdinr_exit - usdinr_entry) * lot_size * lots_needed
inr_after_hedge = inr_investment + futures_pnl_inr
usd_return_hedged = inr_after_hedge / usdinr_exit

st.subheader("Unhedged Scenario")
st.metric("USD Value (Unhedged)", f"${usd_return_unhedged:,.2f}", delta=f"{(usd_return_unhedged - usd_exposure):,.2f}")

st.subheader("Hedged Scenario")
st.metric("Futures P&L (INR)", f"₹{futures_pnl_inr:,.0f}")
st.metric("USD Value (Hedged)", f"${usd_return_hedged:,.2f}", delta=f"{(usd_return_hedged - usd_exposure):,.2f}")

# Chart for visual comparison
st.subheader("🔍 Visual Comparison")
st.bar_chart(pd.DataFrame({
    "USD Value": [usd_exposure, usd_return_unhedged, usd_return_hedged]
}, index=["Initial USD", "Unhedged", "Hedged"]))

st.markdown("---")
st.markdown("""
✅ **Tip**: You hedge by **going long USDINR futures** to protect against INR depreciation. 

ℹ️ This app assumes zero interest/coupon from the bond for simplicity. You can enhance it further by adding bond returns.
""")
