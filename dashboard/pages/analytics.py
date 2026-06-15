import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time
from dashboard_utils import load_sensor_data, load_daily_summary

st.set_page_config(page_title="Analytics & Reports", page_icon="📊", layout="wide")

st.title("📊 Analytics & Deep Insights")
st.markdown("Analyze historical summaries and compute multi-day environmental statistics.")

df_summary = load_daily_summary()
df_sensors = load_sensor_data()

if df_summary.empty:
    st.info("No daily summaries logged yet. Perform operations or run simulations to generate daily reports.")
else:
    # Sort summary by date
    df_summary = df_summary.sort_values("date")
    
    st.subheader("🗓️ Daily Summary Log")
    st.dataframe(df_summary, use_container_width=True)

    st.markdown("---")
    st.subheader("📈 Historical Trends")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        # Temperature summary chart
        fig_temp = go.Figure()
        fig_temp.add_trace(go.Scatter(x=df_summary["date"], y=df_summary["avg_temperature"], mode="lines+markers", name="Avg Temp", line=dict(color="#E74C3C")))
        fig_temp.add_trace(go.Scatter(x=df_summary["date"], y=df_summary["max_temperature"], mode="lines", name="Max Temp", line=dict(color="#C0392B", dash="dash")))
        fig_temp.update_layout(
            title="Temperature Historical Range",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig_temp, use_container_width=True)

    with col_g2:
        # Moisture summary chart
        fig_soil = go.Figure()
        fig_soil.add_trace(go.Scatter(x=df_summary["date"], y=df_summary["avg_soil_moisture"], mode="lines+markers", name="Avg Soil Moisture", line=dict(color="#27AE60")))
        fig_soil.add_trace(go.Scatter(x=df_summary["date"], y=df_summary["min_soil_moisture"], mode="lines", name="Min Soil Moisture", line=dict(color="#1E8449", dash="dash")))
        fig_soil.update_layout(
            title="Soil Moisture Historical Range",
            xaxis_title="Date",
            yaxis_title="Moisture (%)",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig_soil, use_container_width=True)

    col_g3, col_g4 = st.columns(2)

    with col_g3:
        # Alert Count
        fig_alerts = px.bar(
            df_summary,
            x="date",
            y="alert_count",
            title="Alerts Generated per Day",
            labels={"alert_count": "Number of Alerts", "date": "Date"},
            color_discrete_sequence=["#E67E22"]
        )
        fig_alerts.update_layout(template="plotly_white")
        st.plotly_chart(fig_alerts, use_container_width=True)

    with col_g4:
        # Pump Activations
        fig_pump = px.bar(
            df_summary,
            x="date",
            y="pump_activations",
            title="Pump Activations per Day",
            labels={"pump_activations": "Activations Count", "date": "Date"},
            color_discrete_sequence=["#2980B9"]
        )
        fig_pump.update_layout(template="plotly_white")
        st.plotly_chart(fig_pump, use_container_width=True)

# Auto refresh
time.sleep(5)
st.rerun()
