# D124 minimal source fact — Runtime step/command boundary mismatch

Disposition: BLOCKED_RUNTIME_BOUNDARY. No Agent product patch applied. This isolates ONE physical-edge guard root; it does not assert all four retained original failures share it.

## Production trace and proof

1. Production caller builds two genuine child track-create commands with existing capture/execute helpers. The existing native_child fixture registers create_runtime_commit_service() on RuntimeService and invokes service.commit_timeline. C0 ABI1 omission of label/steps synthesizes one complete step, preserving both commands in order; it cannot be split to sidestep validation (C0 §1).
2. Agent commit.py:1331-1335 executes at the verified base; _commit_patch.py:615-648 derives step source/output closures and attaches step-level commit.materialization records to the final ordinal. The two exact source/successor/companion-edge pairs correctly connect the step's initial shot/internal to its final shot/internal. Source roots, intermediate roots and final roots are all distinct. The added passing source test asserts these facts, the exclusive complete owner list and ordinal1 attribution.
3. Agent _commit_patch.py:1150-1156 requires the stored materialization record ordinal to equal the source step's final ordinal during authenticated inverse/history normalization. Moving these bindings to ordinal0 would invalidate established production history consumption; changing original grouping or dropping bindings/effects would lose behavior/custody. No such workaround is applied.
4. Runtime timeline_commit_auth.py:2868-2873 projects each sequential command input. At2910-2918 it passes command_inputs[ordinal] as `boundary` and the outer step input as `step_input` to validate_bindings.
5. The same validator correctly selects `bound = step_input` for commit.materialization at498-499, then uses that image for physical source revision/digest/owner verification. However its successor-edge block at565-580 rederives `before_rows`, before_shot and before_internal from `boundary` (the final command's intermediate input), not from the already-selected materialization source `bound`/`step_input`. With two edits those source edge tuples necessarily differ, although the binding correctly names the complete step's source. It rejects `provider successor differs from its authenticated physical edges`.
6. The new registered-provider regression reproduces that exact failure on a single exclusive child, with no media, virtual shared-shot identity, stale head, rebase or inverse prerequisite. Its companion source test passes. Thus the selected predicate's mismatched evaluation boundaries are proved without assuming that an error message assigns blame. The same source guard/frame is the retained separate original's first failure, but the original private binding pair is not available here and was not invented.

## Unapplied owner action

Owner: Runtime timeline_commit_auth.py validate_bindings successor-edge authentication. Review use of the authenticated materialization step input consistently for before-edge checks, keeping the actual step output, complete physical/source/successor/companion-edge/owner/digest checks, request attribution and all tamper rejection intact. This is a precise unapplied source location, not permission for a new endpoint, cache, caller authority, replacement validator or relaxed guard. The task expressly makes Runtime/auth source read-only, so no Runtime hunk is applied.

The additive behavior test retains accepted status, exact resulting track order and inverse restoration expectations, without skip/xfail/refusal expectations. It remains visibly failing until its owner fixes the production boundary. No currentGREEN is claimed. Independent protected review may decide whether to adopt the reproducer with that correction.

## Remaining retained failures

- scalar/compound: retained first guard is sequential allocation at Runtime auth2225-2227. Exact original physical/owner/allocation pairs remain UNKNOWN. Compiler virtual shared-shot IDs and physical IDs must not be conflated; no authority is inferred from this unshared reproducer.
- occurrence[True]: retained first guard resolves a removed occurrence alias at auth1764-1765 after the grouped inverse stage. Its original stage/write/effect pairs remain UNKNOWN. No stage, grouping, inverse capture or root order was rewritten.

The final read-only wholepath1405 report was consumed as published. All product sources, originals, D116 seed files, provider and runtime.lock.json are byte-identical to a4e016b6. Exact Runtime5e9ad/de2954 remains clean. No source-only source/route count is a passing acceptance count; core425 and REG14 remain unclaimed.
