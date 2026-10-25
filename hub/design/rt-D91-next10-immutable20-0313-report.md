## Report

Completed D91/F-D86 FIRST20 proof using immutable Agent `562ee30b…`, Runtime `6634a17f…`, App `24865fa2…`, and Composition `635f4de0…`.

- Combined exactly 20 unique selectors: D91 ten + inverse7 + compound3.
- Verified zero overlap of the new ten with actual161, actual102, and D91 selectors.
- Immutable preflight passed; wrong mutable-root poison control failed with zero body calls.
- Central run: 20 cases — D91: 10 errors; D86 next10: 7 passed, 3 failed. Automatic NO-GO.
- Exact command preserved: pytest `-n 3`, cache disabled, timeout 45s, no marker filter.
- Four checkout receipts, XML, per-ID outcomes, manifests, logs, hashes, and path audits captured under worker evidence (1.1 MB).
- Central suite registry restored byte-identically.
- Runtime worktree remains clean; no product/test/source changes.
- Required commit message and `DONE` marker created.

Targeted/static checks passed: `bash -n`, import-origin verification, runtime-lock hashes, selector accounting, source hashes, registry restore check.

No local pytest or full suite was run. Next step is review the recorded behavioral failures; do not rerun unchanged proof.