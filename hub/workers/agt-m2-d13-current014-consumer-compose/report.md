Implemented the reviewed D13 registered-native producer/requester port onto staged014.

- Added native admission, settled proposal reads, requester outbox flow, and GenericHost legacy-publication removal.
- Replaced the unapproved render-test skip with `use_runtime()`.
- Preserved P1/F1/WC4/WC9, Scene/save-core, Root/service, and sprite/plate paths.
- Product diff: 821 additions / 240 deletions including two new files.
- Tests: 111 passed, 2 deselected; focused Ruff and `git diff --check` passed.
- Exact a0 integration: 1 passed, 1 failed because the suite omitted `ASTRID_REMOTION_PROJECT_DIR`.
- Current-runtime integration was blocked by schema mismatch. Full two-positive render/decode/undo proof remains unverified on this composed tree.

Handoff and report written under `scratchpad/orch/design` and worker files. `DONE` created; D13 remains held until integration merge/requalification.