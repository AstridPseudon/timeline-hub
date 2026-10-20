# Placement candidate promises disagree with real provider admission

M2 only; no AppM1 impact. Native candidate a6c2db3d (Agent placement-create-unplace-b) is unit qualified, NOT an official Runtime pair.

App source mapping and exact executable provider probe are in workers/app-m2-placement-contract-review/notes/report.md and design/app-writer-contract-gaps.md appended placement section. Candidate's normal RuntimeCommitService.commit with its detached MediaRealm port rejects both same-batch [unplace,create same ID] and separate ordinary recreate with409 identity_collision. Pure execute accepts; provider's persistent created-ID reservation correctly refuses. The candidate document's same-ID re-place recipe therefore cannot be used by App. All state/history stayed unchanged.

Second diagnostic: accepted create→unplace→undo(unplace) restores exact postcreate state, then undo(create) refuses409 intervening_write on childroot. This is the current strict ABA policy, not permission to weaken it. Don't describe it as a qualified normal LIFO stack. Actual Runtime/browser proof remains UNRUN.

Recommended Agent contract correction: withdraw same-ID recreate guidance; use placement.move for existing unchanged media+explicit time, or a genuinely NEW reserved identity for a separately chosen replacement. Confirm intended honest undo-refusal UX/history semantics with Runtime owner before claiming replacement covers old multi-step behaviour; retain concurrent/other-author ABA protections.

App mapping also uncovered all actual legacy create/unplace callers omit explicit occurrence owner; remove path always requests keepAsPooled. Auto/pool/null/shift/video/registry refresh remain unsupported. Keep originals/tests and writers until qualified explicit-owner/media-pin route covers the caller. App audits45positive tests/native35PASS, no behavior changes.

Meanwhile supported capture/session source work continues. No schema extension/op name invented by App; candidate must receive normal owned schema/artifact release and actual Runtime qualification before consumer cuts.
