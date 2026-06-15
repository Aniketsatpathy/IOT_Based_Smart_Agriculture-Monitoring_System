import plotly.graph_objects as go

def create_line_chart(df, y_col, title, color, y_label):
    """
    Helper to generate a styled interactive line chart with a smooth spline curve.
    """
    if df.empty or y_col not in df.columns:
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis={"visible": False},
            yaxis={"visible": False},
            annotations=[{
                "text": "No data available",
                "xref": "paper",
                "yref": "paper",
                "showarrow": False,
                "font": {"size": 16}
            }],
            height=250
        )
        return fig

    # Sort by timestamp to ensure chronological order
    df_sorted = df.sort_values("timestamp")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_sorted["timestamp"],
        y=df_sorted[y_col],
        mode="lines",
        line=dict(color=color, width=2.5, shape="spline"),
        name=y_col.replace("_", " ").title(),
        hovertemplate="<b>Time:</b> %{x|%Y-%m-%d %H:%M:%S}<br><b>Value:</b> %{y:.1f}<extra></extra>"
    ))

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=16, color="#2C3E50", family="Outfit, Arial, sans-serif")
        ),
        xaxis=dict(
            title="Time",
            gridcolor="#EAECEE",
            linecolor="#BDC3C7",
            showgrid=True,
            showline=True
        ),
        yaxis=dict(
            title=y_label,
            gridcolor="#EAECEE",
            linecolor="#BDC3C7",
            showgrid=True,
            showline=True
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode="x unified",
        height=280
    )
    return fig

def create_temperature_chart(df):
    return create_line_chart(df, "temperature", "Temperature Trend", "#E74C3C", "Temperature (°C)")

def create_humidity_chart(df):
    return create_line_chart(df, "humidity", "Humidity Trend", "#9B59B6", "Humidity (%)")

def create_soil_moisture_chart(df):
    return create_line_chart(df, "soil_moisture", "Soil Moisture Trend", "#27AE60", "Soil Moisture (%)")

def create_water_level_chart(df):
    return create_line_chart(df, "water_level", "Water Level Trend", "#2980B9", "Water Level (%)")

def create_light_intensity_chart(df):
    return create_line_chart(df, "light_intensity", "Light Intensity Trend", "#F1C40F", "Light Intensity (%)")
