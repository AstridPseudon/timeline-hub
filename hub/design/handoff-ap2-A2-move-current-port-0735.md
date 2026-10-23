# A2 move-reads current own-commit port — 2026-10-23

## Result

PASS for the bounded current-base port. Current App base is
`890b9561666c3619f69335dd747b15e042b3a9a3`, tree
`20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473`. Exact donor is
`tl/ap2-A2-move-reads-failover-0725` at final SHA
`4090c276372c46bbe164c486117705a788f53f09` (donor tree
`d6108937504538ebca0698cf0068f76a62c39ad5`). Only its seven authorized
blobs were imported; the harness final commit SHA is pending. The current
worktree has no outside-file diff against base.

## Blob and conflict disposition

The seven imported blobs are exactly:

- `timelineLocalSaveHandoff.ts` → `32719e876509cb3cc4b06027dbff0756ee146bac`
- `timelineLocalSaveHandoff.test.ts` → `15fb8bc2ddc33818a9099d4b770b7dfbfca253f7`
- `useClipDrag.helpers.ts` → `6d496e3fd897d7a8396b27a2c2ede4561feb05a2`
- `useClipDrag.ts` → `108f86f7180b882cda4356d1ed4f1e8ff7684b73`
- `useClipDrag.test.tsx` → `b4c78f44692a07b20b70528ab46a8c120cb03030`
- `useTimelineTrackManagement.ts` → `40b12a5d0cadc282400a304efe52dd3fffb247d7`
- `useTimelineTrackManagement.test.ts` → `7c34989fc99cc75d3a7bf40517688546f2d052e4`

Source blob equality passed. The current-base side has no independent changes
to the seven files after merge base `8770aa1625198826778828173ef6e2c55a3c07f3`,
so there was no genuine owner-file conflict. Current paired-head,
startup-spec, private graph, pins, and all other outside files remain equal to
base.

## Commands and results

- Hook targeted Vitest command — PASS, `63/63`.
- Local-save session targeted Vitest command (`localSaveSession.test.ts` and
  `.v2.test.ts`) — PASS, `20/20`.
- `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit` — PASS.
- Scoped seven-file ESLint with `--max-warnings 0` — PASS.
- `git diff --check` — PASS.
- Normal Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc` lock check and
  App vendor-lock check — PASS.
- Private exact `819acf` Composition graph — PASS, 10/10 subtests, archive
  SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`,
  package `0.0.14`.

The shared-install graph probe was not accepted as evidence because the
machine's shared install contains Composition `0.0.8`; a private overlay was
used and passed without modifying shared dependencies.

## Limits / next step

No HTTP, browser, localhost/service, build, full-suite, or central test-service
run. Actual Runtime accepted/merged/refused admission and live restart remain
unverified. Manager should verify `git log tl/integration..tl/ap2-A2-move-current-port-0735`
contains only the harness-created own commit before requesting the remote App
merge.
