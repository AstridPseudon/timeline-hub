# P1 fixture review handoff — 2026-10-23

## Verdict

**PASS for bounded test-only fixture fidelity; FAIL for execution readiness.**

Reviewed current App integration `9eda8e907` with source base
`3ad0e694` (`tl/ap2-P1-fixture-boundary-sol-0337`) and compared the imported
spec with Sol source `4fa831be1`. The only integration delta is the new
`tests/e2e/local/three-products.p1-chain.spec.ts`.

The corrected expectations are faithful to the current product boundary:

- numeric `hold: 8` selects the current App hold-clip split, so the left and
  right clips preserve source windows and authored app state while changing
  hold/at/ID;
- Source In is selected through the existing normal-DOM FieldLabel/input
  container, preserving the same real input intent;
- refusal compares the complete canonical post-refusal parent/closure to the
  accepted Agent move baseline, retaining the move's `app.astrid.fixed_start`
  and duration-based `for`, while preserving exact pre-Agent unaffected-state,
  opaque/null/foreign/order/mirror/closure checks.

The strict merged assertion, accepted/merged/refused paths, both pending and
interleaving boundaries, full v2 scope/base/commands/label/steps/patch/reads/
merge/dry-run/key and reply assertions, durable lost-ACK request/key/raw-reply
replay, created ID, guards, history, and legacy-route absence remain intact.
No legal fixture was invented, no success was converted to refusal/skip, and
no assertion was weakened.

## Execution boundary

**Do not call this READY, body PASS, H3 GO, or passing behavior.** The actual
production caller remains unexecuted and is still blocked: current
`timelineLocalSaveHandoff` omits authoritative reads/intent metadata, so
`localSaveSession` conservatively emits this omitted-read `doc.patch` with
`merge: 'atomic'`. The same-parent Agent edit therefore prevents the required
merged trim from landing. The merged expectation remains strict by design.

No fake transport, request rewrite, forced `reads: []`, new port, executor,
semantic executor, or product change was introduced. The route interception is
only the existing proof's hold/release of real Runtime responses; retries use
the exact persisted request body and idempotency key.

This two-test chain does not exercise invalid `code/path/hint` or preview
`would_status`; neither variant was present in Sol source `4fa831be1`, so no
coverage claim is made for them.

## Evidence

- Playwright exact list — **PASS**, 2 tests in 1 file.
- `npx tsc --noEmit` — **PASS**.
- Scoped ESLint with `--max-warnings 0` — **PASS**.
- `git diff --check` — **PASS**.

No browser, socket, body, full, heavy, or central-suite run was performed.

Next step: App owner supplies the existing authoritative read/intent seam, then
the central test service runs this exact spec and only then can P1/H3 execution
readiness be reconsidered.
