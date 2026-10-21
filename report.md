# WC8 Runtime boundary report

## Result

Bounded Runtime ACK. Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`
has no concrete mismatch for a future retained native basis/row-intent/
original-target batch. No Runtime source or test files were changed.

The current detached sheet is not eligible for migration. It is blocked on
Agent author-time retention of the original revision/publication basis, stable
row intent and identity, reads/selections/order, writes, and the original
Runtime target/request flight. A whole-document snapshot diff cannot recover
that intent, and refreshing guards would discard the original basis. The
detached grammar and local rollback remain live and held; no deletion is
authorized.

## Exact evidence

Preflight, from the Runtime worktree:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python - <<'PY'
import importlib
for name in (
    "runtime_protocol.timeline_commit_port",
    "tests.test_timeline_commit_acceptance",
    "tests.test_timeline_commit_execution",
    "tests.test_timeline_commit_contract",
    "tests.test_timeline_current_union_contract",
):
    print(name, importlib.import_module(name).__file__)
PY
```

All five imports resolved from this tree. Collection found 180 runnable tests
and one intentional deselection.

Required four-file command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_commit_acceptance.py \
  tests/test_timeline_commit_execution.py \
  tests/test_timeline_commit_contract.py \
  tests/test_timeline_current_union_contract.py
```

Result: **180 passed, 1 deselected in 21.27s**.

The exact retained-command evidence is mapped in
`design/runtime-wc8-retained-basis-boundary-0439.md`, including original
recorder guards, stale-head conflict, exact retry, changed-key/payload
refusal, concurrent CAS and atomic no-write rollback.

## Not run / not claimed

- Agent positive-floor tests were not rerun. The exact six IDs are cited in
  the design note and WC8 handoff; the missing dependency is Agent
  author-time retention, not a Runtime test or package.
- No full suite, sockets, browser, renderer, launcher, schema/client,
  generation/version/pin, source migration or activation run was performed.
- No separate positive Runtime disjoint-edit `rebased` assertion exists in
  the four-file lane; the existing store branch is inspected and the stale
  conflict side is tested, but this report does not overclaim that scenario.

## Decisions and next step

No acceptance fix was necessary because the existing retained-command tests
passed. The next step belongs to Agent: add and qualify the bounded
author-time retention seam while preserving detached positives and unsupported
mixed-shape refusal. Runtime should then pair that retained batch with the
existing `/v1` acceptance path; it should not infer intent from snapshots or
refresh guards.

