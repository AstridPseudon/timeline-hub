# H3 Runtime consumer source diagnosis

**Result: PASS_SOURCE_MAP (routing only).** The prior H Runtime full run selected the H Agent `tl/one-head` checkout through the kit's source selector. The `external=agent=2d7b…` field in the recorded run is cache/dependency metadata derived before command rewriting; it is not the provider import path. The worker report treated it as the imported checkout and therefore stated a false mismatch.

## Source path

`tests/suites.conf` configures Runtime `full` as:

```sh
env ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3
```

For a non-integration Runtime worker, `bin/test-run` reads that worker's `base` from `workers/<name>/meta`. For `base=tl/one-head`, it resolves `/home/user/work/agent`'s `refs/heads/tl/one-head`, verifies the commit, chooses `/home/user/work/wt-int/agent-<12-char-sha>`, and rewrites `/home/user/work/agent` in the suite command to that checkout. The H worker metadata says `base=tl/one-head`; the branch resolves to `88a9dfe9856344ade53d88d7dd4ec9883bd7a38c`, and the corresponding detached worktree exists at `/home/user/work/wt-int/agent-88a9dfe98563` with that HEAD. The same selector is present in the immutable `test-run.20261027T1413Z.bak` (made before this request). Thus the effective command's `ASTRID_CHECKOUT` is that path, not the displayed `/home/user/work/agent` path.

Runtime's `tests/astrid_checkout.py` resolves `ASTRID_CHECKOUT`, prepends it to `sys.path`, and removes any already-imported `astrid.*` modules from a different root. The real-provider fixtures then import `astrid.sdk.timeline.commit`; `runtime_protocol/timeline_commit_provider.py` also imports that exact module and calls its `create_runtime_commit_service` factory. The fixture asserts that `astrid.sdk.timeline.commit.__file__` resolves under the selected checkout. Consequently the provider module is sourced from Agent commit `88a9dfe985…` for the H run. This is source-backed control-flow identity; the old run did not persist a per-process `module.__file__` capture.

The Agent `runtime.lock.json` `source_commit=1a0ce6a39dec6701b17918e5c7665745ae76c504` describes the Runtime contract source pinned by that Agent checkout. It is separate from the `ASTRID_CHECKOUT` selector and does not change which Agent provider source Runtime imports.

## Recorded run and scope

- Request: `H-tests-runtime-final-full-1027154307-24227`, requested `2026-10-27T15:43:07Z`.
- Runtime worker metadata: base `tl/one-head`, short base SHA `d3969a86e6`.
- Snapshot source: tree `61568665d2c58da55d2082065dc8b1d4142b8632`, equal to Runtime commit `d3969a86e62f5f8761533499e7d2e3f97195932b`'s tree.
- The run's `ext` and summary show `agent=2d7b9a019431f5592967b2f29799af60da6934fc`. `test-run` writes that field from the static suite command's `/home/user/work/agent` dependency when building the cache key, before the later Runtime-specific `CMD` rewrite. It records the integration checkout dependency, not the actual selected provider checkout.
- A prior one-head full run, `H-tests-runtime-full-1027150617-4802`, records its effective command as `env ASTRID_CHECKOUT=/home/user/work/wt-int/agent-88a9dfe98563 ...`; it used the same Agent target and was non-green overall (7,374 passed, 77 failed, 33 errors). This is a source-matched comparison, not a passing full-suite result.
- Outcome: **7,385 passed, 75 failed, 25 errors, 26 skipped, 13 xfailed**. H's classifier found all failed/error names matched the Runtime owner-pin baseline. This source diagnosis does not turn that non-green full suite into a pass or claim full-suite qualification.
- The earlier one-head full run was also configured against Agent `88a9…`, but it was not green overall. No passing full-suite result for this exact Runtime/Agent pair was found in the inspected run records.

## Correction decision

The current mapping already corrects the alleged source mismatch, and it also applied to the recorded H run: no kit or suite change is justified. Do not retarget or discard the existing H run based on its `ext` field. H retains responsibility for the full-suite failure classification and any final rerun required by its phase gate. No new test request was submitted here.
