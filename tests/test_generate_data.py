from pathlib import Path

from generate_data import generate_player_sessions


def test_generate_player_sessions_creates_expected_file(tmp_path):
    output_path = tmp_path / "player_sessions.csv"

    df = generate_player_sessions(output_path=output_path)

    assert output_path.exists()
    assert len(df) == 50
    assert {"player_id", "session_id", "score", "time_taken", "errors", "attempts", "engagement_score", "completion_rate", "learning_gain", "timestamp"}.issubset(df.columns)
    assert df["player_id"].nunique() == 5
    assert df["session_id"].nunique() == 10
