# REQUESTCHANGES — SDK filmstrip Scene extraction final gate

Verdict: **REQUESTCHANGES**.

The extraction and real Node proof are substantively approved, but the candidate
must remove the extra blank line at EOF from
`astrid/sdk/_timeline_filmstrip_scene.py` before merge:

```text
git diff --check 7ab6cbae2..HEAD
astrid/sdk/_timeline_filmstrip_scene.py:406: new blank line at EOF.
```

No product-code edit was made in this review, per task scope. After that
whitespace-only correction, rerun `git diff --check`; the existing real proof
need not be duplicated for the whitespace change.

## Source and authority review

- `source7ab` is `7ab6cbae2`; the candidate is `3cb69c9b3`.
- All ten moved helper bodies are AST-equivalent to `source7ab` after removing
  only module-local imports and normalizing the extraction's cycle-safe
  qualification of `timeline_filmstrip.prepare_filmstrip`:
  `_scene_only_unavailable`, `_scene_only_authority`,
  `_scene_only_expected_label`, `_scene_only_request`,
  `_scene_only_candidate_request`, `_scene_only_result_sources`,
  `_scene_only_bundle_payload`, `_scene_only_result_payload`,
  `_scene_only_spans`, and `_invoke_scene_only`.
- Authority decisions, Root/source basis, capture mapping, managed
  `filmstrip_bundle`/`entrypoints.scene` result handling, and unavailable
  behavior remain unchanged. The qualified import is the required extraction
  adjustment to avoid a facade/helper circular import.
- The private facade compatibility patchpoints are preserved as aliases for all
  three constants and all ten helper entrypoints. Import provenance confirms
  both modules resolve inside this candidate worktree.
- Packaging/source closure is satisfied by the existing setuptools
  `astrid*` package discovery; `astrid/sdk/__init__.py` and the helper module
  are present and importable. No pack manifest or source factory is involved.
- `docs/giant-file-rationale.md` records the current facade at the exact
  `wc -l` count of **1313**. The documented 1200-line threshold and 50-line
  drift tolerance are unchanged; neighboring entries remain unchanged.

## Evidence

Central real public-host proof, using the existing published014 integration
environment, immutable Runtime pin, C13 Python environment, and Node20:

```text
request-test agt-review-sdk-filmstrip-scene-extract-current published014-scene-real-public-summary-rle
wait-test ...
1 passed in 7.44s, exit 0
```

The named suite was added because the test file is unmarked: unfiltered
collection found one test, while `-m integration` collected zero tests. The
new suite uses `-o addopts= -p no:cacheprovider` and names only
`tests/sdk/test_scene_real_public_summary_rle.py`; it contains no unrelated
fixed files.

Local focused SDK preservation/authority/dispatch/filmstrip tests:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-95bd3c5f" \
  /home/user/work/venv-agent/bin/python -B -m pytest -q -o addopts= \
  -p no:cacheprovider \
  tests/sdk/test_scene_caller_preservation.py \
  tests/sdk/test_scene_save_core.py \
  tests/sdk/test_scene_dispatch_contract.py \
  tests/sdk/test_timeline_checkout_facade.py \
  tests/sdk/test_timeline_filmstrip.py \
  tests/sdk/test_timeline_filmstrip_invocation.py
102 passed, 2 skipped in 3.81s
```

Import/compatibility assertions passed. `ruff check` passed for the new helper;
the existing facade reports ten unrelated baseline lint errors. `ruff format
--check` reports the existing moved-code formatting state and was not used as
approval evidence. No full suite, browser, MP4, duplicate saved/candidate
proof, schema/pin/activation/source-factory work, or full suite was run.

Recommended next step: remove only the extra EOF blank line, rerun
`git diff --check`, then resubmit the same candidate for approval.
