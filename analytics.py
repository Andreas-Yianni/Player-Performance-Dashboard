from __future__ import annotations

import pandas as pd


def build_player_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = df.groupby("player_id", as_index=False).agg(
        sessions=("session_id", "count"),
        avg_score=("score", "mean"),
        avg_engagement=("engagement_score", "mean"),
        avg_completion=("completion_rate", "mean"),
        avg_learning_gain=("learning_gain", "mean"),
        avg_errors=("errors", "mean"),
        avg_time=("time_taken", "mean"),
    )
    return summary.sort_values("avg_learning_gain", ascending=False).reset_index(drop=True)


def build_insights(summary: pd.DataFrame) -> dict[str, str]:
    if summary.empty:
        return {
            "top_performer": "No data",
            "highest_engagement": "No data",
            "most_improved": "No data",
        }

    top_player = summary.iloc[0]
    engagement_player = summary.loc[summary["avg_engagement"].idxmax()]
    improvement_player = summary.loc[summary["avg_learning_gain"].idxmax()]

    return {
        "top_performer": str(top_player["player_id"]),
        "highest_engagement": str(engagement_player["player_id"]),
        "most_improved": str(improvement_player["player_id"]),
    }
