
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Derby Model App", layout="wide")

st.title("🏇 Derby 2025 – Horse Racing Intelligence Model")
st.markdown("Upload your race data to see full model verdicts, stamina, pricing, and value insights.")

uploaded_file = st.file_uploader("Upload your race card CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📋 Full Model Output")
    st.dataframe(df, use_container_width=True)

    # Filters
    with st.expander("🔍 Filters"):
        trip = st.selectbox("Filter by Step-Up Suitability", ["All"] + sorted(df["Step-Up Suitability"].unique()))
        ground = st.selectbox("Filter by Softer Ground?", ["All"] + sorted(df["Softer Ground?"].unique()))
        pedigree = st.selectbox("Filter by Pedigree Stamina Flag", ["All"] + sorted(df["Pedigree Stamina Flag"].unique()))

        filtered_df = df.copy()
        if trip != "All":
            filtered_df = filtered_df[filtered_df["Step-Up Suitability"] == trip]
        if ground != "All":
            filtered_df = filtered_df[filtered_df["Softer Ground?"] == ground]
        if pedigree != "All":
            filtered_df = filtered_df[filtered_df["Pedigree Stamina Flag"] == pedigree]

        st.dataframe(filtered_df, use_container_width=True)

    st.subheader("🏆 Model Verdicts")

    if not df.empty:
        # Best horse based on highest Delta
        best_horse = df.sort_values(by="Delta", ascending=False).iloc[0]
        st.markdown(f"**🥇 Most Likely Winner:** `{best_horse['Horse']}` (Delta: {best_horse['Delta']})")
        st.markdown(f"**📊 Verdict:** {best_horse['Model Verdict']}")

        # Best value based on price cutoff
        df_sorted_by_value = df[df["Predicted Price"] <= 6.0].sort_values(by="Delta", ascending=False)
        if not df_sorted_by_value.empty:
            value_horse = df_sorted_by_value.iloc[0]
            st.markdown(f"**💰 Value Bet:** `{value_horse['Horse']}` — Bet if **over {value_horse['Predicted Price']}** (Model says: {value_horse['Value Cutoff']})")
            st.markdown(f"**📊 Verdict:** {value_horse['Model Verdict']}")

    st.subheader("📖 Full Verdicts")
    for i, row in df.iterrows():
        st.markdown(f"**{row['Horse']}** — {row['Model Verdict']} *(Value: {row['Value Cutoff']})*")

else:
    st.info("Please upload a CSV file to see the model in action.")
