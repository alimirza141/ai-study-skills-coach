import sqlite3
from pathlib import Path


DATABASE_FILE = Path("data/study_coach.db")


def create_database() -> None:
    """Create the SQLite database and study_records table."""

    DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS study_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic_name TEXT NOT NULL,
                confidence_score INTEGER NOT NULL
                    CHECK (confidence_score BETWEEN 1 AND 5),
                minutes_studied INTEGER NOT NULL
                    CHECK (minutes_studied > 0),
                next_revision_date TEXT,
                notes TEXT,
                created_at TEXT NOT NULL
            )
            """
        )

        connection.commit()

    print(f"Database ready: {DATABASE_FILE}")


if __name__ == "__main__":
    create_database()