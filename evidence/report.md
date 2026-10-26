# B-review-T1-fixture-fix-1

## PASS

Reviewed `tl/B-fix-T1-fixture-1` against `tl/shotlayer-integration`.

- The fix adds only the canonical fixture, its focused Runtime validator, and
  the worker evidence note. No existing assertion was removed, weakened,
  skipped, or deleted.
- `conformance/fixtures/shot-layering-v1.json` contains no `UNKNOWN` value at
  any depth and hashes to the required canonical digest:
  `3c75d3ede4f868bedc46bfebe1c6988e159a58d4edf444986509e9a87f8fba1e`.
- All seven settled cases are present: loose above/below/same row,
  transparency/empty area, shot-only suffix tracks, multiple occurrences,
  merged audio, namespaced visual groups via `track.app.group`, and missing-row
  fallback with the exact warning.
- Each input uses top-level occurrences with `occurrence_id`, `shot_id`,
  `revision_id`, `at_ms`, and `duration_ms`; child data is under
  `shot_revisions[].internal_timeline_revision.timeline`.
- Direct projection checks accepted all seven inputs in both consumers:
  Agent `parse_shot_composition` + `project_shot_composition`, and App adapter
  preparation + `projectCanonicalComposition`.
- The focused test is meaningful: it checks recursive `UNKNOWN` rejection,
  canonical shape/linking, all required cases, group tags, track ordering,
  transparency, merged audio, and the missing-row warning.

## Checks

- `python -m pytest -q --basetemp=/tmp/w-4bc1a324c5/t1-review-pytest /tmp/w-4bc1a324c5/t1-review-fix-tree/tests/test_shot_layering_fixture.py`
  — `3 passed`.
- `git diff --check tl/shotlayer-integration..tl/B-fix-T1-fixture-1` — passed.
- Agent direct parse/projection check — `accepted 7 cases`.
- App adapter/projection check — `accepted 7 cases`.

The mandated central request was run exactly as:

```text
$ORCH/bin/request-test B-review-T1-fixture-fix-1 targeted --files "conformance/fixtures/shot-layering-v1.json tests/test_shot_layering_fixture.py"
```

The service did not execute the test. First request
`B-review-T1-fixture-fix-1-targeted-1026225224-11098` failed before collection
because this review worktree lacked the candidate paths. After temporarily
materializing the exact candidate files, request
`B-review-T1-fixture-fix-1-targeted-1026225443-11605` still failed at collection
(`exit=4`): the generated pytest command passed the JSON fixture as a test
path, producing `no tests ran` / `not found ... conformance/fixtures/shot-layering-v1.json`.
This is a central targeted-lane collection defect, not a fixture assertion
failure; the temporary files were removed and no product changes remain.

## T2/T3 follow-up

Vendor this Runtime fixture byte-for-byte in each consumer, pin
`3c75d3ede4f868bedc46bfebe1c6988e159a58d4edf444986509e9a87f8fba1e` in each
consumer test, and run every case through the real Agent/App projection entry
point. Update each copy and digest together if T1 changes. T1 made no Agent or
App changes.
