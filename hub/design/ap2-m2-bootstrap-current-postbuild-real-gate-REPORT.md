# AP2-M2 bootstrap current post-build real gate

## Result

**FAIL — unqualified.** The one permitted central run reached the repaired
hosted build, then the existing bootstrap-only wrapper's exact test selector
failed with `Error: No tests found` before browser execution. This is not a
bootstrap behavior pass.

The central service ran against App tree
`6444fffcaa606bfe83101ccb561c47fbd0d10ce4` (worktree commit
`f487c0ca9a7b916bf842dd7a2cb3fa442ebeda3e`). The public-export setup repair
is present in the composed source: `e401af721` is an ancestor and the
retired Composition fallback aliases are absent from `config/vite/vite.config.ts`.
The separately named gate35 ref `bc9dad558` was observed but is not an
ancestor; I do not claim that branch was merged.

## Central run

- Suite: `ap2-m2-bootstrap-committed-service-qualification`
- Request: `ap2-m2-bootstrap-current-postbuild-real-gate-ap2-m2-bootstrap-committed-service-qualification-1020230540-15749`
- Exact command selected by the service:
  `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-committed-service-qualification/run-bootstrap-committed-service-qualification.sh run "$PWD"`
- Result: exit 1, 81 seconds
- Hosted build: passed (`npm run build:hosted`); private build output and
  caches were verified by the wrapper.
- Browser: not started; the wrapper's exact bootstrap grep reported
  `Error: No tests found`.
- No rerun, broader private014 selector, public013 substitution, full suite,
  local browser/socket run, fallback revival, or setup edit was performed.

## Assertions

Normal create/init, null-head same-ID repair, reservation-before-create,
durable in-flight receipt, restart/exact retry, cancellation/stale generation,
draft preservation, raw opaque/order/closure/undo/zeroLegacy behavior, and
strict immutable guards are all **unverified** by this run. In particular, no
partial create-201/init-200 trace is being counted as a pass.

The prior custody-approved source evidence remains separate: 128 App tests,
12 native parity tests, exact 16-path scope, lint/typecheck, and selector
collection passed before this post-build gate. It does not qualify the real
browser consumer.

## Evidence

Bounded central evidence is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-current-postbuild-real-gate-ap2-m2-bootstrap-committed-service-qualification-1020230540-15749/`

The decisive lines are `normal014 App PRE-browser: private npm/Vite caches
and hosted build output verified`, followed by `[direct] hosted dist is
current; skipping the build` and `Error: No tests found`.

No physical dead-publisher cut is applicable after this failed/unqualified
gate; no whole-row deletion claim is made.

## Recommended next step

The orchestrator should reconcile the existing wrapper's exact selector with
the current source/test registration, then schedule a fresh uniquely selected
bootstrap gate only after that repair. This run must remain classified as
unqualified and must not be rerun under a broader selector.
