# Final owner gate: Agent scene/save-core separation

## Verdict

**APPROVE**, bounded to the Agent save-core candidate at commit
`f5d0b4e090fba31a6e3c55baa55b63b2e739d337`, tree
`f4d74d55c77c76b8d20e5e4b3fd7bb2719f4d1be`, parent
`4ef1391c2c104d5d11b3a27265035c51be296045`.

The review worktree is `tl/agt-review-scene-save-core-final`. The current
integration baseline is `8e3107853d17453758a933d1f47215cc1c002660`; its
changes since the candidate base are confined to four unrelated command,
inverse, and Runtime-schema test paths, with no overlap in the candidate's
14 changed paths.

## Review result

- `Checkout.check()` retains the explicit diagnostic path, including the
  original OFFCANVAS blocking finding and UNKNOWN/UNAVAILABLE scene advice.
- `Checkout._check_core()` shares the existing validation implementation and
  retains schema, structure, formula/reference, type, outside, stale-beat,
  length, and shot-length guards. It omits scene, sprite/visual, lint, text,
  look, and music diagnostics.
- Publication, checked transactions, detached CLI edit reports, and duplicate
  preflights use `_check_core()`. Ordinary save/native commit code is not
  routed through a renderer or Node.
- The OFFCANVAS counterexample remains visible after the accepted core-valid
  save: explicit check is invalid solely for OFFCANVAS, while save/reload and
  publication preserve `params.x=10000` exactly. No clamp or autofix was added.
- Unknown scene results remain advisory and unavailable source/query state is
  not converted into a canonical answer or a silent fallback.
- Changed old test stubs preserve their original semantic assertions; they
  only patch the new private seam or import the defining pure authoring
  module. No test was skipped, weakened, deleted, or newly xfailed.

## Commands and results

```sh
git diff --stat 4ef1391c f5d0b4e0
git diff --numstat 4ef1391c f5d0b4e0
git diff --check f5d0b4e0^ f5d0b4e0
```

Passed. The candidate is 14 files with `tests/sdk/test_scene_save_core.py`
adding 191 lines; the six production files total +33/-25 by `git numstat`
and the complete candidate is +236/-31. `git diff --check` is clean.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_scene_save_core.py \
  tests/sdk/test_timeline_transaction.py \
  tests/sdk/test_timeline_publish_connection.py \
  tests/sdk/test_timeline_checkout_facade.py \
  tests/sdk/test_timeline_checkout_history_boundaries.py \
  tests/packs/timeline/test_verbs_working_copy.py
```

**83 passed in 13.28s.** This includes the source/import, renderer/Node
process-launch, save/reload, transaction, publish, duplicate, CLI, and
core-invalid refusal fences.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_scene_caller_preservation.py \
  tests/sdk/test_timeline_checkout.py -k \
  'nested_param or offcanvas or moment_outside or duplicate_is_all_or_nothing or check_blocks_a_literal_formula_string or check_flags_offcanvas'
```

**5 passed, 107 deselected in 1.92s.** This preserves the explicit scene
formatter/unknown findings and structural-invalidity assertions.

## Non-blocking note and limits

The fresh-process import test is cwd-sensitive when invoked from a different
checkout: its child inherits cwd and does not set an explicit candidate-root
cwd/PYTHONPATH. It passes from the candidate worktree and is a test harness
portability follow-up, not a product save-path defect.

No full suite was requested or run. The existing central native qualification
was not duplicated. D09 remains **HELD** for Viewing Root-prep lifetime,
cache/physical-key parity, and physical pixel/audio parity. No public13
adoption, pin change, public API/DTO/SourceFactory change, Runtime/App
qualification, renderer parity, or owner-film claim is made.
