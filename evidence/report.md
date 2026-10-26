# B-T1 fixture review: FAIL

## Scope

Reviewed `tl/B-T1-fixture-1` (`b9beb767b003e2e0acbcf85e22521bd7f7cf045f`) against
`tl/shotlayer-integration` (`c13379e22557b03dee0c0f36ae6f29ef6b674ca1`). The
diff adds only:

- `conformance/fixtures/shot-layering-v1.json`
- `tests/test_shot_layering_fixture.py`
- the worker's evidence note

No existing assertion was removed, weakened, skipped, or deleted. `git diff
--check` reports only a new blank line at EOF in the added test.

## What passed review

The fixture resolves all literal `UNKNOWN` values and includes the required
cases: the film, loose clips above/below/on the same row, transparency,
shot-only suffix tracks, two occurrences on one row, merged child audio, and
missing-row fallback with a warning. The decided `occurrence~inner-track`
namespacing and `track.app.group = {id, sourceTrack}` shape are represented.
The film's `transparent_windows_ms` and `vision-audio -> audio` expectations
make the empty-area and merged-audio requirements explicit.

## Reasons for FAIL

1. The fixture input is not the current shared document shape. It nests a
   `timeline` under each `shots[]` entry and names the occurrence `id` (for
   example, lines 35-52 and 71-83). Current Agent and App fixtures use a
   top-level `occurrences[]` list with `occurrence_id`, `shot_id`,
   `revision_id`, `at_ms`, and `duration_ms`, and child timelines under the
   revision's `internal_timeline_revision.timeline` (see the existing Agent
   `tests/fixtures/timeline/shot_composition.json` and App
   `src/tools/video-editor/data/shotComposition.fixture.json`). T2/T3 cannot
   pass this file directly to their existing projection entry points; each
   would need an undocumented bespoke conversion first. The fixture needs
   either the canonical document shape or an explicit, tested adapter
   contract.

2. The claimed Runtime read path is only a private test helper: lines 21-23
   of `tests/test_shot_layering_fixture.py` call `json.loads` directly from a
   path relative to the Runtime checkout. Runtime does not have a production
   loader for this fixture, and Agent/App checkouts cannot resolve
   `conformance/fixtures/shot-layering-v1.json` in their own repositories.
   The worker report explicitly leaves Agent/App consumers unverified and
   supplies no synchronization strategy.

The missing-row warning code family is grounded in App's existing
`timeline-patch/target-not-found` diagnostics, but this exact shot-layering
message is new behavior and must be asserted by the T2/T3 consumer tests when
the fallback is implemented.

## Required T2/T3 follow-up

Keep Runtime's file as the source of truth, vendor an exact byte-for-byte copy
into each consumer's test-fixture directory, and pin its SHA-256 in each
consumer test. The reviewed candidate bytes hash to:

`d964db8eecaf540b1f2aa502dbcf66ff4bfe70ec916b3a642529807b91719da5`

T2/T3 should update the copies and digest together whenever T1 changes, and
their tests should fail on a digest mismatch. They should also add a small
adapter (or revise this fixture to canonical document shape) and test every
case through their real projection entry point. A workspace-only optional
check may compare the vendored file with Runtime's path, but consumer tests
must not depend on `/home/user/work` or `$ORCH`.

## Tests

Worker-reported local command:

```text
python -m pytest -q --basetemp=/tmp/w-099a21ba7e/B-T1-fixture-1-pytest tests/test_shot_layering_fixture.py
2 passed, 1 warning in 0.72s
```

The warning was the existing pytest `Unknown config option: timeout` warning.

Mandated central command submitted exactly as:

```text
$ORCH/bin/request-test B-review-T1-fixture-1 targeted --files "conformance/fixtures/shot-layering-v1.json tests/test_shot_layering_fixture.py"
```

Request id:
`B-review-T1-fixture-1-targeted-1026224253-15152`.

At review completion it remained queued because the central service reported
4.72 GB available against its 5 GB floor (`why: low disk`). No central test
result was available; the local result above is not a substitute for the
required service run.
