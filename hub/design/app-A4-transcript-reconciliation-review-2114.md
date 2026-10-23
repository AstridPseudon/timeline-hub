## Result: PASS

PASS for the bounded test addition only. This is not whole-A4 parity, retirement credit, or P1 approval. Branch remains HOLD.

The change is exactly one test file: [project-transcript-host.persistence.test.tsx](/home/user/work/wt/app-A4-transcript-reconciliation-review-2114/src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx:1), `283+ / 9-`. The nine removals are helper/import setup only; existing mounted tests, old capture tests, and production implementations remain.

Source: `cf05c6ca11966eeded8101a2df7a1f5ad827d6a8`, tree `d8f6ff13f0c9e0d9a7203ba9080f202f84345155`. Base: `001145ce1dcba562ab082620e965e73bac1857d1`, tree `e9fc8619a263ac4dee427ec7acd8478b3d03d359`.

### Case qualification

- Existing accepted/refused mounted outbox witnesses remain passing at lines 437–568: real host → A2 save → local outbox → `RuntimeDataProvider` → generated transport seam.
- Config-mirror fallback at line 570 records the actual A2 refusal: no request/wire emission and `contradictory parent clips mirror`. This does not preserve the old dormant positive fallback.
- Caption/review reconciliation at line 605 emits one full-v2 `doc.patch` request and persists the canonical caption/review. It explicitly records that the legacy review key remains; this differs from the old capture’s atomic delete-and-move behavior.
- Collision/shared-row cases at line 644 are accepted generic patches by the mounted transport mock. They do not reproduce the old `transcript.associate` `identity_conflict` refusals.
- Uncovered old cases: exact prior-pin/source-order replacement, pin mismatch, malformed pinned source, full operation records/bindings/selections, and old refusal parity. See [transcriptAssociateCapture.test.ts](/home/user/work/wt/app-A4-transcript-reconciliation-review-2114/src/tools/video-editor/commands/transcriptAssociateCapture.test.ts:161).

The transport uses the genuine mounted App path, but its commit response is locally synthesized with `acceptedCommit` and a permissive patch applier. It is not Python Agent authority, live HTTP, or backend semantic validation. Therefore collision/shared-row acceptance is only an App request/current-shape witness.

Full response variants remain uncovered: `merged`, historical `rebased`, preview/`would_status`, invalid envelopes, and complete records/history/effects/undo fields. The accepted test covers the emitted request, base pair, `doc.patch`, steps, receipt, and canonical adoption.

### Verification

- Targeted Vitest with dirname preload — PASS, 4 files / 56 tests.
- ESLint scoped with `--max-warnings 0` — PASS.
- `tsc --noEmit` for `tsconfig.app.json`, `tsconfig.node.json`, and `tsconfig.json` under `/home/user/work/.app-tsc.lock` — PASS.
- `git diff --check` — PASS.
- Scope audit: only the assigned test file changed.
- Node: `v22.22.0`.
- No browser, live HTTP/backend, seed, build, full suite, or control suite run.

The plain Vitest command first hit the known config-loader `__dirname` startup error; rerunning with the existing dirname preload passed.

Smallest next step: keep A4/P1 on hold until Runtime/Agent integration supplies an authoritative v2 acceptance/refusal witness for collision/shared ownership and the remaining response variants; then extend only this mounted test without introducing a new operation, authority, or guard semantics.

Commit message and `DONE` marker were written.