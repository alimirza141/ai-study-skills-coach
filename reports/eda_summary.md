# EDA Summary

## Dataset

- File: `data\study_records.csv`
- Number of rows: 1
- Number of columns: 6
- Number of topics: 1

## Summary statistics

- Average confidence: 3.00/5
- Median confidence: 3.00/5
- Average minutes studied: 120.00
- Total minutes studied: 120
- Highest-confidence topic: maths
- Lowest-confidence topic: maths

## Weak topics

No topics currently have average confidence below 3.

## Product implication

The current coach recommends topics with the lowest confidence first. A future version should also consider quiz accuracy, revision history, study frequency and time since the previous revision session.

## Data-quality limitations

- Confidence scores are self-reported.
- A small dataset may produce unreliable conclusions.
- Topic names may be inconsistent.
- More study time does not automatically mean better learning.
- The current analysis does not include quiz performance.

## Generated charts

- `reports/figures/confidence_by_topic.png`
- `reports/figures/minutes_by_topic.png`
