# APPROVE — bounded inactive capture-label seam

Reviewed Agent `630c9d0a9be66cf4969b857eeb97930ab8a14f79` against recorded base `86d7cf9b1fcaab7afb7a2e1ba66f57ef84935e31`: the entire diff is three files, 351 additions / 5 deletions (118 added product lines, 233 test lines). Read PLAN, original `vw-m3-live-scene-join-r2/brief.md`, flat join-r2 REPORT, actual transport/Root/public preparation, source projector, filmstrip owner boundary, and approved callback `18ec2b573` with `git show`. No product or repository documentation changes made.

**Verdict: APPROVE landing this explicitly inactive prerequisite. No blocking implementation defect found. Production activation remains unimplemented and is not approved by this review.** No D09 deletion, live source certification, rendered pixels/audio, or M3 completion is established. This follows the original brief's express permission to supply a bounded pure seam when Agent-owned facts are absent; no settled decision was changed.

- `composed_frame.py:29-102`: one-shot observation, detached props/basis/address map and public answers; source/frame checks; answers withheld until the entire observed fresh batch succeeds. Repeated observation or failed retention clears facts. No persisted scene cache or cache/head fallback was added. `retain()` checks keys and file existence, not provenance or PNG validity: only the owner can attest that the result is this fresh successful batch. This limitation is documented and acceptable for the internal inactive seam, not an admission mechanism.
- Actual path is `host_frames_at` → selected-host `scene-query.mjs` → in-memory `native-scene.mjs`/`prepareHostScene` → public `prepareCompositionScene` → `prepareScene`/`querySceneFrame`. Host generated maps and normal aliases are used. Public12 archive SHA256 is `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`. Test runtime-status admission is replaced; preparation/evaluation are real public12, without a stub component. This proves public API compatibility, not installed production runtime/source admission. The reviewed tree itself still pins public10; public12 production adoption remains a separate owner prerequisite.
- Exact frames pass unchanged to the single batch host query. The adapter checks answer frame/canvas/clip IDs. Addresses are owner-supplied exact compiled-ID mappings; no colon split, current-head substitution, private visibility/coverage evaluation or invented clock appears in the diff. Native host rejects Root RenderClockTail. The source string and props equality cannot establish revision/candidate/projector identity; the current report correctly keeps that join held.
- `overlays/labels.py:27-39,69-114`: public rows determine visibility, opacity, geometry and painter order; only rectangle conversion and existing 5% display threshold remain local. Unknown bounds/opacity/visibility stay explicit in the legend. `frame()` preserves coverage/content/findings, including a returned `EMPTY`, without reinterpretation. An empty layer list is still a valid answer; an uncaptured/mismatched/failed query raises unavailable. A no-layer `GAP` has `content=None`, not `EMPTY`. The 53-test lane does not independently demonstrate a public12 `COVERED/EMPTY` scene; preservation of that value is by inspection, not claimed as a new host qualification.
- With no explicit capture, old `labels_for`/`addresses_at`, default motion/contact/index/verify and known box/legend behavior remain. With explicit capture, failure propagates rather than silently showing old facts. Mouth crop/statistics, selected-key denominator, `_timing_evaluators`, pixel verification and renderer-independent saves are untouched. The unchanged neighboring tests reproduce these fallback paths.

## Exact Agent-owner handoff

Existing approved host callback signature (not present in this branch's `run.py` yet):

```python
on_scene_props: Callable[[Mapping[str, Any], Sequence[int]], None] | None
```

Existing seam signatures to wire, without a new DTO, endpoint, projector or source factory:

```python
CaptureSceneLabels(*, source_identity: str, props: Mapping[str, Any],
                   basis: Mapping[str, Any], addresses: Mapping[str, str])
observe(props: Mapping[str, Any], frames: Sequence[int]) -> None
retain(produced: Mapping[int, Path]) -> None
frame(frame: int, *, source_identity: str) -> dict[str, Any]
overlay_labels_frame(image, config, frame, fps, *, capture=None, source_identity="")
```

1. Agent owns `astrid/sdk/timeline_filmstrip.py::prepare_filmstrip` and the admitted retained revision/working candidate + closure. Carry its existing projection and exact per-occurrence source-clip/address correspondence into `actions/timeline_visualize/filmstrip_execution.py`'s `RemotionFrameProvider` handoff (~1771). The projector already retains `app.astrid_shot_composition` occurrence/source IDs; use those verified facts, never parse its colon-composed ID. Include the mapping for every projected clip (the seam requires exact ID-set equality, including nonvisual clips). Existing capture_identity alone does not prove the final staged props, resolved theme or canonical frame basis.
2. From the same immutable materialized inputs obtain existing `_canonical_profile(timeline_path, _load_registry_mapping(assets_path), theme_path)`. Retain `fps_rational`, width and height. Supply `basis={"fps": numerator / denominator, "width": width, "height": height}` only at the public numeric API boundary. Match actual Root whole-canvas selection/defaults; neither merged theme canvas, snapshot's provisional fps nor thumbnail resolution establishes that basis.
3. Land approved callback `18ec2b573` and the coordinated public12 host adoption through their owners. In the synchronous final-props callback, while staged assets live, Agent must validate final serialized Root timeline, materialized assets and resolved theme against that same retained source/projector mapping/basis. Only after that validation construct the adapter with `props=final_props`, then call `capture.observe(final_props, actual_frames)`. Callback receives the actual sorted/unique fresh frame tuple, not planned metadata frames. Constructing from the callback is allowed; constructing from unvalidated arbitrary props is not source certification.
4. Thread this callback through both actual `_PersistentRemotionRenderer.__call__` and `_SharedRemotionOwner.render` capture calls. Each invocation owns a new adapter; do not store/reuse it on the warm shared session. After `capture_remotion_frames` succeeds, retain only its entire fresh `dict[int, Path]`, before those temporary files are removed. Expose it only after provider copying succeeds; discard on any capture/copy error. Provider cache-only cards get no new facts; a mixed batch can use facts only for its freshly observed frames, with cached cards retaining their old fallback. Never pass the combined cached/fresh map to `retain()`.
5. Pass that same successful adapter and source identity to the explicit overlay call for those fresh frames. No second query, metadata-only frame query or recomputation of addresses is required. Future scene-query failure policy must remain explicit; current callback exceptions abort capture, and this seam does not silently recover with stale facts.

## Minimality and deletion recommendation

Livable: ~118 added product lines for one capture lifetime and one consumer; no certification framework, receipt ledger, source DTO or speculative general adapter. Retain the one-shot/retention invalidation and detached inputs; they serve real failure modes. No deletion is required to land this seam. Keep legacy math until its actual consumers are qualified, then delete those replaced paths as D09 requires. Do not duplicate this seam for contact/motion/index/mouth or expand inactive infrastructure. A small optional follow-up is sharing duplicated host fixture provisioning with `test_scene_host.py` when public12 adoption lands; do not add another test-host abstraction just for this review. If the owner elects not to activate this seam, delete the class/new formatter/optional overlay branch and its dedicated test file together instead of retaining permanently dead machinery. No such scope decision or deletion was made here.

## Verification

Cwd `/home/user/work/wt/vw-m3-live-scene-seam-review`. Exact suite/lint commands:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules ASTRID_TEST_COMPOSITION_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --tb=short tests/packs/rendering/test_capture_scene_labels.py tests/packs/rendering/test_timeline_visualize_labels.py tests/packs/rendering/test_labels_overlay.py tests/packs/rendering/test_composed_frame_capture.py
# Exit 0: 53 passed in 7.77s (20 seam cases + 33 unchanged neighbors).
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,I,BLE astrid/packs/rendering/actions/timeline_visualize/overlays/labels.py tests/packs/rendering/test_capture_scene_labels.py
# Exit 0: All checks passed.
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache --isolated --select E4,E7,E9,F,BLE astrid/packs/rendering/actions/timeline_visualize/composed_frame.py
# Exit 0: All checks passed. Import sorting of this pre-existing file was not claimed.
git diff --check 86d7cf9b1 HEAD
# Exit 0.
```

Independent supplemental probe command below exited 0 with three PASS groups: actual public12 two-track painter order, detached basis/map and rational-fps half-open boundary (29 active / 30 absent); failed retention invalidates previously retained facts; real host refuses private Root clock. These are ad hoc pure probes, not new suite cases. Synthetic completion PNGs establish lifecycle only, never captured pixels.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_NODE_EXECUTABLE=/tmp/vw-m3-agent-gate-node20.19.4/bin/node ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules ASTRID_TEST_COMPOSITION_ARTIFACT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz /home/user/work/venv-agent/bin/python - <<'PY'
import copy
import runpy
import tempfile
from pathlib import Path
import pytest

m = runpy.run_path('tests/packs/rendering/test_capture_scene_labels.py')
Capture = m['CaptureSceneLabels']
Unavailable = m['scene_answers'].SceneQueryUnavailable
with tempfile.TemporaryDirectory(prefix='seam-review-', dir='/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-live-scene-seam-review') as temporary:
    root = Path(temporary)
    class Factory:
        def mktemp(self, name):
            path = root / name
            path.mkdir()
            return path
    host = m['host'].__wrapped__(Factory())
    with pytest.MonkeyPatch.context() as mp:
        m['native'].__wrapped__(host, mp)
        p = m['props']()
        p['timeline']['tracks'].append({'id': 'plate', 'kind': 'visual'})
        lower = copy.deepcopy(p['timeline']['clips'][0])
        lower.update(id='another:opaque:id', track='plate')
        p['timeline']['clips'].append(lower)
        addresses = {**m['ADDRESSES'], lower['id']: 'c09.lower'}
        basis = copy.deepcopy(m['BASIS'])
        capture = Capture(source_identity=m['SOURCE'], props=p, basis=basis, addresses=addresses)
        basis['width'] = 999
        addresses[lower['id']] = 'mutated'
        capture.observe(p, (29, 30))
        m['retain'](capture, root, (29, 30))
        answer = capture.frame(29, source_identity=m['SOURCE'])
        assert answer['width'] == 200 and len(answer['layers']) == 2
        labels, _ = capture.labels(29, source_identity=m['SOURCE'])
        assert [label.address for label in labels] == ['c08.title', 'c09.lower']
        assert [label.z for label in labels] == [0, 1]
        ended = capture.frame(30, source_identity=m['SOURCE'])
        assert ended['layers'] == [] and ended['coverage'] == 'GAP' and ended['content'] is None
        assert answer['coverage'] == 'UNKNOWN'
        print('PASS: real public12 two-track painter order, detached basis/address map, rational-fps half-open boundary (29 active, 30 absent), UNKNOWN versus GAP')
        try:
            capture.retain({})
        except Unavailable:
            pass
        else:
            raise AssertionError('failed repeated retention accepted')
        try:
            capture.frame(29, source_identity=m['SOURCE'])
        except Unavailable:
            pass
        else:
            raise AssertionError('stale answers survived failed retention')
        print('PASS: failed retention invalidates previously retained answers')
        clock = m['props']()
        clock['timeline']['app'] = {'astrid_render_clock': {'render_duration_frames': 60}}
        blocked = m['adapter'](clock)
        try:
            blocked.observe(clock, (0,))
        except Unavailable as error:
            assert 'RenderClockTail' in str(error)
        else:
            raise AssertionError('private clock accepted')
        print('PASS: private Root clock refuses through real public host')
PY
```

No browser, renderer, socket, install, network, full suite or central full request ran. No tests changed/weakened/skipped; no git mutation. Review is complete, not blocked. Next: Agent owns the exact source/callback/fresh-result wiring above, followed by its explicitly authorized central live qualification.
