# Runtime ordinary014 current-server cd0 frontier

## Result

Prepared a new unpublished current-server compatibility candidate from the
current `tl/integration` tree. The candidate carries the exact approved
ordinary014 generated/artifact cohort from Runtime `a0dca169` (artifact
`f021e771`, schema `ce3781c2`, raw Agent schema `6ba7b51e`) and the exact
current-server behavior remains in place for CAS, history, catalog, headless,
and text paths. No Runtime service/port/store files were copied from the old
candidate, and no private613 material was added.

The working candidate's central test snapshot tree is
`5ce91b00440a7ad40a57eea273a2d94c2fe2611c`. The official generated/artifact
paths are byte-identical to the reviewed current-server composition
`9cde47523803607f4dfd8d39885a9526de4ce8e7`; the only additional product test
path is `tests/test_timeline_clip_replacement.py`.

## cd0 boundary

The two cases are now one-to-one and named explicitly:

- `test_native_parent_clip_swap_route_refuses_parent_ownership_on_public013_schema`
  validates the real captured command against the immutable public-013 schema
  fixture and asserts the exact `ownership` enum refusal (`shared` /
  `occurrence`). Public producer `2c4ac180` remains untouched.
- `test_native_parent_clip_swap_route_replaces_parent_media` runs the original
  commit-path acceptance body without an xfail. Against ordinary014, the
  `parent` ownership schema branch is accepted and the parent asset replacement
  assertion remains intact.

This is the narrow schema-bound conversion required by D04. No assertion was
deleted, skipped, or broadly xfailed. The existing direct legacy-writer
xfails remain unchanged.

## Evidence

Local schema lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/packages/python" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
  tests/test_timeline_current_union_contract.py
64 passed in 1.12s
```

Central socket-capable targeted lane:

```text
request-test rt-m2-ordinary014-current-cd0-native-frontier targeted \
  --files "tests/test_timeline_current_union_contract.py tests/test_timeline_clip_replacement.py"
```

Result: **64 passed, 15 deselected, 10 existing strict xfails** in 14.65s,
central snapshot tree `5ce91b00440a7ad40a57eea273a2d94c2fe2611c`. The ten
xfails are the pre-existing direct `replace_timeline_clip` retirement cases;
the native parent refusal, ordinary014 parent replacement, and adjacent
native clip-swap cases passed.

The requested named lane was also run exactly once:

```text
request-test integration:agent ordinary014-consumer-integration
```

It failed during collection, before tests ran: **1 skipped, 15,294
deselected, 2 errors**, both because the central environment did not provide
the existing `vibecomfy` module. This is an environment blocker, not a
candidate assertion failure. The already-approved normal014/a0 current-source
evidence remains documented separately as 143 passed in
`agent-ordinary014-normal-pin-candidate.md`; it is not relabeled as proof of
this new current-server snapshot.

No renderer rerun, full suite, App browser run, pin, merge, publication,
release, or integration adoption was performed. Public `2c4ac180` and
ordinary producer `a0dca169` remain immutable.
