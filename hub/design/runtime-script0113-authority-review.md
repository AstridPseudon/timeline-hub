# Runtime 0113 producer input authority review

## Decision

**APPROVE** candidate `0113bc7d558d67816d88e4531c299d72a01eccb3` for the
bounded Runtime change, relative to required base
`e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`. Candidate tree:
`2b4e22cae5261a863d17410944e6d559e1201a77`.

The patch is limited to `runtime_protocol/store.py` and
`tests/test_timeline_producer_guards.py`. It adds no API, schema, table,
scope, or producer-identity surface.

## Source review

`RealmStore._continuation_predecessors` now returns `()` only for the exact
shape `runtime_dependencies == {"publication": {"admitted_target": ...}}`.
That is the required normal-producer carrier shape. Any publication sibling,
edge, child guard, or other extra key misses the exception and continues
through the existing strict two-edge continuation validator. The existing
edge-bearing checks for exactly two ordered edges, fenced `task.succeeded`,
unique predecessor IDs, ordered-CAS aggregation, and empty explicit inputs are
unchanged.

The exception only suppresses continuation-derived input materialization. It
does not skip `_validate_task_inputs`; explicit `input_object_ids` therefore
still require canonical CAS IDs, a project, and a matching project-object
association. The producer authority path remains unchanged: the later real
producer capture still validates the exact admitted target against the request,
task project/current attempt, settled artifact, proposal digest, and proposal
guard.

The added test uses a real project, document update, UTF-8 CAS object,
first-class execution request, live claim, restart, and exact idempotent task
retry. It proves the original descriptor, ordered input identity, bytes, and
publication target remain pinned after the source document changes. It does
not claim DocumentPin behavior or native registered-voiceover integration.

## Checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_producer_guards.py`
  - **41 passed in 30.56s** on the unchanged base neighbor suite.
- Review-only exact candidate test: loaded the test body from candidate
  `0113bc7` and installed the candidate method in memory; the real fixture and
  service path ran `test_admitted_utf8_script_input_stays_pinned_after_source_update_and_restart`.
  - **PASS**.
- Review-only shape/authority probes with the candidate method:
  - exact publication-only shape with explicit CAS input: **PASS**;
  - publication extra keys/edges/child guard: **rejected**;
  - valid edge-bearing continuation: **preserved**;
  - foreign-project explicit input: **rejected by normal project scope**;
  - unknown continuation predecessor: **rejected as not found**.
- `git diff --check e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd 0113bc7d558d67816d88e4531c299d72a01eccb3`: **passed**.

## Limits

No full or matrix suite, DocumentPin case, native registered-voiceover case,
live external producer, or browser/socket journey was run. The exact candidate
test was executed without modifying the worktree by loading its committed test
source and method into memory; the unchanged neighbor suite was run directly
on the review worktree. No source, shared dependency, cache, branch, or
integration worktree was modified.
