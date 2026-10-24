## Report

Implemented D41 caller preparation in only:

- `caller-publication.py`
- `caller-custody.json`

Changes require an explicit receipt-backed Agent source manifest before rebinding decoded P2/P3 rows. Validation covers source/tree/parent/checkouts, Runtime37eb, all four client hashes, backend hashes, keyed child, maker/provision/import receipts, and retained Remotion custody. Legacy Agent079/child0256 remains historical and is not relabeled.

Tests:

- `python -m py_compile caller-publication.py` — passed
- `python -m json.tool caller-custody.json` — passed
- `git diff --check` — passed
- Actual nested P2/P3 rows decoded; inner/outer `bash -n` — passed for both
- Modeled actual replacement — passed; 2 rows, 248 outside rows preserved, outside SHA256 unchanged
- Missing/forged manifest refusal — passed
- Live installed rows unchanged — passed

Final D41 source, child, and receipts are unavailable, so no rows were installed and status remains `PREPARED` / `NOT_GRANTED`. No browser, backend, build, provisioning, HTTP, or full-suite runs were performed.