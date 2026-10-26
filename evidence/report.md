# T2 Agent shot-layer projection

Both `project_shot_composition` and `project_runtime_parent_composition` now build contiguous visual track groups immediately above each occurrence's parent row. Visual tracks use `<occurrence>~<track>` and `track.app.group = {id, sourceTrack}`; authored inner order, track properties/app metadata, and child geometry are retained. Occurrences on the same row keep input order. Missing rows fall back to the top and log the fixture's exact warning message with `code=timeline-patch/target-not-found`.

Audio tracks retain their ids and the existing merge-by-id/neighbor placement; clip timing, gain, mute, volume, and asset handling are unchanged. Non-empty shot opacity/transform is refused before projecting any children, including empty shots, through `_apply_placement_transform`. The user-facing message is: “Shot opacity and transforms are not supported yet. Remove them from the shot placement to render this timeline.” Empty placement values remain supported.

The former ordering test now checks the explicitly required group order and retains its complete track-property comparison. The managed candidate-preview test uses an empty placement transform, retaining every assertion; explicit new tests cover refusal of the former non-empty placement. No tests were skipped or weakened to expect missing behavior.

## Shared fixture

Vendored an exact 26,332-byte copy at `tests/fixtures/timeline/shot-layering-v1.json`, the established Agent fixture location. The canonical source is Runtime `conformance/fixtures/shot-layering-v1.json`, T1 fix commit `5a7a2059c37c6ccd33e66839095756697468ea46` on `tl/B-fix-T1-fixture-1`. SHA-256:

`3c75d3ede4f868bedc46bfebe1c6988e159a58d4edf444986509e9a87f8fba1e`

The consumer test always checks the pinned canonical digest, and additionally compares bytes when the canonical fixture exists in the Runtime checkout discovered by the established `tests.helpers.runtime.locate_runtime` helper. Direct tests were run with `ASTRID_RUNTIME_CHECKOUT` naming the T1 fix worktree before the harness recycled it; byte equality passed. Subsequent independent comparison of `git -C /home/user/work/runtime show tl/B-fix-T1-fixture-1:conformance/fixtures/shot-layering-v1.json | sha256sum` produced the same digest. No fixture values were invented or adapted. A narrow test-only adapter translates the same graph into the Runtime parent-closure entry point.

All seven fixture cases run against both Agent entry points: film, loose above/below/same row, shot-only suffix, two occurrences on one row, missing row. Assertions cover exact flat ordering, group tags, every clip's track, warning shape/message, transparent empty windows with no synthetic fill, unchanged parent clips, and detached source data.

## Validation

Final direct command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/w-cce3665a51/projection-final tests/timeline/test_shot_layering_projection.py tests/timeline/test_shot_composition_projection.py tests/core/timeline/test_shot_composition_projection_volume.py tests/timeline/test_shot_composition.py tests/timeline/test_authoring_recipes.py tests/timeline/test_authoring_bundle.py::test_frozen_candidate_projects_to_labelled_managed_render_without_publication
```

Result: **78 passed in 5.01s**.

Canonical byte-equality run:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/B-fix-T1-fixture-1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/w-cce3665a51/projection-shared tests/timeline/test_shot_layering_projection.py tests/timeline/test_shot_composition_projection.py tests/core/timeline/test_shot_composition_projection_volume.py tests/timeline/test_shot_composition.py
```

Result: **73 passed in 5.36s**.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check astrid/core/timeline/shot_composition_projection.py tests/timeline/test_shot_composition_projection.py tests/timeline/test_shot_layering_projection.py tests/timeline/test_authoring_bundle.py
git diff --check
```

Both passed.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m mypy --follow-imports=silent --cache-dir=/tmp/w-cce3665a51/mypy astrid/core/timeline/shot_composition_projection.py
```

Result: 3 existing errors, identical to HEAD checked using `--shadow-file` and a private baseline cache (Runtime closure key/optional Mapping inference). An initially introduced fourth inference error was fixed before the final direct run. Mypy is not clean at baseline; this change adds no errors.

An initial broad neighbor run produced 71 passed, 5 failed, 1 deselected: four Runtime locator failures in approval/restart tests (these were not rerun directly because live suites belong to the central service), and the candidate-preview test's former non-empty transform. That preview setup was corrected as described above and passes in the final direct run. The first import attempt without Runtime on PYTHONPATH failed before collection; all reported passing commands include Runtime explicitly.

Central service request:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test B-T2-agent-projection-1 targeted --files "tests/timeline/test_shot_composition_projection.py tests/timeline/test_shot_layering_projection.py tests/core/timeline/test_shot_composition_projection_volume.py tests/timeline/test_shot_composition.py tests/timeline/test_authoring_bundle.py tests/timeline/test_authoring_recipes.py"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test B-T2-agent-projection-1-targeted-1026225012-29341
```

Request id: `B-T2-agent-projection-1-targeted-1026225012-29341`. Currently queued by the central disk floor (5,000,000,000 bytes required; last observed 4,729,806,848 bytes available). The existing request has not been resubmitted. Central validation is not yet verified. No full suite or render was run.

A final independent byte comparison passed:

```sh
git -C /home/user/work/runtime show tl/B-fix-T1-fixture-1:conformance/fixtures/shot-layering-v1.json > /tmp/w-cce3665a51/canonical-shot-layering-v1.json
cmp tests/fixtures/timeline/shot-layering-v1.json /tmp/w-cce3665a51/canonical-shot-layering-v1.json
```

Next: restore the central service's free-space threshold and resume `wait-test` on the existing id. Do not resubmit the queued request. Central validation remains blocked; no DONE marker is claimed. Preview/export render parity and App behavior are outside this worker's scope and unverified here.
