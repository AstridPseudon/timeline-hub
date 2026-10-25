# D124 R2: grouped inverse alias boundary

Disposition: **BLOCKED_RUNTIME_INVERSE_BOUNDARY**. No Agent product correction applied. One additive positive regression remains RED; two source/comparison tests pass. This is separate from the already-owned Runtime materialization step-input mismatch at auth565–580.

## Finite production source fact

The new offline test initializes a normal temporary RealmStore/RuntimeService, registers create_runtime_commit_service(), bootstraps a timeline, and commits a parent visual track. Ordinary capture helpers build occurrence.create followed by one child track.create. The second command is captured from execute(bundle, [birth]).bundle. The request omits optional ABI1 label/steps, so C0 section1 synthesizes the single original step [0,1]. Nothing splits or reorders that step. No media, generation, sockets, collector, observer or replacement validator is involved.

The passing source test checks the accepted canonical document, exact native site order (shot root, occurrence root, child track root), exact child previous/after values, allocation facts, complete shot/internal root effects and exact physical revision/digest/owner pins. The registered-provider behavior test then submits an ordinary timeline.inverse. It fails with `provider occurrence alias is outside its boundary`. The ungrouped comparator passes exact birth undo/redo and exact child-track undo; no original acceptance case is rerun.

Source trace:

1. Agent _step_undo.inverse_stages329–352 yields the immutable accepted source step as one group. inverse.apply_inverse1132–1187 reverses native writes within that group: remove the track, then the occurrence, then its shot. Recording.assign captures actual sequential before/after values. inverse.stage keeps the same publication, step ID, ordinals and complete native write range. The final stage correctly has no created occurrence or child roots.
2. Agent _commit_patch.after474–492 projects the actual inverse stage boundaries, and finish564–593 derives their complete canonical effects. The whole-step output removes the created physical roots and occurrence. The original step partition is preserved.
3. Runtime timeline_commit_auth._inverse_stage_boundaries1415+ derives the authenticated stage output from effects and replays each native write against its sequential native_image. Child aliases are valid at their earlier write boundary. Root handling1451–1472 subsequently removes the occurrence and shot/internal images. Full native/effect payload equality is required at1755–1757.
4. The final per-write comparison1764–1765 calls _inverse_stage_write_site(native_image, write) and _inverse_stage_write_site(stage_after, write). Both arguments are now final images with no occurrence. For the earlier child-track write, _inverse_stage_write_site849–860 delegates to native_site/site. site155–156 requires exactly one live occurrence row and refuses. The native write's actual historical evaluation boundary was lost during this final lookup. This predicate rejects an ordinary grouped create/inverse even though the alias was valid at the sequential write boundary and the final closure must remove it.

This conclusion combines the small real-provider failure with the deterministic production source path; it does not claim that original private stage/write/physical records were recovered. Those records remain EXACTMISSING. The retained original occurrence[True] report names this same final lookup/frame, but equivalence of every original physical pair is unverified.

## Why no allowed Agent workaround was applied

Keeping the occurrence in the output contradicts exact undo. Splitting the source step or moving native boundaries contradicts C0 and Runtime _inverse_stage_history1248–1315 / _inverse_stage_ranges1334–1405. Rewriting arbitrary native refs violates its exact site membership and capture-count checks, and would also change inherited native history.

Runtime1404 explicitly permits exact canonical effect sites as an alternative; it is not enough to claim native-site equality alone rules that alternative out. However, Agent effect_diff170–241 represents a changed occurrence ID list as the complete parent/occurrences field, together with physical child-root removals. Runtime1514–1534 accepts native parent/occurrences captures only as row-preserving permutations (same cardinality and identical rows). A birth inverse changes [child] to [], so that exact canonical alternative also fails a current Runtime predicate. No speculative canonical rewrite, source-count claim or fabricated original capture is proposed.

The allowed Agent files cannot repair the observed Runtime final lookup while preserving all required stage boundaries, native captures, endpoint pins and exact output. _doc_patch_materialize.remember controls compiler projection for surviving owners, not Runtime's resolution of a removed alias. No cache, retained ghost owner, new authority, relaxed guard or exception handling is introduced.

## Unapplied owner action

Owner: Runtime, timeline_commit_auth._inverse_stage_boundaries final native-write comparison1764–1769. Review custody of earlier child write sites after authenticated owner/root removal, against C0 sections2/5/7: persisted physical bindings and sequential evaluation boundaries must govern historical native captures. Keep complete source-step provenance, exact native/effect ranges and membership, sequential previous-value checks, root allocation provenance, complete owner/revision/digest/edge proofs and final closure equality. Merely suppressing outside-boundary errors or trusting a historical alias is not a correction.

The new acceptance/undo/redo expectations remain positive and unchanged by the refusal; no skip, xfail or weakened expectation. Recommend adopting the regression with its Runtime correction after independent protected review and targeted genuine-provider validation. Independent source/security review of this final test and finite diagnosis found no weakening/security blocker and agreed with the Runtime-owned disposition. The reviewer ran no tests and made no edits. No release/adoption or core425/REG14 deduction is claimed; Farm core remains once per batch before downstream adoption.
