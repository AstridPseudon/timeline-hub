## Report

Created:

- [full9758-setup-causes.json](/home/user/work/wt/agt-F-full9758-setup-1052/evidence/full9758-setup-causes.json)
- [full9758-setup-causes.csv](/home/user/work/wt/agt-F-full9758-setup-1052/evidence/full9758-setup-causes.csv)

The records contain exactly 45 unique ERROR nodes with matching JSON/CSV membership:

- 3 `Too many levels of symbolic links`: stale composition14 renderer profile has recursive `node_modules`; owner is profile/provisioning setup, next input is qualified profile `agent-remotion-v3-819acf-1110`.
- 42 artifact hash assertions: stale profile artifact `21fde...` versus expected qualified artifact `819acf...`; same owner and next input.

The venue command did use Node 20.19.4 and the runtime projection. None of these 45 errors has a literal `runtime_protocol` or Node-version exception; however, the selected renderer profile remains stale/malformed. This does not establish that the other 231 failures’ runtime-protocol issues are fixed.

Validation:

- JSON/CSV parity: PASS — 45 rows, 45 unique IDs, exact membership.
- Source hash verification via `git show ba55...:<path> | sha256sum`: PASS for all three source files.
- `git diff --check -- evidence`: PASS.
- Product tests, type checks, lint, full reruns: not run per evidence-only instructions.

Prior receipt scope was preserved: only the exact public-checkout node had a prior passing receipt with the qualified profile; no exact prior pass was claimed for the other rows. No source, tests, environment, or official count was changed. Commit message and `DONE` marker were written.