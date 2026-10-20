# Runtime next ordinary official candidate

Status: `UNPUBLISHED` staging candidate for manager/peer release review. This is not release approval, a consumer pin, or publication.

## Frozen inputs

- Runtime producer: commit `7f6dd8920e1ceec41b137358df5e7fecc304888d`, tree `4cccb2d643194df7df95d624e89a6cd9f6f268fc`.
- Agent/Astrid final ordinary source: commit `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, content tree `c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`.
- Agent raw command schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Agent canonical schema: `sha256:63ac77b3c3e2c582f76ab4b2499be5011ea4836e8c92264b1938632b3bfacba7`.
- Schema inventory: 55 definitions, 29 operations. The supported registry is exactly:
  `clip.delete`, `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `timeline.inverse`, `timeline.restore`, `clip.move`, `clip.add`, `occurrence.add-media`, `occurrence.swap-media`, `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`, `track.create`, `clip.set`, `clip.trim`, `clip.split`, `occurrence.duplicate`, `occurrence.delete`, `producer.guard`, `timeline.assembled-target`, `clip.add-media`, `timeline.init`, `clip.anchor`, `occurrence.create`, `clip.swap-media`, `text-binding.set`.

## Candidate identity

- Staging contract version: `0.2.14`.
- Runtime schema digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Artifact version: `sha256:8023c665f0e32835cf06b793c6f5ffa0a278a7ca5aadbfe971d52d163d66c7a3`.
- Artifact count: 75.
- `contract/artifacts.json` SHA-256: `4ddecda4cd892339cc6f1caaebc2bf4ddde76e422077eae8f8c4d2f059f8146f`.
- Reproducible release patch SHA-256: `06ecdfcb17cc975f8bed9e3c62677bbcaa8873b5c5cb1e1d65dbf9ff3c1c719`.
- Patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/candidate-0.2.14.patch`.
- Candidate metadata: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/candidate-0.2.14/candidate-metadata.json`.

The patch applies cleanly to an archive of the exact Runtime commit. It contains the Agent schema, release version, generated Python and TypeScript clients, runtime protocol types, package metadata, and artifact manifests only (17 generated/contract files). No new DTO, port, endpoint, private carrier, or hand-edited public 0.2.13 fixture was introduced.

## Evidence

- Normal Python generation, TypeScript conformance generation, artifact-manifest generation, then Python generator `--check`, TypeScript generator `--check`, and artifact-manifest `--check`: all passed on the candidate.
- Candidate TypeScript client check, `PATH=/home/user/work/app/node_modules/.bin:$PATH npm test --prefix <candidate>/packages/typescript`: passed; build/API compile and 2 Node tests passed, 0 failed.
- Candidate nearest native new-cohort test:
  `ASTRID_RUNTIME_CHECKOUT=<candidate> PYTHONPATH=<agent-final-source>:<candidate> /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration <agent-final-source>/tests/editing_conformance/test_next_ordinary_union_runtime.py`
  Result: `2 passed in 6.13s`.
- Central Runtime current-tree commit integration:
  `request-test rt-m2-next-ordinary-official-prep commit-integration --files 'tests/test_timeline_commit_integration.py'`
  Result: `9 passed in 18.65s` on Runtime tree `4cccb2d...`.
- Central explicit-file Runtime targeted neighbours:
  `request-test rt-m2-next-ordinary-official-prep targeted --files 'tests/test_command_schema_compatibility.py tests/test_artifact_manifest.py tests/test_typescript_generator.py tests/test_timeline_commit_acceptance.py tests/test_timeline_commit_port.py tests/test_timeline_text_binding_clear.py tests/test_timeline_text_selection.py tests/test_timeline_text_legacy_custody.py'`
  Result: `299 passed, 1 deselected in 206.29s` on Runtime tree `4cccb2d...`.
- The same nine-commit test run directly against the private candidate produced `7 passed, 2 failed`; both failures were sandbox `PermissionError` while binding local sockets in the two restart/provider tests. The central current-tree nine-commit lane is the authoritative socket-capable result; no test was weakened or changed.

The assigned Runtime worktree remains clean at the exact current public source. Public 0.2.13 files and fixtures were not modified. No merge, pin, publication, or consumer replacement was performed.

## Review handoff

Manager/peer should review the frozen Agent ref/tree, candidate digests, and the reproducible patch before any consumer qualification or pin/publication. If approval is granted, use this exact candidate for the WC6/RT02/D04 coordinated consumer replacements; retain `0.2.14` as staging until formal publication.
