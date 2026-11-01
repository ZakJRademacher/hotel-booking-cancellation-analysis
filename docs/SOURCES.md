# Source and provenance

Kaggle download: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand

Original documentation: https://pmc.ncbi.nlm.nih.gov/articles/PMC6297060/

Retrieved October 30, 2026. The exact downloaded CSV hashes and archive fingerprint are in [source-download.json](../data/source-download.json). Processing verifies that fingerprint before replacing outputs. A newer Kaggle version must be reviewed explicitly.

Underlying source attribution: Antonio, N., de Almeida, A., and Nunes, L. (2019). Hotel booking demand datasets. Data in Brief 22, 41-49. DOI: 10.1016/j.dib.2018.11.126.

The original source is made available under Creative Commons Attribution 4.0. https://creativecommons.org/licenses/by/4.0/ . Prepared reporting tables are attributed adaptations: selected columns, normalized categories, derived bands and grouped measures. Original code is MIT licensed separately. Raw source files remain outside Git; reporting data is included for portable opening.

One observation represents a booking at one of two hotels in Portugal. Arrival dates span July 2015-August 2017. The source documentation reconstructs input values relative to the day before each booking's arrival where change logs are available. Outcome and final-status fields come from their stated source tables; this is not a record of what was known at booking creation. See the original article's extraction method and variable definitions.
