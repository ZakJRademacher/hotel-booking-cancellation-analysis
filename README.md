# Hotel Booking Cancellations

I looked at hotel cancellations to understand where a reservations team would face the most follow-up work. Comparing counts with rates led to two different answers.

For the **City Hotel in 2016**, online travel agents accounted for the most cancellations. Group bookings had the higher cancellation rate. The **Tableau report** lets a reader compare those patterns within the same hotel and arrival period.

**[Open the live report](https://zakjrademacher.github.io/hotel-booking-cancellation-analysis/report/)** · [Preview image](deliverables/dashboard-preview.png) · [Download the Tableau workbook](deliverables/Hotel%20Cancellation%20Review.twbx) · [Read the decision memo](docs/DECISION_MEMO.md)

The live report is a self-contained page in [report/](report/), rebuilt from the processed data with `python tools/build_web_report.py`.

![Tableau cancellation review with City Hotel and 2016 selected](deliverables/dashboard-preview.png)

## What I found

The City Hotel recorded **15,407 cancellations among 38,140 bookings (40.4%)** in 2016. Online TA accounted for **7,149 cancellations**, while Groups had a **74.7% cancellation rate**.

Online TA is the larger workload to investigate; Groups is a separate lead because of its rate. Before choosing a confirmation-process trial, I'd check lead times, deposit terms, and arrival-month mix. The historical differences don't tell us how much a new process would improve cancellations.

Python and SQLite prepare **119,390 booking records** and preserve their source references. Similar-looking records remain in the analysis because the source has no booking ID that would establish they are erroneous duplicates.

[SQL](sql/cancellation_review.sql) · [Measures and populations](docs/METHOD.md) · [Source and licensing](docs/SOURCES.md)

## Open the report

Open the packaged workbook in Tableau Desktop; its reporting CSV is included. Shared hotel, year, arrival-month, and segment filters update the first dashboard's metrics and charts. The second dashboard explains the proposed trial and the definitions behind the analysis.

The data covers July 2015–August 2017, so **2016 is the only complete year**. Canceled booked nights describe workload and booking volume; they don't establish lost revenue or capacity.

Editable source is in [tableau](tableau). To rebuild, run `python tools/build_report.py`, open and save the workbook in Tableau, then run `python tools/package_report.py`. Keep native authoring metadata intact.

## Reproduce

From the repository root, using Python 3.10+ and the standard library:

```sh
python tools/download_data.py
python refresh.py
python -m unittest discover -s tests -v
```

The pipeline writes a SQLite database, reporting CSVs, source-row references, and [control totals](data/processed/controls.json). Each reporting view is checked against booking-level totals; different `View` values must not be summed together.

## Methods and verification

- [Decision memo](docs/DECISION_MEMO.md) · [Method](docs/METHOD.md) · [Verification](docs/QA.md)
- [Source and licensing](docs/SOURCES.md) · [Visual maintenance](docs/VISUAL_DESIGN.md)

This is an independent analysis of historical public data from two hotels in Portugal. The download runs locally; Tableau Public hosting and scheduled refresh are not configured. Data attribution and reuse terms are in the source guide.
