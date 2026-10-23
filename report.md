# G5 independent publisher review — BLOCKED, 90 PASS / 1 FAIL

Worker: `agt-G5-publisher-review-1229`  
Reviewed: `tl/agt-G5-normal-publisher-1205` (`aa2fa8677`) against `ee7f0b809`

## Disposition

- **Scoped migration: PASS.** Ordinary `_PublishMixin.publish` delegates to the G3 emitter and `TimelineSession`; the old `store.publish_bundle` route is no longer used by this path. The draft preserves the v2 base pair, label/source, commands, steps, patch, merge, idempotency, dry-run/session behavior, narration follow-up, reset, and Runtime receipt path. No guard weakening, fabricated `reads: []`, refusal conversion, executor, schema, generated-file, dependency, or pin change was found.
- **Whole G5: BLOCKED.** Review label: **BLOCKED,90PASS1FAIL**. The retained successful disjoint-clip property is still incompatible with the conservative C0 free-transform rule; the only failing behavior is that retained disjoint-clip success. This is not a reason to change that test to refusal.

## Test trace and source ownership

The legacy promise is `tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head` (the old file-backed `publish_bundle`/three-way path). The real replacement is `tests/sdk/test_timeline_normal_publish.py::test_ordinary_disjoint_clips_merge_onto_peer_head`: a detached checkout edits `p1`, a peer commits `p2`, then the stale checkout publishes.

The real path is:

1. `Checkout.publish` validates a copy and calls `_commit_document`.
2. `_commit_document` scans Runtime history, resolves the checkout revision to a unique publication, fetches that exact authenticated closure, verifies membership/provenance, constructs a candidate, and calls `emit_document_commands`.
3. It submits `doc.patch` calls through `TimelineSession.submit` with `merge="atomic"` and a conservative `timeline` scope read in the step. The narration path's request-level `reads=[]` is for a native text-binding capture whose dependencies are Runtime-captured; it is not used to waive the ordinary free-transform scope.
4. Runtime therefore correctly reports a conflict when the peer publication changed the guarded closure. The new test fails at the expected merged-status assertion.

Legacy helper capture cannot repair this inside the publisher-only scope. `Clip.nudge` mutates the detached bundle; `_journaled` wraps it in a step, and `transaction.py` retains only a before snapshot for local undo. The persisted journal records label, digests, affected clip/cut names, and audit evidence; it does not record the helper operation, its operands, or an authoritative read dependency. `Checkout.edits()` is recomputed from the final bytes. Direct mutable edits, such as the new test's `clip.data['opaque']` writes, have no helper provenance at all. The attached/native session path can capture semantic commands, but ordinary detached publication cannot infer that capture after the fact.

Exact unresolved contract/property question: **Does ordinary `Checkout` need durable, authoritative helper semantic/read capture (including direct mutation policy) so a detached restart can submit bounded per-clip commands/reads, and which owner supplies it?** Until that is answered and implemented outside this bounded publisher change, arbitrary free transforms must remain atomic under C0 and the successful disjoint property remains unresolved.

## Base lookup, closure, ACK, narration, and reset audit

- **Base pair:** the adapter scans all history pages and accepts exactly one entry whose `revision_id` equals the detached checkout base, then fetches `(revision_id, publication_id)`. Multiple matches, missing history, repeated cursors, or failed reads refuse rather than guessing. This is the correct conservative behavior, but the checkout itself persists only the revision in `base_parent`; a revision reused by restore/multiple publications has no durable original publication pair and therefore remains an ownership gap.
- **Raw closure:** the adapter compares base parent, placements, shot membership, provenance, and non-authored shot fields before emitting. It copies authored parent/payload/internal fields onto the authenticated base and emits structural patches. The draft's complete-closure positive covers unknown fields, absent values, explicit `null`/`false`/`0`, media/dependency manifest, and canonical publication output.
- **ACK/replay:** `_ack` validates authenticated identity, base pair, commands, canonical document, digests, manifests, receipt hash, and accepted/merged (plus historical `rebased`) status. `TimelineSession` retains an ambiguous flight and retries the exact body/key. If the flight was cleared before process loss, `_commit_document` matches the durable history entry by base, label, and commands instead of creating a second commit. The draft's lost-ACK cases show one actual commit/history entry.
- **Narration:** a cut ACK followed by ingestion failure is recoverable before a narration flight exists; an existing narration flight is label/operation-checked and flushed by its original key. Binding is a separate guarded commit. The draft covers exact cut/narration replay and pre-flight recovery.
- **Reset:** after publication, `_reset_base` re-reads the Runtime head, writes the new checkout without an undo step, retires draft history, and records the publish journal evidence. Read/reset failures preserve the old in-memory base with an explicit note and retire local draft history; they do not fabricate acceptance.
- **Replies/preview/errors:** the publisher returns Runtime's `data` and `receipt` without normalizing away canonical/records/dependencies/effects/steps/history/undo-step fields. The provider/session owns the full invalid/conflict/preview contract; the draft directly checks preview `would_status`, dependencies, no-write behavior, and changed-key/force refusals. Broad HTTP/provider error-shape qualification was not rerun here.

## Evidence and limits

No product or test files were changed. I did not rerun the known failing disjoint body, per the instruction that source/log evidence suffices and no failed disjoint repeat is wanted. The draft design report records the bounded result as `133 passed, 1 failed, 6 deselected` for the broader lane and `10 passed, 1 failed` for the ordinary-only lane; it also records scoped Ruff/mypy identity parity (existing 2 Ruff findings; existing 19 mypy identities), vendor/artifact checks, and `git diff --check` passing. No full suite, live/browser suite, Git mutation, or shared-install mutation was performed.

## Recommendation

Keep this draft unmerged. Resolve the authoritative helper/read-capture and durable checkout base-pair ownership questions, then rerun the retained positive and strict negatives on the integrated tree and obtain P1 GO before G5 integration.
