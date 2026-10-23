# G5 independent publisher review — BLOCKED, 90 PASS / 1 FAIL

Worker: `agt-G5-publisher-review-1229`  
Reviewed: `tl/agt-G5-normal-publisher-1205` (`aa2fa8677`) against `ee7f0b809`

## Disposition

- **Scoped migration: PASS.** Ordinary `_PublishMixin.publish` delegates to the G3 emitter and `TimelineSession`; the old `store.publish_bundle` route is no longer used by this path. The draft preserves the v2 base pair, label/source, commands, steps, patch, merge, idempotency, dry-run/session behavior, narration follow-up, reset, and Runtime receipt path. No guard weakening, fabricated `reads: []`, refusal conversion, executor, schema, generated-file, dependency, or pin change was found.
- **Whole G5: BLOCKED.** Review label: **BLOCKED,90PASS1FAIL**. The retained successful disjoint-clip property is still incompatible with the conservative C0 free-transform rule; the only failing behavior is that retained disjoint-clip success. This is not a reason to change that test to refusal.

## Source trace

The legacy promise is `tests/sdk/test_timeline_persistence.py::test_publish_after_a_restart_merges_other_clips_onto_the_moved_head`. The real replacement is `tests/sdk/test_timeline_normal_publish.py::test_ordinary_disjoint_clips_merge_onto_peer_head`. The real path is `Checkout.publish` → `_commit_document` → unique history base/publication lookup and authenticated closure fetch → `emit_document_commands` → `TimelineSession.submit` with `merge="atomic"` and a conservative `timeline` scope read. Runtime correctly conflicts when the peer publication changed the guarded closure. The narration path's request-level `reads=[]` is for a native text-binding capture whose dependencies are Runtime-captured; it does not waive the ordinary free-transform scope.

Legacy `Clip.nudge` is a detached bundle mutation wrapped by `_journaled`; transaction state and the persistent journal retain a before snapshot, label, digests, and affected clip/cut names, not an authoritative semantic command or bounded read set. `Checkout.edits()` is only a final-byte diff. Direct mutable edits have no helper provenance. The attached/native session path captures semantic commands, but ordinary detached publication cannot recover that capture.

**Unresolved contract/property question:** does ordinary `Checkout` need durable authoritative helper semantic/read capture, including direct-mutation policy, so a detached restart can submit bounded per-clip commands/reads, and which owner supplies it? Until resolved outside this bounded publisher change, arbitrary free transforms remain atomic under C0 and the successful disjoint property remains unresolved.

## Audit findings

- Base lookup is conservative: all history pages are scanned; exactly one revision match is required and paired with its publication ID. Ambiguous/missing history refuses. Checkout still persists only the revision, so repeated revision IDs after restore remain an ownership gap.
- Raw closure and canonical output are guarded by membership/provenance checks and authenticated base hydration; the draft positive covers unknown fields, absent/null/false/zero values, media/dependency manifest, and complete canonical publication.
- `_ack` validates identity, base, commands, canonical document, digests/manifests, receipt hash, and accepted/merged plus historical `rebased`; outbox flights retain ambiguous requests and retry exact body/key. Durable history matching avoids duplicate commits after a cleared flight. Lost cut ACK, narration pre-flight recovery, exact narration replay, and reset behavior are covered by the draft evidence.
- Preview `would_status`, dependency presence, no-write refusal/error controls, and changed-key/force refusal are covered. The full Runtime-owned invalid/conflict/reply shape was not rerun in this review.

## Evidence and recommendation

No product or test files were changed, and the known failing disjoint body was not rerun. The draft records the bounded result as `133 passed, 1 failed, 6 deselected` (broader lane) and `10 passed, 1 failed` (ordinary-only), with scoped Ruff/mypy identity parity, vendor/artifact checks, and `git diff --check` passing. Keep unmerged; resolve authoritative helper/read capture and durable base-pair ownership, then rerun the retained positive and strict negatives on the integrated tree and obtain P1 GO.
