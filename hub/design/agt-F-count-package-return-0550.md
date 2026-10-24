Implemented bounded F-count metadata correction.

- Updated current census to 267 total / 179 closed / 88 open.
- Preserved historical 172/95 baseline and all 267 node records/statuses/proofs.
- Marked seven H3 originals current-qualified.
- Preserved exact 37-row mapping and CSV.
- Refreshed external SHA references; candidate SHA: `c70b6627e6fe4cd7f6d900e0bcb99168dd8e56a4269ad8d88e12b07eec272268`.
- No product/test changes.

Checks passed:

- JSON parsing for both artifacts.
- External `sha256sum -c`.
- Structural assertions: 267 nodes, 179/88 statuses, 37 mapping rows, unchanged CSV and node identities.
- `git diff --check`.
- No full/browser/body reruns performed.

Commit message recorded and `DONE` created.