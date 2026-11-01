# Hotel cancellation investigation

This review gives a reservations manager two starting points for testing a better confirmation process: the segment with the most cancellations and the segment with the highest rate.

In the complete 2016 calendar year, the City Hotel recorded 15,407 cancellations among 38,140 bookings (40.4%). The Resort Hotel recorded 4,930 among 18,567 (26.6%). These properties serve different markets; the difference is not an estimate of hotel-management quality.

At the City Hotel, Online TA produced 7,149 cancellations from 19,708 bookings (36.3%). Groups had a higher rate (74.7%) but fewer cancellations (3,499). I'd investigate Online TA first for workload and review Groups separately because of its rate. Deposit terms, lead times, and arrival-month mix need checking before choosing either population for a trial.

**Proposed next step:** choose a hotel/month/segment/lead-time group with enough records, check those records, and design a randomized confirmation trial. Track cancellation rate, contact workload and guest complaints in treatment and business-as-usual groups. Do not use historical group differences as expected savings or promised cancellation reduction.

**Limits:** arrival coverage is July 2015 through August 2017; only 2016 is a full year. The source is an extraction snapshot, not event history. Similar records lack a booking ID and remain in the preferred analysis. Canceled booked nights do not prove lost capacity or revenue. No occupancy, profit or causal uplift estimate is supported.
