# SQL Notes

## WHERE

```sql
SELECT topic_name, confidence_score
FROM study_records
WHERE confidence_score < 3;
```

Finds weak topics.

## ORDER BY

```sql
SELECT topic_name, confidence_score
FROM study_records
ORDER BY confidence_score ASC;
```

Lists topics from lowest to highest confidence.

## Aggregation

```sql
SELECT AVG(confidence_score)
FROM study_records;
```

Calculates average confidence.

## COUNT

```sql
SELECT COUNT(*)
FROM study_records;
```

Counts study records.

## Product use

SQL allows the Study Skills Coach to store structured records and answer product questions before attempting machine learning.