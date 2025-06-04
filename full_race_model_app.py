
import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO

st.set_page_config(page_title="Derby Model & Value Finder", layout="wide")

st.title("🏇 Horse Racing Model – Odds, Verdicts & Value Flags")

st.markdown("This app integrates your full racing model with live or simulated odds, full verdicts, and form logic.")

# Simulated data for testing
data = {
    "Horse": ["Galileo's Dream", "Storm Signal", "Velvet Monarch", "Desert Light", "King's Intent"],
    "Speed": [75, 68, 72, 80, 70],
    "RanTo": [88, 70, 78, 82, 69],
    "Step-Up Suitability": ["✅ Yes", "⚠️ Maybe", "✅ Yes", "❌ No", "⚠️ Maybe"],
    "Pedigree Stamina Flag": ["✅", "⚠️", "✅", "❌", "⚠️"],
    "Softer Ground?": ["✅ Yes", "⚠️ Maybe", "✅ Yes", "❌ No", "⚠️ Maybe"],
    "Form Recency": ["1–3m", "0–1m", "3–6m", "1–3m", "1–3m"],
    "Trainer Travel (mi)": [152, 45, 231, 88, 112],
    "Direction Match": ["✅", "✅", "❌", "✅", "✅"],
    "Betfair Odds": [6.0, 9.5, 4.5, 3.0, 8.0],
}

df = pd.DataFrame(data)
df["Delta"] = df["RanTo"] - df["Speed"]

def generate_verdict(row):
    v = []
    if row["Step-Up Suitability"] == "✅ Yes":
        v.append("🆙 Should improve for step up.")
    if row["Pedigree Stamina Flag"] == "✅":
        v.append("🧬 Pedigree supports trip.")
    if row["Softer Ground?"] == "✅ Yes":
        v.append("🌧️ Handles softer ground.")
    if row["Trainer Travel (mi)"] > 150:
        v.append("🚛 Travelled far – positive intent.")
    if row["Delta"] > 10:
        v.append("⚡ RanTo spike – horse ready to pop.")
    return " ".join(v)

def fair_price(delta):
    if delta >= 12:
        return 3.0
    elif delta >= 9:
        return 5.0
    elif delta >= 6:
        return 7.0
    elif delta >= 3:
        return 10.0
    return 15.0

df["Model Verdict"] = df.apply(generate_verdict, axis=1)
df["Fair Price"] = df["Delta"].apply(fair_price)
df["Value Bet?"] = np.where(df["Betfair Odds"] > df["Fair Price"], "💰 YES", "—")

# Display main table
st.subheader("📊 Racecard View")
st.dataframe(df, use_container_width=True)

# Top Picks
top = df.sort_values(by="Delta", ascending=False)
best = top.iloc[0]
st.subheader("🏆 Model Verdicts")
st.markdown(f"**🥇 Most Likely Winner:** `{best['Horse']}` — {best['Model Verdict']}")
value_bets = df[df["Value Bet?"] == "💰 YES"]
if not value_bets.empty:
    vb = value_bets.sort_values(by="Delta", ascending=False).iloc[0]
    st.markdown(f"**💰 Value Pick:** `{vb['Horse']}` — Back if over **{vb['Fair Price']}** (currently {vb['Betfair Odds']})")

# Export to CSV
st.subheader("⬇️ Download Model Data")
csv = df.to_csv(index=False).encode('utf-8')
st.download_button("Download Full Model CSV", data=csv, file_name="race_model_output.csv", mime="text/csv")
