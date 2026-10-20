# D09 current deletion unit — FOR AGENT REVIEW, UNAPPLIED

Prepared `proposal.patch` against **Agent `4a75f68f32049a69fd86135c645fa64c51175c14`**, still the integration head at final inspection. **Zero repository product/test/document writes. Task complete; landing HELD.** Manager + Agent owner review must precede an explicitly selected current-tuple paired gate. No automatic merge.

The proposal deletes the **452-line `astrid/core/timeline/onscreen.py`**, relocates only role/address declarations, and replaces its SDK/label consumers with public scene queries. **18 files, +1060/-573; 9 product files +642/-562 (net +80)**, including the deleted file. This removes duplicate math but is not a net product-size reduction yet. `FILELIST.md` is the one-screen complete review scope; `filelist.json` is machine-readable.

Source is **`09cfd10a44b17a24d6f77ef6b8f41cce9cd0db1e`**, descending through `7b8c4dc42493566b444f35de610bfca45ae4c797` and `f6fbe741a256e2756a1d686350f8a38e37c015ee`. Do not merge that source branch: its diff from current integration spans 67 files and would remove later M1 numeric/opaque/shared-inverse regressions. Static checks prove all **10 files changed by current M1 since f6fbe741** are outside this proposal. All existing test edits are **imports only**, with AST-identical assertions, fixtures and inputs. No new xfail/skip/refusal expectation was introduced.

Observed other integration heads at final inspection (moving independently; **not a tested paired tuple**): Runtime `fc6bb87b6b37f7bcd88b03cd53fda76d964fd9b1`, App `4e7c06a0e6e9920dbc2eceb20adc09ae2d70f053`, Composition `ff0536bb53d84db5008b859be304b932b1dd5252`. Bind the actual later gate to its own exact tuple.

## Extraction choices

- Keep source09 `scene_roles`, SDK `check`/reflow role migration, label adapter and native host preparation. Remove the unrelated occlusion IPC branch/functions from the proposed scene adapter/helper. No motion consumers, sampling framework, capture provider, source adoption, canonical compiler activation or film-wide reservation comes along.
- Include narrowly extracted direct query/host/check tests, with original names and assertions. The pure query fixture can use the **existing public10 archive** via `ASTRID_COMPOSITION_TEST_ARTIFACT`; default and native-host compatibility fixtures retain immutable native8. Missing required Node fails that new direct fixture instead of skipping it.
- Existing legacy tests receive only import relocations and the donor test adapter. **This is not sufficient to make them pass**: their exact source/assets/capabilities remain unresolved. The helper's builtin-theme/empty-assets inputs are test data, never source certification. Its boundary instrumentation is preserved rather than rewritten to expect refusal.
- Leave labels' existing display/capture callers untouched. Their exact frozen asset/theme forwarding is a separate coupled prerequisite; default unavailable labels cannot qualify their previous known-visibility behavior.
- Default SDK check remains renderer-free with lazy imports. Explicit supplied scene rows are advisory and separate from structural validity. UNKNOWN is retained rather than inferred opaque. Exact request payloads, frame order/duplicates and span membership/findings are retained.
- Native-file transitions retain the public preparer's **outgoing default**. No canonical-to-compiled helper is included or activated. A supplied `compiledTransitions` carrier needs the public root ABI and **verified source binding before production use**; donor structural validation does not establish provenance. This patch does not authorize unverified canonical-incoming activation.

No AM source (including presenter), source port `2a62`, semantic provider, candidate, Runtime authority, custody, Root, existing bundler configuration, registry, package/lock/artifact pin, generated file, vendor or generator mutation. The new `native-scene.mjs` is the donor query entry, reusing the existing host aliases and esbuild; it does not edit the bundler. Pixel verification/statistics, private pixel crop pending separate proof and `_timing_evaluators` remain intact.

## Which replacement tests qualify which removal

The **458 PASS** in stage4 are historical source09 evidence (224 public10 / 66 public9 / 168 native8), **not a pass on this extracted patch/current tuple**. The extracted real-package tests have not been run here.

| Named source09 test(s) | What the positive actually establishes; limit |
| --- | --- |
| `test_transition_frames_equal_canonical_public_query` (dip/dissolve × start/center/end); `test_cut_fractional_fps_and_empty_scene_are_answers` | Public evaluator boundaries, rational frame clock and half-open scene absence. Qualifies adapter transport/boundary replacement, not an AM film or source provenance. Included in `test_scene_deletion_query.py`. |
| `test_resolved_painter_order_and_compiled_payload_are_preserved` | Exact IDs, painter order, opaque fields, ordered/duplicate requests. Included; requires actual public-package gate. |
| `test_native_host_default_custom_alias_capability_and_immutable_props`; `test_native_host_uses_exact_assets_and_runtime_theme`; `test_native_host_resolves_custom_transition_defaults_and_boundaries`; `test_native_host_rational_frame_clock_is_half_open` | Registered draw-derived fixture capability, alias/default resolution, actual selected assets/theme, native outgoing clock and unchanged props. Included in `test_scene_deletion_host.py`; synthetic registered fields do not qualify real AM text/sprites/media alpha. |
| `test_large_native_batch_is_not_truncated`; `test_spans_from_frames_does_not_fill_unqueried_frames`; `test_spans_from_frames_merges_only_matching_adjacent_answers` | 300 returned public answers plus exact sparse/membership-preserving RLE. Included; replaces batch truncation/sweep concerns, not the old private Python boundary-call count requirement wholesale. |
| `test_actual_am_public_incoming_crossfade_stays_covered` | Required real-AM **supported incoming-transition** COVERED positive. Keep it in the later coupled gate. Its film differs from independent clip fades; it does not retire their requirement. Not imported here because the AM draw-shared declarations are a separate owned unit. |
| `test_actual_am_one_sided_fade_has_dip_frames_then_coverage` | Public per-frame DIP support for a real declared component. Does not solve the old class-summary split at frame0 or independent-fade MAIN comparison. Same separate AM prerequisite. |
| `test_default_check_reports_scene_unavailable_without_renderer_imports`; `test_sprite_scale_and_source_integrity_diagnostics_remain_renderer_free` | Safety/metadata retention only. Included in `test_scene_deletion_check.py`; neither missing renderer nor UNKNOWN is evidence of supported rendering. |

**No named test currently qualifies the entire 452-line deletion against this current tuple.** The map's old **15 strict gaps remain unresolved**; this patch imports none of their markers. Current passing expectations stay unchanged and can fail, including collection/execution on unprepared renderer inputs; no green claim is made. The map's SDK advisory test names differ from current main's blocking names: PLAN requires advisory scene checks, so Agent must explicitly reconcile that policy with legitimate diagnostics and hold behavior, without masking lost behavior.

## Dependencies before any landing grant

1. **Agent-owned exact source join:** forward the one existing projector's resolved Root props, selected assets/theme, immutable revision/occurrence identities and frame basis through the accepted source path. Current donor `check(render_props=...)` trusts caller data; its revision string is a label, not verification. No-argument SDK check has no scene and the old `picture_gaps()`/`empty_cuts()`/sprite diagnostics are not restored merely by returning UNAVAILABLE. SDK check's new generic span loop also bypasses the retained cut/hold formatter. Known source rows and deliberate-hold diagnostics need direct current-caller positives.
2. **Frozen label/capture forwarding:** current label callers supply config/fps without the exact resolved assets/theme. Query-only deletion would downgrade their prior labels. The captured-source/provider/candidate/Runtime-authority chain is separate, not permission to adopt `2a62` or the 67-file branch. Its legitimate source positive and individual forged/stale-source negatives must pass on the actual tuple before activation.
3. **Legitimate component support:** real flat-field plate support must share actual drawing; text glyph presence/alpha, sprite selected-asset stepped bounds, real transparent-background inset/media alpha and crop/animation geometry cannot be inferred from old x/y/scale or names. The strict-gap map identifies false private layout assertions as well as real missing support. AM changes are outside this grant. Existing presenter grant does not authorize touching other AM sources.
4. **Package dependency, separately coordinated:** this worker verified the existing public10 archive (`cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7`, 77 files); its public `./evaluation` exports prepare/query, and the public **root** exports `compileCanonicalTransitions`. Source09's host accepts no carrier under native8; explicit carriers require newer public ABI. **0.0.11's extra trim/rate exports are not needed by this D09 slice.** Its source is now integrated and archive available, but this worker did not qualify adoption. Reuse public10 for bundle #1; perform any 11 audio adoption separately. Keep native8 compatibility and reviewed paired pins outside this patch.
5. **MAIN0.0.6 / intended DIP proof:** PLAN's ~04:02 decision supersedes the older STATUS/map/correction report: element clip look is an **approved intended difference** from main, with independent fades DIP16–30. Do not relitigate it. Tag `v0.0.6` can reproduce the locked SHA512 via git archive/gzip, so the older 403/unverified-source statement is stale. Remaining blocker is **actual MAIN pixels versus unified pixels**, showing exactly the intended clip-look differences; preserve named incoming-COVERED positive and list affected owner films. No MAIN pixel result was produced here, and no golden was changed.

Then manager + Agent owner select **one** current-tuple paired unit. Run the extracted direct files on the reviewed source, the original onscreen/coverage/checkout/reflow/label neighbors with every legitimate behavior retained, and the source/paired dependency gates. Do not request a broad old-branch merge. Any browser/localhost/actual render work belongs to the central service under its own explicit brief and QUIET coordination, not this worker.

## Exact validation performed

Cwd throughout: `/home/user/work/wt/vw-m3-d09-current-deletion-unit`. Define:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-current-deletion-unit
P=/home/user/work/venv-agent/bin/python
N=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
python3 "$W/check.py" "$P" "$W/run_prototype.py"
python3 "$W/check.py" "$P" "$W/audit.py"
python3 "$W/check.py" "$N" --check "$W/proposed/remotion/scene-query.mjs"
python3 "$W/check.py" "$N" --check "$W/proposed/remotion/native-scene.mjs"
git apply --check --whitespace=error-all "$W/proposal.patch"
git status --porcelain
```

- **Prototype: 6 passed in 0.86s**, exit0 (`prototype.log`). Proposed modules are loaded over unchanged current source with an import hook. IPC tests use explicitly stubbed rows; no Node/render/media support is claimed. Covers opaque exact forwarding, ordered duplicate frames, labels' known bounds/UNKNOWN findings, declaration/address relocation, exact sparse spans, advisory validity separation, and a fresh-interpreter default SDK import fence.
- **Static audit: PASS**, exit0 (`audit.log`): patch applies to exact SHA with strict whitespace; all proposed Python parses; unchanged existing test AST except imports; no skip/xfail; 10 latest M1 files excluded; scoped Ruff **zero new diagnostics**. Nine inherited Ruff findings remain (six I001, three BLE001), detailed in `lint-delta.json`; do not call the whole scope lint-clean. Public10 identity/member count/public ABI read from the existing archive without extraction/install or graph changes.
- **Both Node syntax checks: PASS**, exit0; syntax only, no imports/preparation/query.
- **Working tree status empty**; no build output, test cache or temporary symlink in the repository. Proposal SHA256: `621fcf4966c6a87f100a93d5dfdeb481882e49079a7a927004c394a110edfe1d`.

Initial prototype run had 5 PASS/1 FAIL because its fresh child loaded current source instead of the proposed overlay. Corrected the harness to install the same overlay before the unchanged import-fence assertions; final six pass. Initial static checks caught extra EOF blanks (fixed) and an audit checking the root compiler symbol at the wrong evaluation entry (audit fixed). Logs retained; no behavior assertion weakened. The initial directory Ruff command matched no files; final audit explicitly checks every proposed Python file with repository rules and compares baseline diagnostics.

Absolute `orch/managers/viewing/QUIET.md` was checked before prototype/lint/audit/Node CPU commands by `check.py`; it remained absent. Its pause branch writes a fresh own `QUIET_ACK` and exits75 before launching CPU. No quiet capture grant or ACK was fabricated.

**Not run:** full/make check, old/real-package targeted suites, browser, socket/service, actual render/SSR, network, package build/install, MAIN pixels, frame/audio parity or owner-film review. No existing held 458 result was rerun or relabelled. Recommend completing the named dependency positives, then reviewing this small patch with Agent ownership before a single paired gate.
