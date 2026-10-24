PREPARED — not READY. D42 remains unreleased and unqualified.

- Added [d42-caller-preparation.py](/home/user/work/wt/app-readiness-current-caller-prep-0442/d42-caller-preparation.py) and [d42-caller-custody.json](/home/user/work/wt/app-readiness-current-caller-prep-0442/d42-caller-custody.json).
- Current App: `c0fe889944…`, tree `8e3ef15e…`, parents `bad9a84fea… 19ac2b0dd…`.
- Protected P1/Gate5 blob remains `37caf285…`; popup is exactly the reviewed two ADD/SWAP selector change (`3cb690…` → `8072fc…`).
- 22 changed-source fingerprints recorded; digest `c43da143…`.
- D41 was used only as an old preparation input. Planned child key is deferred, not an installed/qualified receipt.

Controls passed:

- `qualify.py`: 24
- `stages.py`: 28
- `extra.py`: 4
- restricted exports: 2
- fail-closed wrong-key checks: 2, with no registration attempted
- `python -m py_compile d42-caller-preparation.py`
- `git diff --check`

Live rows and all 248 outside bytes were unchanged. Draft row hashes and artifact hashes are recorded in the generated TMPDIR manifest. No builds, HTTP/browser runs, service requests, installs, provisioning, or full suite were run.

Remaining required inputs: qualified D42 Runtime SHA/tree with independent review and 145-case qualification, exact checkout, backend-keyed child, matching Remotion receipts, final import/security/pin/HTTP evidence, then one normal exact pair submission by the manager.

Commit message and `DONE` marker written.