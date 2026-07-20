import random
from pathlib import Path

import pandas as pd

random.seed(42)

rows = []

for _ in range(100):
    planned_minutes = random.randint(15, 120)
    confidence_before = random.randint(1, 5)
    previous_sessions = random.randint(0, 12)
    previous_accuracy = random.randint(20, 100)

    score = (
        confidence_before * 12
        + previous_sessions * 2
        + previous_accuracy * 0.35
        + random.randint(-20, 20)
    )

    rows.append(
        {
            "planned_minutes": planned_minutes,
            "confidence_before": confidence_before,
            "previous_sessions_for_topic": previous_sessions,
            "previous_topic_accuracy": previous_accuracy,
            "session_success": int(score >= 65),
        }
    )

output = Path("data/session_success_demo.csv")
output.parent.mkdir(parents=True, exist_ok=True)

pd.DataFrame(rows).to_csv(output, index=False)

print(f"Created {output}. This is synthetic demonstration data.")