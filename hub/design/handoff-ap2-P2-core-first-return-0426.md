# Handoff: ap2-P2-core-first-return-0426

The source-only P2 repair is ready for review in the worker worktree. The allowed test file now follows the mounted A2 caller rather than assuming semantic `clip.move`/`clip.set` commands:

- normal gestures send one exact `doc.patch` command with guarded `set`/`remove` changes and ordered step patch bytes;
- the caller omits request and step reads, sends `merge: "atomic"`, `dry_run: false`, and `source: { via: "app" }`; the test preserves omission versus `reads: []`;
- accepted replies are checked for base/previous/accepted heads, canonical closure, digest, id map, provider/compiler/publisher, receipt identity, normalized commands, effective merge mode, and authoritative steps;
- Runtime reads are used to compare the complete returned closure, including schema/scope identity, parent/child digests, manifest pins, raw absence versus null, opaque values, order, mirrors, and all untouched siblings;
- history is joined by receipt/publication id and checks authoritative normalized parent paths (`config/clips/id:<id>/field`), records, dependencies, undo attribution, and no new legacy entries; network checks reject any non-GET legacy write route;
- reload and mounted Undo are retained. Undo uses the actual current `undoTimeline` legacy-shaped inverse request, while its accepted canonical result and recorded inverse remain asserted.

## Evidence

- `.../three-products.p2-tour.spec.ts --list` — PASS, exactly 3 tests.
- `npm exec tsc -- --noEmit` — PASS; root project excludes e2e tests through `tsconfig.app.json`.
- `npx eslint tests/e2e/local/three-products.p2-tour.spec.ts --max-warnings 0` — PASS.
- `git diff --check` — PASS.

## UNEXECUTED

No browser/socket/Runtime/farm/full/service execution was performed. The actual three gesture bodies, Runtime history, and mounted Undo require the central service after the App0406 resolver fix.

## Open P2 inventory

Ordinary batch, manual ADD, occurrence duplicate, popup SWAP, selected element/parameters, and the other original/shared-image cases remain open.
