# VW-D09a report

Mapped one remaining fallback: `motion/model.py:mouth_state`.

Verdict: no source/test patch. Public13 `am-presenter/motionAt` → `scene.ts:diagnostics.motion.mouth` is equivalent only for the bounded normal input (valid finite word spans, integral in-range seed, exact retained source and clip-local frame). It cannot replace the remaining fallback because `render_curves` reaches `_presenter_props`/`props_at` without source-bound public rows, and `render_lipsync` must retain private behavior for default/partial/raw-invalid/missing/mixed/stale/forged/UNKNOWN facts.

Exact map, source lines, clock/binding contract, refusal/UNKNOWN behavior, existing positive/negative tests, qualification dependency, and limits are in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-d09a-one-default-fallback-public-map-0816-REPORT.md`

Product worktree remains unchanged.
