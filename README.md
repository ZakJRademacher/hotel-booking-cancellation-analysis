# Hotel Booking Cancellation Review

**Which booking segments account for the greatest cancellation workload, and where should reservations test an improved confirmation process?**

A historical business investigation using Python, SQLite and Tableau. [Decision memo](docs/DECISION_MEMO.md) explains the evidence, next action and limitations.

![Dashboard preview](deliverables/dashboard-preview.png)

## Open the report

[Packaged Tableau workbook](deliverables/Hotel%20Cancellation%20Review.twbx). Open in Tableau Desktop. Its reporting CSV is included. The first dashboard uses shared hotel, year, arrival-month and segment filters. The second dashboard explains the decision and trial. Tableau Public is not configured.

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
