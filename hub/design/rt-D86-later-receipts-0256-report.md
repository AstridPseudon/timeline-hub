Implemented the source-only F-D86 receiving packet.

- Added six F-M2 pool selectors and one core-element selector: 102 unique total.
- Preserved prior 95-selector bytes, current161 cef8 boundary, held identities, D91 scheduled set, and historical artifacts.
- Evidence: [packet README]( /home/user/work/wt/rt-D86-later-receipts-0256/evidence/fd86-later-receipts-0256/README.md) and exact selectors in `inputs/selector-argv.txt`.
- No runtime/test source changes.

Validation passed:

- JSON/TSV/set accounting
- Source SHA-256 and reviewed ancestry
- AST/in-memory compilation
- `bash -n` route syntax
- Byte-preservation checks

Behavior, pytest, collection, service, body, and full suites were intentionally not run per scope. Fresh four-repo custody and body receipts remain pending for the manager.

Commit message written and `DONE` created.