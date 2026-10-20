# Agent Scene committed-source closure

Date: 2026-10-20 UTC

## Disposition

The Scene-only source closure is complete on current `tl/integration` (`340a2d487`). The narrow candidate contains the reviewed SDK dispatch/caller, current executor/query adapter, resource declarations, direct controls, and the approved managed-proof delta. No new Main ABI, DTO, provider, source factory, projector, duplicate guard, or save-path Node dependency was introduced.

## Exact source closure

The port used these already-reviewed committed sources:

- SDK/private dispatch: `4f5873d82` (the reconciled `4f3cd32be` caller plus the private `_invoke_internal_result` continuation), covering `astrid/sdk/timeline_filmstrip.py`, `astrid/sdk/invocation.py`, `astrid/sdk/timeline/check.py`, and `tests/sdk/test_scene_caller_preservation.py`.
- Current executor join: `63aaf2549e1917931e59596c5a5c89dd4c2f93ba`, with the equivalent current Viewing donor `daa0e634788d6be3071c73522361793c97332b59` checked; the implementation/resource shape is the same. This supplies `astrid/core/timeline/scene_answers.py`, the `filmstrip_execution.py` admission seam, `actions/timeline_visualize/scene_only.py`, the Scene action resource, and `tests/packs/rendering/test_scene_only_executor.py`.
- Dispatch contract control: `4f5873d82`'s `tests/sdk/test_scene_dispatch_contract.py` (the later `3c77c939a` copy differs only by import ordering).
- Approved proof delta: `3acb818c3c61f4d9e67b96c21d2ea87840813865` for `astrid/core/execution/generic_host.py`, `astrid/packs/rendering/pack.yaml`, and the two-case `tests/integrations/test_d09_managed_scene_only.py`. The proof test additionally has a tiny candidate-source import preflight.

The rendering pack declares `scene_only.py` exactly once and forwards `ASTRID_PACKS_PATH`. The executor imports the SDK-admitted source through the existing managed path and reuses the prepared Root lifetime; it does not create another evaluator or source admission path.

## Candidate blob and import evidence

The central service snapshotted candidate tree `d0a94dd460366e524c814f82481ce3387e1fdcba` and ran the managed command `python -m pytest -q tests/integrations/test_d09_managed_scene_only.py`. The test passed both saved and frozen-candidate cases: `2 passed in 211.22s`.

The candidate blob IDs for the reviewed source files are:

```text
astrid/core/execution/generic_host.py                                      63b4b0806171895ee2ab401f8bb7e9cbf2caaae3
astrid/core/timeline/scene_answers.py                                      86d6503e167520782257e66242a73b14335ba619
astrid/packs/rendering/actions/timeline_visualize/filmstrip_execution.py   2a7ac2eda779b8af24d39e6fd2f3c0a73fd82589
astrid/packs/rendering/actions/timeline_visualize/scene_only.py            0a966eb36181fd2612912e63f2126a9a2221658e
astrid/packs/rendering/pack.yaml                                            dbfbf0757b0658570c64ee00ab3514e18eec0866
astrid/sdk/invocation.py                                                    4c38c8217663bd9ae543ce0ce250eee8ea8d2eca
astrid/sdk/timeline/check.py                                                cab0b27b327e8a493293dc960d7d47a1e2ee8415
astrid/sdk/timeline_filmstrip.py                                            b043823f4e9086e73c96424171c63b7f174bb76c
tests/sdk/test_scene_caller_preservation.py                                 ae4fff520023f982211b393ee930e481ead3c08b
tests/sdk/test_scene_dispatch_contract.py                                   f6b96c2e6d361933b64f6ae7728c6afa06d28b33
tests/packs/rendering/test_scene_only_executor.py                           1aa860d6cfc1b4142d3a901c4062d1c8bae4137d
tests/integrations/test_d09_managed_scene_only.py                           fde837eb92f170c3a10615a26ac3d2726de2e75d
```

The SDK, executor, query-adapter, and direct-control blobs match the reviewed donor blobs exactly. `generic_host.py` matches the approved `3acb818c3` blob. `pack.yaml` combines the executor resource declaration with the approved `ASTRID_PACKS_PATH` addition, so its combined blob is intentionally new. The integration-test blob includes only the candidate-tree preflight addition over the approved proof test.

The preflight checks the imported `timeline_filmstrip` SDK, `filmstrip_execution`, `scene_only`, `scene_answers`, `root_preparation`, and `verified_source` modules. All resolved under the candidate worktree, and the candidate root was present on `sys.path`; the test also sets `ASTRID_PACKS_PATH` to candidate pack directories. The managed fixture uses Runtime checkout `/home/user/work/runtime`, a private copy of the read-only public13 Remotion profile, pinned Node `v20.19.4`, and the installed timeline schema path. These are test inputs, not hidden Agent source imports.

## Old proof classification

The prior `2b6e5f0e20498489e1fe0e9046c68e3248474452`/`3acb818c3` service evidence remains valid only for that worker's private source snapshot: it proved real Runtime/`astrid-pack-host` saved and candidate cases plus the stale-client-binding control. It was not a proof of the then-current integration tree, because that tree lacked `test_scene_only_executor.py`, `test_scene_dispatch_contract.py`, and the surrounding Scene implementation. The previous report correctly stopped at that boundary; this work does not relabel it.

After the full source closure above, the one permitted current-source managed saved/candidate check passed. The earlier forged/incomplete callback controls remain offline controls, not live-host evidence.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/packs/rendering/test_scene_only_executor.py tests/sdk/test_scene_caller_preservation.py tests/sdk/test_scene_dispatch_contract.py` — `33 passed, 2 skipped`.
- Candidate source compilation for all changed Python files — passed.
- `git diff --check` and explicit new-file whitespace checks — passed.
- Central managed service request `agt-m3-scene-committed-closure-current-targeted-1020231803-4286` — `2 passed` saved/candidate, `211.22s`.
- No full, browser, or additional live suite was run.

