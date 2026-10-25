# D127 commands and results

Worktree source stayed byte-identical to exact task base `5a9e0eb523353a95af45563a4f3e80bd8772222e`. No implementation or qualification PASS is claimed.

| Exact command (from the assigned App worktree unless noted) | Result |
| --- | --- |
| `NODE_COMPILE_CACHE=/tmp/w-d05999a6ac/node-cache /opt/node20/bin/node --import tsx --test --test-name-pattern='D127 reviewed-new validator|D105 launch ownership' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS baseline: 2 passed, 2 selector exclusions; original D127 mutations and D105 ownership only. |
| `/opt/node20/bin/node node_modules/eslint/bin/eslint.js tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --report-unused-disable-directives --max-warnings 0` | PASS, exit 0. |
| `flock -w 60 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json --pretty false` | PASS, exit 0; serialized App config. |
| `/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json --pretty false` | PASS, exit 0. |
| `git diff --check` | PASS, no source diff. |
| `git status --short` | Clean. |
| `/opt/node20/bin/node --version` | v20.20.0. |
| `realpath node_modules` | `/home/user/work/app/node_modules`, used read-only. |
| `git -C /home/user/work/runtime show 231ddb:tests/helpers/p2_commit_phase_capture.py | sha256sum` | `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`. |
| `git -C /home/user/work/runtime show 231ddb:tests/test_p2_commit_phase_capture.py | sha256sum` | `d6b5703492b4b4d399ee1d5d7350faae615a01448df70229efc3cc03a1ecff18`. |
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /tmp/w-d05999a6ac/probe-helper.py` | PASS, exit 0; 12 direct original helper callback projections, no helper activation, Runtime bodies, sockets or sinks. |
| `/opt/node20/bin/node /tmp/w-d05999a6ac/probe-validator.mjs` | PASS of diagnostic assertions, exit 0 after correcting fixture anchor setup; actual unedited validator accepts 8 original helper projections and rejects 4 valid helper projections. This demonstrates source mismatch, not implementation success. |
| `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/w-d05999a6ac/write-evidence.py` | Wrote the pre-edit truth table: 16 internal flag combinations, 128 phase/lifecycle/response projections, 16 retention combinations, exact duration boundary rules and frozen-source citations. |

The first diagnostic wrapper run failed its own baseline assertion because the in-memory helper was not activated and its UTC anchor was left null. The scratch fixture now initializes `_utc_anchor` using the original `_utc_text()` just as `start()` does. No source, validator, helper output normalizer or product file changed. Final projection JSON/logs reflect the corrected initialization; source-custody.json records the setup correction.

## Concrete source conflicts

- Frozen helper lines 913–915 end `dispatch_queue` at handler entry. Ordinary pending output can therefore have an ended queue. This directly contradicts review 1647's claim that the queue ends only at dispatch return.
- Lines 958–959 end the queue at dispatch return only when it is still open. `raised` after handler entry consequently retains an observed queue, which the current validator rejects.
- Lines 498–503 select completed from returned + response count before considering the raised flag. Lines 954–957 leave the completion timestamp null for any dispatch error flag, including a caught error. These completed summaries are rejected by the current validator.
- Lines 909–915 support a late observed handler with no dispatch boundary; the current minimum dispatch count rejects this output. The brief also prohibits relaxing phase counts. The frozen missing-boundary unit case at tests/test_p2_commit_phase_capture.py:315–333 likewise demonstrates that lifecycle cannot be inferred solely from observed dispatch count.
- `_end`/timestamp assignments precede the lock-protected `dispatch_finished` assignment. The trace callback is not atomically snapshotted by stop. The truth table separately records these interleaving cases instead of assuming the enum fully determines phase/duration state.

See lifecycle-truth-table.json for all combination classifications and exact frozen citations. Private callback outputs and diagnostic logs are in evidence/private/; they are not normal/bootstrap qualification controls.

## Controls and preserved evidence

Normal and exact-4ee reviewed bootstrap controls: **NOTRUN**. The contradictory source requirements block editing and source qualification; there are no source-causal changes to qualify. No central test request was submitted. Qualified Runtime `ab1e4f6141987706132916e2da16477f5a019464` and Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` were verified read-only; no external helper copy or profile was created.

Initial free disk: 4,907,585,536 bytes, 92,414,464 bytes below decimal 5 GB. Latest recorded free disk: 5,026,189,312 bytes; decimal-5-GB shortfall: 0 bytes; 5-GiB shortfall: 342,519,808 bytes. Source conflict, rather than an invented disk result, is the decisive blocker.

Prior central Runtime evidence (23 passed in 3.46s) and original 160-predicate custody are reused from the cited 1647/1630 evidence. Runtime test bodies were not rerun. Known strict-islands baseline was not repeated. No full/family/P2/P4/browser/native/original-tour/recovery suite or held SWAP WIP was inspected or executed.

## Disposition

**BLOCKED before source edit**, following the instruction to report a contradicted settled decision rather than deviate. The existing baseline tests passing does not close D127. Orchestrator must correct the queue/completion assumptions and resolve missing-boundary scope, then authorize the source-consistent validator repair and its mutation controls. Independent review must follow the resulting source change.
