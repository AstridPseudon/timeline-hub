# Agent R2 redo media closure 1404

Status: offline diagnosis in progress; no public retry or readiness claim.
Base: `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`.

Consumed settled PLAN §2/§3 R2 and C0 §2/§5 plus Runtime 1338/1354 handoffs.
The 1356 export arrived during inspection: `runtime-R2r-redo-1338-9603ca432b1c9d1c.json`, SHA-256 `9603ca432b1c9d1c1b16908f00547d26da6d04df3ad681308cbae5f3e57635d1`.
All 53 members verified byte-for-byte and extracted only into this worker's durable evidence directory. The original 426995-byte inverse packet is not substituted.

Current `_doc_patch.py` and core `authoring_bundle.py` are byte-identical to captured bfc. `_commit_patch.py` differs only in the later atomic dependency union fix; `inverse_closure` and the failing `after` stage loop remain identical. No wholesale bfc port is needed. `commit.py` remains read-only to this worker (1403 owns it).

Trace under examination: `CommitPatch.after` projects each complete inverse stage with `Closure`, which calls `document_from_bundle`, whose first operation compiles the candidate before historical immutable reuse. Thus source images cannot bypass the selected-media guard. Need distinguish a reconstructed valid historical boundary with lost baseline provenance from a truly competing selected media pair. No guard change is authorized by the traceback alone.

Offline replay will use the exact redo full request and retained source/history/closure data with production provider and ordinary port, before proposing a repair. Runtime narrow review PASS does not establish merged public redo readiness. Overall R2 whole undo/redo and G5 P1 remain incomplete/NO-GO.
