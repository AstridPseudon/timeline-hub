# H3 independent Runtime consumer source-map review

**Result: PASS_SOURCE_MAP, with a historical evidence limit.** The current Runtime full-suite mapping for a worker based at `tl/one-head` selects Agent `88a9dfe9856344ade53d88d7dd4ec9883bd7a38c` from `/home/user/work/wt-int/agent-88a9dfe98563`. The author is right that `external=agent=2d7b…` is not the provider import path. The archived pre-request runner supports that mapping for the historical run too, but no effective command or module-origin capture was retained; that run's provider origin remains a source-backed inference.

## Findings

1. **Current selection is verified.** Runtime `full` in `tests/suites.conf` is `env ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -n 3`. Current `bin/test-run` reads the worker `base`, maps `tl/one-head` to `refs/heads/tl/one-head`, resolves `88a9dfe9856344ade53d88d7dd4ec9883bd7a38c`, verifies the detached worktree at `/home/user/work/wt-int/agent-88a9dfe98563`, and rewrites the command's Agent path. The ref and worktree HEAD both resolve to that SHA.

2. **`external` is dependency/cache metadata, not source identity.** The runner computes `EXT` and appends `external=...` from the original configured command before applying the Runtime `CMD` rewrite. Thus the historical `agent=2d7b9a019431f5592967b2f29799af60da6934fc` says which integration checkout appears in the static command, not which checkout fills `ASTRID_CHECKOUT`. The historical `ext` file repeats this line; repetition does not add per-process module-origin evidence.

3. **Historical selector availability is contemporaneously supported.** The retained `test-run.20261027T1413Z.bak` is timestamped 14:13:15Z, before the 15:43:07Z request, and contains the same `tl/one-head` → Agent ref → detached worktree → command rewrite path. H worker metadata records `base=tl/one-head`. The historical request points to Runtime tree `61568665d2c58da55d2082065dc8b1d4142b8632`, corresponding to Runtime commit `d3969a86e62f5f8761533499e7d2e3f97195932b`. The log contains actual pytest progress and counts, so a test body ran.

4. **Historical exact import is not directly recorded.** The recovered historical summary says `stale runner finalized from existing log`, does not retain the effective command, and `trace-runner.log` is empty. `runner.log` records `line 470: ol: command not found` and a syntax error near `fi` at line 477. These errors and stale finalization limit execution provenance. Combined with the pre-request backup, worker metadata, current ref/worktree state, and Runtime bootstrap/import flow, Agent `88a9…` is the best-supported source-backed inference for the provider, but no historical `module.__file__` manifest proves it.

5. **The author overstates the fixture assertion.** At Runtime `d3969a86e62`, `tests/astrid_checkout.py` resolves `ASTRID_CHECKOUT`, prepends that root to `sys.path`, and removes already-loaded `astrid.*` entries whose files lie outside it. `runtime_protocol/timeline_commit_provider.py` imports `astrid.sdk.timeline.commit` and calls `create_runtime_commit_service`. The fixture does not directly assert `astrid.sdk.timeline.commit.__file__`. Some tests check selected Agent module origins, but they are not a module-origin capture for the historical full run.

6. **This does not qualify the Runtime phase gate.** The historical outcome is **7,385 passed, 75 failed, 25 errors, 26 skipped, 13 xfailed**; the immutable summary marks it `fail`. The H worker report says all failures/errors matched owner-pin names, but that classification is separate from this source review. Neither that comparison nor closing the source-mapping blocker changes the run into a green full suite. H owns any final qualification/rerun decision under H3.

## Contract and plan context

PLAN v2.1 §1–2 place semantic editing in the Python Agent provider executed by Runtime; `design/commit-v2.md` states Runtime is the only writer and that the provider is loaded behind the explicit `astrid` profile. This review traces which provider checkout the Runtime test lane selects. It does not validate v2 request bodies, commit-wire behavior, product code, or phase completion.

Hashes and exact run coordinates are in `source-map.json`. Validation details are in `validation.md`.
