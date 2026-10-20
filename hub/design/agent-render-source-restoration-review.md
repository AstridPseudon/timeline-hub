# Agent render source restoration review

## Verdict: APPROVE

Reviewed tree `4f29c39a849faacdf1704d65f3a5ecbe7478f3a5` (parent/base
`a760ecca02111b0e0841510926f200e398f3b6cb`) against the settled PLAN.
The four changed files are exactly the two carrier/service files and the two
tests named by the change.

The restored `RenderRequest.verified_source` is the existing Python-only
carrier from the approved `62e6d2c2` seam:

- construction obtains the carrier only through `inherited_source()`;
- a supplied carrier must be the exact `VerifiedTimelineSource` type and equal
  the inherited carrier, otherwise construction refuses caller replacement;
- `for_backend()` reconstructs the same Python-only field while backend
  projection remains the normal request projection;
- `to_dict()` and `from_dict()` keep the field out of the wire contract;
- backend namespaces reject all three reserved source keys;
- `RenderService.render_request()` re-derives and validates the inherited
  carrier before localization/selection, and validates its prepared paths and
  bytes again.

The e36ccace and eac529ae main shim-removal commits remove compatibility
aliases/legacy rendering compatibility. They do not establish a competing
source carrier, so this restoration does not revive those shims. The
re-enabled SDK tests were inspected but their unchanged real claim positives
were not repeated, per the review brief.

## Evidence

Focused authority negatives:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -q \
  tests/packs/rendering/test_verified_source.py \
  -k 'render_request_rejects_reserved_backend_source_config or render_service_refuses_lost_verified_source_authority or host_rejects_reserved_source_ports or host_refuses_caller_replacement_of_verified_source or forged_authority_cannot_replace_admitted_ref or missing_authority_fails_closed or host_preserves_literal_source_refusals'
32 passed, 28 deselected
```

Direct request/wire/save-adjacent neighbors, with private pytest cache
disabled:

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -p no:cacheprovider -q tests/core/rendering/test_contracts.py -k 'dto_json_round_trip or optional_request_fields_default_and_selected_config_isolated or unknown_request_top_level_field_is_protocol_error'
3 passed, 71 deselected

PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -p no:cacheprovider -q tests/core/rendering/test_schema_roundtrip.py -k 'every_schema_and_example_is_valid_and_parses or canonical_raw_fixture_validates_and_round_trips_identically'
13 passed, 18 deselected

PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -p no:cacheprovider -q tests/packs/rendering/test_render_facade.py -k 'render_maps_backend_kwargs_into_namespaced_backend_config or render_merges_explicit_backend_config'
2 passed, 17 deselected

PYTHONPATH=. /home/user/work/venv-agent/bin/pytest -p no:cacheprovider -q tests/stage1/test_media_handoff_render_boundary.py -k 'render_request_handoff_roundtrips_and_visualizer_verifies_it'
1 passed, 4 deselected
```

`git diff --check 4f29c39a^ 4f29c39a` passed. The worker worktree remained
clean after inspection and testing.

## Limits

No full suite, whole-root pytest, Node/browser suite, or unchanged real
Runtime claim positives were run. The wire/Node boundary is covered here by
the Python DTO/schema round trips and render-facade namespace tests; no Node
save code is changed by this commit. A future integration qualification can
run the four reactivated SDK combinations through the central test service,
but that is outside this security/source-authority review.
