# Agent managed Scene authority review

Date: 2026-10-20 23:09 UTC

Candidate: `tl/agt-m3-scene-actual-managed-proof` at `2b6e5f0e2`.
Meta base: `a8a40afd37e5560a14fa5e1a09ace6018596793e`.

## Verdict: REQUEST CHANGES

The positive saved/candidate proof is genuine and the authority design is
otherwise sound, but this candidate should not be approved as the complete
review requested here.

Required corrections:

1. Remove the extra blank line at EOF from
   `tests/integrations/test_d09_managed_scene_only.py`. The candidate currently
   fails `git diff --check`:

   ```text
   tests/integrations/test_d09_managed_scene_only.py:291: new blank line at EOF.
   ```

2. Add one decisive real `astrid-pack-host` control for forged or incomplete
   Scene output, or narrow the proof claim to the positive saved/candidate and
   SDK-stale controls. The real two-case test does not substitute
   `_prepared_host_frames_at`, but it only proves the positive saved/candidate
   labels and managed bundle. The incomplete/malformed-result cases in
   `tests/packs/rendering/test_scene_only_executor.py` substitute that query
   callback, so they are not real-host evidence for the stronger
   forged/incomplete claim.

Do not rerun the unchanged live proof merely for this review. The existing
recorded evidence is sufficient for the positive path: central targeted
`2 passed`, and the recorded neighboring lane `79 passed, 2 skipped`.

## Review findings

- `GenericPackHost` retains the `PreparedTimelineInputs` object across command
  value binding and calls the existing `handoff_source` seam. The child gets
  the host-minted `ASTRID_VERIFIED_TIMELINE_SOURCE`; no caller source field is
  promoted to authority.
- The rendering action manifest forwards the already admitted
  `ASTRID_PACKS_PATH`. `scene_answers._query` forwards the same selector into
  the Node environment used by the admitted runtime.
- `scene_only.py` reads the existing inherited source, validates the captured
  snapshot, config IDs, exact address map, digest and timeline identity, then
  validates the source again after the prepared Root/Scene query. It publishes
  labels, map and receipt provenance only after the complete query succeeds.
  Failures produce the existing advisory unavailable document with empty
  answers/map.
- The SDK joins only the existing `filmstrip_bundle` and its `entrypoints.scene`
  `scene-answers.json`. It checks managed digest/size/ZIP membership, receipt
  provenance, candidate/base or committed labels, exact map, full frame extent,
  and layer IDs. Stale, forged, missing and incomplete payloads fail closed to
  `UNAVAILABLE` in the offline contract tests.
- No source factory, second projector, DTO, caller provenance toggle, save or
  publish transaction dependency was added. The new check adapter is explicit
  diagnostics-only; `_check_core` does not call it, and no Node/Scene import
  enters save-core.
- The new real integration assertion `spans[0].cls != "UNAVAILABLE"` is
  appropriate for the pinned public13 fixture: the real public Scene can
  return advisory `UNKNOWN` when bounds are undeclared. It does not weaken an
  existing strict assertion; the pre-existing tests were only appended to.

## Tests run or relied upon

Run directly in this worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_only_executor.py tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_dispatch_contract.py
33 passed, 2 skipped in 1.95s
```

Recorded branch evidence, not rerun because it is the unchanged live proof:

- the real Runtime/`astrid-pack-host` saved and candidate integration cases:
  `2 passed`;
- the neighboring source lane:
  `tests/packs/rendering/test_scene_only_executor.py tests/packs/rendering/test_verified_source.py tests/sdk/test_scene_dispatch_contract.py`
  — `79 passed, 2 skipped`.

`git diff --check` was run against the meta base and failed only for the new
blank line at EOF noted above. No full suite or duplicate live run was made.
