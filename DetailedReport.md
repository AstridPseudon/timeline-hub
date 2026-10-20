# D04 retirement-prep report

## Result

Prepared the Runtime-only D04 deletion deliverable. The actionable map is
[`design/runtime-d04-retirement-ready.md`](design/runtime-d04-retirement-ready.md),
and only the D04 row was updated in
[`design/deletion-ledger.runtime.md`](design/deletion-ledger.runtime.md).
No Runtime product code or generated client was changed.

The current source still has the live collection publication dispatch at
`runtime_protocol/server.py:573-575` on Runtime
`a5a4f6b11a92ac8f01fbc7941db8a1470337ba9d`. The map therefore leaves D04 held
until App D01 and Agent whole-candidate/`clip.set-element` are qualified. It
separates App whole-parent, shot graph/popup, and bootstrap callers from Agent
whole-candidate, `clip.set-element`, and bootstrap fixtures; identifies the
exact future Runtime service/route/contract/client cut; preserves reads,
restore, closure, bootstrap, F1, and F2; and records text-binding,
candidate-promotion, and archive/recover gaps as OPEN rather than deletion
proof.

## Checks

Ran:

- `git diff --check` — passed.
- Read-only source/ledger inventory with `rg`, `sed`, `wc`, and Python line/row checks — passed; current D04 source, caller, fixture, and suite anchors are recorded in the design map.
- `git status --short` — only the intended new `design/` documentation files are present.

Not run:

- No Runtime, Agent, App, browser, live-socket, full, or integration test was run. This task changed documentation only and explicitly forbids a full suite. The map records the exact post-D01 targeted and central-service commands required before the later code cut.

## Limits and next step

The expected deletion size is a current line-span estimate (about 775 authored
Runtime lines plus generated operation/schema metadata); it must be rechecked
with `rg` after consumer ports land. The route must not be removed based on
refusal tests alone: the positive browser and CLI/SDK whole journeys, exact
retry/reload/inverse evidence, and zero legacy POST traffic are still required.
