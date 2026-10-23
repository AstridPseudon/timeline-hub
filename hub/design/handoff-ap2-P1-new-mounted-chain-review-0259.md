# P1 new mounted-chain source review — FAIL

Source `1372d5fe70dc57bf0ab03d4aebe0514db94d0b06` (`1372d5fe7`) against App
base `4394b74a1e3f0e8a2639112aa3bfbf1a3c4a0043` (`App4394b74a1`).

## Disposition

**FAIL — source not ready for the real P1 run.** The source collects exactly
two positive tests and all requested static checks pass, but the core mixed
chain is not represented correctly.

The positive lost-ACK case waits for the split response before starting trim
(spec lines 130–134). It then calls `route.fetch()` and receives/records the
trim response before retaining the route (lines 115–123), so the trim is
already committed when the Agent edit starts at line 175. This proves neither
a dependent trim queued behind a pending split nor a merged trim after an
intervening Agent edit. The retry assertion at lines 192–196 permits
`merged|rebased` and never compares the retry with the original trim envelope;
C0c requires the exact accepted `{data, receipt}` to be returned unchanged.
New v2 calls must not silently accept `rebased`.

The merged case does not assert merged status, `rebased_onto`, the Agent field,
or the final canonical closure. The refusal case checks a message and history
head/count but not structured conflict details or canonical preservation of the
original plus Agent edit. The split patch lacks assertions for authored
`SPLIT_AT=2`, `value.id` identity, order guard, and stable created-ID/id-map
continuity. Full step/dependency fields and the complete accepted/merged,
conflict, invalid, preview, and exact-retry wire shapes are not asserted.

The seed is manually constructed, using the existing direct genesis seam; it
does not consume the original `cases.json` fixture. The source worker's
repo-relative `design/ORCH-handoff-...` is not the required flat ORCH handoff.
The source handoff should be corrected at the true flat ORCH path
`design/handoff-ap2-P1-new-mounted-chain-source-0255.md`; no repository
process-file commit is requested.

## Checks

- Playwright list: PASS, 2 tests listed.
- `node node_modules/typescript/bin/tsc --noEmit`: PASS.
- Targeted ESLint: PASS.
- `git diff --check`: PASS.

No browser/socket/full/heavy/acceptance run was performed. Later selector:
`tests/e2e/local/three-products.p1-chain.spec.ts`, after the official 780
joined consumer/current-trim source, normal A2 outbox caller, and v2
Runtime/Agent client join are present.
