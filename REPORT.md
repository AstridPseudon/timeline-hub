# V1 early schema acceptance map

Date: 2026-10-22 UTC  
Task: `vw-V1-meta-acceptance-map`  
Base: Composition `tl/integration`  
Scope: read-only early case collection for PLAN v2.1 §3 V1 and
`contract/commit-v2.md` §6. No implementation or test changes were made.

## Baseline and authority

The independently reviewed inventory remains authoritative:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/viewing-v1-schema-inventory.md`.
The contract is authoritative for behavior at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/commit-v2.md:4456-4520`.

Facts marked **pre-U1/current** describe the integration trees inspected here.
Facts marked **R4 candidate-only** come from frozen references and are not
available as current checks. U1/source handoff must land before V1 edits.

## Acceptance map

| seam | smallest source slice | existing fixture/test to reuse | later command |
| --- | --- | --- | --- |
| §6 locations and raw-vs-compiled boundary | **pre-U1/current:** Runtime `contract/schemas/shot-composition.json:24-74` (`RawTimelinePayload`), `76-119` (`RawTrack`/`RawClip`), `151-191` (parent/occurrence), `205-245` (shot), `274-285` (internal). These are open (`additionalProperties: true`). Compiled Runtime `contract/schemas/timeline-config.schema.json:1-142,145-...` is closed at root/track/clip/asset; `AssetEntry` is `492-533` and currently has no `meta`. | Runtime `tests/test_shot_composition_contract.py::test_schema_declares_raw_container_boundary_without_a_second_compiled_schema`, `::test_empty_and_ordinary_only_composition_fixtures_validate_losslessly`, `::test_pinned_compiled_timeline_schema_remains_strict`, and `::test_open_shot_payload_keeps_unknown_siblings_but_outer_envelope_stays_closed`. | `cd /home/user/work/runtime && python -m pytest -q tests/test_shot_composition_contract.py` |
| namespace key/object/null/finite-JSON rules | Contract §6 says `meta` is optional at parent, parent/internal TimelineConfig, shot, occurrence, clip, track, and registry asset records; namespace regex is `^[a-z][a-z0-9]*(?:[.-][a-z0-9]+)*$`, ASCII length 1–128, values are objects, descendants may be finite JSON including `null`/arrays, and `meta: null` or namespace `null` is invalid. Empty objects are valid. **pre-U1/current:** no current schema/provider test implements these rules. | Runtime raw open-container fixtures above; Agent `tests/timeline/test_timeline_roundtrip_fixture.py` and `tests/timeline/test_asset_registry_contract.py` are the smallest preservation fixtures, but currently cover an unknown top-level canary and known asset fields, not §6 `meta`. Add focused cases to these existing files after handoff; do not create a matrix. | Runtime targeted command above; Agent `cd /home/user/work/agent && python -m pytest -q tests/timeline/test_timeline_roundtrip_fixture.py tests/timeline/test_asset_registry_contract.py` |
| exact limits: 64 namespaces, 65,536/262,144 canonical UTF-8 bytes, depth 32 | Contract §6: max 64 namespaces; max 65,536 canonical UTF-8 bytes per namespace value; max 262,144 canonical UTF-8 bytes for all `meta`; max 32 nested container levels below a namespace value (namespace root is level 1). **Schema-expressible:** namespace `propertyNames` pattern/maxLength, `maxProperties: 64`, `meta` and namespace `type: object`, and the null rejection. **Provider checks:** canonical sorted-key compact UTF-8 byte counts, recursive container depth, finite-number enforcement, and the `meta_limit_exceeded` code/path/hint. Existing HTTP body limits may reject earlier; they are not substitutes for these per-occurrence checks. | Reuse the Runtime raw publication/shot fixtures and Agent timeline/registry fixtures; test only boundary-adjacent values (one under/at/over per control), not an exhaustive matrix. | Runtime schema check: `cd /home/user/work/runtime && python generators/generate.py --check && python scripts/artifact_manifest.py --check` (**pre-U1/current** generator/artifact checks only). **R4 candidate-only post-U1:** `python generators/materialize_timeline_schema.py --check --source <timeline-schema-root>`. Provider boundary tests belong in Agent targeted pytest after U1. |
| preserved unknown metadata and no opaque reference discovery | Contract §6 explicitly requires unknown namespaces/contents to survive load, patch, semantic edit, compile, acceptance, history, and undo; “strings in `meta` that look like IDs” receive no integrity/remapping/deletion/dependency tracking, and core reference/asset discovery must not interpret descendants or add phantom manifest entries (`commit-v2.md:4482-4493`). The preservation fixture includes `com.other.tool.foreign_id = "missing-is-allowed"` (`4501-4517`). **pre-U1/current:** Agent `banodoco_schema.py:350-393` allowlists only `app` at timeline/track/clip and excludes asset `meta`; `validators/registry.py:29-46` rejects unknown asset keys. `authoring_bundle.py:256-275` remaps only declared item-reference fields, and `603-648` checks only explicit clip media selectors. These are the correct narrow reference seams to retain; do not add a recursive metadata walk. | Agent `tests/timeline/test_timeline_roundtrip_fixture.py::test_unknown_top_level_field_is_preserved`; `tests/timeline/test_asset_registry_contract.py::test_roundtrip_preserves_extended_asset_fields`; `tests/timeline/test_shot_composition_projection.py` existing projected-asset/reference cases. App `src/tools/video-editor/lib/assetRegistryContract.test.ts` currently verifies known-field sanitization and explicitly strips unknown fields; it has no generic `meta` case. | Agent targeted command above plus `cd /home/user/work/agent && python -m pytest -q tests/timeline/test_shot_composition_projection.py`. App later: `cd /home/user/work/app && npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/lib/assetRegistryContract.test.ts`. |
| unchanged Composition evaluator/renderer output with opaque metadata | **pre-U1/current:** Composition `typescript/src/TimelineComposition.tsx:68-73` selects an asset by `clip.asset` only; `231-262` prepares evaluator inputs and component capabilities. `typescript/src/VisualClip.tsx:37-62` consumes only file/type/geometry-related known fields. `typescript/src/scene-evaluation.ts:218-235` reads the selected asset for bounds and frame evaluation; no generic `meta` read exists. Composition has zero reads of Agent compatibility keys such as `astrid_render_clock`, `astrid_bounds`, `liveScene`, or `astrid_layer`; those remain Agent renderer reads (for example Agent `packs/rendering/rendering/renderers/remotion/run.py:917-955`, `actions/timeline_visualize/composed_frame.py:657-666`, and `rendering/renderers/threejs/run.py:189-198`). | Composition `typescript/tests/scene-evaluation.test.ts` (frame/evaluator expectations), `typescript/tests/registries.test.ts` (exact selected asset passed to an effect and input immutability), and `typescript/tests/transition-policy.test.ts` (render/evaluator parity and unchanged input assertions). Add one opaque-`meta` variant to an existing fixture and compare the baseline frame/markup/selected asset; no golden JSON. App neighboring checks are `src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx`, `TimelineRenderer.test.tsx`, and `data/shotCompositionProjection.test.ts`. | Composition targeted build/test: `cd /home/user/work/wt/vw-V1-meta-acceptance-map && npm run build:test && node --import ./typescript/tests/register-extensionless.mjs --test typescript/test-dist/tests/scene-evaluation.test.js typescript/test-dist/tests/registries.test.js typescript/test-dist/tests/transition-policy.test.js`. App consumer check later: `cd /home/user/work/app && npx vitest run --config config/testing/vitest.config.ts src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx src/tools/video-editor/compositions/TimelineRenderer.test.tsx src/tools/video-editor/data/shotCompositionProjection.test.ts`. |

## Smallest implementable slices and overlaps

- Runtime/package handoff: U1 must materialize the canonical schema and
  provenance. Current Runtime checks are
  `python generators/generate.py --check` and
  `python scripts/artifact_manifest.py --check`; neither is a current
  TimelineConfig-source materializer. The frozen Runtime candidate's
  `generators/materialize_timeline_schema.py` and its default source path are
  **R4 candidate-only**.
- Agent V1 slice: the shared-schema projection/allowlists in
  `astrid/core/timeline/banodoco_schema.py`, registry validation in
  `astrid/core/timeline/validators/registry.py`, and the narrow timeline
  validation path in `validators/timeline.py`; preserve explicit reference
  selectors in `astrid/core/timeline/authoring_bundle.py`. The current
  `managed_timeline.py:64-71` stripping seam removes only fixed editor keys;
  generic `meta` must remain opaque after that filtering.
- App U4p overlap: the vendor package's generated schema/type outputs and
  `src/tools/video-editor/types/index.ts:584-614` plus
  `src/tools/video-editor/lib/timeline-domain.ts:230-253,2515-2532` are the
  concrete registry type/sanitization seams. The current sanitizer preserves
  listed fields and drops other keys, so generic asset-record `meta` needs an
  explicit U4p/V1 handoff. Existing vendor commands are
  `npm run gen:types`, `npm run gen:python`, `npm run check:codegen`; `make gen`
  runs only the Python generator.
- Composition V1 slice: `typescript/src/types.ts:81-98` and the three focused
  Composition tests above. Runtime behavior already ignores unknown asset
  fields because the renderer reads known fields by name; the public type still
  lacks generic `meta`.
- Cross-lane need: U4a/U4p schema regeneration and V1 must be serialized at the
  generated-copy boundary. Agent V2 may touch the same
  `banodoco_schema.py`/validator modules; if so, V1's `meta` admission and
  limits must be merged with V2's structural/timing checks rather than landed
  as a competing allowlist. No exact V2 file list is stated in PLAN, so this is
  an implementation handoff constraint, not an invented ownership decision.

## Commands and verification performed

No targeted tests, typechecks, lint, generation, installs, sockets, browsers,
renders, or full suites were run, per the read-only brief. The exact existing
commands to use later are listed in the map. Composition has no `lint` or
`typecheck` script in `package.json`; `build:test` is the available focused
compile/test build. App's `lint` is `npm run lint`; no new lint command is
proposed here.

The report-only worktree was checked with `git diff --check`; product status
remains unchanged apart from this report and the harness markers.
