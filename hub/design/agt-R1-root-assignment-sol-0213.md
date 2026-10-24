**Blocked; candidate is not ready to integrate.**

Changed only `_doc_patch.py` and a new focused test file. Six source lines restore absent clip assignments and refresh the recorder’s clip path for subsequent identity writes. The unchanged parent reproduced the public-provider failure deterministically.

Forward acceptance, preview, metadata, sequential reads, null/clear handling, and no-write guards now pass. **Undo remains broken:** `inverse.py` coalesces physical `parent.clips` into the earlier config assignment, then guards against a nonexistent `config.clips` mirror. Correcting that requires scope beyond the assigned files. The failing expectations remain intact.

Final targeted command:

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
tests/editing_conformance/test_inverse_clip_mirrors.py
```

**164 passed, 5 failed** in 41.79s. All 150 existing tests passed; all five failures are new inverse expectations.

Other checks:

- Private mypy: `python -m mypy astrid scripts/reshape --cache-dir <private-cache> --hide-error-context --no-color-output --no-pretty --show-error-codes` — parent and candidate each had 1,909 diagnostics; exact diagnostic identities and multiplicities matched.
- Ruff: `python -m ruff check --no-cache . --output-format json` — 2,145 findings on each tree; identities and multiplicities matched.
- Ruff on both changed files, `scripts/artifact_manifest.py --check`, and `git diff --check` — passed.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. No vendor checker, full suite, or Runtime headless acceptance ran.

Next: assign the physical clip-address coalescing correction in `inverse.py`, retain these inverse expectations, then have Runtime run its original headless family against the qualified source.