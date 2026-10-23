# G5 bounded guarded-inverse qualification

## Verdict

**BLOCKED — source/test shape is prepared, but the real Runtime inverse witness
failed at the production boundary.** No Agent product code was changed. Broad
guarded undo/redo remains unqualified, as required by the plan.

## Scope and identity

- Agent candidate: `ee7f0b809266690f5c46d6824af1e6ee82f03714`
- Agent tree: `4305240b13e6eefbfdf9a4e34c8a04d9127b2645`
- Runtime: commit `3b926efab2eed122d374540baee297d4cdcec62a`
- Runtime tree: `b794170504544b259781e50d7ca4d61b6729e67c`
- Only product/test path added: `tests/sdk/test_timeline_restructure_guarded_runtime.py`
- Existing restructure fixture reused from `tests/sdk/test_timeline_restructure.py`.

The test uses the real `Checkout.publish(restructure=True)` caller, the real
`timeline.open(...).session.undo(...)` caller, the real Runtime service/store,
and the current authenticated Agent/Runtime bridge. It does not construct a
prepared acceptance, fake journal, synthetic authority, cache injection, or
direct provider waiver.

## Exact bounded request shape

The failing inverse request was one ordinary v2 request with:

```text
api_version: 1
project_id: fixture project id
timeline_id: t
base_revision_id/base_publication_id: the accepted restructure head pair
commands: one timeline.inverse command
  args: {publications: [the accepted restructure receipt id]}
label: Undo timeline edit
steps: [{id: inverse, label: Undo timeline edit, intent: "", tags: [],
         command_ordinals: [0], patch: []}]
merge: fields
dry_run: false
source: {via: python}
idempotency_key: inverse-undo
```

The test captures the complete request, Runtime history (including prepared
records, bindings, writes, dependencies, effects, `undo_steps`, and receipt),
canonical before/after documents, and import origins in its failure output.
The captured run emitted one 605,127-byte JSON witness before pytest reported
the failure; the worker's transient `/tmp` capture was reclaimed by the
execution environment, so this report preserves the stable request shape and
classification but not every generated fixture ID.

## Witness result

The restructure accepted and produced the expected created-root shape before
inverse dispatch: one source shot/internal root became three shot roots, three
internal roots, and three ordered occurrences; the authored opaque value
`{"null": null, "ordered": [null, false, 0]}` was preserved. The inverse was
then sent through the public session caller and Runtime returned:

```text
WorkspaceClientError: Timeline commit outcome unavailable; retry the exact request
details: {reason: runtime_unavailable}
```

This is not the expected one-intervening-write guarded refusal. The source
origins captured by the test were the Agent `publish.py` in this worktree and
`runtime_protocol` from `/home/user/work/runtime`. No repeated inverse body or
production fix was attempted after the captured witness.

The retained-root/order setup was added to the test using the existing fixture,
but the successful undo/redo/refusal assertions are unverified because the
production inverse stopped at the Runtime-unavailable boundary.

## Checks

- Real Runtime targeted test: **1 failed** (`WorkspaceClientError`,
  `runtime_unavailable`; 11.67s) on the one bounded inverse witness.
- Scoped Ruff on the new test: **passed**.
- Private mypy: **passed** (no output, exit 0).
- `git diff --check`: **passed**.
- No full suite, browser, native, HTTP, P1/P2/P3/P4, or broad 109-case rerun.

## Next step

Runtime/Agent owners should diagnose the `runtime_unavailable` failure from the
captured inverse request and Runtime history. After that boundary is repaired,
rerun this new test once against Runtime 3b/tree b794 and complete the exact
canonical undo, redo, and overlapping-write refusal assertions. Do not merge
or call G5 qualified from this blocked witness.
