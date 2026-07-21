from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Union

import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)


def generate_player_sessions(output_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    players = ["P001", "P002", "P003", "P004", "P005"]
    sessions_per_player = 10
    rows = []
    start_date = datetime(2026, 6, 1)

    for player in players:
        skill_level = np.random.uniform(40, 90)

        for session_num in range(1, sessions_per_player + 1):
            improvement = session_num * np.random.uniform(0.5, 2)
            score = round(min(100, max(0, skill_level + improvement + np.random.normal(0, 5))), 1)

            time_taken = round(np.random.uniform(60, 300) - (session_num * 3), 1)
            errors = max(0, int(np.random.poisson(5 - session_num * 0.3)))
            attempts = max(1, int(np.random.poisson(2)))
            engagement_score = round(min(100, max(0, 55 + (session_num * 3) + np.random.normal(0, 8) + (score / 10) - errors * 2)), 1)
            completion_rate = round(min(100, max(0, 60 + (session_num * 2) + np.random.normal(0, 7) + (score / 10) - errors * 1.5)), 1)
            learning_gain = round(max(0, score - (skill_level / 2) + np.random.normal(0, 2)), 1)
            timestamp = start_date + timedelta(days=session_num * 2, hours=np.random.randint(0, 12))

            rows.append({
                "player_id": player,
                "session_id": f"S{session_num}",
                "score": score,
                "time_taken": time_taken,
                "errors": errors,
                "attempts": attempts,
                "engagement_score": engagement_score,
                "completion_rate": completion_rate,
                "learning_gain": learning_gain,
                "timestamp": timestamp,
            })

    df = pd.DataFrame(rows)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    if output_path is None:
        output_path = Path(__file__).resolve().parent / "data" / "player_sessions.csv"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f"Generated {len(df)} sessions for {len(players)} players.")
    print(df.head())
    return df


if __name__ == "__main__":
    generate_player_sessions()