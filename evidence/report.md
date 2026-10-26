# A-review-T1-placement-fix-r1

## Verdict: PASS

Reviewed `tl/A-T1-placement-fix-r1` plus fix commit `5a2643ad50` against the
rejected original and `tl/zoom-integration`. No product code was changed by
this review.

## Code review

- `astrid/sdk/timeline/_clip_scalar_commands.py:127-133` now admits initial
  assignment only when `allow_initial` is true, the target is an occurrence
  clip, `clipType` is exactly `am-discord`, and neither `elementRef` nor the
  legacy `element_ref` exists.
- The existing `before` identity check remains unchanged, preserving id/kind
  and non-null pack-owner rules for referenced clips. Parent clips and other
  occurrence clips still refuse initial assignment.
- `place_element` validates the exact occurrence target and owner-qualified
  element, reads the current admission, captures the exact document pin, and
  executes `clip.set-element` with `schema_source` through the existing
  `TimelineSession.submit`/`flush` durable commit path. The public
  `RemoteTimelines.place_element` route and CLI handler forward the target,
  element identity, expected head, and idempotency key.
- New durable coverage in `tests/core/test_timeline_element_placement.py`
  covers malformed target, missing admission, wrong revision, stale expected
  head, exact pin capture, retry by idempotent identity, and inverse
  restoration. Existing selected-schema/conformance/publication tests retain
  identity, owner, selected-pin, CAS, replay, inverse, and CLI assertions.
- `git diff --stat tl/A-T1-placement-r1..tl/A-T1-placement-fix-r1` is limited
  to `_clip_scalar_commands.py` and the new placement test. Existing tests are
  unchanged; no assertions were removed or weakened.

## Tests

Required central command:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test A-review-T1-placement-fix-r1 targeted --files "astrid/sdk/timeline/_clip_scalar_commands.py tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_selected_schema.py tests/packs/timeline/test_cli_parity.py tests/core/test_timeline_element_placement.py tests/core/test_timeline_element_publication.py") && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Central result: infrastructure qualification failure before collection,
exit 4. The runner omitted the Runtime source path and failed with:
`ModuleNotFoundError: No module named 'runtime_protocol'` from
`astrid/core/pack/source_setup.py`.

The same targeted files passed with the required explicit Runtime path:

```text
TMPROOT=$(mktemp -d /tmp/timeline-review-XXXXXX) && PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -o cache_dir="$TMPROOT/pytest-cache" astrid/sdk/timeline/_clip_scalar_commands.py tests/editing_conformance/test_recipe_clip_set_element.py tests/sdk/test_timeline_selected_schema.py tests/packs/timeline/test_cli_parity.py tests/core/test_timeline_element_placement.py tests/core/test_timeline_element_publication.py
```

Result: **181 passed in 31.99s**.

Additional worker evidence reported compileall, Ruff, and `git diff --check`
passing. No full or live-socket suite was run.

## Follow-up

Promote the fix after the central test service is corrected to include
`/home/user/work/runtime` in Agent test collection, then rerun this exact
targeted request if a central qualification record is required.
