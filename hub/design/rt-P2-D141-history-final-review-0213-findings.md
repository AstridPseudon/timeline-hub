# P2 D141d independent final review

## Verdict

`PASS_BOUNDED`: the SAFE 3118 packet supports a narrow source/path-family contract-vsREG ruling. It does not prove the exact actual request predicate, and it is not a full P2 gate result.

The packet is faithful to the retained strict history-entry diff: two actual-only binding objects, 22 unique actual-only key paths, zero expected-side additions, and no unknown paths. The independent App0153 review confirms that structural comparison and custody, but explicitly says values/raw diff/capture state were not published and that semantic classification remains outside its scope.

## Source association

The 22 paths are exactly the union expected from the reviewed Agent source:

- `_doc_patch.py:174-181` creates `ref`, `physical_ref`, `revision_id`, `content_digest`, `boundary`, and conditional `owners`.
- `_commit_patch.py:359-362` supplies the boundary members observed here: `base_revision_id`, `base_publication_id`, `evaluated_head`, `step_id`, `command_ordinal`, and `phase`; the nested evaluated-head members account for its two child paths.
- `_commit_patch.py:641-665` gates the complete-stage continuation and its exclusive/single-owner/shot-preserving/edge-membership checks.
- `_commit_patch.py:701-718` emits two `commit.materialization` bindings per changed source/successor pair, adding `key`, `policy`, `dependencies`, `successor`, `owner`, `edge_before`, `edge_after`, and `step_id`.

That is an exact source/path-family correspondence. It is not an exact invocation proof: the packet contains no binding values, no request body, no producer capture state, and no raw accepted record. Therefore it cannot independently establish that this run satisfied each D124 predicate or that the two objects were produced by that invocation rather than merely having the same structural shape.

## Contract-vsREG ruling

For Main’s narrow ruling, the source/path evidence is sufficient: these additions match C0’s authenticated physical bindings, evaluation boundaries, materialized successors/edges, provider-derived steps, accepted replies, and history requirements (`/home/user/work/wt/rt-P2-D141-history-final-review-0213/contract/commit-v2.md` §1 lines 60-155; §2 lines 287-350 and 388-438; §4 lines 703-715; §5 lines 1563-1642; §7 lines 4609-4642). They should not be classified as an unrelated Runtime/App REG field family.

The ruling must be stated as structural and bounded. It cannot say “the actual 3118 request satisfied D124” or “the full P2 journey passed.” The source run itself is `FAIL`; the historical 15203 run is also overall `NO-GO`, although its named automatic-placement case passed.

## Historical and security evidence

The historical 15203 receipt preserves the exact automatic-placement case at 88.780 seconds on App `96d4754b4eef0591a208d6b51b60c30fc44b6915`, Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2`, Runtime `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`; the full run was 2 PASS / 2 FAIL / 1 ERROR / 3 NOTRUN. The current and historical App commits resolve the same spec blob and SHA, and the historical placement source covers request, accepted reply, canonical closure, history, reload, and guarded Undo at lines 1214-1295.

The D124 union security review is source/security PASS but records qualification as blocked; the earlier producer security review records product HELD. Those records support source provenance only and do not fill the missing 3118 values/capture state.

The controlling immutable identities and hashes are in the accompanying `source-manifest.json`. They were derived from read-only Git, including full Composition commit/tree identity, rather than copied from short prose strings. The prior 0207 evidence is preserved and not authorized as a broader gate.

## Findings and limits

- PASS: packet count and path conservation; App0153 custody/privacy; App spec provenance; D124 source-family correspondence; C0 structural mapping.
- NOT PROVEN: actual D124 invocation/predicate satisfaction, exact binding values, exact request/reply capture, or producer/runtime causal attribution for this run.
- OUT OF SCOPE: tests, imports, browser/socket execution, product changes, REG fixes, release, and P2 GO.

