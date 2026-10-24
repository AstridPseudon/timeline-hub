## Report

Independent source-cause verdict: **PASS** (diagnosis confirmed; not a product-pass claim).

The ten shared-occurrence redo failures are caused by an unauthenticated test fixture:

- `tests/editing_conformance/test_recipe_m1_commands.py:605-615` defines `recorded_removal()`, directly constructing `Recording` with unregistered `track.remove` / `clip.remove` commands.
- It bypasses `commands.execute`, the operation registry, external caller, Runtime/provider acceptance, and `commit.materialization`.
- `accepted_boundaries()` at lines 618–623 fabricates a minimal boundary and cannot supply authenticated effect/materialization/binding history.
- `_commit_patch.py:801-1042` correctly refuses redo with `history_unavailable` when those authenticated physical-normalization facts are absent.

The live carriers are:

- Parent clip deletion: registered `clip.delete`, used by native checkout and timeline-sheet omission flows. It preserves full rows, order, inverse/redo, ABA, and dependency guards.
- Generic collection membership/order changes: production `doc.patch` through `emitter.py`, authoring commit, Runtime provider, and child internal-revision flows.
- No registered production `track.remove` or generic `clip.remove` caller was found.

Precise input for Sol:

1. For parent clip cases, use `capture_clip_delete()` and the normal Runtime/provider acceptance path.
2. For generic track/clip row removal, construct an authenticated `before` and candidate `after` bundle, call `emit_document_commands(before, after)`, then submit through the existing `TimelineSession.commit_many` / authoring provider path.
3. Obtain redo history from the actual accepted provider receipt/publication. Do not call `Recording` directly, fabricate `accepted_boundaries`, splice bindings, or invent new operations.
4. Preserve all original row, order, opaque/null-field, inverse/redo, and ABA assertions when ported through that carrier.

D52 boundary:

- `recorded_removal()` is exclusively used by the four test regions at lines 626–657, 659–675, 723–735, and 841–847.
- `accepted_boundaries()` is not removable wholesale; it is used elsewhere for existing fixtures.
- The exact ten failures are fixture failures, not evidence that the corresponding production carrier is broken. The broad generic obligations remain live through `doc.patch`; the exact synthetic all-owner/all-kind combination is not proven by one external caller.

No source edits were made. Tests, registry execution, Runtime/realm execution, type checks, lint, and full suites were not run per task instructions.

Validation performed:

```text
git status --short --branch
## tl/agt-R2-M1-whole-path-1136

git diff --check
PASS

git diff --exit-code
PASS
```

Core source hashes were recorded for `_delete_commands.py`, `emitter.py`, `commands.py`, `_commit_patch.py`, and `test_recipe_m1_commands.py`. The required commit message and DONE marker were created.