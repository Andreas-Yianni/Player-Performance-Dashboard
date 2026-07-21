import pandas as pd

from analytics import build_player_summary, build_insights


def test_build_player_summary_returns_expected_metrics():
    df = pd.DataFrame(
        [
            {"player_id": "P001", "session_id": "S1", "score": 80, "errors": 2, "time_taken": 120, "engagement_score": 70, "completion_rate": 75, "learning_gain": 10},
            {"player_id": "P001", "session_id": "S2", "score": 85, "errors": 1, "time_taken": 110, "engagement_score": 78, "completion_rate": 80, "learning_gain": 12},
            {"player_id": "P002", "session_id": "S1", "score": 72, "errors": 4, "time_taken": 140, "engagement_score": 65, "completion_rate": 68, "learning_gain": 8},
        ]
    )

    summary = build_player_summary(df)

    assert list(summary.columns) == [
        "player_id",
        "sessions",
        "avg_score",
        "avg_engagement",
        "avg_completion",
        "avg_learning_gain",
        "avg_errors",
        "avg_time",
    ]
    assert summary.loc[0, "player_id"] == "P001"
    assert summary.loc[0, "sessions"] == 2
    assert summary.loc[1, "player_id"] == "P002"


def test_build_insights_returns_key_highlights():
    summary = pd.DataFrame(
        [
            {"player_id": "P001", "sessions": 2, "avg_score": 82.5, "avg_engagement": 74.0, "avg_completion": 77.5, "avg_learning_gain": 11.0, "avg_errors": 1.5, "avg_time": 115.0},
            {"player_id": "P002", "sessions": 1, "avg_score": 72.0, "avg_engagement": 65.0, "avg_completion": 68.0, "avg_learning_gain": 8.0, "avg_errors": 4.0, "avg_time": 140.0},
        ]
    )

    insights = build_insights(summary)

    assert insights["top_performer"] == "P001"
    assert insights["highest_engagement"] == "P001"
    assert insights["most_improved"] == "P001"
