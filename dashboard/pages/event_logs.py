import streamlit as st
import pandas as pd
import time
from dashboard_utils import load_recent_events

st.set_page_config(page_title="Event Log Center", page_icon="📜", layout="wide")

st.title("📜 Recent Event Logs")
st.markdown("View a sequence of important operations, state changes, and system alerts.")

# Sidebar search
st.sidebar.subheader("Filter Events")
search_query = st.sidebar.text_input("Search Event Description", "")

# Load last 100 events for detailed view
events = load_recent_events(limit=100)

# Filter events if query is provided
if search_query:
    events = [e for e in events if search_query.lower() in e[1].lower()]

st.markdown(f"Showing **{len(events)}** recent events matching your search.")

if events:
    # Display in a clean vertical timeline format
    for time_str, event_desc in events:
        # Determine icons
        icon = "⚪"
        color = "#555"
        
        if "Alert" in event_desc:
            if "High" in event_desc or "Low Soil" in event_desc:
                icon = "🔴"
                color = "#C62828"
            else:
                icon = "🟡"
                color = "#F57F17"
        elif "Activated" in event_desc:
            icon = "🟢"
            color = "#2E7D32"
        elif "Deactivated" in event_desc:
            icon = "⚫"
            color = "#333"
        elif "Reconnected" in event_desc or "connected" in event_desc.lower():
            icon = "🔵"
            color = "#1565C0"

        st.markdown(f"""
            <div style="border-left: 3px solid {color}; padding-left: 15px; margin-bottom: 15px;">
                <span style="font-weight: bold; color: {color};">{time_str}</span><br/>
                <span style="font-size: 16px;">{icon} {event_desc}</span>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("No recent events match the search query or log file is empty.")

# Auto refresh
time.sleep(5)
st.rerun()
