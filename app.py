from pathlib import Path

import pandas as pd
import streamlit as st

from analytics import build_insights, build_player_summary
from generate_data import generate_player_sessions

st.set_page_config(page_title="Interactive Player Performance Monitoring Dashboard", page_icon="🎮", layout="wide")
st.title("Interactive Player Performance Monitoring Dashboard")
st.caption("A portfolio-ready prototype for serious-game analytics, player learning monitoring, and behavior insight generation.")

with st.container():
    st.markdown("### Overview")
    st.write(
        "This dashboard demonstrates how designers, instructors, and researchers can use analytics to monitor player performance, engagement, and learning progression in a serious-game environment."
    )
    st.write(
        "The experience combines interactive filtering, trend visualization, and comparison views so it is easy to identify which players are improving, which are disengaging, and which need support."
    )

st.markdown("---")

DATA_PATH = Path(__file__).resolve().parent / "data" / "player_sessions.csv"
REQUIRED_COLUMNS = {
    "player_id",
    "session_id",
    "score",
    "time_taken",
    "errors",
    "attempts",
    "engagement_score",
    "completion_rate",
    "learning_gain",
    "timestamp",
}


def ensure_data(path: Path) -> None:
    if path.exists():
        df_sample = pd.read_csv(path, nrows=0)
        if not REQUIRED_COLUMNS.issubset(df_sample.columns):
            st.warning("Existing data file is outdated. Regenerating demo data...")
            path.unlink()
            generate_player_sessions(path)
    else:
        st.info("Generating demo data...")
        generate_player_sessions(path)


ensure_data(DATA_PATH)

def load_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


df = load_data(DATA_PATH)

players = sorted(df["player_id"].unique())
with st.sidebar:
    st.header("Filters")
    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()
    date_range = st.date_input("Date range", [min_date, max_date])
selected_players = st.multiselect("Select player profiles", players, default=players)

filtered_df = df[df["player_id"].isin(selected_players)] if selected_players else df

if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date, end_date = date_range
    try:
        filtered_df = filtered_df[(filtered_df["timestamp"].dt.date >= start_date) & (filtered_df["timestamp"].dt.date <= end_date)]
    except Exception:
        filtered_df["timestamp"] = pd.to_datetime(filtered_df["timestamp"])
        filtered_df = filtered_df[(filtered_df["timestamp"].dt.date >= start_date) & (filtered_df["timestamp"].dt.date <= end_date)]

col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
col1.metric("Total sessions", len(filtered_df))
col2.metric("Mean score", f"{filtered_df['score'].mean():.1f}")
col3.metric("Mean engagement", f"{filtered_df['engagement_score'].mean():.1f}")
col4.metric("Mean completion", f"{filtered_df['completion_rate'].mean():.1f}")

st.markdown("---")

with st.sidebar:
    st.markdown("---")
    st.write("Export data: download the currently filtered dataset or a single player's sessions.")
    csv_bytes = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download filtered CSV", data=csv_bytes, file_name="player_sessions_filtered.csv", mime="text/csv")
    player_to_export = st.selectbox("Export single player", [""] + players)
    if player_to_export:
        player_df = filtered_df[filtered_df["player_id"] == player_to_export]
        player_csv = player_df.to_csv(index=False).encode("utf-8")
        st.download_button("Download player CSV", data=player_csv, file_name=f"{player_to_export}_sessions.csv", mime="text/csv")

with st.expander("Why this matters for serious games"):
    st.write("In serious games, monitoring player progress is useful because it can reveal whether the experience is supporting learning, engagement, and motivation. Dashboards can help designers and educators act on these signals.")

st.subheader("Score progression")
st.write("Track how each selected player evolves over time. Rising trajectories suggest stronger learning and confidence.")
chart_df = filtered_df.groupby(["player_id", "timestamp"], as_index=False)["score"].mean()
for player in selected_players or players:
    player_data = chart_df[chart_df["player_id"] == player]
    if not player_data.empty:
        st.line_chart(player_data.set_index("timestamp")["score"], width="stretch")

st.subheader("Engagement and completion")
st.write("Compare the average engagement and completion profiles of the selected players.")
engagement_plot = filtered_df[["player_id", "engagement_score", "completion_rate", "score"]].copy()
engagement_summary = engagement_plot.groupby("player_id", as_index=False).agg(
    avg_engagement=("engagement_score", "mean"),
    avg_completion=("completion_rate", "mean"),
    avg_score=("score", "mean"),
)
st.bar_chart(engagement_summary.set_index("player_id"), width="stretch")

st.subheader("Player comparison")
st.write("Compare selected players across score, engagement, completion, and estimated learning gain.")
comparison = build_player_summary(filtered_df)
comparison = comparison.rename(columns={
    "player_id": "Player",
    "avg_score": "Avg Score",
    "avg_errors": "Avg Errors",
    "avg_time": "Avg Time (s)",
    "avg_engagement": "Avg Engagement",
    "avg_completion": "Avg Completion",
    "avg_learning_gain": "Avg Learning Gain",
    "sessions": "Sessions"
})
comparison = comparison[["Player", "Sessions", "Avg Score", "Avg Engagement", "Avg Completion", "Avg Learning Gain", "Avg Errors", "Avg Time (s)"]]
st.dataframe(comparison, width="stretch")

st.subheader("Insights")
insights = build_insights(build_player_summary(filtered_df))
if insights["top_performer"] != "No data":
    st.success(f"Top improvement profile: {insights['top_performer']} with strong learning-gain performance across sessions.")
    st.info(f"Highest average engagement: {insights['highest_engagement']}.")
    st.caption(f"Most improved player signal: {insights['most_improved']}.")
else:
    st.info("Select at least one player to view insights.")
