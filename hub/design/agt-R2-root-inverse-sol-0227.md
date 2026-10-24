**Blocked; do not integrate yet.** The five original inverse failures are fixed. All **169 author tests pass**; seven new expectations remain red.

Changed only `inverse.py` and separate focused tests. Coalescing preserves source-stage physical clip addresses across storage transitions, and inverse staging refreshes native clip lookup. The 0213 source and tests remain unchanged. Independent source review **passed** after its storage-transition finding was fixed and covered.

Final targeted command, using the prescribed qualified environment:

```bash
PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH=.:/home/user/work/wt/rt-pin-8ea0766f \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f \
ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f \
/home/user/work/venv-agent/bin/python -m pytest -q \
-oaddopts= -p no:cacheprovider --timeout=45 --tb=short \
tests/editing_conformance/test_doc_patch_root_assignment.py \
tests/editing_conformance/test_doc_patch_v2.py \
tests/editing_conformance/test_doc_patch_mirrors.py \
tests/editing_conformance/test_inverse_clip_mirrors.py \
tests/editing_conformance/test_inverse_parent_clip_root.py
```

**180 passed, 7 failed in 32.63s.** The unchanged parent’s original cohort reproduced **164 passed, 5 failed**. Two focused landing-guard regressions turn red→green. Wrong-before, source-order, ABA, membership, order, and foreign-row refusal tests pass without mutation.

Remaining blockers, outside assigned ownership:

- Six exact undo/redo tests pass undo, then fail in `_step_undo.py:143`, which requires mirror history absent from a configless clip root.
- One selected-step undo restoring clip absence is rejected by `validation.py:530`.

No expectations were weakened, skipped, or marked xfail.

Other checks:

- Private `python -m mypy astrid scripts/reshape --cache-dir "$TMPDIR/mypy-current-cache" --hide-error-context --no-color-output --no-pretty --show-error-codes`: **1,909 diagnostics**, exactly matching parent identities and multiplicities.
- `python -m ruff check --no-cache . --output-format json`: **2,145 findings**, exactly matching parent. Changed-file Ruff passes.
- `python scripts/vendor_lock.py check runtime.lock.json`, `python scripts/artifact_manifest.py --check`, and `git diff --check`: **pass**. The additional producer check correctly reported unchanged lock pin `34eac004` versus checkout `8ea0766f`; no pins changed.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. Next: assign the two external blockers, requalify, then perform the required current-only join. Runtime’s original headless qualification remains with its fixture owner.