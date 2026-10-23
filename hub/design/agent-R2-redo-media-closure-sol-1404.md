# Agent R2 redo media closure 1404

Status: offline diagnosis in progress; no public retry or readiness claim.
Base: `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`.

Consumed settled PLAN §2/§3 R2 and C0 §2/§5 plus Runtime 1338/1354 handoffs.
The 1356 export arrived during inspection: `runtime-R2r-redo-1338-9603ca432b1c9d1c.json`, SHA-256 `9603ca432b1c9d1c1b16908f00547d26da6d04df3ad681308cbae5f3e57635d1`.
All 53 members verified byte-for-byte and extracted only into this worker's durable evidence directory. The original 426995-byte inverse packet is not substituted.

Current `_doc_patch.py` and core `authoring_bundle.py` are byte-identical to captured bfc. `_commit_patch.py` differs only in the later atomic dependency union fix; `inverse_closure` and the failing `after` stage loop remain identical. No wholesale bfc port is needed. `commit.py` remains read-only to this worker (1403 owns it).

Trace under examination: `CommitPatch.after` projects each complete inverse stage with `Closure`, which calls `document_from_bundle`, whose first operation compiles the candidate before historical immutable reuse. Thus source images cannot bypass the selected-media guard. Need distinguish a reconstructed valid historical boundary with lost baseline provenance from a truly competing selected media pair. No guard change is authorized by the traceback alone.

Offline replay will use the exact redo full request and retained source/history/closure data with production provider and ordinary port, before proposing a repair. Runtime narrow review PASS does not establish merged public redo readiness. Overall R2 whole undo/redo and G5 P1 remain incomplete/NO-GO.

## Early causal result / ownership interface (14:12 UTC)

Exact production provider + ordinary `RequestCommitPort` offline replay is RED on current Agent: same `invalid_document`, same media guard, SQL unchanged. The dump is restored verbatim in private in-memory SQLite; no acceptance/provisioning/network occurs. The original seed bytes are deterministic in `seed_shared_occurrence_parent`: `connected-occurrence-source-0` / `-1`; their SHA-256 values exactly match the two retained media pins, so the private CAS uses exact originals, not substitute media.

Root cause is **canonical historical child reconstruction**, not transient root write ordering: the complete failing selected shot payload AND complete internal timeline equal the accepted forward boundary in `ctx.inverse_sources[0]`, owner set exactly `{f2-occurrence}`. Reconstruction instead presents a plain `_created: true` shot with no baseline/source mapping. The guard consequently compares existing `{visual, voiceover}` metadata against an empty baseline and internal rendered `{visual}` and correctly refuses that representation. The guard must remain intact.

A repair only inside stage `inverse_closure` is insufficient: final `document_from_bundle(plan.bundle, source_bundles=...)` independently re-enters the same compiler. Straight source-mapping rebasing is also insufficient: controlled candidate reaches `_doc_patch_materialize.project` and fails because the original canonical source index lacks the restored child. This trial is not GREEN and is not a proposed production change.

**Ownership request to 1403 / Agent manager:** release the `document_from_bundle` hunk at `commit.py:302–311` (outside 1403's current 1075/1156/1172 hunks), or have that owner apply the reviewed one-line integration. Causally needed integration: pass already-authenticated inverse `source_bundles` into a narrowly bounded compiler baseline restoration, before `compile_authoring_candidate`; final and stage projections must use the same path. I will not edit `commit.py` without explicit handoff. No product source edit has been made.

Minimum baseline authority: verified same project/timeline historical canonical document; same exact child identity, complete owner set and payload/internal pair, with original source pins/digests untouched; use that accepted pair only as baseline, retaining all current fields and guard checks. Never copy an entire parent/root, infer new history, treat mere equal media sets as proof, or reuse a sibling's identity. Need genuine negative controls for owner/payload/internal/pin/history/step mismatch before product adoption.
