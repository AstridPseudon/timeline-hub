# Handoff: ap2-P1-provenance-original-spec-port-0820

## Verdict

**PASS for the exact source port; live P1/H3 qualification remains unverified.**

The assigned App worktree started at the exact requested base
`tl/ap2-A2-split-authored-provenance-sol-0802`:

- base commit: `e90090991aa6d3f18a97b3cf51ae908e81404f0e`
- base tree: `6ab6f0f1501441f87a664fd9e599d059dcfebcb7`
- `git merge-base 8770aa1625198826778828173ef6e2c55a3c07f3 HEAD`:
  `8770aa1625198826778828173ef6e2c55a3c07f3`

Only `tests/e2e/local/three-products.p1-chain.spec.ts` was changed. Its
working-tree bytes are exactly the final donor
`tl/ap2-P1-reply-diagnostics-0727`:

- donor commit: `2b26c20a99fd14a9076fd0cbd6aa5548de14e35b`
- donor tree: `45f4b3ca9e204d3cc0223bb9929301ab5e40cf25`
- Git blob: `f8f86de446538d1bcf07774564256ecabefc7026`
- SHA-256: `d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8`
- size: 34,149 bytes

`git diff --exit-code tl/ap2-P1-reply-diagnostics-0727 -- tests/e2e/local/three-products.p1-chain.spec.ts`
passes. The port is 25 insertions and 1 deletion relative to the assigned
base: the donor's bounded structural-reply diagnostic and its required
`merge: fields` correction. No independent assertion, fixture, helper,
product, source, generated-file, package, lock, pin, or suite-row change was
made. The original seed, accepted/merged/refused chain, created IDs, reads,
ordering, raw body, opaque/null/absent values, rollback, and undo/history
coverage remain in the exact donor bytes.

The eventual App commit SHA/tree is harness-owned and therefore not available
before exit; the final source SHA/blob/tree identity above is exact and
reproducible.

## Existing suite-row disposition (read-only)

The existing `app ap2-P1-chain-h6` row in
`ORCH/tests/suites.conf` was inspected but not changed. Its current whole-file
SHA-256 is
`c4e4e6f03a3cf79258de2393ce0017009f702238d0a57a4688bbf5a0e5ca1cf8`.

The row already names the donor spec SHA and the exact `819acf…` Composition
artifact, but two expected App source hashes are stale for this requested
base. The row owner must later change only these two App hash fields:

| App source | Row currently expects | Current base SHA-256 |
| --- | --- | --- |
| `src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts` | `55585a495a6ddeb33774cf6cd51fe7b330e76e13242b475f98d57ba2c1354e57` | `2a1d0a2ee20715b4f46830566f099d4f4d2517210ce21a50c79f576c09949192` |
| `src/tools/video-editor/hooks/useTimelineCommit.ts` | `018c6e4a5febfe1398e4422a2c00c65b1335d0a73a3e9ff78259736a4efee1ae` | `7d1ecabd17b19c6ab7557ce989512ee85297b79a1f0edc8000cb59d343f9f269` |

All other inspected product hashes match the row/current base identity:

```text
src/tools/video-editor/commands/localSaveSession.ts aad778d1744c521d207c49c0786ef16e65d6651940443662eab6c22c798ae081
src/tools/video-editor/hooks/useClipEditing.ts 3357c72efad8270688d749ced49675c91fa071c8b7ade067c488b3a30a06de44
src/tools/video-editor/hooks/useTimelinePersistence.ts fb8e0532a3a3bcdf4b68a233774b0e508bf5c2831ee980c0a491be1d30c05bfa
src/tools/video-editor/hooks/useTimelineSave.ts d56fb2c9c3ae4055d9c7a913f927da5e0381399b49593a69bf3bbf1a2bedcfd6
src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts c2dc575f9657ad37453edd27bc6d2e0306cb0fa96047b335ee993b83a086a445
src/integrations/runtime/dataProvider.ts 46fbdca6ecc32292273e87b9f62abf5e8c35a3b39904f1fa8b1165ae69a9894f
config/vite/timelineCompositionPackage.test.mjs 81bd209e7f49d0d7845728784b1dec83233267325773bd598d23b20b70c04f07
vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234
```

`git diff --name-only HEAD` contains only the P1 spec, and the product-only
diff is empty. The current source caller identities are the mounted path
`useClipSplitting` (`handleSplitSelectedClip` / `handleSplitClipAtTime`) →
`useTimelineCommit` (`applyEdit` emits `localCommit` and `scheduleSave`) →
`useTimelineSave` (`createLocalSaveSession` and
`createTimelineLocalSaveHandoff`) → `useTimelinePersistence` (document-save
flush before the legacy fallback). These are source identities only; no live
browser or HTTP execution credit is claimed.

## Producer identities and limits

The inspected normal producer pins are clean and importable:

- Agent `f894c3c9dda25ab03527eeb7f52da5da31d627c1`, tree
  `d24f25a65be282a56b3fcd814a8718a3c0587b9b`
- Runtime `34eac0041b0891e9011966b39bcbd26053fde5bc`, tree
  `9853574865f25e08284e82ffb26c0bdecaa16a30`
- normal34e import check passed for `astrid`, `astrid.sdk`,
  `astrid_runtime_client`, and `runtime_protocol`

The Agent mirror for the exact reviewed checkout is still pending. Do not
rerun the old `f894` service body. No row update, service request, HTTP/body,
browser, socket, full suite, build, or live chain run was made. Independent
OPS review is appropriate after the exact Agent/App source becomes available;
this source port itself needs no new semantic review.

## Evidence

All passed:

- exact donor diff and SHA-256/blob identity check
- durable private Composition graph guards using artifact SHA-256
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`
- `npm run test:e2e:three-products -- --list tests/e2e/local/three-products.p1-chain.spec.ts`
  — exactly 2 tests in 1 file
- `npm exec tsc -- --noEmit --incremental false` — PASS
- `timeout 180 npm exec tsc -- --project tsconfig.app.json --noEmit --incremental false` — PASS
- `npm exec tsc -- --project tsconfig.node.json --noEmit --incremental false` — PASS
- `npx eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` — PASS
- `git diff --check` — PASS
- normal34e import check — PASS

