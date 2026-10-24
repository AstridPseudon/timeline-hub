# E3 custody audit — corrected one-writer reduction design

**Status:** D81 / E-PLAN design-only, non-gating. This is the first return after the independent Sol2001 failure. It corrects the original audit using the recorded independent findings; the original audit and review remain unchanged. It authorizes no product-code, test, generated-file, pin, contract, integration, merge, source-branch, or ledger change.

The settled design is one authenticated Runtime writer. Agent supplies semantic execution and authoritative captures; App persists and transmits exact intent. E1 remains one shared Python module imported by Agent/Runtime as agreed, with no DSL, IR, code generation, new DTO, receipt memo, attestation ledger, or authority seam. The two tiny reductions below are **after ZIP only** and should be folded into that E1 cleanup if they are implemented at all. This audit does not claim that a standalone security refactor is worthwhile.

## Scope, source tuple, and caller correction

The source tuple used by the independent review is fixed and explicit:

| repository | audited source SHA | HEAD observed at verification |
|---|---|---|
| Runtime | `44917baf5976d6a655d582fafc63fde7b6cb242d` | same |
| Agent | `22d00393f7d944f1d01505637ca00b1995c3e158` | same |
| App | `f6a21c285267d6475816adbda74233907ac93911` | `860e9755c876ce510aabc5af0511ffe1886626f6` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | recorded mounted tuple |

App advanced during review only in five harness files; the cited product files and their hashes remain pinned to the audited App SHA. No moving App HEAD is substituted for those citations. The named source-check record contains the hashes and symbol/line resolutions for the fixed trees.

The actual mounted **product** save caller is:

```text
useTimelineSave.ts:319–323
  → createLocalSaveSession(..., send: provider.commitTimeline)
  → dataProvider.ts:751–767
  → client.ts:735–741
  → generated.ts:202–204 (commitTimeline)
  → Runtime POST /v1/projects/{project}/timelines/{timeline}/commit
  → commit_timeline
  → CommitExecutionCoordinator.execute
  → Agent/provider execution
  → durable accept, receipt, and history
```

`commitSession.ts:238–250` selects `operation.transmit` only for placement continuations; its ordinary branch uses `options.send`. `createTimelineCommandSession` has no production call in this mounted tree beyond its definition; direct callers are tests. Therefore it is not the all-path production caller and no reduction or removal is based on it.

The mounted **HARNESS** caller is separate: Runtime `local_worker_composition.py:467–515` creates a `RoleBoundCustodyBroker`, strips inherited `ASTRID_RUNTIME_CUSTODY_*`, injects reserved environment for the isolated process, verifies artifact identity, and binds the child; the Agent wrapper consumes and strips that environment before workload execution. `daemon.py:309–323` constructs the production launcher with its preparer/inspector. These are process-launch/source/role controls, not PRODUCT commit authorization. Harness success must never be reported as product receipt, history, or publisher authorization.

## Independent findings and exact corrections

| independent finding | correction in this revision | consequence |
|---|---|---|
| The audit named no finite reduction or net LOC target. | Retain exactly two source-backed sharing candidates: parent projection comparison at `timeline_commit_auth.py:2216–2224` and `2231–2239`; complete physical-owner enumeration at `521–526` and `2451–2458`. Give each a bounded estimate and require the final post-ZIP diff to count all additions, deletions, tests, and formatting. | The target is approximately 9 fewer nonblank production lines and only 1–5 fewer physical repository lines. If the complete patch is nonnegative, it is not an E3 reduction. |
| Native completeness was overstated. | State the current D62 truth: preserve all existing capture, order, binding, replay, ABI, and use-time refusal checks, while retaining the known submit-time native-coverage omission gap. The current source/test deliberately permits omission packets at submit, freezes ABI 2, and requires exact replay; do not turn that gap into a new attestation or refusal rule. | One writer removes competing acceptance authorities, not hostile or incomplete provider input. No native-completeness claim is made. |
| The mounted App caller was misidentified. | Use the `useTimelineSave → createLocalSaveSession → dataProvider → client/generated commitTimeline` chain above. Keep the placement-continuation `operation.transmit` branch distinct and make no caller-side removal recommendation. | The production reachability argument for the shared Runtime bodies is through the Runtime commit route, not the generic command-session hook. |

## Invariants retained without exception

The one-writer decision removes competing publication authorities. It does **not** remove any of these guards or make their evidence interchangeable:

- Runtime authorization remains bound to authenticated principal, project/timeline route, publisher, exact request/body scope, and HTTP `Idempotency-Key`. Service rechecks scope and hashes operation, path, publisher, and body; the coordinator performs durable lookup before and after provider execution.
- The v2 request/reply remains the C0 contract: exact project/timeline/base revision and publication pair; ordered commands with `schema_version`, `op`, `version`, `select`, `args`, and applicable `created`; label; complete steps with intent/tags/command ordinals/per-step patch and optional reads; merge; optional batch reads and dry-run; source/rationale/group annotations; and idempotency.
- `doc.patch` previous-value checks, absent-versus-null behavior, list membership/order rules, created IDs, declared reads, conservative atomic treatment, and guarded whole/per-step undo remain unchanged. No logical-ID or final-byte equality substitutes for physical history.
- Physical bindings retain phase/base/head/step/ordinal, physical reference, revision/digest, owner edges, successor continuity, exact before/after pairs, and complete ordered correspondence. Alias ambiguity, wrong successor, foreign owner/edge, and changed physical digest remain refusals.
- Allocation and ABA remain strict: reserved IDs cannot be reused, deletion/resurrection retains original provenance, inverse restore does not mint a fresh identity, and equal final values do not erase intervening history. CAS/head checks, idempotency, event links, owner/source guards, and exact catalog/reference projections remain authoritative.
- Undo continues to scan trusted accepted history, later writes/reads/selections/dependencies/bindings, and A→B→A cases. It does not write a current document snapshot as an inferred inverse.
- Durable acceptance continues to verify canonical data and digest, normalized commands and id map, base/previous/rebase identities, provider/compiler versions, recorder ABI, authoritative steps/dependencies, publisher, event metadata, receipt key/hash, sequence/event/creation metadata, and history/head links before the transactional publication.
- D47 remains in force: no mutable result/history/authority memo. D62 remains in force: persisted authentic `recorder_abi` 1/2 compatibility and its historical replay rules. The current submit-time native-coverage gap is documented, not silently upgraded.
- HARNESS custody remains separate: reserved-prefix rejection/stripping, broker binding, artifact/source identity, PID/incarnation, role/generation fences, and cleanup ownership remain. None is a product authorization or receipt proof; no harness LOC saving is claimed.
- Retired product writers stay retired and old routes stay refused. No compatibility writer, new DTO, overwrite path, or alternate authority is introduced.

## C0 request/reply boundary, unchanged

PLAN §3 R1/R2/R2r and C0 §§1–7 remain normative. The request examples in C0 §1 and replies in §4 were read for this correction. In particular:

1. The request carries exact scope and base identities, ordered commands, label, complete steps, merge mode, declared reads, idempotency, and dry-run. A free transform that does not declare reads remains conservatively scoped; omission is not evidence of no dependency.
2. Accepted and merged replies are `{data, receipt}`. `data` and the durable receipt retain accepted/merged status; exact base and previous pairs; accepted revision/publication; `rebased_onto`; complete canonical closure and digest; normalized commands; id map; provider/compiler versions; authoritative steps and dependencies; effective merge mode; authenticated publisher; annotations; event metadata; and `receipt.result == data`.
3. Conflict, invalid, and refused replies remain structured with status/reason, `code`, `path`, `hint`, suggested `command`, base/current heads, and conflicts as applicable. Existing refusal boundaries and messages are not collapsed into a generic error.
4. Preview returns full candidate data and digest, evaluated head, would-status, normalized commands/id map, steps, and merge mode with `receipt: null`; it reserves no IDs, history, event, or authority.

No field is dropped because Runtime is the sole writer. No receipt, history, or authority cache is added to make either reduction easier.

## Finite post-ZIP sharing candidates

These are implementation-review candidates only. They share implementation; they do not remove guards, change refusal semantics, combine distinct validation stages, or authorize a pre-ZIP patch.

### A. Share the parent projection comparison

The blocks at `runtime_protocol/timeline_commit_auth.py:2216–2224` and `2231–2239` are 18 physical/nonblank lines with the same computation and distinct refusal messages. A private helper may accept `result`, `following`, `identity_scope`, `manifest`, and the caller’s original message. It must:

- compute the expected parent identity;
- select every parent input pin;
- require nonempty pins and unanimous exact revision/digest equality;
- assign the expected revision exactly as today; and
- preserve both refusal messages byte-for-byte at their original validation boundaries.

Keep both call sites. Do not hoist the helper out of the promotion loop, combine it with the final created-root check, alter pin selection, or replace physical identity with a logical ID. The review estimate is about 9 helper lines plus 4 call lines replacing 18: approximately 5 fewer nonblank code lines and roughly 1–3 fewer physical lines after normal spacing.

### B. Share complete physical-owner enumeration

The loops at `timeline_commit_auth.py:521–526` and `2451–2458` total 14 physical/nonblank lines. A private helper may enumerate the complete owner list in occurrence order, retaining duplicates, from the boundary, physical reference, and already-selected occurrence rows. It must not use a set or `_physical_owner`, which returns only the first tuple.

Preserve caller-specific row retrieval exactly: strict `bound["parent"]["payload"]["occurrences"]` in `validate_bindings`, and `.get("occurrences", [])` in `_capture_owners`. Preserve the `shot is not None` condition, direct internal revision lookup, `_capture_document_images`, and the nonempty-owner refusal. Keep the existing set comparison and message in `validate_bindings`; do not strengthen it into an order comparison here. Do not fold inverse comprehensions at `1108–1112` or `1720–1724`; their coercion/lookup behavior differs.

The review estimate is about 8 helper lines plus 2 call lines replacing 14: approximately 4 fewer nonblank code lines and roughly 0–2 fewer physical lines after normal spacing. Empty, multiple-owner, malformed-row, duplicate, and owner-order behavior must be proven before implementation approval.

### Net reduction decision

The honest target is **about 9 fewer nonblank production lines and 1–5 fewer physical repository lines**, with zero planned changes to tests, schemas, generated clients, pins, contracts, or historical records. The 1–5 physical-line estimate is deliberately small. It is not a claim that one-writer architecture deletes large amounts of security code. If helper comments, formatting, or required tests make the final total nonnegative, report no E3 reduction and do not compress code or weaken tests to manufacture one. Because E1 is the shared Python-module/no-DSL effort, fold these helpers into E1 only if the post-ZIP implementation and proof already exist; otherwise leave the source unchanged.

## Reachability and proving order

The proposed Runtime bodies are reachable on the actual product path through `server.py:294–319` `_timeline_commit`, `service.py:2435–2509` `commit_timeline`/`_execute_timeline_commit`, `timeline_commit_execution.py:71–115` `execute`, the fixed provider factory, Agent `RuntimeCommitService.commit`, `RequestCommitPort.preview/accept`, and store validation. `preview` and `accept` both retain the shared validation. Historical exact retry re-enters the same auth and sequential-capture validators. This is the production route used by `provider.commitTimeline` above; it does not depend on `createTimelineCommandSession`.

After ZIP only, a proving worker must inspect the actual small diff and count additions/deletions across production and tests. Then it must run the unchanged authentication, sequential, history, inverse, forward-allocation, recorder-ABI, preview, Agent conformance, and App local-save controls named by the source-check and review records. It must cover real accepted, merged, conflict, invalid, refused, lost-ACK, restart, exact retry, foreign-owner, alias, allocation, ABA, physical-digest, complete-order, and guarded-undo cases. Harness custody/source tests run separately and cannot discharge product authorization or receipt gates. Broad, browser, localhost, socket, and full suites use the central test service under the task that implements the post-ZIP change.

No behavioral PASS is claimed here. The source-check record establishes source bytes, hashes, symbol/line existence, and measured duplication inputs only; named tests are proving targets, not executed results.

## Findings-to-correction acceptance checklist

- [x] Finite reductions are named at exact source locations, with a bounded 1–5 physical-LOC estimate.
- [x] Sharing implementation is explicitly distinguished from deleting or weakening guards.
- [x] D62 persisted ABI 1/2 and the known submit-time native-coverage gap are stated honestly; no native attestation is invented.
- [x] The actual mounted App caller is corrected and the placement-continuation branch is kept distinct.
- [x] C0 full v2 request/reply, exact scope/base/previous pairs, steps/reads/idempotency/dry-run, structured failures, and preview null receipt remain unchanged.
- [x] Physical bindings, alias/ABA/allocation/CAS/idempotency/event metadata, owner/source guards, D47, HARNESS/PRODUCT separation, and retired-route refusals remain explicit.
- [x] No product code, integration merge, new shared rule/ledger/authority, test weakening, or pre-ZIP implementation is proposed.

**Worker hours:** approximately 0.5–1 hour for this correction; implementation and proof of both tiny slices, if authorized after ZIP, approximately 2–4 hours.

**Risk:** low for this read-only correction; medium for the post-ZIP security-adjacent sharing patch because exact malformed-row, branch-message, and D62 coverage equivalence must be proven. The highest risk is treating shared code as removed custody or treating HARNESS provenance as PRODUCT authorization.

**Proving gate:** after ZIP, inspect the exact post-ZIP tuple, preserve every existing refusal/check and D62 behavior, run the unchanged named positive/forgery/replay/preview/undo controls plus App local-save and separate harness controls, and accept the E3 slice only if total physical LOC is actually negative. Otherwise retain the guards and report the slice as no reduction.

**Net line estimate:** approximately **−9 nonblank production lines / −1 to −5 physical repository lines**, subject to the complete post-ZIP diff; no larger saving is claimed, and no claim is made if the final total is nonnegative.
