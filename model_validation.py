import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.model_selection import (
    StratifiedKFold,
    cross_val_score,
    train_test_split,
)
from sklearn.tree import DecisionTreeClassifier

DATA_FILE = "data/session_success_demo.csv"

FEATURES = [
    "planned_minutes",
    "confidence_before",
    "previous_sessions_for_topic",
    "previous_topic_accuracy",
]

TARGET = "session_success"


def main():
    df = pd.read_csv(DATA_FILE)

    X = df[FEATURES]
    y = df[TARGET]

    X_dev, X_test, y_dev, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    baseline = DummyClassifier(strategy="most_frequent")
    baseline.fit(X_dev, y_dev)

    print(
        f"Majority baseline: "
        f"{baseline.score(X_test, y_test):.3f}"
    )

    folds = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    results = []

    for depth in [1, 2, 3, 5, None]:
        model = DecisionTreeClassifier(
            max_depth=depth,
            random_state=42,
        )

        scores = cross_val_score(
            model,
            X_dev,
            y_dev,
            cv=folds,
            scoring="accuracy",
        )

        model.fit(X_dev, y_dev)

        results.append(
            {
                "depth": depth,
                "training_accuracy": model.score(X_dev, y_dev),
                "mean_cv_accuracy": scores.mean(),
                "cv_standard_deviation": scores.std(),
                "test_accuracy": model.score(X_test, y_test),
            }
        )

    print(pd.DataFrame(results).to_string(index=False))


if __name__ == "__main__":
    main()