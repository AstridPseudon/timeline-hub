# Farm P3 run4 (tf-p3-run4): preflight GREEN, ONE Gate-5 run RED

Date: 2026-10-23. Tuple: App 2107e1870e51c650d59315f4cc1ab6af338f198c, tree a3ff3584e9b559bbb3c3a82b77be7516ed8e761c.

**Status: the gate ran once and FAILED (exit 1) at the mounted-editor readiness step, inside the original body. No retry. P2 was not started.**

## 1. Guard (decision 1): applied to rows 154 and 155 only

Harness file: `$ORCH/tests/suites.conf` (the run3 state, sha256 `bfe6694d…`, matched before the edit). Backup: `/tmp/w-79d31cf50f/tf-p3-run4/suites.conf.run4-before`.

| Item | Value |
|---|---|
| Old guard primitive count (rows 154, 155) | 1 each |
| Old primitive | `test "$(git rev-parse HEAD^)" = 2107e1870e51c650d59315f4cc1ab6af338f198c` |
| New primitive | `( test "$(git rev-parse HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c \|\| test "$(git show -s --format=%P HEAD)" = 2107e1870e51c650d59315f4cc1ab6af338f198c ) && test "$(git rev-parse HEAD^{tree})" = a3ff3584e9b559bbb3c3a82b77be7516ed8e761c` |
| Diagnostic rows 156, 157 | untouched (still carry `HEAD^`; not acceptance rows) |
| `suites.conf` sha256 before / after | `bfe6694db0a659b752448193e677d91aa4c8f631ead8312b3c38a32a6ec250d1` / `bccffe75a2df5605cb711f1640f84c0937ac710cbf384b9a43fd7c16a2f1283f` |
| Changed lines | 154, 155 only (script asserted this) |

## 2. Graph (decision 2): built on the farm, private to this worker

Location: `/tmp/w-79d31cf50f/tf-p3-run4/private/node_modules` (`$TMPDIR`, dispatcher-assigned host path). The row GRAPH variable now points there in rows 154 and 155. The 0407 proof path is gone from both rows (0 remaining).

Build (`/tmp/w-79d31cf50f/tf-p3-run4/build-graph.mjs`, run with default node v22.22.0; no npm, no Node 20, no toolchain PATH):

1. `prepareNodeModulesOverlay(appRoot=/home/user/work/wt/tf-p3-run4, dependencyRoot=/home/user/work/app/node_modules, privateRoot=…/private)` from the existing helper. The shared install was read only. The helper's own restore function was **not** called, because it deletes the overlay.
2. The helper linked the scoped package `@banodoco/timeline-composition` to the shared install, which carries **0.0.13**, not 0.0.14. Inside the private overlay only, I unlinked that one symlink and replaced it with a physical extraction of the locked archive (`tar -xzf … --strip-components=1`).
3. My worktree's `node_modules` link was restored to `/home/user/work/app/node_modules`. This link is in the worktree, not in a shared install.

Verification (`verify-graph.mjs`):

| Check | Result |
|---|---|
| Archive `vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz` sha256 | `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` (match) |
| Archive bytes / regular members | 73,451 / 80 (match) |
| Regular files in graph composition | 80 |
| Byte mismatches, graph vs archive | 0 |
| Composition version | 0.0.14 |
| Package-root `effects/animations/transitions.generated.js` and `typescript` | absent |
| Composition directory physical (not symlink) | true |
| Shared composition still | 0.0.13 (untouched) |
| Worktree `node_modules` realpath | `/home/user/work/app/node_modules` (restored) |

Not used: the helper's gate-level constants (0.0.13 / 77 files) do not apply to this 0.0.14 graph, so I did not call `runRealProxyGate`. The row's own 80-file, export, probe and version checks did run on the runner.

## 3. Body hashes (command bytes after `app <suite> `, no newline)

| Row | Before | After |
|---|---|---|
| 154 `ap2-P3-gate5-h6-0348` | `5ca8c17202c98c29da273f3c353402f66a2a3f72d72a85b06049b9b03b601b0a` (matches run3 "after") | `b40072a8b8c5b13dd71618b4e0efda6f33e33030269838b179a65829b5cdcf3b` |
| 155 `…-preflight` | `43228e52599ce0a19ee8b34f546e367e4fb428be70bb0303e7b062f8cb1508da` | `20a9702ae3d3fe9e94b7feb35183510b25399a7f93bf8845a67da9302141208f` |

The only body changes are the guard primitive and the GRAPH path. Every other byte is unchanged, including the protected Gate-5 invocation and the hashes it checks.

## 4. Preflight: GREEN

- Command: `bin/request-test integration:app ap2-P3-gate5-h6-0348-preflight --no-cache`
- Test id: `app-ap2-P3-gate5-h6-0348-preflight-1023190416-17114`
- Result: `pass exit=0 in 97s`, log ends `P3 D21 native-seed GREEN …` then `P3 D21 PREFLIGHT GREEN; body not run`.
- Log has no NOTREADY, p3fail, NOTRUN or skipped markers.
- Snapshot identity: `integration:app` is `/home/user/work/app` at 2107e1870, tree a3ff3584, clean. The runner's source tuple shows `appHead 43b71a9e…` with the same tree. That HEAD is likely the test-run's synthetic commit with single parent 2107. The guard's `%P` arm accepted it. Direct arm is also valid.

## 5. Gate-5 run: RED (one run, no retry)

- Command: `bin/request-test integration:app ap2-P3-gate5-h6-0348 --no-cache`, then `wait-test`.
- Test id: `app-ap2-P3-gate5-h6-0348-1023190626-15659`
- Result: `fail exit=1 in 224s`.
- Playwright: `1 failed`, `tests/e2e/local/three-products.spec.ts:1533:1 › M2 real gate 5 …`, `1.6m`.
- Failure:

```
Error: the mounted editor must claim a new durable command owner before the gesture
Call Log: - Timeout 90000ms exceeded while waiting on the predicate
expected { ready: true }, received { ready: false }
  > 1275 | … message: 'the mounted editor must claim a new durable command owner before the gesture' }).toMatchObject({ ready: true });
```

- Interpretation: the graph, guard, native seed and setup all passed. The journey reached `openCommandTimeline` and the mounted editor never reported a new durable command owner. This is a product or test-readiness failure in the body, not a graph or harness failure. I did not investigate further, per the no-retry rule. Trace: `test-results/three-products/three-products-M2-real-gat-710b3-rt-and-undo-preserve-intent/trace.zip` in the run's worktree snapshot `/home/user/work/wt/.test-app-ap2-P3-gate5-h6-0348-1023190626-15659`.

## 6. P2

Not started. The gate is not green, so no same-bench P2 inputs are recorded.

## 7. Items for the orchestrator

1. Decide on the Gate-5 failure. The owner readiness predicate (`ready: false` after 90 s) is the first red line. It is for app2 to decide whether this is a product defect or a timing issue. I have not edited any product, test or spec file.
2. Durability of the graph: it lives in `/tmp/w-79d31cf50f/tf-p3-run4/private`, which is harness-cleaned. A re-run needs a rebuild: `node /tmp/w-79d31cf50f/tf-p3-run4/build-graph.mjs`, then the verify script. If the orchestrator wants it durable, move it under the worker folder, but mind the 50 MB cap (the overlay is mostly symlinks plus Vite and Rollup copies).
3. Diagnostic rows 156 and 157 still have `HEAD^`. Remove them only once the actual row is decided, per app2's disposition.
4. The rule against deleting by glob or `rm -f` was observed. The only deletion was one symlink inside my private overlay (the helper-created scoped link), made with `unlinkSync` in the scratch script.

## 8. Commands (for the record)

| Step | Command | Exit |
|---|---|---|
| Build graph | `node /tmp/w-79d31cf50f/tf-p3-run4/build-graph.mjs` | 0 |
| Verify graph | `node /tmp/w-79d31cf50f/tf-p3-run4/verify-graph.mjs` | 0 (all checks as above) |
| Edit rows | `node /tmp/w-79d31cf50f/tf-p3-run4/edit-rows.mjs` | 0 |
| Preflight | `…/bin/request-test integration:app ap2-P3-gate5-h6-0348-preflight --no-cache` then `wait-test app-ap2-P3-gate5-h6-0348-preflight-1023190416-17114` | pass, 0 |
| Gate | `…/bin/request-test integration:app ap2-P3-gate5-h6-0348 --no-cache` then `wait-test app-ap2-P3-gate5-h6-0348-1023190626-15659` | 1 (fail) |

No product, test or spec edits. The worktree has no changes; the harness commits nothing from it.
