Implemented D138 in `ops-d138-cli22/` only.

- Updated source provenance to Agent `41ad…` / Runtime `f103…`, preserving canonical 15 bytes.
- Added pre-dispatch manifest validation before the unchanged launcher; duplicate, malformed, and tuple-mismatch manifests produce zero launches/artifacts.
- Added exact-row controls and evidence packet.

Tests:

- 11/11 private controls passed.
- Ruff, Python compile, `bash -n`, `git diff --check`: passed.
- Exact 22 selectors/marker/parser/per-ID checks: passed.
- Source check: correctly `NOT_READY` without central rendered manifest/receipts.
- No full suite or live body run performed.

Evidence: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-OPS-D138-cli22-service-return-2251/evidence/`

Commit message and `DONE` marker created.