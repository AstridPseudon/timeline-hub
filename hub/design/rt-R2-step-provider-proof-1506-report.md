# Report: R2 step provider proof

- Verified clean Runtime candidate `39229be9…` and immutable parent `5e9ad1c6…`; no source edits.
- Agent checkout receipt `checkout-agent-8d2d5882…` verified clean at `8d2d5882…`; regression hash unchanged.
- Registered-provider test:
  - Parent: `1 passed, 1 failed` — expected physical-edge failure.
  - Candidate: `2 passed` — acceptance, ordering, and inverse restoration.
- Native smoke: `scripts/check-before-push --native-provider-smoke` → `2 passed`.
- Admission stayed above 5 GB before each body; evidence 19,065 bytes, TMPDIR 713,350 bytes.
- Source/security PASS80 and Agent independent boundary evidence were consumed, not rerun.

Evidence is under the assigned `evidence/` directory. Commit message and empty `DONE` marker were created. No full/original-four/TEN/P4/browser suites ran. Flat design publication remains manager-owned per harness rules.