# Security policy

## Supported versions

Only the live report and the latest release get security fixes.

| Version | Supported |
| --- | --- |
| 1.x (latest) | Yes |
| Older | No |

## Reporting a vulnerability

Please report security problems privately, not in a public issue.

1. Go to the repository's **Security** tab and choose **Report a vulnerability**. This opens a private advisory that only the maintainer can see.
2. Describe the problem, the affected page or file, and how to reproduce it.

You should get a reply within 7 days. Once a fix is released, the advisory is published with credit to you, unless you'd rather stay anonymous.

## Scope

These are in scope:

- The live report at https://zakjrademacher.github.io/hotel-booking-cancellation-analysis/report/, including script injection.
- The code that prepares the data and builds the report, and the downloadable files in this repository (for example a workbook that runs unexpected content).
- Secrets or private data committed to the repository, the GitHub Actions workflows, and pinned dependencies.

Out of scope are problems in the public source dataset, third-party desktop tools and GitHub themselves, and disagreements about the analysis (open an issue for those).
