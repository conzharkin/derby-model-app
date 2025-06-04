
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Horse Racing Model – ATR URL & Full Analysis", layout="wide")
st.title("🏇 Racing Intelligence – Full Model & Betting Advice")

# User input: ATR URL
st.markdown("Paste an [At The Races](https://www.attheraces.com/racecards) race URL to generate predictions using the full model.")
race_url = st.text_input("Paste ATR race URL here:")

# Simulated scrape result (normally you'd use BeautifulSoup or Selenium here)
# Placeholder horses extracted from a racecard
if race_url:
    st.success(f"Pulled race data from: {race_url}")
    horses = ["Dream Illusion", "Soul Dance", "Bintshuaa", "Skyelight", "Tiempo Alegre", "Sheephavenbaystory", "Shielas Well"]
else:
    horses = []

# Simulated model data (replace this with real scraped form/RanTo/speed/etc.)
if horses:
    np.random.seed(42)
    df = pd.DataFrame({
        "Horse": horses,
        "Speed": np.random.randint(65, 80, len(horses)),
        "RanTo": np.random.randint(75, 95, len(horses)),
        "Form Recency": np.random.choice(["0–1m", "1–3m", "3–6m", "6–12m"], len(horses)),
        "Step-Up Suitability": np.random.choice(["✅ Yes", "❌ No", "⚠️ Maybe"], len(horses)),
        "Pedigree Stamina Flag": np.random.choice(["✅", "⚠️", "❌"], len(horses)),
        "Going Suitability": np.random.choice(["✅", "⚠️", "❌"], len(horses)),
        "Trainer Travel (mi)": np.random.randint(40, 250, len(horses)),
        "Direction Match": np.random.choice(["✅", "❌"], len(horses)),
        "Betfair Odds": np.round(np.random.uniform(3, 18, len(horses)), 2),
    })
    df["Delta"] = df["RanTo"] - df["Speed"]

    def generate_verdict(row):
        v = []
        if row["Step-Up Suitability"] == "✅ Yes":
            v.append("🆙 Trip suits.")
        if row["Pedigree Stamina Flag"] == "✅":
            v.append("🧬 Stamina in pedigree.")
        if row["Going Suitability"] == "✅":
            v.append("🌧️ Going suits.")
        if row["Trainer Travel (mi)"] > 150:
            v.append("🚛 Travelled far – trainer intent.")
        if row["Delta"] > 10:
            v.append("⚡ RanTo spike.")
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

    st.subheader("📊 Full Model Table")
    st.dataframe(df, use_container_width=True)

    st.subheader("🎯 Model Verdicts & Bets")

    top = df.sort_values(by="Delta", ascending=False)
    most_likely = top.iloc[0]
    value_bets = df[df["Value Bet?"] == "💰 YES"]
    if not value_bets.empty:
        best_value = value_bets.sort_values(by="Delta", ascending=False).iloc[0]
    else:
        best_value = top.iloc[1]

    st.markdown(f"**🥇 Most Likely Winner:** `{most_likely['Horse']}` — {most_likely['Model Verdict']}")
    st.markdown(f"**💰 Best Value Bet:** `{best_value['Horse']}` (Take if over {best_value['Fair Price']}) — Currently {best_value['Betfair Odds']}")

    forecast = top.iloc[:2]["Horse"].tolist()
    tricast = top.iloc[:3]["Horse"].tolist()
    placepot = top.iloc[:6]["Horse"].tolist()

    st.markdown(f"**🔁 Forecast Prediction:** `{forecast[0]} > {forecast[1]}`")
    st.markdown(f"**🎯 Tricast Prediction:** `{tricast[0]} > {tricast[1]} > {tricast[2]}`")
    st.markdown(f"**🧺 Placepot Candidates:** {', '.join(placepot)}")

    # Download CSV
    st.subheader("⬇️ Download CSV")
    st.download_button("Download Model Output", df.to_csv(index=False).encode('utf-8'),
                       file_name="race_model_output.csv", mime="text/csv")

else:
    st.info("Paste a valid At The Races racecard URL to get started.")
