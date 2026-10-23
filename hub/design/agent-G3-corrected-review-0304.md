# G3 corrected join independent review — FAIL

Reviewed `ecea7d8563c93059283ef9475ecb41a37e628a38` with true parents current
G3 `8e7fbea7cf3ce9dbf7d0deffb60c858bdd104afa` and corrected U4a
`7d356202826ce60ff676d6e46151187aad9f4a70` (U4a parent `fc515591b`). No
tracked edits were made.

Blocking finding: the merged canonical edit schema is not the approved d106
schema. Corrected U4a and current R2/R3/meta source have
`sha256:d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`,
while HEAD `astrid/core/timeline/schema/edit-command.schema.json` hashes to
`sha256:a51678f277f66f43dec04a6986d03f2c0e2874ffbaa36995489e019046eee28c`.
The remerge diff shows the 16-line `timeline.inverse.args.steps` property was
removed during resolution. The typed DTO retains `InverseArgs.steps`, but the
canonical schema consumed by the command engine does not. **FAIL**; restore the
exact d106 schema in the merge resolution and rerun schema-floor tests.

Preservation checks passed: exact two-parent merge; first-parent delta only
generated client plus `runtime.lock.json`; all 15 lock mappings byte-identical to
corrected U4a Runtime `780da6d605033ca71dbe2ad48c10ec2870ea4865`; vendor lock and
artifact manifest checks; corrected generated client admits valid `merged` with a
receipt; current G3/R2/R3/meta source and six approved V4-deleted paths retained;
obsolete `21482` pin and stale report resurrection absent; full v2 DTO/request and
reply surface retained.

Evidence:

- compound post-join: **1 passed**;
- focused G3/G2/R2/R3/meta neighbors: **149 passed**;
- vendor/artifact tests: **37 passed**;
- Ruff: **2150/2150**;
- private scoped mypy: **10 files, no issues**;
- private normal mypy: **1915/1915**;
- `git diff --check`: passed; worktree clean.

Separate Runtime-owned hold remains: corrected Runtime-780 negative probes accept
malformed partial receipts and previews missing `would_status`. No generated-client
repair or Runtime wire acceptance is claimed by this Agent review.
