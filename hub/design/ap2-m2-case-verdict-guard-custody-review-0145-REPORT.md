# App2 normal014 required-case verdict guard custody review

## Decision

APPROVE the worker 0132 artifact at this exact hash:

`design/normal014-app-central.sh`  
`c18d79205ca3b6af4a679ecef9cba0c11a1c3afee23b1daa56d95f109bedbf20`

The unchanged companion helper is:

`design/normal014-source-common.sh`  
`3b2018de1fbc123135590c37d4b17e995fd194fc39089b793e3f1b82e742bd56`

No source files were edited in this review.

## Real-schema comparison

- `playwright.three-products.config.ts:11` sets `outputDir` from
  `PLAYWRIGHT_OUTPUT_DIR`; the runner exports that directory as
  `$run_root/browser-output`, so its JSON path is the actual reporter path
  `$run_root/browser-output/three-products-summary.json`.
- `tests/e2e/local/three-products.spec.ts:180-188` records each case as
  `{ name: testInfo.title, status: testInfo.status, ... }`.
- `tests/e2e/local/three-products.spec.ts:193-205` writes the existing
  summary object with `cases: journey.cases`; no new report format is used.
- The exact bootstrap spec title at line 1637 is
  `M2 real gate 5 bootstrap actual consumer: production initializer uses
  native create/init, exact retry, restart and guarded undo`, matching the
  runner constant exactly.
- The current95 neighbor at line 1145 has a different full title. The runner
  uses an anchored exact `--grep` and the parser uses exact `item.name`
  equality, so that neighbor cannot be selected or counted as bootstrap.

There is no `beginCase` symbol in the current App source. The effective
begin/end bookkeeping is the existing `beforeEach`/`afterEach` pair; the
reporter’s authoritative case name/status are `testInfo.title` and
`testInfo.status` as above.

## Guard behavior

The parser requires the existing `cases` array to contain exactly one record
with the exact bootstrap name and `status: "passed"`. Missing, failed,
duplicate, wrong-name, and other-status records fail closed. The child status
is captured around the existing `flock`/Playwright command; the guard changes
status only when the child returned zero, preserving a genuine child error.
The guard runs before the existing EXIT cleanup. The existing cleanup/retention
controls remain in `normal014-source-common.sh`; no historical result was
rewritten and no generic log regex was added.

## Evidence

Commands run:

- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-app-central.sh` — PASS.
- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/normal014-source-common.sh` — PASS.
- `sha256sum` on both helper files — PASS; hashes above match worker 0132.
- `git diff --check` and `git status --short --branch` in the assigned
  worktree — PASS; clean worktree.
- Read-only private Node/bash probe using the actual guard function and the
  real reporter field shape — PASS: complete passed case/child 0 => 0;
  failed, missing, wrong-name, and duplicate cases/child 0 => 1; failed case
  with child 23 => 23. The probe used a private `/tmp` root and removed it at
  EXIT; no browser, socket, build, install, gate, or full suite ran.

Worker 0132’s existing synthetic wrapper probe also verified the actual
wrapper’s `flock` child path, exact grep argument, and EXIT cleanup. Its
targeted Node test was unavailable under the environment’s Node 22 and the
qualified Node 20 toolchain was unavailable; this review did not relabel that
limitation as a pass.

HOME remains the sole owner of the real bootstrap execution. No duplicate
bootstrap run is authorized by this review.

## Next step

Consume only the approved `c18d792...` helper artifact in the existing HOME
bootstrap workflow, then qualify the real bootstrap case from its real
structured summary. Keep the retained 4657 contradictory evidence as FAIL
until that one authorized run supplies a complete real-schema passed case.
