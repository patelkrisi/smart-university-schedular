# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os

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

# ----------------------------
# Sidebar Navigation
# ----------------------------
st.sidebar.title("📊 Dashboard Navigation")
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Course Demand Forecast", "Room Assignment", "Utilization Analytics"]
)

# ----------------------------
# Overview Page
# ----------------------------
if page == "Overview":

    st.title("🎓 Smart University Resource Allocation & Scheduling System")
    st.markdown("")
    st.markdown("")


    # KPIs
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Courses", len(courses))
    with col2:
        st.metric("Total Rooms", len(rooms))
    with col3:
        st.metric("Avg Predicted Enrollment", round(courses["predicted_students"].mean(), 2))
    with col4:
        success_rate = len(assignments[assignments["room_id"].notna()]) / len(assignments)
        st.metric("Assignment Success Rate", f"{success_rate*100:.1f}%")

    st.markdown("---")

    # Charts
    c1, c2 = st.columns(2)

    with c1:
        fig = px.histogram(
            courses,
            x="predicted_students",
            title="Predicted Enrollment Distribution",
            nbins=20,
            color_discrete_sequence=["#4A90E2"]
        )
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        fig = px.histogram(
            rooms,
            x="capacity",
            title="Room Capacity Distribution",
            nbins=15,
            color_discrete_sequence=["#50E3C2"]
        )
        st.plotly_chart(fig, use_container_width=True)


# ----------------------------
# Course Demand Forecast
# ----------------------------
elif page == "Course Demand Forecast":

    st.title("📈 Course Demand Forecasting")

    st.dataframe(courses)

    st.markdown("### Predicted vs. Historical Enrollment")
    courses["hist_mean"] = courses["historical_enrollment"].apply(lambda x: np.mean(eval(x)))

    fig = px.scatter(
        courses,
        x="hist_mean",
        y="predicted_students",
        hover_name="course_name",
        trendline="ols",
        title="Historical Mean vs Predicted Enrollment"
    )
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------
# Room Assignment Page
# ----------------------------
elif page == "Room Assignment":

    st.title("🏫 Optimized Room Assignment")

    st.dataframe(assignments)

    st.markdown("### Rooms Used vs Unused")

    usage = assignments.groupby("room_id").size().reset_index(name="count")
    usage = usage.merge(rooms[["room_id", "capacity"]], on="room_id", how="right").fillna(0)

    fig = px.bar(
        usage,
        x="room_id",
        y="count",
        title="Room Usage Count",
        labels={"count": "Courses Assigned"},
        color="count"
    )
    st.plotly_chart(fig, use_container_width=True)


# ----------------------------
# Utilization Analytics
# ----------------------------
elif page == "Utilization Analytics":

    st.title("📊 Resource Utilization Analytics")

    st.markdown("### Room Utilization (%)")

    assignments_count = assignments.groupby("room_id").size().reset_index(name="assigned")

    merged = rooms.merge(assignments_count, on="room_id", how="left").fillna(0)
    merged["utilization"] = merged["assigned"] / merged["capacity"]

    fig = px.bar(
        merged,
        x="room_id",
        y="utilization",
        title="Room Utilization Percentage",
        color="utilization",
        range_y=[0, 1],
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Timeslot Demand")
    ts_demand = assignments.groupby("timeslot").size().reset_index(name="count")

    fig = px.bar(
        ts_demand,
        x="timeslot",
        y="count",
        title="Demand per Timeslot",
        color="count"
    )
    st.plotly_chart(fig, use_container_width=True)
