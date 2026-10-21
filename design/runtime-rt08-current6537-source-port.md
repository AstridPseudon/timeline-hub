# RT08 current Runtime source port

Status: bounded private SOURCE result only. No generation, schema/artifact
production, version allocation, pin, publication, release, integration merge,
native claim, or consumer adoption.

## Base and reviewed donor

- Base: Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
- Materialization donor: Runtime `83a982eb1185477e50817e10b8c61212c43c8e03`,
  tree `becc776a4f0c88ae2f4c8ba9350116a040d223c7`.
- C3d authority: `c3d26567ff6fe4e20a959476d40aff90ad23a0ca`, tree
  `f3ae49d38454ce73a9c91a954bb530b3ce51c122`.
- Approved f8da lineage: `f8da4b6d46b0ec5ebeb7a42be47c5bf3438c5414`, tree
  `8be43e13acb436120f8a63b1a178d64c49422461`.

C3d and f8da are byte-identical to 83a for all three reviewed Runtime
materialization paths; their Runtime-file diffs are empty. The helper SHA-256
is `92ec9b7f105d5e0fd1c5f9e9f2a4602ee3dd005365a570e7ba91a573bb8b31fb` in
all three sources.

## Ported hunks

1. Added `runtime_protocol/timeline_materialization.py` from donor blob
   `bfb1217ed19d6071ecafc2b4941f38fdfabeef6d`. It performs the closed,
   read-only source/owner join: project/timeline and digest scope, parent and
   shot/internal/item membership, exact source pins, owner occurrence, fixed
   bindings, inverse provenance, and source-bound `id_map` validation.
2. Ported materialization validation/invocation into
   `runtime_protocol/timeline_commit_port.py` from donor blob
   `99a075befe009d05d11cfef4ecb3a96e6e0b48fa`: request-private closure use,
   sealed-request binding equality, and closed-port refusal before the helper
   can supply authority. The current b92 `PROJECT_PACK_KIND, TRANSCRIPT_KIND`
   import and allowlist remain byte-preserved; the donor’s obsolete removal of
   `TRANSCRIPT_KIND` was not copied.
3. Ported the materialization acceptance and occupancy guards into
   `runtime_protocol/timeline_commit_store.py` from donor blob
   `d9781479f92360fa5899d9b14b0aa38f6e78caa6`: accepted-record verification,
   inherited inverse allocations, own-slot matching, native birth reservation,
   global item reservation, durable-ledger checks, and preview/accept helper
   invocation. Current history, authority, catalog/head, source, CAS, retry,
   and private v1/v2 intent paths remain around these hunks.

## Explicit exclusions

No `timeline_commit.py` raw-media custody, reference projection module, schema,
generator, generated client, lock, manifest, version, pin, or artifact files
were changed. No old whole-file replacement was used. Current public schemas,
validation, fixtures, and negative assertions remain untouched. No prepared
provider evidence is treated as native admission.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_projection_occupancy.py -k 'occupied_destination or historical_slot or verified_inverse or tampered_historical or external_source or immutable_reuse' --basetemp=/tmp/rt08-pytest-occupancy`: **14 passed, 4 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_legacy_occupancy.py -k 'occupied_destination or current_closure or historical_reuse' --basetemp=/tmp/rt08-pytest-legacy`: **10 passed, 5 deselected**.
- `PYTHONDONTWRITEBYTECODE=1 python -m pytest -q tests/test_timeline_commit_port.py tests/test_timeline_current_union_contract.py tests/test_command_schema_compatibility.py --basetemp=/tmp/rt08-pytest-contract-neighbors`: **230 passed**.
- `python -m py_compile runtime_protocol/timeline_materialization.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py`: passed.
- `git diff --check`: passed.

No full, socket, browser, renderer, generation, release, or native matrix was
run. This is a source-bound prerequisite for later matched cohorts, not a
qualification or adoption result.
