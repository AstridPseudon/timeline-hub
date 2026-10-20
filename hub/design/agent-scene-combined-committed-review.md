# Independent review: combined committed Scene closure

Date: 2026-10-20 UTC

## Verdict

**APPROVE** `2b020eaef07a2ef138291bfea357d3924d5c7956` for the reviewed
committed Scene source closure. This is an integration/custody approval, not a
new audiovisual parity qualification.

## Identity and donor closure

- Target parent/meta base: `340a2d487627ff62db9eb04c2c00efcc08a89977`.
- Target tree: `d0a94dd460366e524c814f82481ce3387e1fdcba`.
- Central managed-proof service tree: `d0a94dd460366e524c814f82481ce3387e1fdcba`.
- `git diff --name-status` between the target tree and service tree is empty;
  all 3,096 tracked entries match exactly. Each of the 12 target-file blobs
  also matches the service tree, so there is no harmless delta to name.
- SDK blobs match the reviewed `4f5873d827c3f4db76725913cc6720d688a499b`
  donor exactly for `timeline_filmstrip.py`, `invocation.py`,
  `timeline/check.py`, and both SDK controls.
- Executor/query blobs match the reviewed
  `63aaf2549e1917931e59596c5a5c89dd4c2f93ba` donor exactly. The reviewed
  `daa0e634788d6be3071c73522361793c97332b59` donor is the equivalent earlier
  seam; the target intentionally uses the later 63a donor, so no unchanged
  daa code was re-reviewed.
- `generic_host.py` matches the approved `3acb818c3c61f4d9e67b96c21d2ea87840813865`
  proof delta exactly. The combined `pack.yaml` and managed proof test are the
  expected composition: one resource/env addition and the candidate import
  provenance preflight.

## Authority/custody findings

- The caller path is private (`_scene_only_request` / `_invoke_scene_only`),
  rejects caller authority/source/provider/store/endpoint keys, and obtains a
  saved or frozen-candidate closure through existing `prepare_filmstrip`.
  Runtime admission carries only the capture reference; it does not accept an
  inline caller snapshot or rendered-video substitute.
- Generic host source handoff remains host-owned. `scene_only.py` obtains the
  inherited verified source, validates the bound snapshot/config/compiled IDs,
  exact scene address map, capture digest, timeline identity, and snapshot
  extent before querying. Labels are produced by `snapshot_label(...,
  source=source)`, not copied from outer authority metadata.
- There is one public Scene projector/query path: `scene_answers.host_frames_at`
  through `_prepared_host_frames_at`; the Scene action only packages its
  answers and does not implement a second evaluator or visibility model.
- `ASTRID_PACKS_PATH` is forwarded in the rendering action environment, and
  `scene_only.py` is declared exactly once in the rendering pack resources.
- The SDK result parser reads the reviewed `filmstrip_bundle` managed row and
  artifact row, requires digest agreement and managed size, reads by the
  managed digest, verifies byte length and SHA-256, rejects unsafe/duplicate
  ZIP members, checks the nested manifest and every declared member hash, and
  requires the `scene-answers.json` entrypoint. It then requires managed
  provenance (`video_digest`, `timeline_id`), the verified snapshot label,
  exact compiled-address map, and the complete ordered frame extent before
  producing spans.
- Scene findings remain advisory. Missing/stale/forged output becomes an
  `UNAVAILABLE` span; it is never reinterpreted as physical parity, and
  `UNKNOWN` remains an advisory Scene answer. The new check formatter is not
  called from save/core validation.
- No public authority/DTO, Runtime route, provider, source factory, projector,
  or save-path Node dependency is introduced by this 12-file Agent commit.

## Evidence

Independent offline targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_only_executor.py tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_dispatch_contract.py
33 passed, 2 skipped in 2.17s
```

Additional read-only checks passed:

- `git diff --check` on the target commit.
- Python compilation of all changed Python source files.
- Exact target/service tree and all 12 target-file blob comparisons.
- Pack resource count: one `scene_only.py` entry and one
  `ASTRID_PACKS_PATH` entry.

The existing central managed saved/candidate evidence for service request
`agt-m3-scene-committed-closure-current-targeted-1020231803-4286` is `2 passed`
in `211.22s` on the exact matching service tree. I did not duplicate that live
Runtime/pack-host run or request a new matrix. The prior `2b6e5f0e2` proof
remains private-snapshot-only evidence and is not relabeled here. No full,
browser, socket, or physical pixel/audio parity suite was run in this review.

## Cleanup

No giant-file or pack metadata drift was found in the target closure. The
largest additions are the reviewed 393-line SDK caller and 334-line direct
control; no generated output, archive, node_modules, or large artifact entered
the tree.
