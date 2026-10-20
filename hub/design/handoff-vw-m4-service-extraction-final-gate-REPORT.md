# APPROVE — `vw-m4-service-window-source-extract`

## Reviewed commit and scope

- Agent repo: `/home/user/peteromallet/astrid-agent`
- Reviewed commit: `0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6`
- Reviewed base: `4ef1391c2c104d5d11b3a27265035c51be296045`
- Commit subject: `refactor(rendering): extract window input materialization`
- Exact changed product files (and only these):
  - `astrid/core/rendering/service.py`
  - `astrid/core/rendering/window_inputs.py`

The extraction is cohesive and limited to Timeline-added native/legacy window-input selection and materialization. `RenderService._segment_request` remains the public service entrypoint and passes `self._window_timeline` as the slicing hook. The helper has no new policy, timing math, DTO, factory, custody, or main-feature behavior. `parallelrun.py`/helper and Root preparation are untouched.

## Source review

- `service.py`: 2367 lines at base → 2298 lines at reviewed commit.
- New helper: 106 lines.
- Commit diff: 8 additions / 77 deletions in `service.py`, 106 additions in `window_inputs.py`.
- Existing inventory remains unchanged. The service count is within the recorded 2314 target and unchanged 1200/50 tolerance; no threshold or inventory entry was edited.
- The moved executable body is AST-identical after normalizing the wrapper name and the injected `slice_timeline=self._window_timeline` hook (`AST_BODY_EQUAL True`).
- Native unlayered pass-through, reserved extent stripping, native original render-view extent measurement, exact track/clip isolation, legacy slicing, alpha stamps, atomic materialization, and SHA256 sidecars retain their prior ordering and behavior.
- Current Agent compatibility at `4ef1391c2` is preserved: normal service → helper → original `Timeline.for_render()` extent path remains intact, while the unchanged service `_window_timeline` retains legacy frame slicing, fade source-origin handling, pre-tail positives, empty-gap behavior, and its known tail limitations.

## Evidence

Owner handoff evidence, reviewed rather than re-run in the Agent worktree:

- `tests/core/rendering/test_service.py`, `tests/packs/rendering/test_native_layer_extent.py`, and `tests/packs/rendering/test_live_scene_composition.py`: **139 passed, 4 deselected** (real renderer cases excluded under the task’s no-local-render rule).
- Central `tests/packs/rendering/test_remotion_native_window.py`: **25 passed**, exit 0.
- Before/after identity harness: **78 identical payload/error/immutability examples**, including rational FPS, native/legacy, layer variants, source/empty/sparse cases, and malformed inputs.
- Helper Ruff and mypy passed; `git diff --check` passed; service lint findings were unchanged.
- Global giant-file inventory was run and failed only after the service entry: separate `run.py` was 1929 vs recorded 1851 (+78). This is outside this two-file review scope; no threshold or other inventory entry was changed.

Independent final-gate evidence run against committed source, without loading the whole Agent checkout:

```text
PYTHONDONTWRITEBYTECODE=1 python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m4-service-extraction-final-gate-tiny-extract.py
PASS tiny committed-source window_inputs harness: native/no-layer, native/layer extent+alpha, legacy hook+clear, immutability/hash, structured error
```

The harness extracts only the committed helper AST and uses tiny local stubs for its read-only dependencies. It verifies native no-read pass-through and stale extent removal, original-source extent propagation, layer isolation/alpha, legacy hook arguments and null-window behavior, source immutability, sidecar digest, and malformed non-object errors.

Additional read-only checks:

```text
git diff-tree --check 0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6^ 0611b0f9c34ad56d8e1faab08f10bbe665d4fdd6
# pass

AST comparison of base _segment_request body vs committed helper body
# AST_BODY_EQUAL True
```

## Main-vs-base compatibility note

Actual Agent `origin/main` is `a411628f8fd6129f9c58c332019b56769d997384`; the reviewed extraction base is current integration `4ef1391c2`. The main→base delta is broad integration work, including `service.py` (+63/-10), `remotion_runtime.py` (+109/-17), new `verified_source.py` (+206), and the existing rationale/baseline updates. The reviewed commit adds only the two listed extraction files on top of that integration base; it does not alter those main-vs-base changes or broaden their policy. This is the expected merge context, not a reason to reject this bounded extraction.

## Limits and recommendation

- No browser, render, HTTP/socket, install, network, or full suite was run, per brief.
- The four real-render cases remain unverified by this review; the owner explicitly excluded them under the no-local-render grant.
- The separate `run.py` inventory drift remains for its owner/combined extraction review.

**Recommendation: APPROVE for Agent owner merge.** Merge this exact two-file commit with the separately owned extraction, then rerun the unchanged global inventory gate on the combined tree.
