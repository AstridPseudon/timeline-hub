# Runtime private392 current final-review tuple

**Status: PRIVATE HANDOFF ONLY.** This is an unpublished, test-only current
forward of the complete private392 Runtime candidate. It carries the exact
later current integration delta before reciprocal review. It does not authorize
a release, public pin, integration adoption, activation, or native qualification.

## Exact identity

- Required base: Runtime commit `f0268d2b817de8b2d9917a1395b272e5f4c8ddbb`,
  tree `c24c0a5c06bb83622a038ec99a30401ca68eca0f`.
- f026 parent/current base: `d1ea66bb749ce4f696fec440eb6dc0b5ad86bd87`,
  tree `3bf3ac159580cece24e3321ffc6c3a44b42bf67b`.
- Actual current integration: merge
  `a020a1c77a07aa657efb60b0442450209e55e470`, tree
  `9243cb9227d97515bf87a46bd694a7c72c520c04`, with only the announced
  test parent `5988a3b38293a82175052e84a2717ae5578b61dd` beyond `d1ea`.
- Forwarded candidate commit: **pending harness commit** (worker commits are
  prohibited); prospective final tree, computed from the resulting files, is
  `8be43e13acb436120f8a63b1a178d64c49422461`.

The exact forwarded file is
`tests/test_timeline_clip_replacement.py`, matching current `a020` blob
`3cb75e46b4ef2e35a0a566593bf93a0f0f7a92da`, and includes
`test_rt02_project_shot_crud_native_replacement_retries_after_restart` (39
added lines, exactly the `5988a3b` patch). No source, guard, schema, generator,
generated, artifact, or type file was copied.

## Generated identity from files

- Raw Agent command schema file:
  `contract/schemas/edit-command.json`, SHA-256
  `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`.
- Runtime bundle file:
  `runtime_protocol/schemas/timeline-commit-bundle.json`, SHA-256
  `fa7717e25c95126b18bb6f37b4c2d813d4a815456a06d438d52ef41c2cf1eab3`.
- Runtime health/schema digest from
  `packages/python/astrid_runtime_client/contract_metadata.py`:
  `sha256:242d2bc193bf16b699eb87592736769aacd8fdb75a1bb859dff3255d83ea5042`.
- Contract metadata remains `0.2.13`; no version bump was made.
- Artifact manifest version:
  `sha256:52df520b8384c70dc10d0b15bdce00e758c153019d26ddb9e141f5840885ba2d`;
  `contract/artifacts.json` file SHA-256
  `1c684f53582a44b12a7438b79ddeace8696768b4fb98f8f704d58a640fa6cd5f`.
- Generated inventory remains 56 definitions, 30 operations, and 12 explicit
  private v2 operation branches.

All 75 artifact paths exist, have their declared hashes, and are byte-identical
to f026. The Runtime product carrier files are also byte-identical to f026:

| Path | SHA-256 |
| --- | --- |
| `runtime_protocol/timeline_materialization.py` | `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb` |
| `runtime_protocol/timeline_commit_port.py` | `00ecf62412b3e1a1339794d8229e048521cebb6f26ca3eca24d6e0517a2f3767` |
| `runtime_protocol/timeline_commit_store.py` | `c06fdc3d4d1ee0e2f1cdc00a41f6c094fe4c7ffbc649810d7c289ea88954862a` |

Frozen private952, public013, and ordinary/a0 cohorts were not changed.

## Current-base and allowlist inventory

The complete candidate allowlist is the 23 f026-vs-d1ea paths plus the one
current-forward path, `tests/test_timeline_clip_replacement.py` (24 paths total):

```text
conformance/typescript/contract-metadata.ts
conformance/typescript/generated.ts
contract/artifacts.json
contract/schemas/edit-command.json
generators/agent-command-source.json
generators/generate.py
generators/python_client_init_template.py
packages/python/astrid_runtime_client/__init__.py
packages/python/astrid_runtime_client/contract_metadata.py
packages/python/astrid_runtime_client/generated.py
packages/python/astrid_runtime_client/timeline_commit_types.py
packages/typescript/src/contract-metadata.ts
packages/typescript/src/generated.ts
packages/typescript/src/timeline-commit-types.ts
runtime_protocol/contract_metadata.py
runtime_protocol/schemas/timeline-commit-bundle.json
runtime_protocol/timeline_commit_port.py
runtime_protocol/timeline_commit_store.py
runtime_protocol/timeline_commit_types.py
runtime_protocol/timeline_materialization.py
tests/test_timeline_clip_replacement.py
tests/test_timeline_commit_type_generator.py
tests/test_timeline_current_union_contract.py
tests/test_timeline_projection_occupancy.py
```

Read-only inventory results:

- Actual `a020` versus f026 outside this 24-path allowlist: **0 mismatches**.
- Working candidate versus f026 outside the allowlist: **0 mismatches**.
- Every current integration test function remains present: **0 missing**.
- The forwarded clip-replacement test file is byte-identical to actual `a020`.
- No old test was restored and the current-public-floor marker remains from
  f026; no private014 parent-marker conversion was performed.

## Required next gates

1. Independent Runtime review of this exact pending-harness candidate.
2. Reciprocal Agent review against the exact normal Agent private392 source pin.
3. Only after both reviews approve: prepare the matched private Agent pin and
   Runtime/Agent native392 pair.

No native392 run was performed here, and no unchanged 319/199/246/43 lanes,
full suite, release, pin, activation, or adoption operation was performed.
