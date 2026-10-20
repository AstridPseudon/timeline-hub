# Agent public10 / capture-chain audit

Status: **PASS WITH LIMITS — not a public10 or M3 qualification**

## Scope and pinned state

This audit reviewed the current Agent integration after public10 adoption, rather than the old fc6candidate state. The pinned integration and assigned-worker SHA are both:

`384918908aa8c75229c2b6ccdd8fda03b7ce24a1`

The requested comparison base is `b46140036e21948f1f807d8366b2e5d03e720697`; it is an ancestor of the pinned SHA. `git diff --check b461400..HEAD` passes. The Agent STATUS file named by the handoff was not present in the available STATUS/report roots; this report therefore uses the current Viewing status plus the checked-out Agent source and history as the operational record.

The public10 package adoption is already present at the b461 ancestor and is unchanged in the requested current delta. The current delta from b461 is principally the capture-chain and D09 current-check slice, not a new package adoption.

## Public10 artifact and toolchain

The committed artifact is `remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz`.

- SHA-256: `cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`
- Archive members: 77
- Size: 58,008 bytes
- SHA-512/base64: `SmJAoem9f+86D+eO+PvBAz3JydlefpUUwcOOkG7SU9k2ZPKpjXLWKHm/N4424TO5HNQtCHMt5T6Jy2Y5zA6Ycg==`
- Package version: `0.0.10`
- Package exports: `.`, `./evaluation`, `./theme-api`, `./registry.generated`, `./effects.generated`, `./animations.generated`, `./transitions.generated`, `./registries`, and `./package.json`
- Peers: React/React DOM `18.3.1`; Remotion packages `4.0.509`
- Runtime/toolchain pins: Node `20.19.4`, npm `10.8.2`, Remotion `4.0.509`

The archive contains package `dist`, declarations, package metadata, and README only. It has no source tree, TypeScript tree, or nested `node_modules`. Its evaluator closure has only local package chunks plus declared peer dependencies. The current readiness source requires version `0.0.10`, the above public exports, package metadata, dist, and a provisioned project install; it does not turn a missing install into a pass.

`remotion/package.json`, `remotion/package-lock.json`, and the artifact are byte-identical across b461 and the pinned current tree for this adoption slice. Static artifact/readiness checks pass. The assigned worktree has no Remotion `node_modules`, so actual package imports, bundling, SSR, or a live renderer were intentionally not claimed.

## Capture-chain result

The current capture path is materially more explicit and preserves source identity:

- `RuntimeCommitService.project_capture` validates the exact closure, freezes candidate bases and placements, rebuilds image closure, and projects through the existing runtime parent-composition projector without invoking a renderer or provider.
- Managed timeline capture projects image-only rows plus project/timeline identity, retaining canonical digest/payload while stripping GET-only decoration.
- Filmstrip capture opens an exact saved or candidate input closure. Saved captures carry the immutable requested parent revision and content digest. Candidate captures carry the committed base as authority, retain unpublished identity, and use a working-copy marker rather than claiming a committed candidate revision.
- Invocation keeps a forwarded candidate inline for Runtime admission. A working copy lacking the forwarded authoring preview is deliberately reduced to a CAS-only source reference (`source_kind: "cas"`), with no revision or working-copy claim. This is an honest unverified path, not a fabricated certification.

The source contains no literal `UNCERTIFIED` label. The unverified branch is represented structurally by CAS-only source handling, and the existing host expectation is that no verified `timeline_source` is available. If the product/handoff specifically requires a user-facing literal `UNCERTIFIED` label, that label is still absent; adding one was outside this audit and would require a settled display contract.

## Native M1 revision and pixel-lane behavior

Native saved provenance preserves the actual native revision. `snapshot_label` takes the canonical capture authority / inspection revision and intentionally ignores requested-revision or current-head hints. Candidate provenance is labeled as a candidate based on its committed base and sets `actual_revision_id` to null. Composed candidates likewise use the working-copy base rather than claiming their capture parent is a committed revision. The fast-lane tests cover historical, input-only, candidate, composed-candidate, missing-base, and contradictory-marker cases.

This preserves the M1 revision semantics. It does **not** qualify the pixel lane: the unverified CAS path does not enter the verified timeline source, and the current operational status still records native frame divergence (popup/backdrop and later background differences). No live capture, browser, renderer, audio, or pixel comparison was run here. There is no evidence in this audit for full-source certification or live Runtime equivalence.

## D09 private evaluator/caller census

The proposed D09 deletion was not adopted in the pinned tree. The private evaluator remains live:

- `astrid/core/timeline/onscreen.py` is present (452 lines) and still defines `Visible`, `Span`, `element_coverage`, `role_of`, `layout_bounds`, `visible_at`, and `coverage`.
- `astrid/sdk/timeline/check.py` still calls `onscreen.coverage`, `onscreen.element_coverage`, and `onscreen.layout_bounds`; its `_sprite_problems` path remains private.
- `astrid/sdk/timeline/reflow.py` still calls `onscreen.role_of` for authored-role/anchor survival.
- `astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py` still imports `element_coverage` and `visible_at`.
- Direct tests remain in `tests/core/timeline/test_onscreen.py`, `tests/core/timeline/test_onscreen_more.py`, `tests/packs/rendering/test_labels_overlay.py`, and `tests/packs/rendering/test_timeline_visualize_labels.py`; `tests/sdk/test_intent_app_astrid.py` also imports `_address`.

The proposed replacement files (`scene_answers.py`, `scene_roles.py`, `remotion/native-scene.mjs`, `remotion/scene-query.mjs`, `remotion/src/host-scene.ts`, and the associated deletion tests) are absent. Therefore the current tree has no public evaluator/caller source join that would support declaring D09 complete. This is an intentional readiness hold, not a regression introduced by this audit.

The adopted current-check slice changes scene gaps, empty cuts, and dips to advisory findings and keeps structural validity blocking. That matches the settled policy that checks do not block a human save. The tests were updated to preserve valid-save behavior; this is not evidence that the private evaluator has been deleted.

## Findings and owner dependencies

1. **Readiness hold:** D09 private evaluation and callers remain live. Owner: Viewing/Composition, after public evaluator source join, capability proof, and the required pixel qualification.
2. **Honest-but-not-labeled unverified path:** CAS-only handling prevents false revision or verified-source claims, but no literal `UNCERTIFIED` output label exists. Owner: Viewing/product contract if that label is required.
3. **No native revision regression found:** saved native captures use the actual canonical inspection revision; candidate labels do not claim an actual committed candidate revision. Owner dependency: Runtime must continue to accept the exact saved/candidate closure and source authority contract.
4. **No public10 package regression found in the static scope:** artifact bytes, 77-member composition package, lockfile pins, export contract, readiness refusal behavior, host generators, and custom-pack discovery are coherent. Actual imports and render behavior remain unverified because the required Remotion install was absent and installs/network/browser/full suites were prohibited.

Required follow-up dependencies are the exact current Runtime/client pair, a provisioned Node `20.19.4` / npm `10.8.2` project install, verified source admission, native capture frame/audio parity, and the public evaluator/source join needed before D09 deletion. This audit does not recommend deleting or weakening the current private paths.

## Tests and checks

All commands ran from `/home/user/work/wt/vw-m3-current-agent-public10-audit` with the shared Agent venv at `/home/user/work/venv-agent`; no dependency installation, network, browser, socket, or full-suite run was performed.

Targeted capture/D09/provenance lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= --basetemp=/tmp/vw-m3-public10-audit-pytest tests/sdk/test_capture_closure_source.py tests/sdk/test_timeline_capture_projection.py tests/sdk/test_visualize_authority_objects.py tests/sdk/test_scene_caller_preservation.py tests/sdk/test_coverage_empty_cut.py tests/sdk/test_timeline_reflow_golden.py tests/packs/rendering/test_fast_lane.py tests/packs/rendering/test_timeline_filmstrip_execution.py
```

Result: **117 passed, 9 skipped, 9 xfailed, 1 warning, 171.53s**. The warning is Pillow's `Image.Image.getdata` deprecation in `test_timeline_filmstrip_execution.py`.

Public10 readiness and alias pure lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= -m 'not integration' --basetemp=/tmp/vw-m3-public10-audit-public-pure tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_remotion_v3_aliases.py
```

Result: **9 passed, 2 deselected, 0.52s**. The two deselected cases require the absent Remotion install and were not converted into failures or skipped product behavior.

Host generator/custom-pack discovery lane:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -o addopts= --basetemp=/tmp/vw-m3-public10-audit-generator tests/packs/rendering/test_remotion_element_generation.py tests/packs/rendering/test_effect_registry_target.py tests/core/test_pack_coherence_elements.py
```

Result: **7 passed, 9.26s**.

Static check: `git diff --check b46140036e21948f1f807d8366b2e5d03e720697..HEAD` passed.

## Handoff conclusion

The current Agent tree is internally coherent for the reviewed public10 static/readiness and capture/provenance contracts, and preserves actual native M1 revision semantics. It is **not** evidence for D09 deletion, verified pixel/audio parity, full-source certification, or live Runtime equivalence. Keep the private evaluator/callers until the named owner dependencies are satisfied.
