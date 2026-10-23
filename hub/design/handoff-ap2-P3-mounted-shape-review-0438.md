# Handoff: P3 mounted-shape review — FAIL / execution blocked

Reviewed `cc64db3a8e804886d4331987da8344108b97fb3d` against reviewed metadata
source `bd4a89bb31484e6b973f8657b39514c0ecb3d244`. The diff is limited to
`tests/e2e/local/three-products.spec.ts` and is source-faithful:

- persisted `local-save.documentIntent` is the source for the mounted A/B
  document shape, `{ after: A }` dependency basis, canonical before/after
  positions 5 → 7, exact `parent/clips/id:<appClipId>/at` guarded set, and
  request/step metadata;
- A, reset, Agent C, lost ACK, B, reload, Runtime restart, exact retry
  key/body/receipt, strict `merged`, closure, opaque data, undo, authoritative
  history, and zero-legacy assertions remain preserved;
- native journeys and `expectV2History` are unchanged; no semantic TS apply,
  forced fields, or synthetic `reads` were added.

The source/fixture review is PASS, but execution readiness is **FAIL/BLOCKED**.
Current `66b` move production flow is:

`useClipEditing.ts:235-283` `{ at }` move → `useTimelineCommit.ts:398-402`
`scheduleSave(nextData)` → `useTimelinePersistence.ts:1008-1011` snapshot-only
capture → `useTimelineSave.ts:85-92` source-only forwarding →
`timelineLocalSaveHandoff.ts:163-190` no read basis →
`localSaveSession.ts:161-169` omitted `reads`, atomic fallback.

The provider consequently guards the whole touched parent. Gate5’s intervening
Agent C is in that parent, so strict merged B cannot be qualified from this
fixture. Readonly D13 source `0e15600a6` handles only split/trim
(`timelineLocalSaveHandoff.ts:18-25,198-248`); its `useClipEditing.ts:246-248`
condition excludes move `at`. The exact missing seam is the move read-basis
carrier through `useTimelineCommit` → `useTimelinePersistence` →
`timelineLocalSaveHandoff`; no duplicate D13 review or fixture workaround is
recommended.

Evidence:

- Gate5 `--list`: PASS, exactly 1 test.
- `npm exec tsc -- --noEmit`: PASS.
- exact-file ESLint with `--max-warnings 0`: PASS.
- `git diff --check`: PASS; only the requested spec changed.
- No browser/socket/service/body/build/full run.

Next: land the production move read-basis seam with faithful consulted reads,
then re-run Gate5 and retain strict `merged`.
