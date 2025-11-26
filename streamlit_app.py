# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import ast

# ----------------------------
# Load Data
# ----------------------------
def load_data():
    courses = pd.read_csv("data/synthetic/courses_with_predictions.csv")
    rooms = pd.read_csv("data/synthetic/rooms.csv")
    assignments = pd.read_csv("data/synthetic/assignments.csv")
    return courses, rooms, assignments

courses, rooms, assignments = load_data()

st.set_page_config(
    page_title="Smart University Resource Allocation System",
    layout="wide",
)

# -----------------------------------
# DARK THEME + FORCE WHITE TEXT CSS
# -----------------------------------
dark_theme = """
<style>
/* Ensure global text is white */
html, body, [class*="css"]  {
    color: #FFFFFF !important;
}

/* Main App Background */
[data-testid="stAppViewContainer"] > .main {
    background-color: #0E1117 !important;
    color: #FFFFFF !important;
}

/* Full App Background */
.stApp {
    background-color: #0E1117 !important;
    color: #FFFFFF !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #15171c !important;
    color: #FFFFFF !important;
    border-right: 1px solid #23252a !important;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}

/* Headings and text */
h1, h2, h3, h4, h5, label, p, span {
    color: #FFFFFF !important;
}

/* KPI card text (force both label and value to white) */
.stMetric > div:nth-child(1) {
    color: #FFFFFF !important; /* label */
    font-weight: 600 !important;
}
.stMetric > div:nth-child(2) {
    color: #FFFFFF !important; /* value */
    font-weight: 700 !important;
    font-size: 1.15em !important;
}

/* DataFrame text */
.stDataFrame, .dataframe, .css-1d391kg, .css-1w0yn3d {
    color: #FFFFFF !important;
}

/* Plotly container background */
.stPlotlyChart > div {
    background: transparent !important;
}
</style>
"""
st.markdown(dark_theme, unsafe_allow_html=True)

# -----------------------------------
# Plotly dark theme helper (force white for axis, ticks, titles)
# -----------------------------------
def apply_dark_theme(fig):
    fig.update_layout(
        template="plotly_dark",
        title_font_color="#FFFFFF",
        font_color="#FFFFFF",
        legend_title_font_color="#FFFFFF",
        legend_font_color="#FFFFFF",
        xaxis=dict(
            color="#FFFFFF",
            tickfont=dict(color="#FFFFFF"),
            title_font=dict(color="#FFFFFF"),
            gridcolor="#2b2b2b",
        ),
        yaxis=dict(
            color="#FFFFFF",
            tickfont=dict(color="#FFFFFF"),
            title_font=dict(color="#FFFFFF"),
            gridcolor="#2b2b2b",
        ),
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        margin=dict(l=20, r=20, t=60, b=40),
    )
    # if colorbar exists, ensure its title is white
    try:
        fig.update_coloraxes(colorbar=dict(title=dict(font=dict(color="#FFFFFF"))))
    except Exception:
        pass
    return fig

# Academic color palette
PALETTE = {
    "teal": "#4DD0E1",
    "blue": "#4A90E2",
    "emerald": "#2ECC71"
}

# ----------------------------
# Sidebar Navigation (simple)
# ----------------------------
st.sidebar.title("Dashboard Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Course Demand Forecast", "Room Assignment", "Utilization Analytics"]
)

# ----------------------------
# Overview Page
# ----------------------------
if page == "Overview":

    st.markdown("<h1>Smart University Resource Allocation & Scheduling System</h1>", unsafe_allow_html=True)
    

    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Courses", len(courses))
    with col2:
        st.metric("Total Rooms", len(rooms))
    with col3:
        st.metric("Avg Predicted Enrollment", round(courses["predicted_students"].mean(), 2))
    with col4:
        success_rate = len(assignments[assignments["room_id"].notna()]) / max(1, len(assignments))
        st.metric("Assignment Success Rate", f"{success_rate*100:.1f}%")

    st.markdown("---")

    # Charts side by side
    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            courses,
            x="predicted_students",
            title="Predicted Enrollment Distribution",
            nbins=20,
            color_discrete_sequence=[PALETTE["teal"]]
        )
        st.plotly_chart(apply_dark_theme(fig), use_container_width=True)

    with c2:
        fig = px.histogram(
            rooms,
            x="capacity",
            title="Room Capacity Distribution",
            nbins=15,
            color_discrete_sequence=[PALETTE["blue"]]
        )
        st.plotly_chart(apply_dark_theme(fig), use_container_width=True)

# ----------------------------
# Course Demand Forecast
# ----------------------------
elif page == "Course Demand Forecast":

    st.markdown("<h2>Course Demand Forecasting</h2>", unsafe_allow_html=True)

    st.markdown("### Predicted Enrollments")
    st.dataframe(courses)

    st.markdown("### Predicted vs Historical Enrollment")

    def safe_hist_mean(val):
        try:
            arr = ast.literal_eval(val)
            return float(np.mean(arr)) if len(arr) > 0 else 0.0
        except Exception:
            return 0.0

    # compute hist_mean for display
    courses["hist_mean"] = courses["historical_enrollment"].apply(safe_hist_mean)

    fig = px.scatter(
        courses,
        x="hist_mean",
        y="predicted_students",
        hover_name="course_name",
        title="Historical Mean vs Predicted Enrollment",
        color_discrete_sequence=[PALETTE["blue"]],
    )
    fig.update_traces(marker=dict(size=8, line=dict(width=0.5, color="#0b0b0b")))
    st.plotly_chart(apply_dark_theme(fig), use_container_width=True)

# ----------------------------
# Room Assignment Page
# ----------------------------
elif page == "Room Assignment":

    st.markdown("<h2>Optimized Room Assignment</h2>", unsafe_allow_html=True)
    st.markdown("### All Assignments")
    st.dataframe(assignments)

    st.markdown("### Rooms Used vs Unused")
    usage = assignments.groupby("room_id").size().reset_index(name="count")
    usage = usage.merge(rooms[["room_id", "capacity"]], on="room_id", how="right").fillna(0)

    fig = px.bar(
        usage.sort_values("count", ascending=False),
        x="room_id",
        y="count",
        title="Room Usage Count",
        labels={"count": "Courses Assigned"},
        color="count",
        color_continuous_scale=[PALETTE["teal"], PALETTE["blue"]],
    )
    st.plotly_chart(apply_dark_theme(fig), use_container_width=True)

# ----------------------------
# Utilization Analytics
# ----------------------------
elif page == "Utilization Analytics":

    st.markdown("<h2>Resource Utilization Analytics</h2>", unsafe_allow_html=True)

    st.markdown("### Room Utilization (%)")
    assignments_count = assignments.groupby("room_id").size().reset_index(name="assigned")
    merged = rooms.merge(assignments_count, on="room_id", how="left").fillna(0)
    merged["utilization"] = merged.apply(lambda r: r["assigned"] / r["capacity"] if r["capacity"] > 0 else 0.0, axis=1)

    fig = px.bar(
        merged.sort_values("utilization", ascending=False),
        x="room_id",
        y="utilization",
        title="Room Utilization Percentage",
        color="utilization",
        color_continuous_scale=[PALETTE["emerald"], PALETTE["teal"], PALETTE["blue"]],
        range_y=[0, 1],
    )
    st.plotly_chart(apply_dark_theme(fig), use_container_width=True)

    st.markdown("### Timeslot Demand")
    ts_demand = assignments.groupby("timeslot").size().reset_index(name="count")

    fig = px.bar(
        ts_demand.sort_values("count", ascending=False),
        x="timeslot",
        y="count",
        title="Demand per Timeslot",
        color="count",
        color_continuous_scale=[PALETTE["teal"], PALETTE["blue"]],
    )
    st.plotly_chart(apply_dark_theme(fig), use_container_width=True)
