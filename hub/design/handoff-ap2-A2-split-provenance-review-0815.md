# Independent A2 provenance review — PASS

Review target: `tl/ap2-A2-split-authored-provenance-sol-0802`  
Reviewed commit: `e90090991aa6d3f18a97b3cf51ae908e81404f0e`  
Base: `890b9561666c3619f69335dd747b15e042b3a9a3`  
Reviewed tree: `6ab6f0f1501441f87a664fd9e599d059dcfebcb7`  
Base tree: `20c8c1ed5e9ca48bc1f56f66f0404c83f8d97473`

Read first: PLAN v2.1 §3/A2 and `design/handoff-ap2-A2-split-authored-provenance-sol-0802.md`; compared with the source-derived causal report/handoff `ap2-P1-first-split-conflict-sol-0747`.

## Scope and result

PASS for the requested A2 four-file review. The production path is intact:

`useClipSplitting` (all three gesture entry points) -> `useClipEditing.applyConfigEdit` -> `useTimelineCommit.applyEdit` -> `serializeResolvedTimelineEdit` -> `serializeForDisk` -> registry rebuild/assembly -> scheduleSave -> mounted A2 handoff -> document intent/outbox.

The only tracked files changed from the A2 base are the allowlisted four:

- `src/tools/video-editor/lib/serialize.ts`
- `src/tools/video-editor/hooks/useTimelineCommit.ts`
- `src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts`
- `src/tools/video-editor/hooks/useTimelineCommit.test.tsx`

No P1 GO is inferred. No Agent/provider mirror fix is inferred.

## Four-file blob IDs

| file | base blob | reviewed blob |
|---|---|---|
| `src/tools/video-editor/lib/serialize.ts` | `11c5a665eb4bb80e3655b1e768a3f9c11998557f` | `aab660cd3f27925194f23e52f8227458fdc3f22f` |
| `src/tools/video-editor/hooks/useTimelineCommit.ts` | `e821e48be2d1e9a740c0c9749f1613cf03e4ed52` | `19b0b236a7f40d613d5a08fad4d23136e35d8880` |
| `src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts` | `79f93eb5d7152683e9c21c44d414f866d8a3ee0f` | `83f39d377a365575902837f5ae69f209ca75b64c` |
| `src/tools/video-editor/hooks/useTimelineCommit.test.tsx` | `3df19368d3ba2813158246d4f04cf66f509babd6` | `936df060b71c46d60e30279389e6c4d0960ab929` |

Diff: 112 insertions, 6 deletions; `git diff --name-only 890b95616..HEAD` lists only these four files.

## Independent implementation audit

- `withAuthoredClipLabels` joins raw authored clips and the prior displayed clips by exact existing ID. It restores raw own-label presence/value only when the displayed value is unchanged; it preserves changed labels and does not compare labels to filenames or infer identity from prefixes.
- The mapping runs before the split helper copies the source row and allocates the right-row ID in all three split entry points. The existing `createSplitClipId` is still the sole allocator; the new ID is generated once per split and remains the existing insertion/order/guard path.
- Absent, null, and default output provenance is retained through the config-edit serializer: the resolved output is carried into the local editor config while `serializeForDisk` still deletes `output` for strict disk serialization. The handoff's existing raw-vs-display diff therefore preserves raw absent/null/default output fields and applies only actual output edits.
- Unknown/opaque app data remains carried through the existing serializer/handoff. No atomic mode, declared-read derivation, fabricated reads, output-first reorder, label heuristic, provider guard, executor, fixture, or new save route was added.
- Existing order, collection guard, previous-value operands, created-ID behavior, and all 13 split consulted reads are unchanged. The new regression asserts the exact one `list.insert` plus source `hold` set, original order, `before`/order guards, right ID, raw labels, opaque data, and exact reads.
- Full-v2 request/reply fields and behavior (api_version 1, scope/base pair, commands, label, per-step id/label/intent/tags/ordinals/patch/reads, merge/reads/dry_run/key, accepted/merged canonical/head/digest/receipt/records/effects/bindings/dependencies/undo/history/publisher/provider/compiler, and conflict/invalid code/path/hint) are outside the four-file diff and remained unchanged in the targeted integration tests.

## Exact commands and results

All Vitest runs used a private config/cache under `/tmp/w-8c83cf971a`, `--configLoader runner`, and `--no-cache`; no shared `.vite` or install was modified.

1. Normal author-targeted run, exit 0, **8 files / 162 tests passed**:

```sh
timeout 45s node_modules/.bin/vitest run --config /tmp/w-8c83cf971a/review-vitest.config.mjs --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/documentPatchIntent.test.ts src/integrations/runtime/client.test.ts
```

2. Private exact Composition run using artifact SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`, package 0.0.14, exit 0, **8 files / 162 tests passed**:

```sh
REVIEW_COMPOSITION=/tmp/w-8c83cf971a/composition-exact/package timeout 45s node_modules/.bin/vitest run --config /tmp/w-8c83cf971a/review-vitest.config.mjs --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/useClipEditing.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/commands/localSaveSession.test.ts src/tools/video-editor/commands/localSaveSession.v2.test.ts src/tools/video-editor/commands/documentPatchIntent.test.ts src/integrations/runtime/client.test.ts
```

3. Private baseline RED overlay: baseline source `890b95616` plus the reviewed regression test, exit 1, **3 failures / 13 skipped**. All three fail at the expected unchanged baseline behavior: `out.mp4` becomes `output.mp4`. The third failure is the intentional filename-equal label control added by the reviewed regression; it has the same baseline output-root cause.

```sh
REVIEW_ROOT=/tmp/w-8c83cf971a/baseline-890b95616 REVIEW_ASTRID=/tmp/w-8c83cf971a/baseline-890b95616/vendor/astrid-browser/astrid timeout 45s node_modules/.bin/vitest run --config /tmp/w-8c83cf971a/review-vitest.config.mjs --configLoader runner --no-cache src/tools/video-editor/hooks/useTimelineCommit.test.tsx -t 'splits the original raw seed'
```

4. Unchanged `timeline-save-utils` comparison:

```sh
timeout 45s node_modules/.bin/vitest run --config /tmp/w-8c83cf971a/review-vitest.config.mjs --configLoader runner --no-cache src/tools/video-editor/lib/timeline-save-utils.test.ts
```

Current result: exit 1, **3 failures / 24 passes**. The same command on the private baseline overlay produced the same exit/result and the same three named failures:

- `assembleTimelineData produces consistent output with the resolved-config signature`
- `buildDataFromCurrentRegistry materializes rows from clip geometry while keeping soft-tag groups unchanged`
- `repairs legacy pinned groups to soft-tag `clipIds` without re-projecting clip geometry`

These are the pre-existing resolved-config identity/signature failures caused by display-label projection; no assertion was changed, skipped, or weakened.

5. Typechecks, all exit 0:

```sh
timeout 180s node_modules/.bin/tsc --noEmit --incremental false
timeout 180s node_modules/.bin/tsc -p tsconfig.app.json --noEmit --incremental false
timeout 180s node_modules/.bin/tsc -p tsconfig.node.json --noEmit --incremental false
timeout 180s node_modules/.bin/tsc -p /tmp/w-8c83cf971a/tsconfig-exact-publicgraph.json --noEmit --incremental false
```

The exact public-graph check maps Composition types to the private 0.0.14 artifact above. No new diagnostics.

6. Scoped hygiene checks, all exit 0:

```sh
timeout 45s node_modules/.bin/eslint src/tools/video-editor/lib/serialize.ts src/tools/video-editor/hooks/useTimelineCommit.ts src/tools/video-editor/hooks/clip-editing/useClipSplitting.ts src/tools/video-editor/hooks/useTimelineCommit.test.tsx --max-warnings 0
git diff --check 890b95616..HEAD
node scripts/vendor-lock.mjs check runtime.lock.json
```

Vendor-lock output: `ok runtime.lock.json`.

## Preserved identity/hashes

- Original P1 source `tests/e2e/local/three-products.p1-chain.spec.ts` SHA-256 is unchanged: `cae24b8e5481557f4812e47f06828aed3cf2176c6da92b4ca265095dbefd8175` both at HEAD and base.
- `package.json`: `ce59c57b8f2a9da6e86cccbb31ad71876a86e33f910bb601ebf2dc727d040bdf`.
- `package-lock.json`: `59cd66da9a223eb1ff3cf60fd06dfa5b4b376533786366bd94b74ae3d95140ba`.
- `runtime.lock.json`: `eb52cbbb3a1f40caca965eb0cb2c87142100adabb4c876a8582b6894c4281c8e`.
- Worktree status is clean relative to the reviewed commit; no product files outside the allowlist changed.

## Limits and next steps

- No full suite, browser, HTTP, live socket/service, build, or original P1 body execution was run, per task/orchestrator limits.
- The private baseline RED and targeted tests exercise the real hooks, handoff, patch emitter, session, and outbox with mocked transport; they do not claim accepted/merged/refused/restart or H3/P1 end-to-end proof.
- App typecheck is now qualified in this environment, including the private exact public graph; the original author’s 45-second timeout was not treated as a failure.
- Recommended next step: owner-controlled integration preserving queued move/Undo work, followed by changed-evidence P1 execution and independent Agent mirror correction/qualification. Do not grant P1 GO or infer an Agent fix from this App review.

