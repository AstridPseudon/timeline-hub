I added a `shot.set` EditCommand for the shot name and a bounded set of scalar generation settings. Targeted tests pass (1797 passed, 4 skipped, 5 xfailed). I did not run a full suite, and I did not run the Runtime provider-level commit tests for this op.

## What it does
- **Selector and args:** `shot.set` takes `occurrence:<id>/shot` and `args = {values: {name?, settings?}, clear: [...]}`, closed like `track.set` and `clip.set`.
- **Ownership:** it is occurrence-only. A shared-shot edit is refused, and a sibling occurrence of the same source shot is never touched.
- **Clear policy:** clear removes the field, and `""` and `null` are values. Unchanged writes are recorded, and the inverse restores missing vs null vs value.
- **Supported settings:** 22 scalar roots such as `prompt`, `selectedModel` and `turboMode`. Several can change in one atomic command, which is how a model change with its coupled fields works.
- **Unsupported settings:** `steerableMotionSettings`, `phaseConfig`, `pairConfigs`, `shotImageIds`, `loras`, `structureVideo` and `modelSettingsByModel` are refused, set or clear. This means the "selected model plus its coupled model fields" golden from the gap doc covers only the scalar coupled fields. The compound `modelSettingsByModel` part is not covered.
- **Schema:** the changes are additive (a new `ShotSetArgs` and a new op block). I edited the JSON by hand, so I didn't confirm its formatting round-trips.
- **Code changes:**
  - `State.set` in `_command_state.py` now writes below an occurrence's shot payload.
  - The handler is the new `_shot_commands.py`.
  - It is registered in `commands.py`.

## Name decision
The canonical name field is root `payload.name`.
- **Why:** every Agent reader already uses it, and the App already displays it before `provenance.name`.
- **Legacy names:** `provenance.name`, then `provenance.title`, then `metadata.name`, are read-time fallbacks only. No command rewrites them.
- **Migration:** moving a legacy name is an explicit `shot.set {name: …}` that is recorded, guarded and invertible.
- **After a clear:** a reader that still falls back will show the legacy name again.

## Tests and fixture
`tests/editing_conformance/test_recipe_shot_set.py` (61 tests) covers:
- round-trip per presence state, and replay;
- unchanged-write and A→B→A edges;
- disjoint rebase and same-field conflict;
- occurrence vs shared isolation, including compiled shot revisions;
- original-guard refusals;
- closed-arg refusals and unsupported roots;
- the clear vs empty vs null distinction.

The golden fixture is `tests/editing_conformance/fixtures/recipe_m2_shot_set.json`.

## Test commands and results
- `pytest -q tests/editing_conformance/test_recipe_scalar_commands.py` passed, 70 tests.
- `pytest -q tests/editing_conformance/test_recipe_shot_set.py` passed, 61 tests.
- Central service: `request-test agt-m2-shot-settings targeted --files "tests/editing_conformance tests/timeline tests/sdk/test_timeline_commit_provider_scalar.py tests/test_schema_contract.py"` passed with 1797 passed, 4 skipped, 137 deselected, 5 xfailed, 179 subtests passed.

## What's unverified
- **Runtime artifacts:** I did not regenerate them, and the provider compatibility check hasn't been run for `shot.set`.
- **Real shot data:** I assumed the settings live at `payload.settings`, matching the App's `revision.settings`. I did not check this against real Runtime shot revisions, and the test fixture has no top-level `settings`.
- **Gap-doc items not covered:**
  - "stale source pin" refusal: a changed source is refused, but only through the shot identity read.
  - The mixed supported/unsupported batch refusal is tested, but only as a rejection of the whole batch.

## What App and Runtime must do
- **App:** switch the settings and rename publishes to `shot.set`, sending only touched roots. Rename must write `name`, not `provenance.name`. Compound roots stay on the existing guarded fallback for now.
- **Runtime:** regenerate the schema-derived artifact for `ShotSetArgs` and the new op, and run the provider compatibility check.

The design note is `docs/design/shot-set-command.md`, and the commit message is at `.../workers/agt-m2-shot-settings/commit-msg`. I created `DONE`.
