# D139 independent union review

## Result

PASS. The candidate is commit `d133a14838a4e607947893408bc34ba2742a19c6`,
whose direct parent is the exact required base
`4c4ee35d5687c4cd40a0e5395efda53aa56f939d`.

The diff has exactly the five authorized paths. Each final blob equals its
named reviewed donor. All other base-tree paths are byte-identical; the
current `_timing_evaluators.py` and `runtime.lock.json` blobs remain exact.
The normal `tl/integration` head `cd63be424d62226e3ee5c26fc5ce03227f5394a5`
already carries the exact D136a `20dbfdef…` FPS blobs, so its newer source was
used for the preimage comparison rather than treating that adoption as a
conflict. The D100 test is intentionally additive and absent from the base.

The physical correspondence review rechecked the exact D100 donor's strict
source-image, revision/digest, owner, item-ID uniqueness, copied-placement,
replacement, and no-write refusal guards. The projection donor preserves all
11 pre-existing test bodies and 43 assertion predicates by AST identity,
including authored inputs and shot/order goldens. D100 has 10 test functions;
D136 has 6. No skip or xfail controls were added.

## Exact commands and results

- Python AST/object/scope audit (inline `python3`): PASS. It checked exact
  donor blobs, base ancestry, five-path scope, all outside-tree blobs,
  protected files, normal `cd63be4…` FPS blobs, projection AST/body/assertion
  conservation, D100/D136 test structure, and physical correspondence guard
  markers.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-c57daa549f/d139-review-2202/pyc
  /usr/bin/python3.11 -m py_compile astrid/sdk/timeline/_command_state.py
  astrid/sdk/timeline/validation.py tests/sdk/test_d100_item_birth_boundary.py
  tests/sdk/test_d136_fps_upstream_compat.py
  tests/sdk/test_timeline_capture_projection.py`: PASS.
- `/home/user/work/venv-agent/bin/ruff check --no-cache` on the five exact
  paths: PASS (`All checks passed!`).
- `MYPY_CACHE_DIR=/tmp/w-c57daa549f/d139-review-2202/mypy /home/user/work/venv-agent/bin/mypy` on
  the five exact paths: PASS (`Success: no issues found in 5 source files`).
- `git diff --check 4c4ee35d5687c4cd40a0e5395efda53aa56f939d HEAD`: PASS.
- `git diff --check HEAD`: PASS.

## Boundary

No pytest, provider, collection, RuntimeStore, child, profile, acquisition,
native, browser, live-socket, core, full-suite, D130, or App original9/27 run
was performed. This review gives source qualification only and no behavior,
core, or release credit. Free space was above the 5 GB source floor during
the static run.
