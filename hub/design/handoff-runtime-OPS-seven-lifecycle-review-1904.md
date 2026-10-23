# Runtime handoff: OPS seven-lifecycle review (1904)

## Result

**PASS** for exact private proposal fidelity; **FAIL/NO-GO** for any current
live normal lifecycle command; **UNKNOWN** for HOST idleness and legacy-run
lease coverage.

The reviewed packet is exactly seven generated registrations at
`tests/suites.conf` lines 162–168 plus seven matching env files. Patch SHA-256
is `5984d485a2840c780c00a6461e3d6cb98462cef21428e8a9bbc233d18bf18b6a`;
source manifest SHA-256 is
`acb5cf9d2e4f989650e9dfd6eba98f53e89d45db835eeafad1f693091f777678`.
Private hash/JSON/flat-cmp, patch dry-run/apply, and invariants all pass.

The exact targets are:

1. `agent-remotion-ap2-p1-f611-1346-nodes`
2. `agent-remotion-ap2-current-8c355-1402-nodes`
3. `agent-remotion-ap2-current-8c-cfa-1415-nodes`
4. `agent-remotion-ap2-current-583-cfa-1451-nodes`
5. `agent-remotion-ap2-current-583-9ce-1513-nodes`
6. `agent-remotion-ap2-current-98ef-259-1608-nodes`
7. `agent-remotion-ap2-current-bac-d9e-1643-nodes`

Protected current 1743, P1/P2/P3/F/template inputs, all unrelated rows, and
the unrelated P3 position-36 race are preserved. Seven historical REFUSE
references and nine process errors remain STOPPED. No live mutation is
authorized.

## Permitted next action and missing coverage

Keep this exact proposal as input to the combined new-store proof. Do not
apply it live, retry refused targets, retire directories, waive guards, or
adopt refused targets as deletion authority. Existing unknown legacy/unleased
runs remain protected.

Core-1858 is now published source, not an absent design, but it is not yet a
qualified production install: tests/review and actual caller installation are
pending. Runtime 2a9 has no installed `bench_store` or caller reference.
Existing request-child-venv/request-runtime remain legacy maker callers, and
existing test-run lacks exact managed registration resolution and inheritable
flock FD coverage through command descendants. A current normal command is
therefore not qualified.

After qualified install, the smallest supported sequence is: build/verify
dedicated-store entries with exact child/runtime keys and final-path custody;
publish exact suite/env/index registration transactionally; resolve the exact
repo/suite/base-command row; acquire all managed names under one mutex and
retain stable lease FDs through the supervised command and descendants; then
prove journal recovery, latest-two-plus-leased retention, and preservation of
unknown legacy material. Only then can a separately reviewed managed
migration/adoption or eviction operation be considered. No `/proc` waiver or
invented HOST-idle proof is valid.

Full C0v2 schemas and frozen34e are unchanged. No product tests/typecheck/lint
were applicable to this proposal-only review.

See the worker report for exact row/env hashes and command results:
`../workers/rt-OPS-seven-lifecycle-review-1904/report.md`.
