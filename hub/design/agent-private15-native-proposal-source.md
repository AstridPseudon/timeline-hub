# Agent private15 native proposal source report

## Implemented

- Replaced the shared `sync_draft_voiceover` caller-bound `bound.publish(...)`
  boundary with existing `native_voiceover.capture_draft_voiceover(...)` and
  `producer.build_producer_batch(...)` validation.
- Successful preparation now returns `authoring_proposal`, the existing
  six-key settled proposal (`schema_version`, `producer`, `admitted_target`,
  `commands`, `rationale`, `proposal_digest`), and reports `published: false`.
- The proposal target uses the observed settled head revision and
  `head_publication_id`; missing publication identity refuses.
- Generated media is accepted only from an exact five-field settled selection,
  the matching settled object identity, Runtime output intrinsic duration, and
  verified byte size. Existing source media keeps its exact selection and
  source duration for the native swap carrier.
- The approved 74925 inner speech intent/runtime-context hunk is included
  exactly. Inner speech task/attempt/media identity is not used as the outer
  producer pin.
- Outer producer identity is accepted only from `client.trusted_execution_context`
  with the five existing producer fields. The current normal Python action host
  does not expose this mapping, so the shared operation refuses with the exact
  host-boundary message instead of fabricating authority.
- Direct tests preserve all original 22 positive cases and add proposal,
  no-publish, and missing-trusted-context controls. The former CAS-publish
  assertion is explicitly mapped to proposal readiness plus zero
  `bound.publish` calls.

## Verification

```text
PYTHONPATH=. /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/packs/video_editing/test_draft_voiceover.py \
  tests/editing_conformance/test_recipe_native_voiceover.py \
  tests/editing_conformance/test_producer_guard.py \
  tests/editing_conformance/test_settled_proposal_contract.py
133 passed in 6.07s
```

Also passed `python3 -m py_compile` and `git diff --check`. The source file
passes the repository Ruff invocation; the touched test file retains existing
baseline compact-statement lint findings.

## Not run / next seam

No full, live, browser, Runtime, or normal-pin execution was run. The action
worker must connect the existing host trusted execution context and managed
proposal output settlement; this worker intentionally did not add a DTO, API,
scope, store, whitelist, or caller identity field.
