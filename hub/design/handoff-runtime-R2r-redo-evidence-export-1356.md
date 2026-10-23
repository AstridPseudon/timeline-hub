# Runtime R2r redo evidence export — Sol-1338

Status: complete, evidence-only. This handoff exports the existing Sol-1338 capture; it does not rerun the service, add a product fix, alter tests, or claim redo success.

## Immutable artifacts

- Packet: `runtime-R2r-redo-1338-9603ca432b1c9d1c.json`
  - SHA-256: `9603ca432b1c9d1c1b16908f00547d26da6d04df3ad681308cbae5f3e57635d1`
  - Size: 6,901,649 bytes
- Manifest: `runtime-R2r-redo-1338-9603ca432b1c9d1c.manifest.json`
  - SHA-256: `399b3461fdb8c8657afd4a7c9d6b21cd8b49d8b9ba3abbdc8e6b345a09d080c1`
  - Size: 239,038 bytes
- Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-leaf-sol-1338/evidence`
- 53 source members, 6,058,747 raw UTF-8 bytes. The manifest records every filename, byte length, raw SHA-256, and content-section digest. Packet member data re-encodes byte-for-byte to each recorded raw hash.

The packet retains the service-01..05 request/reply/before/after boundaries, the redo exception, accepted forward and undo replies, source history and prepared closure, actual undo stages, original/restored document closure, public module origins, setup/resume custody, verification and execution logs/source. Repeated `public-auth-*.json` snapshots were not needed after retaining `public-undo-auth.json` and `public-undo-stages.json`; no database dump or archive was added.

## Exact public sequence

| Call | Idempotency / label | Result | Receipt |
| --- | --- | --- | --- |
| 1 | `preview` / `preview` | `preview` | none |
| 2 | `fork-edit` / `fork-edit` | `accepted` | `txn-f73af2c66fa248c69eae159c3e4a8a64` |
| 3 | `undo` / `undo` | `accepted` | `txn-f962cd740f864c8e9449fbd22407853a` |
| 4 | exact `undo` retry / `undo` | same accepted reply, no write | `txn-f962cd740f864c8e9449fbd22407853a` |
| 5 | `redo` / `redo` | `invalid_document` | none |

The redo request is the normal public `TimelineSession.undo` path's full v2-shaped request: `api_version`, project/timeline IDs, base revision/publication, `timeline.inverse` command, label, steps with `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, and `reads`, `merge`, `reads`, `dry_run`, `source`, `rationale`, `group_id`, and idempotency. The complete parsed request is retained in `public-service-05-request.json` and duplicated as a field inventory in the packet.

## Boundary and cause

The exact redo refusal is:

```text
shot 'selected-shot' has competing selected media between shot items and internal clips
```

The retained Agent stack is:

```text
commit.py:1072 -> commands.py:258 -> _commit_patch.py:387
-> inverse_closure:222 -> _doc_patch.py:117
-> document_from_bundle:309 -> authoring_bundle.py:1127
```

This is Agent inverse-closure compilation before Runtime acceptance for redo. The packet does not claim a Runtime guard failure, another public body, a redo PASS, a redo retry, or a merged/conflict journey. The initial observer bookkeeping `ValueError` after successful undo and the resume continuation are retained exactly; the continuation retried only the exact undo idempotency request, then attempted redo once and stopped.

Independent checks in the packet show:

- redo before/after `head`, `document`, `history`, and `database` are all equal;
- original `public-service-01-before` document equals restored `public-service-03-after` document;
- parsed full request fields remain intact;
- origin verification reports exact source matches for the captured module-origin boundaries;
- Agent commit/tree and Runtime parent/candidate tree/module/port hashes are recorded in custody metadata;
- frozen `34e`, `d106`, and `819acf` references were not touched by this evidence-only export.

Credential scanning ran before publication: zero bearer/API/private-key token-pattern matches and zero nonempty structured credential fields. No credential values or hidden redactions are present.

## Verification

```text
python packet/manifest validator:
PASS hashes, 53-member counts, UTF-8 roundtrip, raw hashes, section digests
checks: redo no-write {head: true, document: true, history: true, database: true}; original/restored document: true

git diff --check -- design:
PASS
```

No product tests or full suite were run because this task changes only immutable evidence/design artifacts; the source Sol-1338 test results remain in the packet and source evidence.
