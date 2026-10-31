# Measures and boundaries

One source row is a booking; Source Row points to its CSV line. Exact repeats remain, since anonymized attributes do not form a reliable unique booking key. There are 31,994 repeats after the first equal row in the original CSV. That is a sensitivity concern, not a demonstrated count of erroneous duplicates.

Bookings count records. Cancellations sum binary is_canceled. Rate is SUM(canceled)/COUNT(*), never an average of segment rates. Booked nights sum weekday plus weekend stay nights; canceled booked nights restrict that sum to canceled records. No occupancy denominator, collected revenue or intervention history exists.

Default complete-year comparison: City Hotel, 2016. Compare the same arrival month and hotel when reviewing segments. 2015 and 2017 are partial years. Every dashboard view has a disjoint View population in a reporting cube; do not sum across View values. Per-view tests reconcile each to booking-grain controls. Filter-sensitive KPIs use the kpi population. Rate tooltips include booking counts. Counts below 100 warrant caution; 100 is not a significance threshold.

Source validation checks calendar dates, nonnegative lead times/stays and binary cancellation status. Missing or undefined categories remain visible. Regeneration uses the pinned historical source and deliberately rejects an unexpected version.
