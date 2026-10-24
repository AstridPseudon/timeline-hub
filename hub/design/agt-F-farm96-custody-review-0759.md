# PASS — F-farm96 custody review

Reviewed all three complete artifacts read-only.

- 96 rows: historical 88 + newer 8.
- Classifications: 80 environment, 1 regression, 15 unknown.
- All 2,976 CSV cells across 31 mapped fields match authoritative JSON paths.
- All 96 node IDs map to `proven_passed` reconciliation entries with valid prior-proof references.
- Farm tuple is consistently Agent `9cd3dbe8`, tree `57f0231d`, Runtime `45c3a7f4`; prior qualified scopes remain distinct.
- Exactly 384 CSV cells changed from `856de6e3f2`: 288 tuple cells + 96 citations. JSON bytes are unchanged.
- Artifact hashes match:
  - JSON `9b9bc96b…8b896`
  - CSV `d0dd5e79…17913da4`
  - Markdown `c3590bf6…711291298`

Validation commands/results:

- Standalone Python parity/count/offset/source validation — PASS.
- `python3 -m json.tool farm96-causes.json` — PASS.
- `git diff --check` — PASS.
- Frozen Agent/Runtime citation path and line checks — PASS.
- Worktree remains clean.

Limits:

- Raw Farm log and extracts are not local; their manifest-reported hashes were not independently rehashed.
- Seven summary failures lack exact node identities; no PASS/JUnit/global credit was inferred.
- The single giant-file documentation challenge remains unclaimed.
- No product tests, full/browser/live runs, v2 caller execution, or production-caller proof was run.

Required commit message and `DONE` marker were created.