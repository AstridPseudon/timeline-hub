# D120 full P2 report

Submitted exactly one normal D66 `p2` run on the qualified tuple.

- Preflight: PASS
- Service: `app-pin-34d46445-d73-p2-34d46445-submit-1025114516-11251`
- Terminal: FAIL, exit 1, 643s
- Readiness: 1 PASS
- Original: 5 PASS, 2 FAIL, 1 NOTRUN

Failures:

- SWAP: `three-products.p2-popup.spec.ts:495`; HTTP 409 `history_unavailable`.
- Element edit: `three-products.p2-elements-assets.spec.ts:1052`; completion did not reach `applied`, page closed, backend outcome UNKNOWN.
- registerAsset: NOTRUN at `three-products.p2-elements-assets.spec.ts:1133`.

Passing gestures: ADD, parent move, both transition clears, automatic placement.

Exact tuple, receipts, source hashes, recipes, XML/manifest hashes, and bounded diagnostics:

- [submission.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D120-full-P2-D111b-1145/notes/submission.json)
- [terminal.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D120-full-P2-D111b-1145/notes/terminal.json)
- [terminal.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/notes/terminal.md)
- [p2-submit-plan.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/submission/full-p2/p2-submit-plan.json)

No App source changes, retries, collectors, or second body were made. The tuple is NO-GO; manager review is required for next steps.