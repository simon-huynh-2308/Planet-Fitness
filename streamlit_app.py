pip install streamlit pandas matplotlib plotly
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load dataset
df = pd.read_csv("Regenerated_Planet_Fitness_KPI_Dataset.csv")

# Sidebar filter
selected_location = st.sidebar.selectbox("Select Location", ["All"] + sorted(df["Location"].unique().tolist()))

# Filter data
filtered_df = df if selected_location == "All" else df[df["Location"] == selected_location]

st.title("Planet Fitness Dashboard: Customer Satisfaction & Operational Efficiency")
st.markdown("""
This dashboard helps regional managers assess customer satisfaction trends and equipment maintenance issues to support marketing and operational decisions.
""")

# --- NPS Stacked Bar Chart ---
st.header("Net Promoter Score (NPS) by Location")
nps_df = df[["Location", "NPS_Promoters", "NPS_Passives", "NPS_Detractors"]].set_index("Location")
nps_df = nps_df.sort_index()
nps_chart = px.bar(nps_df, 
                  x=nps_df.index, 
                  y=["NPS_Promoters", "NPS_Passives", "NPS_Detractors"],
                  labels={"value": "Count", "variable": "NPS Category"},
                  title="NPS Breakdown by Location",
                  barmode="stack")
st.plotly_chart(nps_chart)

# --- Churn Rate ---
st.header("Monthly Churn Rate")
st.subheader("Churn by Location")
churn_chart = px.bar(filtered_df, 
                    x="Location", 
                    y="Monthly_Churn_Rate (%)", 
                    title="Churn Rate by Location")
st.plotly_chart(churn_chart)

# --- Satisfaction Score ---
st.header("Average Satisfaction Score")
sat_score = filtered_df["Avg_Satisfaction_Score (1-10)"].mean()
gauge_fig = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = sat_score,
    title = {"text": "Avg Satisfaction Score"},
    gauge = {"axis": {"range": [0, 10]},
             "bar": {"color": "darkblue"}}
))
st.plotly_chart(gauge_fig)

# --- Equipment Downtime ---
st.header("Equipment Downtime (hrs/month)")
bar_chart = px.bar(filtered_df, 
                   x="Location", 
                   y="Equipment_Downtime (hrs/month)", 
                   title="Monthly Equipment Downtime")
st.plotly_chart(bar_chart)

st.subheader("Color-Coded Downtime Table")
def color_downtime(val):
    if val < 30:
        return 'background-color: lightgreen'
    elif val < 50:
        return 'background-color: khaki'
    else:
        return 'background-color: lightcoral'

styled_df = filtered_df[["Location", "Equipment_Downtime (hrs/month)"]].style.applymap(color_downtime, subset=["Equipment_Downtime (hrs/month)"])
st.dataframe(styled_df, use_container_width=True)

st.markdown("---")
st.caption("Dashboard by Khanh Huynh | Data Mining Class | Streamlit")

