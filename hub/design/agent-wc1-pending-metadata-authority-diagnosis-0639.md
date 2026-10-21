# WC1 pending metadata authority diagnosis

Date: 2026-10-21 UTC  
Scope: `2aa627af22c8087022101b23aeeb93eca1b2b1a6` and corrected
`d161b4a44adf90330df8227beb63acd8cefb9140` (tree
`3ff62be3ac74b814c321bf12182d28063098f0f3`).

## Diagnosis

The independent HOLD is a real predicate gap, but its mutated
`reads`/`selections` example is not a normal caller-reachable unsafe retry.
Those fields are produced by the native capture and are not caller inputs to
`replace_selected_media`. A normal retry can change `source_object_id`,
`expected_head`, the media selections, or the caller key; those are already
checked against the persisted command/base. It cannot ask this API to replace
the persisted command's reads or selections.

The remaining example requires an injected or corrupted outbox (or an
in-process test double mutating `state['pending']`). It is still worth
classifying because `_pending_matches` currently accepts any lists there, but
it does not establish the third patch's needed normal-path data-loss case.

## Exact normal path and ownership

`RemoteTimelines.replace_parent_media` routes the exact-selection form to
`replace_selected_media` with the caller's `occurrence_id`, `clip_id`,
`source_object_id`, `expected_head`, `expected_publication`, `old_media`,
`media`, and idempotency key. The selected route requires both complete
five-field selections, requires `media['object_id'] == source_object_id`,
and opens `TimelineSession` pinned to the supplied original revision and
publication. `TimelineSession.open` refuses a pending outbox whose base does
not equal that pin; it never refreshes the base from current head.

With no pending state, the route reads the pinned bundle, verifies both exact
media selections, and captures either `clip.swap-media` (parent) or
`occurrence.swap-media` (occurrence). The capture is the authoritative command
metadata: exact command keys, operation/select/args/ownership intent,
`resolved`, `reads`, `selections`, `bindings`, `created`, `expect`, and
`authorship`. On the occurrence fixture the command has 26 reads and 3
selections. `TimelineSession.commit` stages a deep copy of that command into
the outbox, then `flush` constructs and durably stores the flight before POST:

```text
body = {
  api_version, project_id, timeline_id,
  base_revision_id, base_publication_id,
  commands: [the complete captured command],
  source: {via: "python"}, dry_run: false,
  # rationale only when already present in the outbox
}
flight = {path, body: canonical request bytes, key: caller key or generated key,
          count: 1, fence}
```

The selected-media caller supplies no rationale. `rationale` is state-level
metadata used by the proposal/publish path; selected-media capture does not
set or recapture it. A matching media command with an unexpected rationale
would require an already-mutated outbox state, not this API's capture path.
On retry, `flush` owns the persisted `flight['key']` and exact `flight['body']`;
it does not substitute a new caller key or recapture guards.

## Executable proof

This source-only probe captured the real occurrence swap command, then changed
only the first read's `ref` to `occurrence:foreign` and only a selection's
owner/membership in separate runs:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -B - <<'PY'
from copy import deepcopy
from tests.editing_conformance.test_recipe_occurrence_media import inputs
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.native_occurrence_media_commands import capture_occurrence_swap_media
from astrid.sdk.timeline_media_replacement import _pending_matches
from astrid.sdk.timeline.commands import execute

document, old, new, verified = inputs()
bundle = bundle_from_document(document)
command = capture_occurrence_swap_media(
    bundle, 'occurrence:occ-a/clip:clip-a', old, new, verified_media=verified)
kwargs = dict(owner='occurrence:occ-a', clip_id='clip-a',
              source_object_id=new['object_id'], old_media=old, media=new)
bad = deepcopy(command)
bad['reads'][0]['ref'] = 'occurrence:foreign'
assert _pending_matches(bad, **kwargs) is True  # predicate gap
try:
    execute(bundle, [bad], verified_media=verified)
except Exception as exc:
    print(type(exc).__name__, str(exc), getattr(exc, 'kind', None))
else:
    raise AssertionError('authoritative provider accepted altered read')
PY
```

Observed: `_pending_matches` returned `True`; the authoritative Agent
provider refused before acceptance with `CommandError: original authored
guard changed` (`dependency_changed`). An altered selection membership/owner
was likewise refused with `selection_changed`. No provider acceptance/write
occurred.

For an already-created flight, the existing carrier is stronger and requires
no new checksum/store/DTO: `_flight_body` parses the frozen flight body and
requires exact equality between `body['commands']` and the pending prefix,
the original project/timeline/base, path, key, and dry-run flag. The same
probe with the mutated pending command and the original flight produced:

```text
TimelineEditError: in-flight request is immutable; retry its original payload and key
transport_calls=0
```

This is the settled exact-flight precedent also covered by
`tests/sdk/test_timeline_sync.py` lost-ack/reload and changed-key controls.

## Correction recipe / disposition

Use the existing original flight body as the comparison carrier on the retry
branch; retain `_flight_body` as the final complete command-metadata check.
Do not refresh reads, selections, guards, or the base from current head, and
do not add a digest, store, DTO, or new retained authority solely to satisfy
the static `_pending_matches` predicate. For a no-flight pending state, the
existing durable pending command is the retained original capture; the normal
API has no alternate metadata to compare against. If that state is externally
mutated, the existing Agent provider's authoritative capture/claim checks
refuse representative altered reads/selections before Runtime acceptance.

Therefore this review does not authorize a third product patch or HTTP/full/
native run. Keep the two source attempts on HOLD for the review gate, but scope
the remaining finding as corrupt/injected outbox metadata, not a demonstrated
normal-path unsafe retry. The normal selected-media tests and adjacent sync
tests remain passing; paired published-014 HTTP parent/occurrence acceptance
is still unverified and was intentionally not run here.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/test_timeline_clip_replacement.py tests/sdk/test_timeline_sync.py tests/sdk/test_timeline_native_frontends.py` — **83 passed in 10.72s**.
- `ruff check astrid/sdk/timeline_media_replacement.py tests/test_timeline_clip_replacement.py` — passed.
- `git diff --check` — passed.
- No product or fixture edits; no HTTP, full, browser, renderer, or native acceptance run.
