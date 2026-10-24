# P4 D73 independent verdict

**FAIL — qualified to the ten-note path.**

Service: `agent-p4-current-becfe-http-3legs-1024174105-16328`

- CLI/sheet: **PASS**, 3.013s
- Ten-note commit/per-step undo-redo: **FAIL**, 45.336s JSON Schema timeout
- Conflict/rerun: **PASS**, 12.386s
- Aggregate: `1 failed, 2 passed in 63.58s`, exit 1

The genuine body reached the ten-note test’s first redo request after the initial ten-note commit and history checks had succeeded. The captured stack is:

`HTTP server → service.commit_timeline → Agent provider → port.accept → store._validate → _inverse_stage_history → _historical_sequential → validate_sequential_capture → _capture_document_images → validate_commit_value → jsonschema resolver`

The timeout occurred while validating the `fps` schema instance:

`{'denominator': 1001, 'numerator': 30000}`

No phase beyond the captured stack is inferred. The dry-stub call-count limitation remains: `COUNT` was not exported. The genuine bodies did run.

## Whole-path findings

1. CLI and Python callers enter the Agent `TimelineSession` path, emit v2 `doc.patch` commands, and submit through `_remote_timeline`.
2. Runtime receives the unchanged v2 request through `runtime_protocol/server.py`, builds the commit service/coordinator, and invokes the Agent semantic provider.
3. Agent commit construction captures the canonical original/landing sequential execution.
4. Runtime acceptance stores the commit and revalidates accepted history.
5. The ten-note redo enters historical sequential validation, where every command boundary is recaptured and canonical documents are validated, including image payload digests.
6. The resolver improvement only reuses immutable schema-resolution lookups. It does not cache mutable validation results, history, authority, or document state. Fresh finite-JSON and schema validation still occur.
7. Retained measurements report 54 `CanonicalDocument` validations, 2 `Recorder` validations, and 56 finite-JSON checks. Resolver lookup work improved (`8188 → 0` warmed native lookups; CPU profile `1.304375s → 0.661699s`), but the ten-note path still exceeds the 45-second limit.

## Smallest Runtime proposal — unapplied

Runtime owner only: instrument the existing seam at:

- `runtime_protocol/timeline_commit_auth.py::validate_sequential_capture`
- `_capture_document_images`

Add disabled-by-default, local-only counters/timers tagged by:

- original vs. landing
- command ordinal
- live acceptance vs. historical/inverse verification
- schema validation, finite validation, and payload digest work

Emit only to the local diagnostic log. Do not persist it, include it in replies, alter receipts, skip validation, cache mutable results, or change the time budget.

## Input identity

- Agent commit/tree: `f4d6c72ce336da66813fc39828187bccbaf80a5b` / `5d328a24dd64fb216ae527b6c05f51d99d7c564e`
- Runtime commit/tree: `327da207ed30880fe2ae0cd0b116722bb2c6f7a6` / `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf`
- App commit/tree: `255f9f1218765f9a407354cf230aab9a452c8073` / `3f6d3df601452eb00ac0a664590c45f28a0f3734`
- Composition commit/tree: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`
- Original test hash: `11c075bb257314cba368dd469c45e7f7b50b7b5f5964db11c0c9425a9cac74e0`
- Tuple manifest SHA-256: `be8760dfdf3574b3079e53e8b65998ef02c1175e1af02d2054898cba40c101ca`

## Verification

Static checks passed:

```text
python3 -m py_compile astrid/sdk/timeline/sync.py astrid/sdk/timeline/commit_session.py astrid/sdk/timeline/emitter.py astrid/packs/timeline/cli_native.py
python3 -m py_compile /home/user/work/wt/rt-pin-327da207/runtime_protocol/timeline_commit_validation.py /home/user/work/wt/rt-pin-327da207/runtime_protocol/timeline_commit_auth.py /home/user/work/wt/rt-pin-327da207/runtime_protocol/timeline_commit_store.py
git diff --check
```

No product, test, schema, registry, pin, or shared-ledger files were changed. No full suite or body rerun was performed.

Remaining unknowns are the exact per-boundary timing/count split in this current 45-second body and whether schema validation or payload digest work dominates it. The commit message and `DONE` marker were written as requested.