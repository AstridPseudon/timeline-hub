# Agent reciprocal review of Runtime private84fc counterpart

Date: 2026-10-21

## Decision

**APPROVE — bounded reciprocal Runtime source/artifact review only.**

This approves the exact unpublished Runtime `0.2.15` producer for the next
private workflow step. It does not claim a normal Agent pin, release,
activation, integration, rendering, native/outer/Speech execution, or any
public/current tuple.

## Exact identities

- Runtime producer commit/tree: `c3d26567ff6fe4e20a959476d40aff90ad23a0ca` /
  `f3ae49d38454ce73a9c91a954bb530b3ce51c122`.
- Immutable Runtime checkout: `/home/user/work/wt/rt-pin-c3d26567`, detached
  at the exact producer commit. Its parent is
  `83a982eb1185477e50817e10b8c61212c43c8e03` /
  `becc776a4f0c88ae2f4c8ba9350116a040d223c7`.
- Agent source commit/tree: `4d4535882f1e028805c3da178bf9a7fa53696da8` /
  `f18245ced9c231ddf8f6f2ee64405a84d3517921`.
- Agent source: `astrid/core/timeline/schema/edit-command.schema.json`.
- Raw Agent schema SHA-256:
  `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.

## Source and contract review

The Runtime packaged schema and the bundle resource are byte-identical to the
exact Agent source. The inventory is 59 definitions, 33 closed operation
clauses, 12 explicit v2 clauses, and 31 `*Args` definitions. The five exact
authorized floor reconstructions are preserved:

- voiceover: `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`
- groups: `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`
- project-data: `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`
- carrier: `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- ordinary: `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`

All 31 Args are top-level closed objects. Generated Python and TypeScript
roots export the complete set, including `ProjectDataWriteArgs`,
`MigrateGroupsArgs`, `OccurrenceMoveArgs`, and `OccurrenceResizeArgs`; the
Runtime closed-union tests reject unknown argument keys.

`occurrence.move` retains the Agent-owned semantics: either non-negative
integer authored `start_ms`, or the existing `on`/`track`/`child_track`
frame-quantized form, with mixed forms rejected. `occurrence.resize` requires
positive integer authored `duration_ms`. No padding leaf or guessed lane was
introduced; timing meaning remains delegated to the reviewed Agent source.

The producer manifest has exactly 76 artifacts, and an independent recompute
matched every declared hash. The tuple identities remain distinct:

- health/schema digest: `sha256:07c0668b2fb16226475429ec65637404c0b2e885e1b88e67f896e249089d6680`
- raw Runtime bundle: `sha256:bbbae375837456b267d9f0c7de89b962966da79a24abe7c4720301423b333bcb`
- artifact manifest version: `sha256:2df8ebf4fb17cae1b62e78a262b2b20b393770d045d0ef8748207ac7efacbfbb`

The package is `0.2.15`; the ordinary parent remains `0.2.14` with the
ordinary schema floor `6ba7b51e…`. No private392, normal95bd, older952/a0,
public013, or other sibling schema/artifact identity was substituted in the
reviewed producer identity surfaces.

The Runtime parent diff is limited to generated contract/client resources,
generator inputs, package/release metadata, the artifact manifest, and focused
contract tests. The current Main/RT08 materialization helper, commit port,
store, catalog, headless bootstrap/overwrite refusal, raw payload and managed
media/CAS checks, single-FD filesystem boundary, custody broker, and one-shot
producer checkpoint are unchanged from the producer parent. Direct source
inspection covered, in particular:

- `runtime_protocol/timeline_materialization.py:39-183`: read-only source and
  owner provenance join, authenticated closure/digests, exact item maps,
  duplicate-owner/raw-item refusal, and no write authority;
- `runtime_protocol/timeline_commit_port.py:387-455,757-875`: recaptured
  revision/shot/media/text/document inputs, sealed materialization bindings,
  managed selection identity, exact catalog/CAS fields, and project scope;
- `runtime_protocol/timeline_commit_store.py:117-218,230-260,620-850,888-920`:
  ledger-first exact retry, accepted-history verification, catalog-tail/head
  checks, destination/global-item occupancy, retained source identity, and
  transactional acceptance;
- `runtime_protocol/timeline_catalog.py:28-97` and
  `runtime_protocol/timeline_commit_producer_checkpoint.py:1-161`: catalog
  receipt/projection ancestry and one-shot producer-consumption/render-link
  identity;
- `runtime_protocol/dirfd.py` and `astrid_runtime/custody_broker.py`: retained
  descriptor/path and process-custody boundaries.

No changed Runtime product path bypasses these safeguards.

## Tests and exact results

Passed:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-private84fc-agent-schema tests/sdk/test_timeline_materialization_schema_union.py` — **22 passed**. This is the exact Agent floor reconstruction lane.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-private84fc-runtime-generator tests/test_timeline_commit_type_generator.py tests/test_typescript_generator.py tests/test_artifact_manifest.py tests/test_command_schema_compatibility.py` — **142 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-private84fc-runtime-public tests/test_timeline_current_union_contract.py tests/test_client_parity.py tests/test_client_release.py` — **73 passed**.
- In `/home/user/work/wt/rt-pin-c3d26567`: `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B generators/generate.py --check` — **passed**.
- In `/home/user/work/wt/rt-pin-c3d26567`: `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B scripts/artifact_manifest.py --check` — **passed** (`contract/artifacts.json is current`).
- In `/home/user/work/wt/rt-pin-c3d26567`: TypeScript conformance generator `--check` — **passed**.
- In `/home/user/work/wt/rt-pin-c3d26567`: `git diff --check HEAD^ HEAD` — **passed**.
- A direct read-only identity probe — **passed** for Agent/Runtime schema bytes, all five floor hashes, 59/33/12/31 inventory, closed Args, Python/TypeScript roots, all 76 manifest entries, and the three distinct producer digests.

Known pre-existing Agent test lag, not introduced by this Runtime producer:

- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/agt-review-private84fc-agent-current tests/sdk/test_timeline_current_union_schema.py` — **32 passed, 2 failed** in 158.89s. Both failures are stale hard-coded expectations of 58 definitions/32 clauses and the pre-`occurrence.resize` 32-operation cohort. `HEAD^` already contains the same 59/33 schema, while this review commit only changes reconstruction-test ordering. The exact current tuple is covered by the passing 22-test materialization/floor lane; the Agent owner should update these stale assertions before claiming a clean current Agent suite.

No full suite, live socket/browser suite, native/outer/Speech execution,
normal pin, release, activation, adoption, rendering, or integration was run
or claimed. No repository files were changed; only this orchestrator report,
the worker commit message, and the completion marker were produced.

