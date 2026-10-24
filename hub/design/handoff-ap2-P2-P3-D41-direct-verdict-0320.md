## D41 P2/P3 direct verdict

- Source/no-weakening: **PASS**. App804/tree8437 is unchanged; Agent079/tree2deab and Runtime37eb/treebe411 identities match. Original eight P2 selectors, Gate5 body, guards, waits, native/history setup, reload/undo tails, and legacy-route assertions remain intact. No tracked edits.
- Direct-file custody: **PASS** for the three published P3 files only. All parsed successfully and matched exact sizes/hashes:
  - `d21-environment.json`: 5,230 B, `09c8735d…b94df26`
  - `mounted-readiness-diagnostics.json`: 652 B, `eea4457b…f84c9ce`
  - `mounted-bootstrap-lifecycle.json`: 12,494 B, `679cc75e…8cee77b`
  
  Nested type/enum/bound/security checks passed. P2 artifacts were not claimed or invented.

### P2 verdict: NO-GO

Run `app-readiness-D41-caller-sol-0250-full-e2e-three-products-1024030427-12221`: exit 1, 501 s.

- Readiness preflight passed; its 37.4 s process scope is not equated with the cause report’s 17.4 s test scope.
- Original eight: 3 failed, 5 not run.
- Element edit failed first: expected `applied`, received “captured timeline head changed or is missing.”
- Popup ADD and parent move each timed out at 90 s.
- Native seed/history setup passed; this does not make the gesture body green.

### P3 verdict: NO-GO

Run `app-readiness-D41-caller-sol-0250-ap2-P3-gate5-h6-0348-1024030427-3362`: exit 2, 147 s.

- Native21/history setup passed.
- Mandatory mounted readiness failed: outbox read was `unknown`, expected `verified`.
- Gate5 selected 1, executed 0: **NOTRUN**, not a pass or failure result.
- Daemon/provider import metadata remains UNKNOWN; do not upgrade declared launcher metadata into daemon-import proof.

### Verification commands

- `TMPDIR="$TMPDIR/ap2-p2-p3-local-checks" /opt/node20/bin/node --import tsx tests/e2e/local/mounted-readiness-safety.test.ts` — exit 0, 12/12 passed.
- `TMPDIR="$TMPDIR/ap2-p2-p3-local-checks" /opt/node20/bin/node --import tsx tests/e2e/local/d21-environment.test.ts` — exit 0, 7/7 passed.
- `git diff --check` — exit 0.
- Fixed App source comparison — no diff.
- Frozen Agent/Runtime object identity checks — passed.

No browser, service, full-suite, reproduction, or causal extraction was performed. P1 GO and P4 remain separate evidence; neither implies P2/P3 GO.

Next owner boundary: App Sol0309 and the named independent reviewer classify the failures and own any narrowly scoped source work. Proof should only re-verdict one newly authorized pair; no alternate route or changed assertion is justified.