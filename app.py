from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from scripts.seed_data import OUTPUT, main as seed_data


st.set_page_config(page_title="Product Retention Analytics", layout="wide")


FUNNEL = ["signup", "session_start", "view_feature", "activation", "checkout_start", "purchase"]


def ensure_data():
    if not OUTPUT.exists():
        seed_data()
    return pd.read_csv(OUTPUT, parse_dates=["event_time"])


def build_funnel(events):
    base = events.groupby("event_name")["user_id"].nunique().reindex(FUNNEL).fillna(0).astype(int)
    funnel = base.reset_index()
    funnel.columns = ["stage", "users"]
    funnel["conversion_from_signup"] = funnel["users"] / max(funnel.loc[0, "users"], 1)
    funnel["step_conversion"] = funnel["users"] / funnel["users"].shift(1).replace(0, pd.NA)
    funnel.loc[0, "step_conversion"] = 1
    return funnel


def build_retention(events):
    first_seen = events.groupby("user_id")["event_time"].min().rename("signup_time")
    active = events[events["event_name"].isin(["session_start", "activation", "purchase"])].merge(first_seen, on="user_id")
    active["cohort"] = active["signup_time"].dt.to_period("M").astype(str)
    active["period"] = ((active["event_time"] - active["signup_time"]).dt.days // 30).clip(lower=0, upper=5)
    cohort = active.groupby(["cohort", "period"])["user_id"].nunique().unstack(fill_value=0)
    cohort_size = cohort[0].replace(0, pd.NA)
    retention = cohort.divide(cohort_size, axis=0).fillna(0)
    return retention


def churn_table(events):
    last_seen = events.groupby("user_id").agg(
        last_seen=("event_time", "max"),
        plan=("plan", "last"),
        channel=("acquisition_channel", "last"),
    )
    as_of = events["event_time"].max()
    last_seen["days_since_seen"] = (as_of - last_seen["last_seen"]).dt.days
    last_seen["churn_risk"] = pd.cut(
        last_seen["days_since_seen"],
        bins=[-1, 14, 30, 60, 999],
        labels=["Healthy", "Watch", "At Risk", "Churned"],
    )
    return last_seen.reset_index()


events = ensure_data()
st.title("Product/User Behavior Analytics & Retention Analysis")
st.caption("Funnel, cohort, churn, retention, and journey analytics for product and growth analyst portfolios.")

with st.sidebar:
    st.header("Filters")
    channels = st.multiselect("Acquisition channel", sorted(events["acquisition_channel"].unique()), default=sorted(events["acquisition_channel"].unique()))
    plans = st.multiselect("Plan", sorted(events["plan"].unique()), default=sorted(events["plan"].unique()))

filtered = events[events["acquisition_channel"].isin(channels) & events["plan"].isin(plans)]
funnel = build_funnel(filtered)
retention = build_retention(filtered)
churn = churn_table(filtered)

d7 = retention[retention.columns[retention.columns >= 0]].iloc[:, :1].mean().iloc[0] if not retention.empty else 0
d30 = retention[1].mean() if 1 in retention.columns else 0
purchase_users = filtered[filtered["event_name"] == "purchase"]["user_id"].nunique()
total_users = filtered["user_id"].nunique()
churn_rate = (churn["churn_risk"].eq("Churned").mean() * 100) if len(churn) else 0

k1, k2, k3, k4 = st.columns(4)
k1.metric("Users", f"{total_users:,}")
k2.metric("Purchasers", f"{purchase_users:,}")
k3.metric("Month 1 Retention", f"{d30:.1%}")
k4.metric("Churned Users", f"{churn_rate:.1f}%")

tab_funnel, tab_cohort, tab_churn, tab_journey, tab_sql = st.tabs(["Funnel", "Cohorts", "Churn", "Journey", "SQL"])

with tab_funnel:
    st.subheader("Product Funnel")
    st.dataframe(funnel, use_container_width=True, hide_index=True)
    st.bar_chart(funnel, x="stage", y="users", height=330)

with tab_cohort:
    st.subheader("Cohort Retention Matrix")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.heatmap(retention, annot=True, fmt=".0%", cmap="YlGnBu", ax=ax)
    ax.set_xlabel("Months Since Signup")
    ax.set_ylabel("Signup Cohort")
    st.pyplot(fig, clear_figure=True)

with tab_churn:
    st.subheader("Churn Risk by Plan")
    risk = churn.groupby(["plan", "churn_risk"], observed=True)["user_id"].count().reset_index()
    st.dataframe(risk, use_container_width=True, hide_index=True)
    st.subheader("Users Needing Attention")
    st.dataframe(churn.sort_values("days_since_seen", ascending=False).head(50), use_container_width=True, hide_index=True)

with tab_journey:
    st.subheader("Common User Journey Paths")
    journeys = (
        filtered.sort_values("event_time")
        .groupby("user_id")["event_name"]
        .apply(lambda x: " > ".join(pd.Series(x).drop_duplicates().head(6)))
        .value_counts()
        .head(12)
        .reset_index()
    )
    journeys.columns = ["journey_path", "users"]
    st.dataframe(journeys, use_container_width=True, hide_index=True)

with tab_sql:
    st.subheader("SQL Analysis Examples")
    st.code(Path("sql/retention_queries.sql").read_text(encoding="utf-8"), language="sql")
