# D141l independent read-only validation

Result: `FAIL` for the completed author result. Source qualification is
`SOURCE_QUALIFIED_UNDER_MAIN`; executable receipt qualification is
`NOT_EXECUTABLE_WITH_RETAINED_ORIGINALS`.

## Direct checks

- Read `/tmp/.../PLAN.md` before review — PASS.
- Read all five author evidence files (`measurement.json`, `witnesses.json`,
  `source-manifest.json`, `validation.md`, `handoff.md`) — PASS.
- Read the named controller admission, retained normal/pristine result and
  receipt records, and the closed manager round logs `20261026T0035Z.log` and
  `20261026T0110Z.log` — PASS.
- `git rev-parse HEAD HEAD^{tree}` in this assigned Composition worktree —
  PASS: `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` /
  `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
- `git status --short --branch` — PASS; assigned worktree was clean before and
  after the review.
- `git diff --check` — PASS.
- `sha256sum` over all named JSON, result, test-run and manager-log inputs —
  PASS; exact values are in `source-manifest.json`.
- Direct byte-offset reads of the retained manager logs — PASS; the exact
  table rows, offsets, source hashes and timestamps are in `review.json`.
- Direct arithmetic — PASS:
  `5433016320 - 4839120896 = 593895424`, then
  `max(4600000000, 4000000000 + 593895424 + 200000000) = 4793895424`.
- Read-only inspection of installed `/home/user/timeline-hub/hub/kit/bin/test-run`
  and `/home/user/timeline-hub/hub/kit/bin/d141-validate-receipt.py` — PASS;
  hashes and the exact receipt/witness rules are in `source-manifest.json`.
- Search of only the named retained logs/result/evidence paths for original
  `Avail` witnesses — PASS: none found. The retained rows are full multi-line
  `df -B1` tables with `Filesystem` columns.
- Read runtime `contract/commit-v2.md` sections 1–5 and 7 — PASS; no request,
  reply, undo/history, or C0 shape was changed by this review.

## Corrected qualification

MAIN05:20 authorizes the retained controller dispatch admission as the bracket
start. The normal full run is bound to App HEAD
`867cb2737af1b46dc608c7cd37c349e920fe9422` and tree
`2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`; it starts at `00:43:38Z`. The
admission record is `5,433,016,320` bytes at
`2026-10-26T00:42:39.754967+00:00`. The exact in-body minimum is
`4,839,120,896` bytes at `00:48:37Z`, manager-log byte offset `1157219`.
This supports `X=593,895,424` and floor `4,793,895,424` bytes.

The pristine full run was checked as well. Its exact timestamped in-body
minimum is `4,938,567,680` at `01:15:43Z`, offset `1276493`; the timestamped
bracket is only `11,431,936` bytes. The earlier `4,951,003,136` row is retained
at offset `256541` but has no recoverable event timestamp. The global maximum is
therefore the normal run’s corrected `593,895,424` bound, not the lower
`216,776,704` ordinary in-body bracket and not a continuous-peak claim.

Gaps remain unobserved: 44 seconds before the normal first sample, 10m35s before
the first timestamped pristine sample, and the intervals between/after samples.

## Explicitly not run

No private test-run, validator invocation, fabricated live ID, receipt attach,
new `df` consumption, body, tests, TypeScript, lint, import, browser, localhost,
or full-suite request was run. No repository, product, test, kit, pin, queue,
registry, hub, or Git state was mutated.
