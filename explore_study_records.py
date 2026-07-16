from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_FILE = Path("data/study_records.csv")
FIGURE_DIR = Path("reports/figures")
REPORT_FILE = Path("reports/eda_summary.md")


def load_and_clean_data() -> pd.DataFrame:
    """Load the study records CSV and clean numerical columns."""

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "data/study_records.csv does not exist. "
            "Run study_tracker.py and add some records first."
        )

    df = pd.read_csv(DATA_FILE)

    if df.empty:
        raise ValueError(
            "data/study_records.csv exists but contains no study records."
        )

    required_columns = {
        "topic_name",
        "confidence_score",
        "minutes_studied",
    }

    missing_columns = required_columns.difference(df.columns)

    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(
            f"The CSV is missing required columns: {missing_text}"
        )

    df["topic_name"] = df["topic_name"].astype(str).str.strip()

    df["confidence_score"] = pd.to_numeric(
        df["confidence_score"],
        errors="coerce",
    )

    df["minutes_studied"] = pd.to_numeric(
        df["minutes_studied"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "topic_name",
            "confidence_score",
            "minutes_studied",
        ]
    )

    df = df[df["topic_name"] != ""]

    if df.empty:
        raise ValueError(
            "No valid study records remain after cleaning the CSV."
        )

    return df


def create_topic_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Group the study records by topic."""

    return (
        df.groupby("topic_name")
        .agg(
            average_confidence=("confidence_score", "mean"),
            total_minutes=("minutes_studied", "sum"),
            study_sessions=("topic_name", "size"),
        )
        .sort_values("average_confidence")
    )


def create_charts(topic_summary: pd.DataFrame) -> None:
    """Create and save confidence and study-time charts."""

    FIGURE_DIR.mkdir(parents=True, exist_ok=True)

    confidence_chart = (
        FIGURE_DIR / "confidence_by_topic.png"
    )

    minutes_chart = (
        FIGURE_DIR / "minutes_by_topic.png"
    )

    plt.figure(figsize=(10, 6))
    topic_summary["average_confidence"].plot(kind="bar")
    plt.title("Average Confidence by Topic")
    plt.xlabel("Topic")
    plt.ylabel("Average Confidence Score")
    plt.ylim(0, 5)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(confidence_chart, dpi=150)
    plt.close()

    plt.figure(figsize=(10, 6))
    topic_summary["total_minutes"].plot(kind="bar")
    plt.title("Total Minutes Studied by Topic")
    plt.xlabel("Topic")
    plt.ylabel("Total Minutes")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(minutes_chart, dpi=150)
    plt.close()


def create_report(
    df: pd.DataFrame,
    topic_summary: pd.DataFrame,
) -> str:
    """Create the Markdown EDA report."""

    weak_topics = topic_summary[
        topic_summary["average_confidence"] < 3
    ]

    highest_confidence_topic = (
        topic_summary["average_confidence"].idxmax()
    )

    lowest_confidence_topic = (
        topic_summary["average_confidence"].idxmin()
    )

    if weak_topics.empty:
        weak_topics_text = "No topics currently have average confidence below 3."
    else:
        weak_topic_lines = []

        for topic_name, row in weak_topics.iterrows():
            weak_topic_lines.append(
                f"- {topic_name}: "
                f"{row['average_confidence']:.2f}/5 average confidence, "
                f"{row['total_minutes']:.0f} total minutes, "
                f"{int(row['study_sessions'])} session(s)"
            )

        weak_topics_text = "\n".join(weak_topic_lines)

    report = (
        "# EDA Summary\n\n"
        "## Dataset\n\n"
        f"- File: `{DATA_FILE}`\n"
        f"- Number of rows: {len(df)}\n"
        f"- Number of columns: {len(df.columns)}\n"
        f"- Number of topics: {df['topic_name'].nunique()}\n\n"
        "## Summary statistics\n\n"
        f"- Average confidence: "
        f"{df['confidence_score'].mean():.2f}/5\n"
        f"- Median confidence: "
        f"{df['confidence_score'].median():.2f}/5\n"
        f"- Average minutes studied: "
        f"{df['minutes_studied'].mean():.2f}\n"
        f"- Total minutes studied: "
        f"{df['minutes_studied'].sum():.0f}\n"
        f"- Highest-confidence topic: "
        f"{highest_confidence_topic}\n"
        f"- Lowest-confidence topic: "
        f"{lowest_confidence_topic}\n\n"
        "## Weak topics\n\n"
        f"{weak_topics_text}\n\n"
        "## Product implication\n\n"
        "The current coach recommends topics with the lowest confidence "
        "first. A future version should also consider quiz accuracy, "
        "revision history, study frequency and time since the previous "
        "revision session.\n\n"
        "## Data-quality limitations\n\n"
        "- Confidence scores are self-reported.\n"
        "- A small dataset may produce unreliable conclusions.\n"
        "- Topic names may be inconsistent.\n"
        "- More study time does not automatically mean better learning.\n"
        "- The current analysis does not include quiz performance.\n\n"
        "## Generated charts\n\n"
        "- `reports/figures/confidence_by_topic.png`\n"
        "- `reports/figures/minutes_by_topic.png`\n"
    )

    return report


def main() -> None:
    """Run the complete exploratory data analysis."""

    try:
        df = load_and_clean_data()
        topic_summary = create_topic_summary(df)

        create_charts(topic_summary)

        report = create_report(
            df=df,
            topic_summary=topic_summary,
        )

        REPORT_FILE.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        REPORT_FILE.write_text(
            report,
            encoding="utf-8",
        )

        print(report)
        print("\nEDA completed successfully.")
        print(f"Report saved to: {REPORT_FILE}")
        print(f"Charts saved to: {FIGURE_DIR}")

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.EmptyDataError,
        pd.errors.ParserError,
    ) as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()