**BLOCKED: current cause is outside the assigned persistence scope. No product changes retained.**

On Agent `1f15f274824f`, the fresh-process probe verified the saved nudge against the authenticated raw base. Production `publish()` sent `merge="fields"`, the original command, all **137 reads**, the exact base pair, and stable key. The historical digest mismatch was already repaired by `3b0dc9e80f`.

Runtime then refused with:

```text
invalid_document:
missing exact word binding for ('occ-A', 'A', 'a-rocket').on
```

The nudge changes `"viral"` to `"viral" +0.5s`; the raw dependency manifest has `documents: []`. Database and history stayed unchanged. The precise next seam is V2 timing/native word binding: `_timing_evaluators.py:387`, with internal-shot binding restricted by `_commit_timing_validation.py:563`. I did not fabricate authority or weaken those guards.

[Evidence directory](/tmp/w-18f97bd8f0/final-trace/test_persisted_cut_helper_boun0) contains the raw closure, registries, saved record, complete persisted request, exact base/current pairs, history, and no-write comparison.

Commands and results:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider \
tests/sdk/test_timeline_helper_capture.py \
tests/sdk/test_timeline_helper_normalization.py \
tests/sdk/test_timeline_normal_publish.py \
tests/sdk/test_timeline_session_pair.py \
--basetemp="$TMPDIR/controls" --junitxml="$TMPDIR/controls.xml"
```

**55 passed, 1 failed.** The failure is the existing `"second"` word-anchor setup, also missing an exact binding. Numeric restart, captured restart, disjoint merge, pair persistence, and safety controls passed.

The scratch boundary probe passed; the production publish probe retained its merge expectation and failed at the binding guard. Final diagnostic command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -pno:cacheprovider \
"$TMPDIR/test_persisted_helper_trace.py" \
--basetemp="$TMPDIR/final-trace" --junitxml="$TMPDIR/final-trace.xml"
```

Scoped Ruff: 4 existing diagnostics. Private-cache scoped Mypy: 19 existing errors. **Zero new findings; source is unchanged from HEAD.** Artifact manifest, vendor-lock check, and `git diff --check` passed.

The original selector was not rerun without a source change. No full/browser runs, installs, or reserved-file edits. `BLOCKED` and `commit-msg` were written; no `DONE`.

**Target verdict: unqualified.** Route the authenticated legacy word-binding/ownership requirement to its owner before further persistence changes.