# App2 bootstrap gate environment evidence

Date: 2026-10-20 UTC

## Scope

Prepared a private, test-only runner for the Runtime fresh-scope and
absent/null-head bootstrap tests. No repository source, test, package, pin,
generated file, or shared environment was changed.

Sources were extracted with read-only `git archive` from Agent
`310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3` (tree
`c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`) and Runtime
`7f6dd8920e1ceec41b137358df5e7fecc304888d` (tree
`4cccb2d643194df7df95d624e89a6cd9f6f268fc`). The extracted roots and runner
are under the worker directory, not a repository worktree.

## Import preflight

Interpreter: `/home/user/work/venv-app2-native/bin/python` (Python 3.12.3).

The following imports succeeded from the private pair:

```text
pytest 9.0.2
jsonschema 4.26.0
referencing 0.37.0
PyYAML 6.0.3
runtime_protocol
runtime_protocol.service
runtime_protocol.timeline_commit_provider
astrid.sdk.timeline
```

`pytest-timeout`, `pytest-xdist`, and `httpx` are absent, but none is required
by the selected tests or runner. No install was attempted. The first
collection probe omitted `runtime/tests` from `PYTHONPATH` and therefore could
not resolve the unchanged flat helper imports; the corrected runner includes
`runtime/tests`.

## Commands and results

All commands use `PYTHONDONTWRITEBYTECODE=1` and `-p no:cacheprovider`.

Collection of both files:

```sh
PYTHONPATH="$RUNTIME/tests:$RUNTIME:$AGENT" \
/home/user/work/venv-app2-native/bin/python -m pytest --collect-only -q \
  -c /dev/null -p no:cacheprovider \
  "$RUNTIME/tests/test_timeline_fresh_bootstrap_scope.py" \
  "$RUNTIME/tests/test_timeline_absent_head_repair_integration.py"
```

Result: 12 tests collected (7 deselected by the integration-only collection
filter when that filter was requested).

Safe non-integration lane:

```sh
PYTHONPATH="$RUNTIME/tests:$RUNTIME:$AGENT" \
/home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null \
  -p no:cacheprovider -m 'not integration and not darwin_native and not live' \
  "$RUNTIME/tests/test_timeline_fresh_bootstrap_scope.py"
```

Result: `7 passed, 1 deselected`.

The private runner is:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-gate-environment/harness/run-frozen-bootstrap-gate.sh
```

Its direct execution result against the extracted frozen pair was `12 passed
in 4.53s`. The central service run was not requested because the manager-owned
suite allow-list is read-only for this worker; the exact one-line registration
and request are in
`app2-bootstrap-gate-environment-suite-proposal.md`.

## Hold and qualification boundary

The separate Agent opaque-inverse hold remains unchanged and unclaimed fixed:
the four original unrelated-parent opaque inverse positives fail on Agent 310e
with `inverse_dependency_changed`, reference `parent`, path `[]`. This task
does not alter, skip, weaken, or relabel those expectations.

No App cutover, Runtime admission, writer retirement, or central qualification
claim follows from this environment preparation. The manager must register
and run the named central suite before treating the Runtime result as central
service evidence.
