import sqlite3
from pathlib import Path

import pandas as pd

from database_setup import DATABASE_FILE, create_database


REPORT_FILE = Path("docs/SQL_ANALYSIS_SUMMARY.md")


def dataframe_as_text(dataframe: pd.DataFrame) -> str:
    if dataframe.empty:
        return "No matching records."

    return (
        "```text\n"
        f"{dataframe.to_string(index=False)}\n"
        "```"
    )


def main() -> None:
    create_database()

    with sqlite3.connect(DATABASE_FILE) as connection:
        total_records = pd.read_sql_query(
            """
            SELECT COUNT(*) AS total_records
            FROM study_records
            """,
            connection,
        )

        averages = pd.read_sql_query(
            """
            SELECT
                ROUND(AVG(confidence_score), 2)
                    AS average_confidence,
                ROUND(AVG(minutes_studied), 2)
                    AS average_minutes
            FROM study_records
            """,
            connection,
        )

        weak_topics = pd.read_sql_query(
            """
            SELECT
                topic_name,
                confidence_score,
                minutes_studied,
                next_revision_date
            FROM study_records
            WHERE confidence_score < 3
            ORDER BY confidence_score ASC
            """,
            connection,
        )

        highest_study_time = pd.read_sql_query(
            """
            SELECT
                topic_name,
                MAX(minutes_studied) AS highest_minutes
            FROM study_records
            """,
            connection,
        )

        revise_next = pd.read_sql_query(
            """
            SELECT
                topic_name,
                confidence_score,
                next_revision_date
            FROM study_records
            ORDER BY
                confidence_score ASC,
                next_revision_date ASC
            LIMIT 5
            """,
            connection,
        )

    report = (
        "# SQL Analysis Summary\n\n"
        "## Total records\n\n"
        f"{dataframe_as_text(total_records)}\n\n"
        "## Average confidence and study time\n\n"
        f"{dataframe_as_text(averages)}\n\n"
        "## Topics with confidence below 3\n\n"
        f"{dataframe_as_text(weak_topics)}\n\n"
        "## Highest study time\n\n"
        f"{dataframe_as_text(highest_study_time)}\n\n"
        "## Suggested revision order\n\n"
        f"{dataframe_as_text(revise_next)}\n\n"
        "## Limitation\n\n"
        "The database currently contains only a small amount of "
        "sample data. Confidence is self-reported and should not "
        "be treated as proof of subject mastery.\n"
    )

    REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
    REPORT_FILE.write_text(report, encoding="utf-8")

    print(report)
    print(f"\nSaved report to {REPORT_FILE}")


if __name__ == "__main__":
    main()