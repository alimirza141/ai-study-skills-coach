import sqlite3
from datetime import datetime

from database_setup import DATABASE_FILE, create_database


def get_valid_number(
    prompt: str,
    minimum: int,
    maximum: int | None = None,
) -> int:
    while True:
        try:
            value = int(input(prompt))

            if value < minimum:
                print(f"Enter a number of at least {minimum}.")
                continue

            if maximum is not None and value > maximum:
                print(f"Enter a number no higher than {maximum}.")
                continue

            return value

        except ValueError:
            print("Enter a valid whole number.")


def add_record() -> None:
    create_database()

    topic_name = input("Enter topic name: ").strip()

    if not topic_name:
        print("Topic name cannot be blank.")
        return

    confidence_score = get_valid_number(
        "Rate confidence from 1-5: ",
        minimum=1,
        maximum=5,
    )

    minutes_studied = get_valid_number(
        "Enter minutes studied: ",
        minimum=1,
    )

    next_revision_date = input(
        "Enter next revision date, preferably YYYY-MM-DD: "
    ).strip()

    notes = input("Enter notes: ").strip()

    with sqlite3.connect(DATABASE_FILE) as connection:
        connection.execute(
            """
            INSERT INTO study_records (
                topic_name,
                confidence_score,
                minutes_studied,
                next_revision_date,
                notes,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                topic_name,
                confidence_score,
                minutes_studied,
                next_revision_date,
                notes,
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        connection.commit()

    print(f"Saved SQLite record for {topic_name}.")


if __name__ == "__main__":
    add_record()