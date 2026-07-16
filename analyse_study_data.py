from pathlib import Path

import pandas as pd

DATA_FILE = Path("data/study_records.csv")
OUTPUT_FILE = Path("docs/INSIGHTS.md")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Run study_tracker.py and add records first."
        )

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        print("The dataset is empty.")
        return

    df["confidence_score"] = pd.to_numeric(
        df["confidence_score"],
        errors="coerce",
    )

    df["minutes_studied"] = pd.to_numeric(
        df["minutes_studied"],
        errors="coerce",
    )

    valid_df = df.dropna(
        subset=["confidence_score", "minutes_studied"]
    )

    topic_summary = (
        valid_df.groupby("topic_name")
        .agg(
            average_confidence=("confidence_score", "mean"),
            total_minutes=("minutes_studied", "sum"),
            sessions=("topic_name", "size"),
        )
        .sort_values("average_confidence")
    )

    weakest_topic = topic_summary.index[0]
    strongest_topic = topic_summary.index[-1]

    weak_topics = topic_summary[
        topic_summary["average_confidence"] < 3
    ]

    report = f"""# Study Insights

## Summary

- Total sessions: {len(valid_df)}
- Average confidence: {valid_df["confidence_score"].mean():.2f}
- Average study duration: {valid_df["minutes_studied"].mean():.2f} minutes
- Total study time: {valid_df["minutes_studied"].sum():.0f} minutes
- Weakest topic: {weakest_topic}
- Strongest topic: {strongest_topic}

## Topics currently below confidence 3

{weak_topics.to_markdown() if not weak_topics.empty else "No topics are currently below confidence 3."}

## Limitation

Confidence is self-reported and the dataset is small. These results are early indicators, not proof of actual subject mastery.
"""

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")

    print(report)


if __name__ == "__main__":
    main()