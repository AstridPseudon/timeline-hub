# P2 D141d final actual/source join

## Final classification

`INTENDED_CONTRACT` for the bounded SAFE actual-only field family. The supplied App packet is present and complete for this join: it reports two actual-only binding objects, 22 actual-only key paths, zero expected-side additions, and no unknown paths. Those paths are exactly the binding shape produced by Agent D124's `commit.materialization` emitter.

The correspondence is causal at the source/path-family boundary. `Closure.binding()` supplies the physical reference, revision, digest, evaluation boundary and owners; D124 commit `16bbd56dbf016bcddeafa891291129efcfa87196` adds the `complete_stage` branch and retains `materializations()` output only for an exclusive, single-owner, shot-preserving turnover. `materializations()` emits the paired shot-revision and internal-revision source/successor bindings, adding `key`, `policy`, `dependencies`, `successor`, `owner`, `edge_before`, `edge_after` and `step_id`. The App packet's 22 paths are the complete union of those fields, including the nested boundary paths.

This is not a product REG: the observed additions are not an unaccounted Runtime/App field family. Runtime's reviewed cut validates authenticated bindings and persists the provider records/history; it is not the producer of this family. The prior author/security record is consistent: the D124 producer source was security-reviewed PASS, while broader producer acceptance remained separately held. The exact App expected oracle's strict equality therefore rejects a provider-authoritative materialization family that C0 requires.

## Evidence and corrections carried forward

- The SAFE actual packet is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-P2-D141-history-safe-fields-0146-extra-fields.json`; its source manifest binds run 3118 to App `867cb273…`, Agent `28e56cac…`, Runtime `6a011d58…`, and Composition `635f4de…`.
- The historical identity is preserved from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-P2-D141-history-safe-fields-0146-prior-pass.json`: the exact automatic-placement case passed in 88.780s on App `96d4754b…`, Agent `070dfc…`, Runtime `d23a8e0…`, Composition `635f4de…`. The overall historical 15203 run was FAIL; only the named case receives PASS evidence.
- The corrected D124 direct parent is `5caa12bda353cc46143d3125bce60f8019cf839d`; `070dfc5…` is an ancestor, not its direct parent.
- The historical 88.780s receipt exists at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D118-P2-15203-pass-review-1019-verdict.json` and `.md`. It is retained as case-level historical evidence, not substituted for the 3118 packet.

## Contract citations

The reviewed C0 contract is `/home/user/work/wt/rt-P2-D141-history-final-0207/contract/commit-v2.md`, SHA-256 `4581ea85aada0af405b1b1b9284e9938a6dba3ca4f6980b7c3c0be8f135f9bb7`.

- Physical identity and boundary fields (`ref`, `physical_ref`, `revision_id`, `content_digest`, `boundary`, nested head/ordinal/phase/step fields): C0 §2, lines 324-329; the closure identity rules are §2, lines 287-322.
- Association fields (`key`, `step_id`, `dependencies`, `policy`): C0 §1, lines 94-110 and 144-155, plus §2, lines 333-336.
- Materialization provenance (`successor`, `owner`, `owners`, `edge_before`, `edge_after`): C0 §2, lines 338-350 and 388-405; C0 §5, lines 1593-1622 requires authenticated materialization sources for undo/redo.
- Full request/reply/history shape preservation: C0 §1, lines 60-155; C0 §4, lines 703-715; C0 §5, lines 1563-1642.

## Scope boundary

This is source-only evidence. No product, test, expectation, caller, wire shape, pin, release, or gate change was made. Main owns the broader P2 gate; this worker classifies the supplied actual-extra family only.
