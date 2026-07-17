import csv
from datetime import datetime
from pathlib import Path


DATA_FILE = Path("data/study_records.csv")

FIELDS = [
    "topic_name",
    "confidence_score",
    "minutes_studied",
    "next_revision_date",
    "notes",
    "created_at",
]


def ensure_data_file() -> None:
    """Create the data folder and CSV file when they do not exist."""

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        with DATA_FILE.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=FIELDS,
            )
            writer.writeheader()


def get_valid_number(
    prompt: str,
    minimum: int,
    maximum: int | None = None,
) -> int:
    """Ask repeatedly until the user enters a valid whole number."""

    while True:
        try:
            value = int(input(prompt))

            if value < minimum:
                print(
                    f"Enter a number of at least {minimum}."
                )
                continue

            if maximum is not None and value > maximum:
                print(
                    f"Enter a number no higher than {maximum}."
                )
                continue

            return value

        except ValueError:
            print("Enter a valid whole number.")


def load_study_records() -> list[dict[str, str]]:
    """Load all existing study records from the CSV file."""

    ensure_data_file()

    with DATA_FILE.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        return list(csv.DictReader(file))


def save_study_records(
    records: list[dict[str, str]],
) -> None:
    """Write all study records back to the CSV file."""

    ensure_data_file()

    with DATA_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
        )
        writer.writeheader()
        writer.writerows(records)


def add_topic() -> None:
    """Ask for a study record and save it to the CSV file."""

    topic = input("Enter topic name: ").strip()

    if not topic:
        print("Topic cannot be blank.")
        return

    confidence = get_valid_number(
        "Rate your confidence from 1-5: ",
        minimum=1,
        maximum=5,
    )

    minutes = get_valid_number(
        "How many minutes did you study? ",
        minimum=1,
    )

    next_revision = input(
        "When would you like to revise next? "
    ).strip()

    notes = input("Add any notes: ").strip()

    record = {
        "topic_name": topic,
        "confidence_score": str(confidence),
        "minutes_studied": str(minutes),
        "next_revision_date": next_revision,
        "notes": notes,
        "created_at": datetime.now().isoformat(
            timespec="seconds"
        ),
    }

    ensure_data_file()

    with DATA_FILE.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=FIELDS,
        )
        writer.writerow(record)

    print(f"\nSaved study record for {topic}.")

    if confidence <= 2:
        print(f"I suggest you revise {topic} soon.")


def list_topics() -> None:
    """Display all saved study records."""

    records = load_study_records()

    if not records:
        print("No study records exist.")
        return

    print("\nStudy records")

    for index, record in enumerate(
        records,
        start=1,
    ):
        print(
            f"{index}. {record['topic_name']} | "
            f"confidence: "
            f"{record['confidence_score']}/5 | "
            f"minutes: "
            f"{record['minutes_studied']} | "
            f"next revision: "
            f"{record['next_revision_date']}"
        )


def update_confidence() -> None:
    """Update the confidence score for one saved record."""

    records = load_study_records()

    if not records:
        print("No study records exist.")
        return

    list_topics()

    record_number = get_valid_number(
        "Select a record number: ",
        minimum=1,
        maximum=len(records),
    )

    new_confidence = get_valid_number(
        "Enter the new confidence score from 1-5: ",
        minimum=1,
        maximum=5,
    )

    selected_record = records[record_number - 1]
    selected_record["confidence_score"] = str(
        new_confidence
    )

    save_study_records(records)

    print(
        f"Confidence updated for "
        f"{selected_record['topic_name']}."
    )


def recommend_topic() -> None:
    """Recommend the topic with the lowest confidence score."""

    records = load_study_records()

    if not records:
        print("Add a study record first.")
        return

    valid_records = []

    for record in records:
        try:
            confidence = int(
                record["confidence_score"]
            )
            valid_records.append(
                (record, confidence)
            )
        except (
            ValueError,
            TypeError,
            KeyError,
        ):
            continue

    if not valid_records:
        print(
            "No records contain a valid "
            "confidence score."
        )
        return

    weakest_record, weakest_confidence = min(
        valid_records,
        key=lambda item: item[1],
    )

    print(
        f"Revise "
        f"{weakest_record['topic_name']} next. "
        f"Current confidence: "
        f"{weakest_confidence}/5."
    )


def show_menu() -> None:
    """Display the main menu."""

    print(
        "\nAI Study Skills Coach\n"
        "1. Add topic\n"
        "2. List topics\n"
        "3. Update confidence\n"
        "4. Recommend next topic\n"
        "5. Exit"
    )


def main() -> None:
    """Run the command-line study tracker."""

    ensure_data_file()

    while True:
        show_menu()

        choice = input(
            "Choose an option: "
        ).strip()

        if choice == "1":
            add_topic()
        elif choice == "2":
            list_topics()
        elif choice == "3":
            update_confidence()
        elif choice == "4":
            recommend_topic()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print(
                "Choose a number from 1 to 5."
            )


if __name__ == "__main__":
    main()
