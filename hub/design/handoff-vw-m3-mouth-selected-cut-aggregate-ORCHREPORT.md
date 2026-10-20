Completed the bounded **UNAPPLIED** selected-cut regression/proposal on exact
source `54b9c1feeae01037fac64594824d2d3fd748a250`. Product capture, private math,
fallbacks, thresholds and repository files are unchanged. Application and the
production source join remain HELD; this is one explicit fixture qualification,
not D09 completion or a Gate 6 claim.

Read PLAN, D09 known-caller REPORT/ORCHREPORT, central `1020061231-9845` raw log
(1 passed in 13.05s, full guards passed), and flat retention MANAGER-PASS. Read
the raw archive itself: 10319 bytes, SHA256
`e7f32e40aa1aa25d81f30d05fd5ccb83a8a19cd8ce4a5a560e9fd93dc73d7c39`.
All six archive members equal the retained originals byte for byte. The
proposal contains unchanged originals of frames `[0,3,4,5]`, inspection JSON
and its hash manifest, plus provenance README and two test files. Frame 0 and
4 naturally have identical bytes; neither is a relabelled copy.

The regression calls real `sheet.select_cut` / `build_context` on the original
flat Root timeline. The selected cut is index 1, clip `presenter`, track
`overlay`, interval `[0,2)`, with empty occurrence/shot IDs exactly as recorded.
Selectors `1`, `presenter` and `@0` agree; `2` and `foreign:presenter` refuse.
No occurrence provenance was invented. The built-in pixel line has no embedded
cut ref: attribution is its actual `LayerContext.cut` (the sheet adds its
MOTION header). Both observed results retain that identical context reference;
sheet-page formatting was traced, not rendered here.

One actual public10 generated-host preparation uses the exact retained Root
props/theme/assets and basis, exact compiled ID and registered owner. The
unchanged `seriesInspection` validates the public DrawPlan/component zero,
makes one successful public ROI query and retains it for every original PNG.
Missing/ambiguous ID, foreign owner and stale params refuse before another ROI
query. The test-only public adapter reuses existing `png_crop`, `public_box`
and `_diff_fraction`; no mouth geometry, clock or new sample planner is copied.
The private side executes real `builtin.render_lipsync`, observing its real
comparator and frame reads. It does not replace `mouth_box`, attach public
motion as private math, or use semantic mouth state as pixel evidence.

| Verified original-capture result | Private == public ROI adapter |
| --- | --- |
| PNG crop / area | `(298,202,345,219)` / 799 pixels |
| Selected/read frames | `[0,3,4,5]` |
| Adjacent pairs | `0→3`, `3→4`, `4→5` |
| Changed pixel counts | `336,336,336` |
| Fractions | `336/799 = 0.42052565707133915`, each pair |
| Changes / selected-key denominator | `3 / 3` |
| Exact finding | `LIPSYNC pixels: mouth region changed between 3 of 3 sampled frame pairs` |

Negative controls preserve existing behavior. Unordered/duplicate frame
requests collapse to the same sorted dictionary keys. Removing key 3 leaves
`[0,4,5]`: comparisons `0→4` (0/799) and `4→5` (336/799), reporting **1 of 2**.
A present key whose image callback returns None resets adjacency, but its key
remains in the denominator: missing image 3 compares only `4→5`; missing image
4 compares only `0→3`; both report **1 of 3**. A nonexistent file raises
FileNotFoundError in both paths. This denominator behavior is recorded, not
changed. Window-only controls include the start and exclude the end: end=5/30
selects `[0,3,4]` (2/2), start=3/30 selects `[3,4,5]` (2/2); fewer than three
selected keys produce no aggregate or image reads. These are explicitly
synthetic selection windows over the same originals, not new authored cuts.
Memory-only planted copies retain `15/799 <= .02 < 16/799`; no planted file is
used as an actual captured frame. All originals remain byte-identical.

The earlier D09 caller report is stale **on this source** about an absent
capture callback. The concrete current trace is:

| Existing boundary | Current behavior / remaining join |
| --- | --- |
| `rendering/renderers/remotion/run.py:1100,1169,1372` | Materializes registry/theme/timeline; `on_scene_props(merged_props, frame_numbers)` runs while staging lives. Batch capture sorts/deduplicates requested numbers and refuses missing returned captures. This seam exists; do not invent a second capture/provider. |
| `timeline_visualize/composed_frame.py:576` | `_scene_labels` consumes actual Root props, queries capture frames plus reserved metadata frames, and retains scene rows and projected source/occurrence hints. It does not resolve a mouth component-zero selection or retain its ROI/owner for the series. |
| `filmstrip_cards.py:1788,1885` | Existing reservations are for composition checks/curves; scene rows and identity hints flow to context. They are not a mouth-zero source contract. |
| `composed_frame.py:630,696` | Per-batch rows reset; cached/mixed pixels can lack exact scene facts and are labelled unavailable. A sparse/missing row cannot silently supply mouth-zero geometry. |
| `layers/base.py:LayerContext`; `motion/sheet.py:build_context` | Frames, cut, config and scene-row maps are available; no prepared scene, exact live Root props or verified retained mouth-zero selection is supplied to lipsync. |
| `layers/builtin.py:475,532` | First presenter from sorted context elements; selected capture keys sorted and filtered to `[start,end)`; private component-zero `mouth_box`; at least 3 keys; unchanged luminance `>18` and fraction `>.02` comparator. |
| `motion/model.py:541`; `core/timeline/cuts.py:160,323` | Private crop/fallback untouched. Real picture-bed grouping is used; this fixture has one overlay-bed clip and no extra occurrence identity. |

**Specific join hold:** the callback can observe exact Root props, but the
current lipsync consumer cannot receive a verified, source/owner-matched,
component-zero ROI retained for its selected PNG series. Selected capture
rows alone do not guarantee that zero, especially on another cut, speed/preroll
or a cache hit. This prototype reconstructs the retained controlled fixture;
it does not exercise Runtime candidate/historical admission, live callback
custody, source closure or a production consumer replacement. No product
adapter/API is proposed or activated. After Agent review, reuse the existing
callback/prepared-host boundary and exact projected identity mapping; obtain
and retain zero there, then feed the existing context without a new sampler.
Do not default known supported scenes to unavailable. All default/partial/
fractional/raw-invalid public diagnostics remain KNOWN, with legacy statistic
equivalence unqualified. The unchanged 10-test crop-equivalence neighbor file
passes and retains those distinctions.

Exact final commands, cwd `/home/user/work/wt/vw-m3-mouth-selected-cut-aggregate`:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-mouth-selected-cut-aggregate
P=/home/user/work/venv-agent/bin/python
N=/tmp/vw-m3-agent-gate-node20.19.4/bin/node
python3 "$W/check.py" "$P" -m pytest -q -s -c pyproject.toml -o addopts= -p no:cacheprovider --tb=short "$W/proposed/tests/packs/rendering/test_presenter_selected_cut_aggregate.py" tests/packs/rendering/test_presenter_crop_equivalence.py
# 25 passed in 4.71s, exit0: 15 new proposal cases + 10 unchanged neighbors.
python3 "$W/check.py" "$P" -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE "$W/proposed/tests/packs/rendering/test_presenter_selected_cut_aggregate.py" "$W/check.py"
# All checks passed, exit0.
python3 "$W/check.py" "$N" --check "$W/proposed/tests/packs/rendering/presenter_selected_cut_query.mjs"
# exit0.
git apply --check --whitespace=error-all "$W/../../design/handoff-vw-m3-mouth-selected-cut-aggregate-proposal.patch"
git apply --numstat "$W/../../design/handoff-vw-m3-mouth-selected-cut-aggregate-proposal.patch"
git diff --check
git status --porcelain
# exit0; patch is nine added test/fixture files, no product files; status empty.
```

`targeted.log`, `lint.log`, `syntax.log` retain output. The wrapper verifies all
2933 source files, the complete current dependency graph (21495 entries),
original and staged fixture bytes, Node and public10 artifact pre/post. The
existing host fixture verifies all 77 artifact files and coherent resolved
React18.3.1/Remotion4.0.509 peer entrypoints/versions/hashes. Current graph size
is seven entries larger than central's historical 21488; historical full-graph
identity is not asserted. The six historical patched peer files were also
individually checked against the central controller's expected hashes. No
source/peer/artifact changes occurred during the offline commands.

First attempt: 2 passed / 13 setup errors, because Node's deep equality
distinguishes negative zero from the retained JSON's zero in pan_x/pan_y.
Corrected only the assertion to compare the capture's same JSON boundary;
geometry, pixels and threshold were unchanged. Initial log retained as
`prototype-first.log`; its empty scratch directory was removed. Final test
code has no new skip/xfail, refused-known expectation or modified original
suite. No browser, capture/renderStill, SSR render, live socket, full suite,
installation, network, central request, git mutation or push ran. Ordinary
PIL lip-sync panels were computed only in memory; no new captured images or
worktree build output were written.

Flat ORCH design handoff prefix:
`design/handoff-vw-m3-mouth-selected-cut-aggregate-`:
`ORCHREPORT.md`, `proposal.patch`, `exactcounts.json`, and two `fixture-*` code
copies. The patch includes the original PNG bytes, not download instructions.
It applies to clean source54b9. Review/apply the test-only patch in the selected
Agent landing source, then close the existing callback/context source join
under its owner before any consumer activation or private deletion. No full
or additional render is needed to review this bounded result. The assigned
worktree remains clean; no repository commit is needed for the ORCH proposal.
