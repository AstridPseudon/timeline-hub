## Verdict

- Custody: PASS. All four published files matched their declared SHA-256 hashes.
- P2/P3 gate: NOT PROVEN. Both runs fail the existing 5000 ms outbox-read prerequisite.
- P1 pinned GO remains unchanged.
- No repeat until a named meaningful fix and owner authorization.

## Evidence

- P2/10973: 7 lifecycle records; cancellation followed by generation-1 basis-read restart.
- P3/14249: 5 records; no captured cancellation.
- Both: `outbox-read` failure; only `before-load` diagnostics; connected-selection, fresh-owner stages, all eight P2 cases, and original Gate-5 were NOT RUN.
- All six recorded ports are distinct, ruling out only this pair’s port collision.
- Four-file nested schema/type/enum/bounds/security audit: PASS.
- Production projector idempotence: 2/2 PASS.
- Production writer roundtrip on real records in bounded TMPDIR: 2/2 PASS.
- Relevant App source blobs equal base `804134d74782d40855146aa568ff289200b79142`; no tracked changes.

Direct files are diagnostic evidence, not authority or full wire proof. Published producer-certified observations retain native21/history and bootstrap connection/selection PASS, but do not prove daemon import identity. Missing basis-ready/error, identity/session, and history completion are absent observations—not proven refusal or IndexedDB failure. Server cause and `f38e` attribution remain UNKNOWN.

## Commands

- `/opt/node20/bin/node --import tsx tests/e2e/local/mounted-readiness-safety.test.ts` — exit 0, 12/12 passed.
- `/opt/node20/bin/node --import tsx tests/e2e/local/d21-environment.test.ts` — exit 0, 7/7 passed.
- Production inline Node20 schema/security/projector/writer audit — exit 0.
- `git diff --check` — exit 0.
- `git status --short --branch` — clean.

No browser/backend/service/build/install/provision/graph/kit/pin/source/row/Git changes or raw trace/request/environment/credential output was produced.

## Next owner boundary

Runtime owns the next causal investigation of the pinned `_dispatch → list_timeline_commits → history verification` path using authentic daemon evidence. App/Proof should not change readiness or rerun P2/P3 until that fix is named and authorized.