## Report

Added [caller-stage-retention.py](/home/user/work/wt/app-P2-P3-stage-retention-0542/caller-stage-retention.py).

- Inspected real rows: P2 line 75, P3 line 245.
- Verified `bash -n`, argv counts, source/body locks, and 248 unrelated-row digest.
- Real Playwright fixture: Node `v22.22.0`, Playwright `1.60.0`.
- Same output root: expected RED; 7 files before, 7 after, 6 prior files removed.
- Per-stage P2/P3 child roots: GREEN; readiness and original-body hashes preserved separately.
- Selected row hashes: P2 `51f39c2c…fd34a`; P3 `4fdad3a5…18df`.
- Unrelated rows: `b33d3091…d734`.

Checks passed:

```text
python3 caller-stage-retention.py --static-only
python3 caller-stage-retention.py
python3 -m py_compile caller-stage-retention.py
git diff --check
```

No live journey, browser/backend/native/bootstrap/full suite, or `suites.conf` modification was performed. Adoption instruction: assign `PLAYWRIGHT_OUTPUT_DIR` to per-request `p2/<stage>` and `p3/<stage>` children while preserving all existing guards.

Commit message and `DONE` marker written.