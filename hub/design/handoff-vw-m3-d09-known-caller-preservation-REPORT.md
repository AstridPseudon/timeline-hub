# D09 bounded SDK caller preservation — UNAPPLIED

**Proposal complete; application HELD for Agent review and the source prerequisite below.** Base is current Agent `tl/integration`, `4a75f68f32049a69fd86135c645fa64c51175c14`; integration still had that head at final inspection. Repository status is empty. Everything written is in this worker's ORCH directory. No old branch was applied, checked out or merged.

Read PLAN, completed `vw-m3-d09-current-deletion-unit/ORCHREPORT.md` and proposal, and `vw-m3-strict-gap-contract-map/ORCHREPORT.md`. PLAN's advisory checks, retained pixel lane, and approved element clip-look/DIP difference are settled.

## Concrete bounded change

`proposal.patch` applies directly to current Agent: **2 files, +106/-4** (`FILELIST.md`). A **13-line private `_scene_problems(spans)`** calls the existing `picture_gaps`, `empty_cuts`, and `dips` formatters and retains their messages and cut/address attribution. `check()` puts those lines in `problems`, separate from structural `blocking`, as PLAN requires. Only actual UNKNOWN/UNAVAILABLE/content-UNKNOWN spans get an additional status line and their findings. Known COVERED/CONTENT answers produce no refusal or unavailable label. The existing sustained/incidental EMPTY buckets, including the deliberate-hold waiver, remain intact and tested directly. There is no new public parameter, flag, source declaration, provider or DTO, and no copied timing, geometry or coverage calculation.

This is a **companion formatter/policy slice**, not a claim to delete onscreen.py independently. The current-base overlay still uses current `_on_screen()` except where a unit test supplies spans. Its existing private sprite implementation is untouched; the earlier deletion proposal separately replaces it. Do not land this slice alone and call D09 complete.

`donor-amendment.patch` is an **alternative composition aid** against the previous UNAPPLIED D09 proposal's `check.py` (+14/-13): insert the same helper and replace its generic span loop with that helper. It is not sequential with `proposal.patch`. Its tested `donor-overlay/` uses the prior proposal for other modules without applying it. **The donor's raw `check(render_props=..., frame_basis=...)` remains untrusted and is not an approved final source API.** Merely adding this amendment to that proposal still does not qualify default callers.

All existing methods other than `check()` are AST-identical in the current-base proposal, including the three formatters and `_sprite_problems`. All existing tests remain byte-for-byte untouched. No skip, xfail or refusal substitution was added. Five existing old-policy nodes would require Agent reconciliation before landing: the four invalidity/blocking assertions in `test_coverage_empty_cut.py` (background-only, deliberate hold's initial check, inset, translucent) and `test_a_picture_gap_blocks_publishing_and_says_what_is_left_on_screen`. They are not claimed green under the proposal. Diagnostic preservation is tested independently of PLAN's intentional advisory policy; no permission to weaken their legitimate rendering/diagnostic expectations is implied.

## Actual caller trace on current Agent

| Entry / implementation | What actually happens; smallest preservation seam |
| --- | --- |
| `sdk/timeline/check.py:521` `check()` | `resolve()` mutates derived authored values before `document()`/validation; `_on_screen()` builds a config from current checkout clips and calls private coverage. No trusted Root props are retained here. Query must be prepared for the exact **post-resolve** document, not a pre-edit head or supplied revision label. Replace the evaluation source, then retain these formatters. |
| `sdk/timeline/transaction.py:147,169`, `publish.py:37`, `timeline_duplicate.py:152,175`; `packs/timeline/cli_common.py:215`, `cli.py:2909,3274,3540`, `cli_visualize.py:76` | All call `check()` without render props. Defaulting them all to UNAVAILABLE loses previously known diagnostics. Save/transaction/duplicate structural work must remain renderer-independent. Resolve scene input at the Agent's read/check/preview boundary when available; report unavailable separately if it actually cannot be prepared. No per-caller fake empty assets or new caller flag. |
| `sdk/timeline/reflow.py:149,349,809` and `:1012` `_doomed_cuts` | Reflow/retime/resolve do authored timing, not rendering. `_doomed_cuts` uses declared picture/background **roles** to decide anchor survival; it is not a scene query. Keep the earlier proposal's role relocation only. Do not require a renderer during reflow or copy the timing compiler. |
| `sdk/timeline/check.py:459` `verify()` | Builds footer with default `check().brief()`, then enters `fast_lane.verify`. The footer is computed **before** capture preparation. The trusted-source adapter must join it to the same candidate/source, rather than interpreting any later head as the check source. |
| `timeline_visualize/fast_lane.py:722` `_labelled_tiles`; `filmstrip_cards.py:1668` `attach_frame_addresses`, `:1684` `_contact_overlay_for_layers`; `layers/builtin.py:505` strip | They pass config/fps/canvas only to label functions. Their snapshots can retain registry/authority but do not thereby contain the final materialized assets and runtime theme. Forward the host-prepared source and reuse its rows for labels, rather than issuing a query with default inputs. Preserve exact selected frame numbers. |
| `timeline_visualize/composed_frame.py:286,385,516`; `renderers/remotion/run.py:1369` `capture_remotion_frames` | Existing capture batch delegates to `_execute_remotion_locked`; returns frame paths, not prepared scene/source rows. Keep this capture owner and pixel comparison path. Do not add another provider. |
| `renderers/remotion/run.py:1100–1115` | This existing trusted host computes `materializer.resolved_registry(asset_server)`, `_resolved_theme_for_render`, `_serialize_timeline` and `merged_props`. This is the actual resolved asset/theme join. The materialization lifetime matters; raw snapshot registry is not the selected URL registry. |

## Exact trusted-source API prerequisite — absent, not invented

There is **no existing SDK function on this base** that takes the exact post-resolve Checkout candidate and delivers a fully verified, prepared scene to its diagnostics. `ManagedRenderSnapshot` has config/registry/graph/authority but **no resolved theme member**. The source09 public Python `host_frames_at(props, basis, frames)` is an evaluation transport with shape checks, not source verification. Current `capture_remotion_frames(...) -> dict[int, Path]` exposes neither exact Root props nor scene rows. A revision string and matching fps do not close this gap.

Agent must extend the **existing Agent source/capture preparation boundary**, under its ownership, before caller activation. Required behavior (not a proposed new API name/schema):

1. Freeze the post-resolve document with existing `preview_authoring_candidate(candidate)` and retain its candidate/publication digests and `identity_mapping`. For a candidate, use the existing `candidate_preview_snapshot(preview, snapshot=..., client=...)` validation: exact base/project/timeline and dependency pins. For accepted/historical source, retain that exact immutable revision/closure. `resolve_managed_render_snapshot` reads the active head; it must not silently substitute that head for a historical selector or a changed checkout. `candidate_projection` alone is not the complete validation/materialization path.
2. Reuse **`project_runtime_parent_composition(parent, shot_revisions=..., internal_timeline_revisions=...)`**, including its occurrence outputs and immutable closure. No second projector. `timeline_restructure.renderer_input` is a normalized comparison view that strips identities and manufactures comparison revision labels; it is unsuitable for this join.
3. Keep exact projected IDs and selected asset keys. The projector emits `occurrence_id:source_clip_id` and namespaces internal assets. Map findings back using existing `app.astrid_shot_composition.{occurrence_id,source_clip_id,shot_revision_id,internal_timeline_revision_id}`, candidate `identity_mapping` and the source closure. Do not strip colon prefixes or join by asset alias/address alone. The donor sprite lookup compares `layer.clipId == checkout.clip.id`; without this join, projected known rows can silently lose OFFCANVAS findings. A different occurrence of the same child must remain distinct.
4. At the existing host materialization lifetime, retain exactly `merged_props.timeline/assets/theme`, generated element maps, and the actual fps rational/canvas/frame basis used by that source. Forward these to the earlier proposal's **same** `scene_answers.host_frames_at` -> `native-scene.mjs` -> public `prepareCompositionScene`/`querySceneFrames`. Keep native outgoing/default transition interpretation; any canonical incoming carrier needs the separately approved source binding. No empty registry, builtin-theme guess, caller config certification or metadata-only trust check.
5. Query once for the required frame set, retain exact returned rows. Feed rows to existing `spans_from_frames` and the retained formatters on the **matching frozen checkout**, and to `labels_from_frames` for the same captured frames. Do not format historical rows using a subsequently edited checkout's cut table/addresses. A new edit invalidates the join; a captured historical source stays historical. The source must retain enough full-frame answers for whole-clip OFFCANVAS assertions; a sparse capture is not proof that a sprite is never visible.
6. Structurally valid saves remain possible with rendering stopped. Distinguish inability to prepare/query the source (UNAVAILABLE), evaluated unknown internals (UNKNOWN with exact findings), and a known empty scene (GAP/EMPTY, a real answer). Known supported scenes must retain known answers through this adapter, not become unavailable or xfail.

This prerequisite deliberately does **not** define a new certification format or provider. The existing PLAN optional semantic-provider/source-validation work stays with its owner. No working-copy/historical trust claim or new DTO is made here.

## Evidence and named historical cases

- **46 PASS on unchanged current main-suite files**, including `test_a_cut_left_with_only_a_background_plate_is_not_valid`, `test_a_deliberate_hold_waives_an_empty_cut`, `test_a_declared_fade_in_is_a_dip_not_a_gap`, `test_a_picture_gap_blocks_publishing_and_says_what_is_left_on_screen`, `test_check_flags_offcanvas_mixed_scale_and_damaged_sprite_by_address`, and the original label/frame-index/display-copy expectations. This preserves the baseline; it does **not** certify those scenes under the public package.
- **16 PASS current-base overlay**; **16 PASS amended-deletion overlay**. Eight formatter cases reuse current historical fixture constructors, retaining c02 4–8s EMPTY and hold buckets, c2 4–6s GAP with `c2.live`, c02 0.50s DIP, known CONTENT, explicit UNKNOWN/UNAVAILABLE, and structural-invalidity separation. Eight transport/label cases exercise prior proposed adapters: exact request body with occurrence/asset/theme/opaque identities and rational-derived fps, ordered duplicate frames, three mismatched-frame responses, known label address/bounds/opacity, reuse without a second query, and genuinely missing inputs versus known-empty answers.
- These overlay inputs are **explicit span/IPC doubles**. They do not prove source certification, glyph alpha, actual AM drawing, selected media, transitions, or package/pixel parity. Source-looking metadata in a transport test is explicitly `test-only`; no doubles are called real. The known-label test does not exercise existing config-only callers end to end.
- **Static audit PASS**: strict patch applies to exact current base, existing formatter AST preserved, all proposed Python parses, no new skip/xfail; new test lint clean, zero new product lint findings. Product retains **5 inherited findings (2 I001, 3 BLE001)**; scoped lint itself exits1. `lint-delta.json` records the comparison.
- First donor-overlay attempt had **9 failures/7 passes**, all because the test `_on_screen` lambda did not accept donor arguments. The harness now accepts both signatures, with all behavior assertions unchanged. Initial failure log retained; final runs above pass.

Exact commands, from this worktree:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-known-caller-preservation
P=/home/user/work/venv-agent/bin/python
python3 "$W/check.py" "$P" -m pytest -q -p no:cacheprovider -o addopts= \
  tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py \
  tests/sdk/test_coverage_empty_cut.py tests/sdk/test_timeline_reflow_golden.py \
  tests/sdk/test_timeline_checkout.py::test_check_flags_offcanvas_mixed_scale_and_damaged_sprite_by_address \
  tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py
# 46 passed in 1.39s, exit0; baseline-targeted.log
python3 "$W/check.py" "$P" "$W/run_prototype.py"
# 16 passed in 0.55s, exit0; prototype-current.log
python3 "$W/check.py" "$P" "$W/run_prototype.py" --donor-overlay
# 16 passed in 0.54s, exit0; prototype-donor.log
python3 "$W/check.py" "$P" "$W/audit.py"
# PASS, exit0; audit.log
python3 "$W/check.py" "$P" -m ruff check --config pyproject.toml --output-format json \
  "$W/proposed/astrid/sdk/timeline/check.py" "$W/proposed/tests/sdk/test_scene_caller_preservation.py"
# exit1: 5 inherited product diagnostics, zero new; ruff-proposed.json
 git apply --check --whitespace=error-all "$W/proposal.patch"
 git status --porcelain
# exit0; status empty
```

QUIET was checked through `check.py` immediately before test/lint/audit CPU commands. Absolute `orch/managers/viewing/QUIET.md` was absent; GlobalQUIET was the completed App install notice. No capture grant/ACK was fabricated. No install, Node build, browser, socket/service or full suite was run/requested. No build output/cache was written to the worktree.

## Acceptance after Agent review — not executed

1. Select **one** reviewed current-base D09 unit including this formatter, trusted-source join and exact source capabilities. Do not merge broad09/2a, do not apply both alternative patches. Retain all M1 changes and the pixel lane. Existing originals stay present; no blanket xfail/refusal rewrite for legitimate known cases.
2. Re-run the baseline command above and the new `tests/sdk/test_scene_caller_preservation.py` in the owner-approved landing worktree, resolving PLAN's advisory-policy assertions explicitly with Agent ownership. Run direct query/host files on the actual package, plus unchanged legitimate original expectations: background/hold, fade, c2 Live overlay, sprite source/frame/asset IDs, real incoming-transition COVERED, independent-fade intended DIP. Public10/native8 compatibility and source identity are prerequisites; this worker made no package selection change.
3. For browser/socket/render-dependent acceptance, the registered landing worker must use the central service. This exact template requires its real registered name (not this unapplied tree), and must run only after all reviewed edits are finished:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
: "${ACCEPTANCE_WORKER:?set the registered Agent landing worker name}"
R=$("$ORCH/bin/request-test" "$ACCEPTANCE_WORKER" targeted --files \
  "tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_deletion_check.py tests/packs/rendering/test_scene_deletion_query.py tests/packs/rendering/test_scene_deletion_host.py tests/core/timeline/test_onscreen.py tests/core/timeline/test_onscreen_more.py tests/sdk/test_coverage_empty_cut.py tests/sdk/test_timeline_reflow_golden.py tests/sdk/test_timeline_checkout.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_timeline_visualize_labels.py") && "$ORCH/bin/wait-test" "$R"
# On exit124 wait again for the same R; never resubmit.
```

Do not run this against the current unapplied tree: added files/source prerequisites are absent. A selected later paired source/pixel gate needs its own exact tuple and authorized central brief. MAIN0.0.6 versus intended unified element clip look, actual owner films, frame/audio parity and the 15 strict-gap retirement requirements remain unverified here. Sparse membership-preserving spans may still fragment old summary windows; no class-only coalescer was added. **No complete D09/M3 or production source-positive claim.**
