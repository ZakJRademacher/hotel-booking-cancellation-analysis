# Measures and boundaries

## What one record represents

Each source row represents a booking. `Source Row` points back to its CSV record. I retained exact repeats because the anonymized attributes aren't a reliable booking key. The original CSV has **31,994 repeats after the first equal row**; that is a reason to test sensitivity, rather than a count of proven errors.

## Counts, rates, and nights

Bookings count records. Cancellations sum the binary `is_canceled` field. Cancellation rate is `SUM(canceled) / COUNT(*)` for the same selection, rather than an average of segment rates.

Booked nights add weekday and weekend stay nights. Canceled booked nights use that same sum for canceled records. These figures describe bookings; without an occupancy denominator, collected revenue, or intervention history, they can't establish lost capacity, revenue, or a trial's effect.

## Comparable populations

The default view is **City Hotel / 2016**. It is the only complete calendar year in the source; 2015 and 2017 are partial. Compare segments within the same hotel and arrival period before interpreting their differences.

The reporting cube stores separate chart populations under `View`. Each view is checked against booking-level controls. **Do not add different View values together.** Filter-responsive KPIs use the `kpi` population, and rate tooltips include booking counts. Counts below 100 are flagged for caution; 100 isn't a significance threshold.

## Validation

Preparation checks calendar dates, nonnegative lead times and stays, and binary cancellation status. Missing or undefined categories remain visible. Rebuilding uses the pinned historical source and stops if its fingerprint has changed, so a new source version needs an explicit review.
