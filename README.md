# Hotel Booking Cancellation Review

**Which segments create cancellation workload, and where should reservations test a better confirmation process?**

In **2016 City Hotel data**, **15,407 of 38,140 bookings canceled (40.4%)**. Online TA supplied the largest cancellation workload (**7,149**), while Groups had the higher rate (**74.7%**). Review the same hotel and arrival period before comparing segments; these historical differences do not establish intervention effects.

Python/SQLite preparation and a filter-responsive Tableau report use **119,390 historical booking records**, retaining uncertain repeated-looking records and source-row lineage.

[View current preview](deliverables/dashboard-preview.png) · [Download current Tableau workbook](deliverables/Hotel%20Cancellation%20Review.twbx) · [Decision memo](docs/DECISION_MEMO.md) · [SQL](sql/cancellation_review.sql) · [Reproduce](#reproduce)

![Current Tableau report, default City Hotel / 2016 selection](deliverables/dashboard-preview.png)

Filters update the selected population and calculated KPIs. The definitions/trial page remains explanatory context. The package includes its reporting CSV; no Tableau Public hosting is configured. [Earlier workbook layout](https://github.com/ZakJRademacher/hotel-booking-cancellation-analysis/blob/d6b6e9c23c546d840221904a12f23d5b5b98e598/deliverables/Hotel%20Cancellation%20Review.twbx) is preserved in history.

## Open the report

[Download the redesigned Tableau workbook](deliverables/Hotel%20Cancellation%20Review.twbx). Open in Tableau Desktop. Its reporting CSV is included. The first dashboard uses shared hotel, year, arrival-month and segment filters. The second dashboard explains the decision and trial. Tableau Public is not configured.

Editable source: [tableau](tableau). Run `python tools/build_report.py` to regenerate, open and save in Tableau, then run `python tools/package_report.py`. Preserve native authoring metadata in the committed workbook.

## Reproduce

Python 3.10+, standard library only:

```sh
python tools/download_data.py
python refresh.py
python -m unittest discover -s tests -v
```

The preparation writes source-row lineage, a SQLite database, reporting CSVs, comparison cells and [control totals](data/processed/controls.json). [SQL investigation](sql) shows counts and denominators explicitly. Source records are retained; repeated-looking rows without durable IDs are not automatically removed.

## Read the analysis

- [Source, version and licensing](docs/SOURCES.md)
- [Measure definitions and refresh boundaries](docs/METHOD.md)
- [Beginner walkthrough and practice](docs/LEARNING.md)
- [Verification](docs/QA.md)

Independent portfolio demonstration. Historical associations motivate a controlled follow-up experiment; they do not establish causal lift, profit or realized client outcomes. The previous Retail and Complaint projects remain available as separate supporting work.

## Presentation history

[Cover preview](deliverables/portfolio-cover-wide.png) · [Motion cover](deliverables/portfolio-motion.webm) · [Design maintenance](docs/VISUAL_DESIGN.md) · [November 1 release record](docs/DASHBOARD_RELEASE.md). Covers are presentation assets; native report behavior is documented separately.
