# P2 Review — FAIL

Cumulative review: `6635416195 → 672127b534 → 7d3ef22794`.

Finding: genuine `localSaveSession` producer output includes `row.opacity: 1`. The tightened helper rejects it at `p2-semantic-oracle.ts:96` due to its invented fixed row-key set.

Authentic request otherwise matched:

- exact v2 top-level keys;
- command keys exactly `args/created/intent/op/schema_version/select/version`;
- `merge: fields`, omitted reads;
- ordered claims: `parent/asset:synthetic-image`, `parent/clip:clip-0`;
- empty submitted step patch;
- exact source/project/timeline/head fields.

Authentic body hash: `sha256:bc3fe9f3dfda5db0904b39227bde6eb9300b53f9d60197f174132a928cce20ae`.

Checks:

- Helper controls: PASS, 3/3.
- `tsconfig.json`: PASS.
- `tsconfig.app.json`: PASS.
- `tsconfig.node.json`: PASS.
- Scoped ESLint: PASS.
- Playwright list-only: PASS, 3 tests.
- `git diff --check`: PASS.
- Genuine prepared producer suite: PASS, 28 tests.
- Genuine automatic-placement producer suite: PASS, 18 tests.
- Authentic producer → helper probe: FAIL, due to `row.opacity`.

Hashes:

- Baseline spec: `e98bb092...`
- 672 spec/helper/controls: `d549cd...`, `21286e...`, `315d5a...`
- Current spec/helper/controls: `e1fe7a...`, `076fe9...`, `3e230b...`

No tracked changes; worktree clean. No browser, backend, HTTP, socket, service, or full-suite run. `DONE` marker and P2 commit message were written.

Recommended next step: reconcile the documented semantic row contract with the genuine producer’s `opacity` field before qualification; do not broaden the helper speculatively.