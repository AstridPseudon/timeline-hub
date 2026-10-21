# AP2 M2 parent final current packet review 0413

## Verdict

**HOLD. Do not approve the 0356 tuple or authorize the parent actual.**

The smallest concrete defect is a source-identity/guard mismatch. The packet
commit is `0daaee4698c83e749dc2c3e204965b12ff3cd8ec`, with tree
`a95793cc2179200dd9ef5fe551360a4f6f965ea1`, parent `976e08c6c`, and it is not
descended from the merged HOME source `5d36b0e53ff0d17ef045e226a6e6ca7584322858`
(tree `1b07030d63216294f849422523b0d55a17422f23`). The 0356 report instead
claims the actual source argument is a snapshot of `5d36b0e53`/`1b07030d`.
Those are not the same frozen source tree: the packet adds the proof support
and exact assertion after the claimed source snapshot.

The closed shared source guard is also still stale for the claimed final
source:

```text
NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent
APP_ROOT_SHA=da6d910f7ab3dfc71142ece7f632d43341238882
APP_ROOT_TREE=6809757f93ca5e166b24b8bc0160ca09005e984a
```

The 0356 report records that the shared full preflight was not run because of
this stale guard. Therefore the final source SHA/tree, actual source argument,
complete prerequisite preflight, and final-source wrong-source/graph/argv
negative controls are not qualified. The packet's own helper only checks that
the observed HEAD descends from `84ec385a`; it does not establish the exact
final tree requested by this review.

## What was preserved and checked

- The packet has author 0230's exact `404` assertion and exact JSON body:
  `code: not_found` and `selected media is not a managed project
  generation/variant/object`.
- The ADD body retains the native acceptance, raw/opaque data, order,
  lost-ack, reload, restart, exact body/key retry, undo, and zero-legacy
  assertions. The packet diff against the 0230 candidate changes only the
  exact wrong-selection assertion in the expected direction.
- The current HOME source remains present at merged `5d36b0e53`, including the
  qualified native bootstrap production merge at `1557c312b`; no bootstrap
  replay was requested or run. The 0356 packet does not remove HOME tests or
  the zero-test guard.
- Durable driver SHA-256 is
  `40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f`.
- Reported suite is
  `app ap2-m2-parent-composed-driver-label-durable-stage-0323-e2e-integration`.
- Reported actual command is:

  ```text
  env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh <durable-driver> run "$PWD"
  ```

- The exact manual-drop collection is one test in one file, at
  `three-products.spec.ts:1440`.

## Commands and results

- `df -BG /tmp` — PASS; 16 GiB free, above the 10 GiB floor.
- `realpath node_modules` — PASS; resolves to the shared read-only App install
  `/home/user/work/app/node_modules`.
- `sh -n` on the packet's extracted `run-parent-manual-drop-evidence.sh` —
  PASS.
- `git diff --check 5d36b0e53 0daaee469 -- tests/e2e/local/support/run-parent-manual-drop-evidence.sh tests/e2e/local/three-products.spec.ts` — PASS.
- Packet support `probe` — PASS; the zero-test child was refused and the
  failure-trap evidence was copied before cleanup.
- `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list` — PASS; exactly 1 test collected. This was collection only, not a browser run.
- The 0356 report's shared full preflight — **not run**; it stopped at the
  stale parent source guard. No browser/actual run, repeated build, or full
  suite was run for this review.

## Changed live callers

Only test/proof callers changed in the packet:

- `tests/e2e/local/support/run-parent-manual-drop-evidence.sh` — durable
  parent proof wrapper/source guard.
- `tests/e2e/local/three-products.spec.ts` — existing mounted parent ADD
  journey assertion.

No production live caller changed in this packet review.

## Required next step

Recompose the exact 0356 proof changes on the merged HOME source, freeze and
report that resulting commit/tree as the actual source argument, update the
closed `final95:parent` guard to that exact source identity, then obtain a
fresh complete preflight with the wrong-source, wrong-graph, wrong-argv, and
zero-child negatives. Only then can the exact tuple be reviewed for approval.
