# Report

- Added `ops-handoff/farm-agent-full-v2/` with source-selection record, deferred registration row, normal-route instructions, manifest, and private Store/projection fixtures.
- Correctly preserves declared Runtime lock/client hashes (`45c3a7f4`) while requiring Runtime `1d9ddba5`, which contains `external_pack_sources`.
- Candidate row is not publishable until authentic checkout, managed receipt, module origins, and baseline checks exist.
- No live Store, registry, provisioning, dispatcher, product, or generated files changed.

Tests/checks:

- Targeted pytest: `3 passed`
- Ruff: passed
- Python compile: passed
- Manifest SHA checks: passed
- README shell snippets `bash -n`: passed
- `git diff --check`: passed

Blocked/unverified: normal Runtime checkout/managed receipt and the later full Agent run remain Farm-owned. Commit message and `DONE` marker written.