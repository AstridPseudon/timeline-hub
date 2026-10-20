# Runtime private 613 / 952 closed-intent artifact review

Decision: **APPROVE for Agent peer review/private pin only.** This review does not authorize public release, consumer pin, activation, or integration.

## Candidate identity

- Runtime commit: `95202c2b09e83aaae028287d6c59b773410141f3`
- Runtime tree: `d438d3e28a29ad80fa6b7c19c55e1b7a4485eae2`
- Frozen Agent source commit: `357230816c86da65d5f8cc92b10a3a90d29874e0`
- Frozen Agent source tree: `94692ec85167d5c606626c4ec678fe2a63ee0aa6`
- Source: `contract/schemas/edit-command.json` and Agent `astrid/core/timeline/schema/edit-command.schema.json`, byte-identical SHA-256 `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- Wire: `runtime_protocol/schemas/timeline-commit-bundle.json`, SHA-256 `4a0779db14b9bbd827e964a495367b465bab5c00ee0b5717b8ff27777010a858`
- Runtime contract/health schema digest: `sha256:ddf6396dc32bd54bfeed549a99034693eaed76478b45ad0b7242117f6b734d36`
- Artifact manifest version: `sha256:b397e5fdb9fc25502bbda9ad5011e82dd2d63330d5af373834d31e6761276e20`
- Package/release version: `0.2.14` (unchanged)

The source inventory is exactly 55 definitions, 29 operation clauses, and 12 v2-capable operations: `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `clip.move`, `occurrence.add-media`, `occurrence.swap-media`, `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`, and `clip.set`.

## Review findings

The 952 generator change is limited to recognizing `type: object` with `additionalProperties: false` as closed in nested-definition discovery, expression rendering, and Python TypedDict emission. It uses `schema.get("properties", {})` for empty closed objects. Truly open authored payloads remain open.

The generated closed-empty behavior is correct:

- Python emits `EditCommandVariant1Intent = TypedDict('EditCommandVariant1Intent', {})` for `clip.delete`.
- TypeScript emits the equivalent `{ [key: string]: never }` representation.
- Closed empty intents reject own keys; open authored JSON fields remain open.
- Representative closed fields remain typed, including Python `ClipMoveArgs.on: float`, `WordAnchor.source: str`, `AgentRead.path: str`, and the producer pin.

The Main receipt alias was not altered: `MutationReceipt.project_seq` remains Python `list[int]`; the TypeScript generated client retains the intentional bounded tuple. The parent-to-952 diff has no `MutationReceipt` or `project_seq` change.

Only the expected generated files, manifest, focused generator test, and focused TypeScript fixture changed. No source schema, wire bundle, release metadata, Main receipt, or unrelated runtime product files changed. `generate.py --check` and `artifact_manifest.py --check` both pass, so the generated outputs and manifest are reproducible rather than hand-edited.

The private-fix brief lists stale generated digest values (`0b816f...` and `9c8911...`). The checked-in 952 manifest and actual files agree on the authoritative current values:
`runtime_protocol/timeline_commit_types.py` and Python package DTO: `78a76f4f87afcfd23c43d43fcb56c3130a9759d357d19b6eec5ec32b18261044`; TypeScript DTO: `b9f2cb417d63e9656187a73647cc23bafcde523568928bf31c59178468c92e57). This documentation discrepancy is non-blocking.

## Commands and results

1. Corrected Python consumer probe materialized from `fe59f6a3`, with the exact Agent schema streamed from `git show`:

```
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-review-952-closed-intent-artifact/probes/python_reflection_probe.py /home/user/work/wt/rt-m2-review-952-closed-intent-artifact <(git -C /home/user/peteromallet/astrid-agent show 357230816c86da65d5f8cc92b10a3a90d29874e0:astrid/core/timeline/schema/edit-command.schema.json)
```

Result: **PASS**, all six checks; exit 0.

2. Corrected TypeScript consumer probe from `fe59f6a3`, with only candidate input paths updated to 952:

```
tsc --noEmit --strict --module NodeNext --moduleResolution NodeNext --target ES2022 /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-review-952-closed-intent-artifact/probes/typescript_consumer_probe.mts
```

Result: no missing-export or shape-widening diagnostics. It reports the expected `Type 'true' is not assignable to type 'never'` for the bad empty-intent key, plus `TS2578` because the inherited fixture places `@ts-expect-error` on the enclosing object line rather than the nested property line. This is scratch-fixture directive placement noise, not a product failure; the focused TypeScript generator tests pass.

3. `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check`: exit 0.

4. `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check`: exit 0; `contract/artifacts.json is current`.

5. `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_commit_type_generator.py tests/test_typescript_generator.py tests/test_artifact_manifest.py tests/test_command_schema_compatibility.py`: **147 passed** in 69.95s.

No full, native, socket, metadata-override, public-release, pin, or integration run was performed.

## Remaining action

Agent may use the tuple above for private peer review/pin. If desired, correct the stale digest prose and move the TypeScript fixture's `@ts-expect-error` immediately before the nested bad property in a future scratch-only probe repair; neither is an executable Runtime product blocker.

