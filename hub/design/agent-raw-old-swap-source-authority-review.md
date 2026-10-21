# Agent raw OLD swap source-authority review

## Verdict

**APPROVE SOURCE.** The finished Agent source at commit `9b9baa01a`
(`feat(timeline): add raw old swap successor`) implements the settled bounded
successor. I found no concrete data-safety or cross-contract defect in the
specified scope.

This is a source review only. It does not qualify a native Runtime/Agent raw
OLD acceptance positive, a client, generated schema artifact, pin or
activation.

## Contract checked

- `clip.swap-media@2` and `occurrence.swap-media@3` are the only raw-OLD
  branches. Frozen `occurrence.swap-media@2` remains the existing selected-
  media/source-bound operation.
- `old_media` is exactly the two-field `MediaManifestEntry`:
  `media_id` plus equal `content_digest`; `additionalProperties: false`
  rejects generation, variant, catalog, duration, owner and other metadata.
- NEW remains the exact five-field `MediaSelection` and is admitted through
  the existing `selected_media` path.
- Commit capture calls the optional private `raw_media_info` only for the
  exact OLD pin and calls `selected_media` only for NEW. No raw metadata,
  duration, latest lookup or managed-generation identity is promoted into
  authored state.

The native handler validates the raw pin and the private verified result,
checks media kind, reads the explicit target and scoped clip collection,
checks the current target alias against the exact OLD manifest, and requires
an exact NEW binding when the destination alias is already occupied. A
conflicting occupied NEW alias refuses; no alias-wide rewrite or fan-out is
performed. The only authored writes are the target clip's `asset` field and,
when absent, the scoped NEW asset birth. The OLD alias and siblings remain
untouched.

The normal recorder supplies target/collection membership and order, old/new
alias reads, exact media dependencies, target binding, created identity, and
ordinary `expect` guards. Existing inverse/rebase machinery therefore keeps
the original-base, ABA, dependency, reload and retry protections; raw mode
does not introduce a guard refresh or a different owner/addressing path.

The prior Runtime carrier review and peer ACK were also checked:
`runtime-raw-old-swap-existing-carrier-review.md` and
`peer-runtime-to-agent-20261021T0323-raw-old-swap-existing-carrier.md` confirm
that the existing request-declared, project-owned, single-FD
`raw_media_info`/acceptance recheck is the intended private boundary. That
evidence does not claim the end-to-end raw swap positive.

## Evidence

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_raw_old_swap_successor.py \
  tests/editing_conformance/test_recipe_parent_media.py \
  tests/editing_conformance/test_recipe_occurrence_media.py \
  tests/sdk/test_timeline_materialization_schema_union.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py
158 passed in 188.80s (0:03:08)

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B -m ruff check --no-cache \
  astrid/sdk/timeline/native_occurrence_media_commands.py \
  astrid/sdk/timeline/commands.py astrid/sdk/timeline/commit.py \
  tests/editing_conformance/test_raw_old_swap_successor.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_materialization_schema_union.py --output-format=concise
All checks passed!

git diff --check
passed
```

I also directly inspected an executed raw command: it retained exactly the
two OLD fields, recorded `media.old` and `media.new`, read the target and old
and new aliases, created only `parent/asset:reserved-new`, and wrote only the
new alias plus `parent/clip:clip-a::asset`.

The first test invocation without the shared Runtime source failed during
collection with `ModuleNotFoundError: runtime_protocol`; no tests ran. The
rerun above added the read-only shared Runtime path and passed.

## Not run / next step

Per the task boundary, I did not run Runtime/client/schema-generation,
pin/activation, full, browser, socket, renderer, or end-to-end native raw
qualification. The next bounded step is the paired Runtime/Agent acceptance
positive and exact retry/restart proof once its Runtime source is selected.

No repository source or test files were changed by this review.
