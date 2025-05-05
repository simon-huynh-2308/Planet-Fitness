import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import datetime as dt

# Load dataset
df = pd.read_csv("Regenerated_Planet_Fitness_KPI_Dataset.csv")

# Sidebar filters
selected_location = st.sidebar.selectbox("Select Location", ["All"] + sorted(df["Location"].unique().tolist()))
satisfaction_threshold = st.sidebar.slider("Minimum Satisfaction Score", 6.0, 10.0, 7.0, 0.1)
show_equipment_table = st.sidebar.checkbox("Show Detailed Equipment Table", value=True)

# Filter data based on user inputs
filtered_df = df if selected_location == "All" else df[df["Location"] == selected_location]
filtered_df = filtered_df[filtered_df["Avg_Satisfaction_Score (1-10)"] >= satisfaction_threshold]

# Filter Summary
st.markdown(f"**Viewing Data for:** `{selected_location}`  |  **Min Satisfaction Score:** `{satisfaction_threshold}`")

# KPI Summary Cards
st.subheader("📊 Key Metrics Overview")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Avg NPS Score", f"{df['NPS_Score'].mean():.1f}")
with col2:
    st.metric("Avg Churn Rate", f"{df['Monthly_Churn_Rate (%)'].mean():.2f}%")
with col3:
    st.metric("Avg Equipment Downtime", f"{df['Equipment_Downtime (hrs/month)'].mean():.2f} hrs")

st.title("Planet Fitness Dashboard: Customer Satisfaction & Operational Efficiency")
st.markdown("""
This dashboard helps regional managers assess customer satisfaction trends and equipment maintenance issues to support marketing and operational decisions.
""")

# NPS Chart
with st.expander("Net Promoter Score (NPS) by Location", expanded=True):
    nps_df = df[["Location", "NPS_Promoters", "NPS_Passives", "NPS_Detractors"]].set_index("Location")
    nps_df = nps_df.sort_index()
    nps_chart = px.bar(nps_df, 
                      x=nps_df.index, 
                      y=["NPS_Promoters", "NPS_Passives", "NPS_Detractors"],
                      labels={"value": "Count", "variable": "NPS Category"},
                      title="NPS Breakdown by Location",
                      barmode="stack")
    st.plotly_chart(nps_chart)

# Churn Trend
with st.expander("Monthly Churn Rate Trend", expanded=False):
    months = pd.date_range(end=dt.datetime.today(), periods=6, freq='M')
    trend_data = pd.DataFrame({
        "Month": months,
        "Churn Rate (%)": np.random.uniform(2.0, 9.0, size=6).round(2)
    })
    churn_trend_chart = px.line(trend_data, x="Month", y="Churn Rate (%)", markers=True, title="Churn Rate Over Last 6 Months")
    st.plotly_chart(churn_trend_chart)

# Satisfaction Score
with st.expander("Average Satisfaction Score", expanded=False):
    sat_score = filtered_df["Avg_Satisfaction_Score (1-10)"].mean()
    gauge_fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = sat_score,
        title = {"text": "Avg Satisfaction Score"},
        gauge = {"axis": {"range": [0, 10]},
                 "bar": {"color": "darkblue"}}
    ))
    st.plotly_chart(gauge_fig)

# Alerts
    if sat_score < 7.0:
        st.warning("⚠️ Warning: Average satisfaction is below acceptable level.")
    if filtered_df["Monthly_Churn_Rate (%)"].mean() > 6.0:
        st.error("🚨 High churn rate detected. Investigate retention strategies.")

# Equipment Downtime
with st.expander("Equipment Downtime", expanded=False):
    bar_chart = px.bar(filtered_df, 
                       x="Location", 
                       y="Equipment_Downtime (hrs/month)", 
                       title="Monthly Equipment Downtime")
    st.plotly_chart(bar_chart)

    if show_equipment_table:
        st.subheader("Color-Coded Downtime Table")
        def color_downtime(val):
            val_float = float(val)
            if val_float < 30:
                return 'background-color: lightcoral'
            elif val_float < 50:
                return 'background-color: khaki'
            else:
                return 'background-color: lightgreen'

        formatted_df = filtered_df[["Location", "Equipment_Downtime (hrs/month)"]].copy()
        formatted_df["Equipment_Downtime (hrs/month)"] = formatted_df["Equipment_Downtime (hrs/month)"].map(lambda x: f"{x:.2f}")
        styled_df = formatted_df.style.applymap(color_downtime, subset=["Equipment_Downtime (hrs/month)"])
        st.dataframe(styled_df, use_container_width=True)


st.markdown("---")
st.caption("Dashboard by Khanh Huynh | Data Mining Class | Streamlit")


