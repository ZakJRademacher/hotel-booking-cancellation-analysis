-- Run against data/processed/analysis.sqlite. Counts use source booking rows.
SELECT hotel, segment, COUNT(*) AS bookings, SUM(canceled) AS cancellations,
       ROUND(100.0*SUM(canceled)/COUNT(*),2) AS cancellation_pct,
       SUM(canceled_nights) AS canceled_booked_nights
FROM bookings WHERE year='2016'
GROUP BY hotel,segment ORDER BY hotel,cancellations DESC;

-- Comparable cells: inspect segment differences within the same hotel and month.
SELECT hotel,period,segment,lead_band,COUNT(*) AS bookings,
       SUM(canceled) AS cancellations,
       1.0*SUM(canceled)/COUNT(*) AS cancellation_rate,
       CASE WHEN COUNT(*)<100 THEN 'Small sample' ELSE 'Descriptive comparison' END AS population_note
FROM bookings WHERE year='2016'
GROUP BY hotel,period,segment,lead_band ORDER BY hotel,period,segment,lead_band;
