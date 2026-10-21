# RT07 final Main95 adoption and deletion cut plan

## Verdict

RT07 stays **HELD**. The Runtime deletion is immediately executable after the
ordinary014 consumer is adopted, but Agent `6efc8150` is not that adoption: it
does not contain the reviewed D13 consumer cut. No Runtime deletion merge or
normal pin/public adoption is authorized by this note.

This is a source/read review only. Generated clients, source pins, artifacts,
tests, and renderer evidence were not changed or regenerated.

## Immutable source identities

| purpose | commit | tree |
|---|---|---|
| Runtime base | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3` | `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Runtime deletion parent | `6e845a187684919c162b29568496c015bda1a591` | `7f11d7e159d46a88a22111c414aa7bdf7b599d9d` |
| Runtime 67-line deletion | `67ea129f6a1a96f633ec409d04ff811a89eeb4c6` | `5cd8bf63e395b8fc2870915c9aafdd706541570d` |
| Agent current normal014 source | `6efc81500a0e0688c2bb41e736503f0fc3e04abb` | `2ed2b8a12b5b3391ca221ba6ff05390f71a73556` |
| Agent qualified D13 source | `7b3e1205a374443c46bad6b18753ef146e1e42c6` | `7d807bc27b1b237de7138c13672d2fa814a22f3f` |

The registered-native qualification `7012` is the existing immutable proof:
the two original `tests/packs/video_editing/test_runtime_publication_chain.py`
positives passed, `2 passed in 300.96s`. It is historical evidence and is not
rerun here.

## Runtime cut validation

`git diff 6e845a1 67ea129 -- runtime_protocol/service.py` is exactly **53
additions / 120 removals**, a net 67-line reduction. The candidate changes no
other path. Read-only checks passed:

- `git diff --check 6e845a1 67ea129 -- runtime_protocol/service.py`;
- compile of the candidate `runtime_protocol/service.py` with the Runtime
  venv and `PYTHONDONTWRITEBYTECODE=1`;
- an outside-method identity check against base `95bd`: all service lines
  before and after `publish_timeline_render` are identical;
- keeper-token inspection of the cut.

The retained method still has `_verified_mutation`, idempotency-key
validation, attempt identity and lease checks, project/target custody checks,
and exact request-hash comparison. An already-published checkpoint returns
its durable result without consulting live target, document, CAS, task, or
history state. Unknown/missing targets, changed payloads, target mismatches,
prepared checkpoints, and current legacy publication all refuse visibly. The
removed body no longer calls `prepare_timeline_render_publication`, updates a
timeline document, publishes a snapshot, creates a render task, or completes
the legacy checkpoint.

## Final6ef live consumer census

The names below are source sites, not a claim that every adapter is an
independent product writer.

| site in Agent `6efc8150` | classification | evidence |
|---|---|---|
| `astrid/core/execution/generic_host.py:8501-8591`, called at `:9731-9739` | **held legacy consumer** | `_publish_assembled_timeline` reads `authoring-proposal.json` and calls `self.client.publish_timeline_render` at `:8512`; this hook is absent from qualified `7b3`. |
| `astrid/packs/rendering/shared/runtime_stitch.py:104-211`, call at `:144-147` | migrated helper surface | It forwards a settled authoring proposal through `tasks.publish_timeline_render`; it is the reviewed helper, but final6ef has no requester-side `TimelineSession` assembly reader/queue path. |
| `astrid/packs/video_editing/shared/runtime_orchestration.py:426-470`, call at `:452-470` | migrated compatibility helper | `publish_stitched_render` delegates to the helper above. The source has no other in-tree product call to this function; its presence does not prove D13 adoption. |
| `astrid/sdk/remote.py:410,2023-2050` | retained client adapter | Dispatch and typed forwarding for the Runtime checkpoint; not a direct document writer. |
| `astrid/sdk/workspace_client.py:266,1191-1253` | retained client adapter | Allowlist and generated-client argument translation; not a direct document writer. |
| `astrid/chat/runtime-client.ts:257` | generated client surface | Direct HTTP method definition only; no in-tree call site was found. Generated/source pins are immutable. |
| `tests/packs/video_editing/test_runtime_publication_chain.py:152` and assertion-only name matches | dead test names | Explicitly excluded from the live-caller census. |

The final6ef source also retains the old `GenericPackHost.publish_timeline_render`
adapter at `:4942-4956`; that is plumbing, not a second product consumer.

## D13 comparison and precise Agent request

The qualified D13 source has the native assembler contract and requester
handoff that final6ef lacks:

- `astrid/core/contracts/runtime_orchestration.py` has
  `is_native_assembler_spec` and `build_assembler_admission` (qualified
  `7b3`: lines 73 and 94); final6ef has neither;
- qualified `astrid/sdk/timeline/assembly.py` is present and reads the exact
  settled managed proposal; final6ef has no file at that path;
- qualified `TimelineSession.admit_assembly` and `queue_assembly` are at
  `astrid/sdk/timeline/sync.py:211-263`; final6ef has neither;
- qualified `astrid/sdk/workspace_client.py:262,824-830` exposes the existing
  media-selection and verified-media adapters; final6ef has the generated
  operations but not these WorkspaceClient adapters;
- qualified `astrid/packs/rendering/actions/assemble_timeline/run.py` and
  `astrid/packs/rendering/pack.yaml` carry the native proposal semantics;
  final6ef's pack description still says “legacy admissions retain Runtime
  publication”;
- qualified `generic_host.py` removes the pre-settlement hook and invocation;
  final6ef retains both.

The two already-reviewed files
`astrid/packs/rendering/shared/runtime_stitch.py` and
`astrid/packs/video_editing/shared/runtime_orchestration.py` are byte-identical
between final6ef and qualified 7b3, so they do not need to be ported again.

Agent request, sent through the hub inbox: on a branch derived from final6ef,
port only the reviewed D13 consumer seam from qualified 7b3 / compose commit
`65c87dd5d5310bc028acafaf1cab31196a03a86d`:

1. port the native assembler contract, `assemble_timeline` action/pack
   semantics, requester `assembly.py`, `TimelineSession` assembly methods,
   and the two existing WorkspaceClient media adapters;
2. remove `_publish_assembled_timeline` and its `run_task` invocation while
   preserving final6ef's unrelated current host/custody source;
3. keep the generated client, Runtime source pin, artifact manifests, and
   existing assertions immutable; no new endpoint, DTO, fallback writer,
   generated refresh, or renderer rerun;
4. return exact changed paths and source/tree identities, then coordinate the
   normal014 Agent/App/Runtime adoption before any RT07 deletion merge.

This request is intentionally bounded: it does not relabel the historical
`7012` run as current adoption and does not ask Runtime to change its 67-line
cut.

## Adoption order and stop condition

1. Agent supplies the bounded D13 consumer port on final6ef and confirms the
   last live `publish_timeline_render` caller is the requester path.
2. Agent/App/Runtime coordinate the exact ordinary014 adoption with Runtime
   `95bd` and preserve the immutable generated/artifact tuple.
3. Runtime rechecks the candidate source identity, refusal/replay keeper
   behavior, and last-caller census on the coordinated tuple.
4. Only then may the held Runtime deletion be merged and RT07 move to
   `DELETED`; until then the ledger remains `HELD`.
