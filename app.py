from pathlib import Path

import pandas as pd
import streamlit as st

from generate_data import generate_player_sessions

st.set_page_config(page_title="Interactive Player Performance Monitoring Dashboard", page_icon="🎮", layout="wide")
st.title("Interactive Player Performance Monitoring Dashboard")
st.caption("A professional prototype for serious-game analytics and player progress monitoring.")

with st.container():
    st.markdown("### Overview")
    st.write(
        "This dashboard is designed to demonstrate how serious-game designers, instructors, and researchers can monitor player performance and engagement using actionable analytics."
    )
    st.write(
        "Use the controls to inspect individual profiles, compare key metrics, and identify which players are improving, engaged, and completing sessions effectively."
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
selected_players = st.multiselect("Select player profiles", players, default=players)

filtered_df = df[df["player_id"].isin(selected_players)] if selected_players else df

col1, col2, col3, col4 = st.columns([1.2, 1, 1, 1])
col1.metric("Total sessions", len(filtered_df))
col2.metric("Mean score", f"{filtered_df['score'].mean():.1f}")
col3.metric("Mean engagement", f"{filtered_df['engagement_score'].mean():.1f}")
col4.metric("Mean completion", f"{filtered_df['completion_rate'].mean():.1f}")

st.markdown("---")

with st.expander("Why this matters for serious games"):
    st.write("In serious games, monitoring player progress is useful because it can reveal whether the experience is supporting learning, engagement, and motivation. Dashboards can help designers and educators act on these signals.")

st.subheader("Score progression")
st.write("Track performance trends across sessions. Upward trends indicate learning improvement.")
chart_df = filtered_df.groupby(["player_id", "timestamp"], as_index=False)["score"].mean()
for player in selected_players or players:
    player_data = chart_df[chart_df["player_id"] == player]
    if not player_data.empty:
        st.line_chart(player_data.set_index("timestamp")["score"], width='stretch')

st.subheader("Engagement and completion")
st.write("Compare average engagement and completion rates for selected players.")
engagement_plot = filtered_df[["player_id", "engagement_score", "completion_rate", "score"]].copy()
engagement_summary = engagement_plot.groupby("player_id", as_index=False).agg(
    avg_engagement=("engagement_score", "mean"),
    avg_completion=("completion_rate", "mean"),
    avg_score=("score", "mean"),
)
st.bar_chart(engagement_summary.set_index("player_id"), width='stretch')

st.subheader("Player comparison")
st.write("Compare selected players across performance, engagement, completion and estimated learning gain.")
comparison = filtered_df.groupby("player_id", as_index=False).agg(
    avg_score=("score", "mean"),
    avg_errors=("errors", "mean"),
    avg_time=("time_taken", "mean"),
    avg_engagement=("engagement_score", "mean"),
    avg_completion=("completion_rate", "mean"),
    avg_learning_gain=("learning_gain", "mean"),
    sessions=("session_id", "count"),
)
comparison = comparison.sort_values("avg_learning_gain", ascending=False)
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
st.dataframe(comparison, width='stretch')

st.subheader("Insights")
if not comparison.empty:
    top_player = comparison.iloc[0]
    high_eng_player = comparison.loc[comparison['Avg Engagement'].idxmax()]
    st.success(f"Top improvement profile: {top_player['Player']} with average learning gain of {top_player['Avg Learning Gain']:.1f}.")
    st.info(f"Highest average engagement: {high_eng_player['Player']} ({high_eng_player['Avg Engagement']:.1f}).")
