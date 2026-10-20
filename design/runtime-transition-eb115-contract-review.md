# Runtime transition `eb115` bounded contract review

## Verdict

**MISMATCH — do not approve or activate this contract yet.**

The paired `clip.set` carrier and the distinction between explicit paired
removal and legacy transition-only clear are sound. The exact Agent candidate
still diverges from Main and Runtime in two acceptance-critical ways:

1. It records an incoming predecessor but does not enforce Main's same-track
   adjacency or shortest-adjacent-clip duration fit.
2. Its selected-pack `clip.set` path accepts the caller-supplied `schema_source`
   after exact descriptor validation, but does not apply the existing retained
   P1 authority fence used for selected `clip.set-params` edits. A same-reference
   update can therefore present a later P2 pin.

## Reviewed identities

- Agent candidate: commit `eb115db81ac2c24b182fe6873fbd883da851571e`.
- Agent candidate tree: `10ea4f3adb085adf7589239f852248cc9811eeb4`.
- Candidate schema blob: `95d7f4eb90a3afe8b3b6c554f31ac2cce4300d44`.
- Candidate schema digest asserted by Agent: `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`.
- Frozen Agent independent review read once: `design/ap2-m2-transition-explicit-contract-review-REPORT.md`.

## Evidence

### Incoming-neighbor validation

Agent's `_transition_set` reads the selected predecessor at
`astrid/sdk/timeline/_clip_scalar_commands.py:142-152` and checks that the clip
has a track and safe positive frame count at `:128-138`, but it never compares
the predecessor's end to the destination start and never checks the duration
against either neighbor's extent.

Main's literal implementation requires same-track adjacency with the existing
`0.001` tolerance in
`/home/user/work/app/src/tools/video-editor/runtime/element-adapter.ts:175-189`
and `:345-357`, then rejects a duration longer than the shorter adjacent clip
at `:231-243`. Runtime's canonical incoming interpretation independently
requires the incoming overlap to be positive and no larger than the transition
duration, with that duration no larger than either clip, at
`runtime_protocol/visual_seam.py:363-391`.

Therefore the Agent candidate can accept an incoming transition that Main
would refuse and that Runtime canonical seam analysis reports as an invalid
overlap. Recording `transition.predecessor` is not a substitute for enforcing
the guarded neighbor relation and fit.

### Retained selected-pack pin authority

Agent's transition path calls `_selected_schema` from
`astrid/sdk/timeline/_clip_scalar_commands.py:118-120`. In the corresponding
commit resolver, `resolve_selected_param_source` is invoked only for
`clip.set-params` at
`astrid/sdk/timeline/commit.py:513-524`; `clip.set` is handled by the generic
exact requested-pin branch at `:525-532`. Thus a transition update carrying
the same `elementRef` can supply P2 and pass exact P2 descriptor validation,
even though ordinary same-reference updates must retain the accepted first P1.
The existing inverse additions do not repair this missing forward authority
check.

### Clear semantics that do match

The candidate correctly keeps legacy `clear: ['transition']` separate: the
handler's `:211-219` leaves both `elementRef` spellings untouched. The explicit
paired clear requires `transition` at `:183-186` and validates reference kind,
id, and revision against the stored transition at `:154-176`, then removes the
legacy alias at `:211-214`. This preserves unrelated effect/component refs and
provides the requested exact associated-removal guard.

### Runtime artifact status

The current Runtime carrier is not yet the Agent candidate contract:
`runtime_protocol/timeline_commit_types.py:111-112` permits only
`hold`, `asset`, and `transition` in `clip.set` clears, while
`runtime_protocol/schemas/timeline-commit-bundle.json:611-640` still describes
transition authoring as outside v1. No Runtime schema, DTO, or public pin was
changed by this review.

## Focused evidence command

```text
python -m pytest -q tests/test_visual_seam_admission.py -k 'test_incoming_crossfade_never_grants_an_unrelated_parent_effect or test_unknown_transition_does_not_excuse_overlap or test_overlap_is_allowed_only_with_valid_transition'
```

Result: **4 passed, 79 deselected** (one existing `PytestConfigWarning` for the
environment's unknown `timeout` option). No full suite, socket suite, or
browser run was performed.

## Required disposition

Keep the existing `clip.set` carrier and clear split, but do not qualify this
pair until the Agent command enforces Main/Runtime incoming-neighbor membership
and fit, and the selected-pack transition path reuses an existing exact P1
authority/binding proof for same-reference updates and inverse/replay.
