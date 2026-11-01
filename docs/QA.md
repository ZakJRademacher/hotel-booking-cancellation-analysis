# Verification — October 30, 2026

Four automated tests pass: band boundaries, independent raw-source reconciliation, reconciliation of each reporting-cube view, and row lineage/empty selections. Native Tableau opened and saved both dashboards. Shared Hotel filtering was checked against City and Resort 2016 control totals; all four KPIs and charts changed together. Final City baseline: 38,140 bookings, 15,407 cancellations, 40.4%, 47,199 canceled booked nights. Monthly labels use YYMM and run chronologically. The reporting cube repeats populations across View values: never sum across views.

Desktop screenshots are captured from the actual application. These are historical local reports, with no scheduled cloud refresh. Automated checks establish specified properties, not every possible interaction.

## November 1, 2026 release recheck

A disposable copy of the current public Tableau package opened in Desktop 2026.3. City / 2016 showed 38,140 bookings, 15,407 cancellations, 40.4% and 47,199 canceled booked nights. Switching the shared Hotel selector to Resort changed the cards and segment/lead-time/monthly charts together: 18,567 bookings, 4,930 cancellations, 26.6% and 22,222 canceled booked nights. Invoking Data > the packaged source > Refresh preserved the Resort values without a visible error. The four source/reconciliation tests pass after preparing the public source.

This recheck uses the package's existing reporting CSV. It does not establish a changed-source refresh, every filter combination, Tableau Public hosting or a newly saved report. The published workbook and design are unchanged.
