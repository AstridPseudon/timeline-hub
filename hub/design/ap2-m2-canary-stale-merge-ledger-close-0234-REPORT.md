# App2 M2 canary stale-reference ledger closure

Closed only `D01-app-ordinary-batch-compiler-canary-strict-debt` in both
`design/deletion-ledger.app.md` and the matching row in
`design/deletion-ledger.md`.

The row is now `DELETED`, backed by HOME merge
`743d3464d1ed548986f29249bd9b4215baccf9bb`, which merges candidate
`ff04c7d2cfa02f2b4aaa2a92a634cac4c4539bb0`. The synced `tl/integration` ref
points to that merge. Its first-parent diff is exactly two deletions in two
files:

- `eslint.strict-debt.js`: the stale `src/tools/video-editor/lib/compiler-canary.ts` entry.
- `docs/cutover-inventory.md`: the stale `tools/video-editor/lib/compiler-canary.test.ts` row.

No threshold, caller, product source, or test behavior changed. The broad
`D01-app-ordinary-batch` row remains `OPEN`; the original canary module row
remains `DELETED692765846`; the bootstrap row and all other rows are preserved.

Evidence and checks:

- Merge identity: `git show -s --format=... 743d3464d1ed548986f29249bd9b4215baccf9bb` showed parents `ce7152ee4bd5c2dc07454d18200d3be8225ca391` and candidate `ff04c7d2cfa02f2b4aaa2a92a634cac4c4539bb0`.
- Merge delta: `git diff --stat ce7152ee4bd5c2dc07454d18200d3be8225ca391 743d3464d1ed548986f29249bd9b4215baccf9bb -- eslint.strict-debt.js docs/cutover-inventory.md` reported `2 files changed, 2 deletions(-)`; `--numstat` reported `0 1` for each file.
- Candidate focused checks passed: `./node_modules/.bin/eslint eslint.strict-debt.js --max-warnings 0`; `node --check eslint.strict-debt.js`; the exact `rg`/`test ! -e` inventory/module absence check; and `git diff --check`.
- Synced merge-tree checks found neither stale compiler-canary inventory reference.

No new product tests, browser, localhost, socket, full suite, install, or
source sweep was run, as required for this ledger-only closure.

Blocked: none.
