from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st


DATA_PATH = Path("data/online_shoppers_intention.csv")

st.set_page_config(page_title="Product Behavior Analytics", layout="wide")


@st.cache_data
def load_sessions():
    data = pd.read_csv(DATA_PATH)
    bool_cols = ["weekend", "revenue"]
    for col in bool_cols:
        data[col] = data[col].astype(bool)
    data["total_pages"] = data["administrative"] + data["informational"] + data["productrelated"]
    data["total_duration"] = (
        data["administrative_duration"]
        + data["informational_duration"]
        + data["productrelated_duration"]
    )
    data["engagement_band"] = pd.cut(
        data["total_pages"],
        bins=[-1, 2, 8, 20, 999],
        labels=["Low", "Medium", "High", "Power"],
    )
    return data


def rate(value):
    return f"{value:.2%}"


def conversion_summary(data, group_col):
    return (
        data.groupby(group_col, observed=True)
        .agg(
            sessions=("session_id", "count"),
            conversions=("revenue", "sum"),
            conversion_rate=("revenue", "mean"),
            avg_page_value=("pagevalues", "mean"),
            avg_exit_rate=("exitrates", "mean"),
            avg_bounce_rate=("bouncerates", "mean"),
        )
        .reset_index()
        .sort_values("conversion_rate", ascending=False)
    )


sessions = load_sessions()

st.title("Product/User Behavior Analytics Dashboard")
st.caption(
    "Built on the UCI Online Shoppers Purchasing Intention dataset. "
    "This session-level dataset is ideal for conversion behavior, funnel proxy, traffic analysis, and engagement diagnostics."
)

with st.sidebar:
    st.header("Filters")
    months = st.multiselect("Month", sorted(sessions["month"].unique()), default=sorted(sessions["month"].unique()))
    visitor_types = st.multiselect(
        "Visitor type",
        sorted(sessions["visitortype"].unique()),
        default=sorted(sessions["visitortype"].unique()),
    )
    weekend_choice = st.selectbox("Weekend", ["All", "Weekend only", "Weekday only"])

filtered = sessions[sessions["month"].isin(months) & sessions["visitortype"].isin(visitor_types)]
if weekend_choice == "Weekend only":
    filtered = filtered[filtered["weekend"]]
elif weekend_choice == "Weekday only":
    filtered = filtered[~filtered["weekend"]]

sessions_count = len(filtered)
conversions = int(filtered["revenue"].sum())
conversion_rate = filtered["revenue"].mean() if sessions_count else 0
avg_pages = filtered["total_pages"].mean() if sessions_count else 0
avg_duration = filtered["total_duration"].mean() if sessions_count else 0
bounce_rate = filtered["bouncerates"].mean() if sessions_count else 0
exit_rate = filtered["exitrates"].mean() if sessions_count else 0

k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Sessions", f"{sessions_count:,}")
k2.metric("Conversions", f"{conversions:,}")
k3.metric("Conversion Rate", rate(conversion_rate))
k4.metric("Avg Pages", f"{avg_pages:.1f}")
k5.metric("Avg Duration", f"{avg_duration:,.0f}s")
k6.metric("Bounce Rate", rate(bounce_rate))

tab_funnel, tab_segments, tab_behavior, tab_sql = st.tabs(
    ["Funnel Proxy", "Segments", "Behavior Diagnostics", "SQL"]
)

with tab_funnel:
    st.subheader("Session Funnel Proxy")
    funnel = pd.DataFrame(
        [
            {"stage": "All Sessions", "sessions": sessions_count},
            {"stage": "Product Browsing", "sessions": int((filtered["productrelated"] > 0).sum())},
            {"stage": "High Engagement", "sessions": int((filtered["total_pages"] >= 8).sum())},
            {"stage": "Page Value Present", "sessions": int((filtered["pagevalues"] > 0).sum())},
            {"stage": "Converted", "sessions": conversions},
        ]
    )
    funnel["rate_from_total"] = funnel["sessions"] / max(sessions_count, 1)
    st.dataframe(funnel, width="stretch", hide_index=True)
    st.bar_chart(funnel, x="stage", y="sessions", height=330)

with tab_segments:
    left, right = st.columns(2)
    with left:
        st.subheader("Conversion by Visitor Type")
        st.dataframe(conversion_summary(filtered, "visitortype"), width="stretch", hide_index=True)
    with right:
        st.subheader("Conversion by Traffic Type")
        st.dataframe(conversion_summary(filtered, "traffictype"), width="stretch", hide_index=True)

    st.subheader("Conversion by Engagement Band")
    st.dataframe(conversion_summary(filtered, "engagement_band"), width="stretch", hide_index=True)

with tab_behavior:
    st.subheader("Behavior Drivers")
    fig, ax = plt.subplots(figsize=(9, 5))
    sns.boxplot(data=filtered, x="revenue", y="pagevalues", ax=ax)
    ax.set_xlabel("Converted")
    ax.set_ylabel("Page Value")
    ax.set_title("Page Value Distribution by Conversion Outcome")
    st.pyplot(fig, clear_figure=True)

    st.subheader("Month-Level Conversion Trend")
    month = conversion_summary(filtered, "month")
    st.dataframe(month, width="stretch", hide_index=True)

    st.subheader("High Exit / High Bounce Sessions")
    risk = filtered.sort_values(["exitrates", "bouncerates"], ascending=False).head(50)
    st.dataframe(risk, width="stretch", hide_index=True)

with tab_sql:
    st.subheader("SQL Analysis Examples")
    st.code(Path("sql/retention_queries.sql").read_text(encoding="utf-8"), language="sql")
