## Verdict: REJECT, narrow

The branch fails one stated requirement. Everything else I checked is sound, and the fix is small. Re-review after R1; no other rework needed.

The review is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-review-agent12-cohort.md`. `DONE` is created. No repo changes and no commit-msg.

### Blocking
- **R1: the theme-constant test is not real.** `tests/packs/rendering/presenter_scene_capability.mjs` (lines 50–59) asserts `DEFAULT_THEME` against a hand-typed navy literal. Nothing compares it to Agent's `BUILTIN_DEFAULT_THEME` (`astrid/core/theme/_schema.py:174`). `grep BUILTIN_DEFAULT_THEME tests/` is empty. I compared the values by eye and they match, but no test guards that. Fix: serialise `BUILTIN_DEFAULT_THEME` into the fixture and `deepEqual` against it. Keep the historical black/Georgia block.

### Non-blocking
- N1: `test_presenter_scene_capability.py` uses `in {SHA256, "0a7b…"}`, which is the same value twice. Use `==`.
- N2: the handoff's test run borrowed another worker's `node_modules`. Evidence should come from the central service on the merged tree.

### Verified
- Tarball sha256 `0a7b6152…` matches all test constants.
- sha512 SRI computed from the blob matches the lock `integrity`.
- The lock diff is 4 lines (version, resolved, integrity).
- Peer deps are unchanged between 0.0.10 and 0.0.12.
- Composition repo `5e06f40` is version 0.0.12.
- `artifacts.json` passes `--check` on an exported `ce251003`.
- Presenter bytes are identical to integration's.
- The 0.0.10 tarball has no remaining references.
- No schema, provider or compiler changes.
- No crop lines removed.
- No skip/xfail added.

### Runtime lock mismatch (not a branch defect)
`runtimes/agent-remotion-0012/package-lock.json` is not byte-equal to the reviewed lock. It is missing 8 `"libc"` blocks. The tarball and `package.json` match. The Agent lock is the correct one. Orchestrator should re-materialise that runtime from the reviewed lock.

### Merge plan (summary; full table in the file)
0. Orchestrator re-materialises the runtime lock.
1. Owner applies R1/N1 and regenerates `artifacts.json`.
2. Land the Composition unit on `tl/integration` (`0e951d68`). Conflicts:
   - `artifacts.json`: regenerate, don't hand-merge.
   - `presenter_scene_capability.mjs`, `presenter_crop_geometry.mjs`, `test_presenter_scene_capability.py`: take branch. Integration lacks the series regression and the historical theme.
3. Runtime pin unit: BLOCKED. It needs a Runtime checkout at `94114269`. `tl/agt-m2-runtime-pin-current` (`b7789c19`) is a merge stack, not a pin commit, so cut the pin fresh from integration after step 2.
   - Its files overlap with the Composition unit only in `artifacts.json`.
4. Regenerate `artifacts.json` on the final tree and run `--check`.

### Couldn't do
- I did not run any tests, so the handoff's 33/5/48 results are unverified by me.
- I could not delete my scratch copies. `rm-own` refuses paths outside the worktree, and a direct `rm` was denied. They are under `orch/workers/agt-review-agent12-cohort/` and `orch/workers/agt-review-agent12-cohort-a0{012,010}.tgz`, and nothing is in the worktree.
