# PASS — A3/P2 core source review

Reviewed `90058e4ff7` against base `913686448c`.

Source trace confirms:

- Popup mounts shared controls through `ShotTimelinePreview`.
- Runtime supplies a stable per-editor `Symbol` owner.
- Controls now use `useTimelineMultiSelect(runtime.agentSelectionOwner)` for display, capture, and async stale-selection guards.
- Projection produces occurrence-qualified IDs: `${occurrenceId}:${rawClipId}`.

Evidence:

- Mounted controls: **11/11 passed**
- Neighbor Vitest suite: **62/62 passed**
- Popup selector oracle: **PASS** — old selector RED; exact target/reference GREEN; wrong occurrence, sibling, and same-byte identities remain distinct/refused.
- `tsconfig.node.json`, `tsconfig.app.json`, `tsconfig.json`: PASS
- Scoped ESLint `--max-warnings=0`: PASS
- `git diff --check`: PASS

Reviewed blobs:

- Product: `9afbf18c4b2ecd8c357c0ee0caa416575c2c639f`
- Test: `444c9249eca75c845a9ad3eb6fd6be452502e84e`

All six protected SHA-256 hashes and popup predicates/waits are unchanged. No product/test files were authored by this reviewer.

Normal merge completed:

- Receipt: `18de74bd43bab71d11188054bd3035016b37ceaa`
- Merged into `tl/integration`
- Merged blobs match exactly.

Existing ledger: prior selector review/merge remains preserved. Historical ADD body `app-pin-c9d71b65...6954` correctly failed at the selected-label predicate; this review claims no browser, history, or Undo rerun.

No next ADD was reserved: placement body `...0062...16952` is terminal `fail`, but other App bodies remain running (`...6629`, `...4151`, `...11089`). `DONE` and commit message were created.