# Agent full current canonical union candidate

2026-10-20. PLAN 4.1 / D13 source candidate only. Manager freeze is pending the harness commit; this document does not authorize generation, consumer pin changes or endpoint retirement.

Source: branch `tl/agt-m2-producer-current-union`, worktree `/home/user/work/wt/agt-m2-producer-current-union`, based on `c456b3281497653cecf44f61acd6fa30565d83c8`. The harness must provide the new commit, then the manager must verify this exact schema hash before freezing the source ref.

Canonical path: `astrid/core/timeline/schema/edit-command.schema.json`.
Raw SHA256: `30da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd`.
Inventory: **48 definitions, 22 registered operation conditions** (20 native recipes plus inverse/restore).

Operations, in canonical order:

`clip.delete`, `track.set`, `shot.set`, `clip.set-params`, `clip.set-element`, `timeline.inverse`, `timeline.restore`, `clip.move`, `clip.add`, `occurrence.add-media`, `occurrence.swap-media`, `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`, `track.create`, `clip.set`, `clip.trim`, `clip.split`, `occurrence.duplicate`, `occurrence.delete`, `producer.guard`.

## Composition and preservation

Ported the reviewed `931d7ec56dadffc2efdc893fec80b4c4aadf8a8e` → `5c6467da34f53ce8d5111c0162eca5ff614380ed` bounded auto-placement delta, then the producer-only `1441bdf1a4795aad318cf27e8b26331146bc0d92` delta. Current registry, semantic rebase policy, selected-schema resolver, client/core/scene carry and durable requester session remain current. No old whole source trees were copied. No parent-media insertion/assembled-target variant was added.

The only canonical changes from c456b328 are five producer definitions, the `producer.guard` conditional, and optional closed `consumed` args on `placement.create` / `occurrence.add-media`. Every other definition/condition is structurally identical. `producer.guard` args contain only `pin`; original settled artifact digest is forwarded, never recomputed from requester serialization. Commands/rationale use numeric-value equality with booleans distinct. Runtime capture remains required at provider preparation, including preview. The original admitted base, commands and rationale persist through the existing requester outbox and exact retry.

Permanent tests: `tests/sdk/test_timeline_current_union_schema.py`; exact authored compatibility helper from Agent `ffa5325c69c575a883af25123f4d1c20a3706e4b` (`tests/sdk/command_schema_compatibility.py`, raw SHA256 `d54e1b83fc65ee44fbdcea57876dd040f919b553fff6aac1aa90a3e49bb31b78`). Each entire immutable schema below is checked, not a subset floor. Regressions drop every definition and registered operation individually, and reject narrowed numeric args. A separate exact comparison permits only the approved additions above.

| Immutable input | Source path | Raw SHA256 | Definitions / ops |
| --- | --- | --- | --- |
| Agent c456b3281497653cecf44f61acd6fa30565d83c8 | astrid/core/timeline/schema/edit-command.schema.json | 40ce6d81487f39236fbfb3adf13e6e0c3f43cfcc375b39b7badc32d65531fd4b | 43 / 21 |
| Runtime 6023cfb10307b4c0004642b5fa1995d72ba4f6d1, release 0.2.10 | contract/schemas/edit-command.json | 472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9 | 35 / 14 |

Both containment checks pass. Exact snapshots live under `tests/fixtures/current-union-command-schemas/`, extracted with read-only `git show` from those refs.

## Runtime qualification findings — activation remains held

**The brief's statement that Runtime6023cfb has a public producer guard schema is incorrect.** Its release metadata is 0.2.10 and its real producer port/checkpoint exists, but its public `contract/schemas/edit-command.json` has the ordinary 472622c4 hash above, with no `ProducerGuardArgs`, `ProducerAttemptPin`, `SettledProducerProposal` or `producer.guard` condition. Generated command types lack those producer types too. The generic unknown-op envelope can carry the guard; that is not explicit typed/closed guard publication. Do not claim normally generated guard/consumed public types from that release. Agent stays pinned to Runtime94114269 / 0.2.9.

`tests/sdk/test_timeline_producer_guard_runtime.py` creates real tasks, claims and immutable managed output settlements through public RuntimeService APIs, including two ordered settled data children and a captured media-free track-create proposal. No store rows are injected, no prepared provider simulates acceptance, and no validator/schema/port is replaced. Tested against an untouched `git archive 6023cfb...` using the existing Runtime locator, with the normal Agent semantic provider.

Four real changed-number/boolean/rationale/digest refusals pass without timeline-history changes. The positive Node numeric forwarding → preview → acceptance → restart/retry/one-shot → undo requirement **fails at preview**: `producer_dependency_unavailable`, “producer authority requires its guard record”. Runtime `RequestCommitPort._producer_captures` requires record command == original request guard, while normal Agent recording adds intent/resolved/reads/selections/bindings/created/expect/authorship metadata. Runtime `request_pin` simultaneously requires the bare five-field guard envelope, so adding those fields to the request cannot solve it. The original positive expectation stays `xfail(strict=True)` with a D13 restoration comment. `--runxfail` reproduces the failure. No accepted producer mutation/restart/undo is claimed. Runtime owner must reconcile that boundary without weakening original settled command/pin/dependency checks.

This fixture is an authentic **media-free generic producer** settlement. An authentic assembler proposal over its selected visual outputs, media insertion, requester-to-render handoff and production/App journey remain unqualified. No full suite, sockets, browsers or renderer were run.

## Bounded auto-placement limits

The review `design/agent-review-auto-guards-current.md` approves timing/lane/exclusive-owner guards only. Pool membership/absence for promotion and builder-only legacy pinnedShotGroups eligibility remain unrecorded; mixed pool/legacy flows stay held. Whole-row reads conservatively conflict with unrelated clip field edits. Parent births, append growth beyond the occurrence window, video unplace, and short-video/default-style preservation remain separate work. Unreleased incompatible `clip.add-media` / `timeline.assembled-target` variants are excluded. A rebuilt continuation is a new capture for requester approval, never an in-flight rewrite.

Targeted source evidence: 291 guard/numeric/settled/auto tests passed; 264 schema/outbox/provider/reservation neighbors passed. The Runtime run with `--runxfail` has 4 passed / 1 failed as explained above. Exact commands, final strict-xfail result and lint evidence are in `workers/agt-m2-producer-current-union/report.md`. Shared dependencies stayed read-only.

Next: harness commit; manager verifies hash/ref and freezes this full source; Runtime owner resolves the guard-record/public-schema gaps, normally regenerates from the approved full schema, and re-runs the original positive producer qualification before any activation or consumer pin change.

## Manager schema freeze — 2026-10-20 09:47 UTC

APPROVED CANONICAL SCHEMA SOURCE FOR NORMAL GENERATION ONLY:
- Agent source0a0ac7baaa74e15485b10bcbaa80eda1afe48c00 (tl/agt-m2-producer-current-union).
- Raw schema SHA25630da4fde84c328e7cb44035b50eb53fd2cd9637a14a0c948f4412f6469ce34bd, 48definitions/22ops as inventoried above.
- Independent manager check against currentefb96034: all prior definitions except EditCommand remain structurally equal; EditCommand only gains the producer.guard condition and keeps prior conditions. Five producer definitions are added beyond already-landed consumed additions.
- Superset tests555targetedPASS and actual4refusalPASS/1strictpositivegap retained; no activation/product-merge/endpoint-retirement/paired-green claim.

Runtime may normally generate this complete schema as a NEW release candidate with postF1/F2 fixes. Do not mutate historical94114269/0.2.9 or6023cfb/0.2.10 tuples. Actual producer positive remains blocked on Runtime guard-record matching (normalized recorded command versus original bare guard); fix that and re-run tests/sdk/test_timeline_producer_guard_runtime.py with this exact provider before Agent merge. Parent clip.add-media variants and pending retained element declaration args are excluded; later additions require explicit additive successor, never silent file replacement.
