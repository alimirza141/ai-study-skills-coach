# SQL Analysis Summary

## Total records

```text
 total_records
             5
```

## Average confidence and study time

```text
 average_confidence  average_minutes
                3.2             61.0
```

## Topics with confidence below 3

```text
topic_name  confidence_score  minutes_studied next_revision_date
     maths                 1              120         2026-07-24
     maths                 2               30         2026-07-30
```

## Highest study time

```text
topic_name  highest_minutes
     maths              120
```

## Suggested revision order

```text
      topic_name  confidence_score next_revision_date
           maths                 1         2026-07-24
           maths                 2         2026-07-30
         physics                 4         2026-07-21
           maths                 4         2026-08-03
computer science                 5         2026-08-01
```

## Limitation

The database currently contains only a small amount of sample data. Confidence is self-reported and should not be treated as proof of subject mastery.
