# App P2/P3 farm-readiness handoff

This is a collection/readiness handoff only. It is not P2/P3 proof, does not
claim v2 readiness, and does not certify an integrated App/Agent/Runtime or farm
run. No product source, test, generated file, pin, launcher, selector, suite
budget, or process was changed for this handoff.

## Source and scope

The inspected App head is:

```text
commit 8b979bd2139c96e029dbc42be9a47f4309c8ee37
tree   e5cde440ce2f31bd0e20dbf2bb7d9d5cbd9d09da
branch tl/ap2-P2-P3-farm-readiness-sol-fix (based on tl/integration)
```

The current App source is clean before and after this document-only correction.
Runtime integration was read statically at commit
`992136137ce03bad618aea89f45de584ee0b0781`, tree
`4002a708474f09f0824d5a411b328660fbf8bcc7`, only to verify the current history
pagination API. This is not an integrated run pin. Record the exact full App,
Agent and Runtime SHAs actually used, the integrated Runtime `/commits`
implementation, and the farm seed/project before claiming qualification. Do
not infer them from a branch name or from a browser door log.

The existing runner is `npm run test:e2e:three-products`, configured by
`playwright.three-products.config.ts` with `testMatch: 'three-products*.spec.ts'`,
one worker, and a 300-second timeout. It is a real App + Runtime + Agent
journey and was not executed here.

The original successful journeys remain migration obligations. They must be
migrated as passing tests with their behavior assertions retained. Do not add
`it.fails`, `xfail`, skips, weaker expectations, or a refusal expectation for
the old-route cases. The existing snapshot-route cases are baseline/migration
coverage until A2 moves them to the v2 path; they are not a reason to weaken
their successful behavior.

## Required v2 compatibility defaults

Contract `design/commit-v2.md` §1 requires new producers to supply a nonempty
`label` and nonempty `steps`. For existing ABI-1 callers, omitted `label`
normalizes to `"Timeline edit"`; omitted `steps` synthesizes one step with
`id: "edit"`, `label: <normalized commit label>`, `intent: ""`, `tags: []`, and
`command_ordinals` containing every command index in order. The provider derives
that step's complete `patch`. Explicit empty/null `label` or `steps` is invalid;
omission is not equivalent to `""`, `[]`, or `null`. Omitted `merge` defaults to
`"fields"` (the allowed values are `"fields" | "atomic"`); omitted `dry_run`
defaults to `false`. The conservative patch-read rule can make the effective
`merge_mode` atomic. These are required contract behavior, not evidence that the
current App DTOs or provider implement v2.

## Current v1/native inventory, not v2 evidence

The App integration is still on the older DTO/helper shape. In
`src/integrations/runtime/timeline-commit-types.ts`, the current generated
types show:

- `CommitRequest` has no v2 request-level `steps`, `merge`, or `reads` fields.
- `CommitAccepted.status` is `accepted | rebased`; v2 uses `merged` for a
  disjoint-head success while retaining `rebased_onto` as the landing-head pin.
- `CommitAccepted` has no v2 complete `steps` or effective merge metadata.
- `Recorder` has `commands`, `undo_of`, and `restored_from`, but no
  authoritative `records.steps` or `undo_steps`.
- `HistoryEntry` has no v2 history `steps`, requested/effective merge fields, or
  declared reads.

The current test helper accepts `accepted|rebased` at
`tests/e2e/local/three-products.spec.ts:803-808`. The M1 move and Gate-5 journeys
assert `rebased` at lines 1050 and 1186 respectively. Line 1352 belongs to the
ordinary-extension batch journey (starts at 1239); line 2001 belongs to the
occurrence-duplicate journey (starts at 1888). Mixed editing starts at 2070.
The stale `rebased` observation remains valid for those assertions.

The current `history()` helper at lines 818-832 already follows `next_cursor`
with `limit=50`. GET
`/v1/projects/{project_id}/timelines/{timeline_id}/commits` accepts `limit` and
`cursor` and returns `items`, `head`, and `next_cursor`. The first page selects
the current head; each opaque cursor binds the scope and that fixed through
head for subsequent pages. The helper relies on this binding but does not
assert that each page's `head` equals the first page's `head`. Runtime sources:
`runtime_protocol/server.py:535-545`, `service.py:2502-2529`, and
`timeline_commit_store.py:282-322`. There is no current `through` query
parameter. Contract §7's chosen-through requirement uses the existing cursor
behavior; any future explicit query would be pending API work, not an available
route. Existing helper presence, current native command records, and current
v1 `rebased` journeys are not v2 execution evidence.

For v2 qualification, every accepted App gesture and inverse must assert the
authoritative history entry joined by its publication ID, not merely inspect
the network body or a door/audit log. The future test must:

1. Capture the network `POST` to the Runtime `COMMITS` route for the gesture,
   assert the expected command/body and idempotency behavior, and assert zero
   old-route writes (`SAVES`, `/composition-revisions`, or equivalent legacy
   snapshot POSTs).
2. Read Runtime `/commits` using `limit` and then its returned `next_cursor`.
   Capture the first page's `head`, follow every opaque cursor, and assert that
   every page retains that head; do not start a fresh first-page read mid-walk
   or add a `through` query. Join the new history entries to network
   publications by `publication_id == receipt.receipt_id`.
3. Assert the v2 result status (`accepted` at the requested base or `merged`
   on a disjoint later head), `intent: "recorded"`, non-null `records`, and
   `receipt.command_kind: "timeline.commit"` for normal edits. Reject any
   post-bootstrap `legacy_unknown`, `records: null`, or
   `parent_composition.publish` entry.
4. Assert the exact contract §7 history fields: `label`, authoritative
   `publisher`, `intent`, `merge` (requested), `merge_mode` (effective), `reads`
   (declared), `steps`, `records`, and `receipt`; inspect `records.steps`,
   `records.commands`, `records.undo_steps`, and `records.undo_of`. Assert step
   IDs, labels, intents, tags, command ordinals and complete provider patches,
   including verified step reads and authoritative dependencies. For
   whole-commit undo, assert `records.undo_steps: null`. Preserve the command
   records' authoritative reads, writes, bindings, dependencies and derived
   writes.
5. Compare the canonical before/after documents using an explicit allowlist of
   intended field deltas, then reload/reopen and verify the landed state. Click
   the mounted Undo action and assert a guarded `timeline.inverse`, its
   publication-linked history record, and the expected restored document.

### P2 gesture inventory

These are the current operation/selector rows and their intended allowlists.
They are v1/native baseline rows until U4p, R1, A2/A3, R2, and Runtime integration
supply the v2 metadata and authoritative history checks above.

| Gesture and expected command | Current source | Intended delta | Current qualification state |
| --- | --- | --- | --- |
| App track label: `track.set`, `parent/track:V1`, label only | `three-products.spec.ts:408`, Agent-to-open-App case | `config.tracks[id:V1].label` only | Existing mixed Agent/App case; no v2 Runtime-history, reload, and Undo proof for this row. |
| Single move: `clip.move`, `parent/clip:<appClipId>`, `args.on` | `three-products.spec.ts:1002`, `M1 real gesture` | Selected parent clip authored `at` only | Existing retry/reload/Undo behavior; status/history still use v1 shape. |
| Ordinary extension batch: five `clip.move` plus five `clip.set` commands | `three-products.spec.ts:1239`, `M2 ordinary extension batch` | Listed parent/occurrence clip `at`/`hold` fields only; Agent label is a separate dependent intent | Existing recovery/restart/Undo and `wire.legacy=[]`; no v2 history classification or complete step assertions. |
| Native manual ADD: `clip.add-media`, selected verified media and requested placement | `three-products.spec.ts:1410`, `M2 real mounted manual video drop`; producer `parentClipAddMediaPort` in `src/tools/video-editor/commands/commitSession.ts:433` | One new media asset/clip row with authored track, placement, type and asset identity; no unrelated existing-row or opaque-data mutation | Existing refusal/recovery/retry/restart/Undo; popup/native path still needs v2 history and explicit field comparison. |
| Occurrence duplicate: `occurrence.duplicate` | `three-products.spec.ts:1888`, `M2 native occurrence duplicate` | New occurrence/shot and copied authored fields only; source occurrence unchanged | Existing retry/restart/Undo; no v2 Runtime-history classification. |
| Native transition clear: `None`, single and bulk | `three-products.spec.ts:2253` and `2331`; `expectTransitionClear` helpers around 2200 | Only the selected transition's raw mirrors, or explicitly selected transition IDs in bulk | Existing exact retry/reload/restart/conflict/Undo; v2 command/step/merge/read history is absent. |
| Selected element/parameter: `clip.set-params` or supported element command | `three-products.selected-param-dev.spec.ts:25`; capture in `src/tools/video-editor/commands/elementCapture.ts:215-270` | Selected clip's admitted parameter/element fields only; refusal creates no commit | Supporting DEV coverage, not seeded three-products farm proof; A3 must qualify the same path. |

Popup SWAP remains missing. The implementation surfaces are
`parentClipSwapMediaPort` in `src/tools/video-editor/commands/commitSession.ts:509`
and `captureParentClipSwapMedia`/`finishParentClipSwapMedia` in
`src/tools/video-editor/commands/parentClipSwapCapture.ts`; the expected
command is `clip.swap-media`. The Agent CLI swap in the track-label case is not
App popup-swap evidence. A3 must provide the real popup gesture, with an
allowlist limited to the target clip's asset replacement and the selected old
and new media identities, followed by the same reload and guarded Undo checks.

## P3 Gate-5 journey

The candidate is `tests/e2e/local/three-products.spec.ts:1115`,
`M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local
gesture, exact retry, restart and undo preserve intent`.

Its first drag from the seeded position to `5` (lines 1119-1124) is a fixture
normalization/reset. It must be reported separately and is not the adversarial
sequence. The adversarial sequence begins after that reset and is:

```text
App A accepted
→ independent Agent C
→ lose A's durable acknowledgement
→ author dependent App B
→ reload
→ restart Runtime
→ exact A key/body/receipt retry
→ recover dependent B at the canonical A head
→ guarded Undo of B
```

C must remain in the final document. B must be sent with a fresh key and the
canonical predecessor while the exact A retry is byte-identical and idempotent.
The final inverse must be linked to B by `records.undo_of`, preserve C, and
show the v2 inverse step metadata. The initial reset must not be counted as an
adversarial publication when comparing the network and pinned Runtime-history
intervals.

The current candidate already exercises persisted outbox state, reload,
Runtime restart, exact retry, dependent ordering, canonical reads, immutable
closure, and mounted Undo. It still asserts v1 `rebased` and only partial
command-record metadata. The future v2 proof must snapshot pinned Runtime
history before A, after A/C/B recovery, and after Undo, joining each new
entry to the corresponding publication ID and asserting the full field list in
the v2 checklist above.

The separate bootstrap case at `three-products.spec.ts:1642` intentionally
has a baseline `parent_composition.publish`/`bootstrap` entry with
`records: null`. Exclude that pre-gesture baseline from the post-bootstrap
legacy check; the native initialization and every later gesture must be
`intent: "recorded"` with non-null records and the expected command kind.

The older snapshot-route cases at lines 495 and 665 are migration coverage.
Retain their successful behavior assertions and migrate them to the commit path
as passing tests; do not convert them to strict expected failures.

## Dependencies and missing work

- R1/Agent (plus Runtime store integration) must provide `doc.patch` semantics,
  previous-value checks, declared-read handling, membership/order conflict
  detection, and inverse handling before these v2 journeys can qualify.
- U4p/App must adopt the regenerated U1 schema/client, following U1 and U3;
  the current App DTOs do not establish v2 request/reply/history support.
- A2 must route App gesture writers through the v2 commit/outbox path, preserve
  dependent-intent chaining, exact retry, refusal/revalidation, reload recovery,
  and canonical reply handling.
- A3 must qualify popup ADD/SWAP, placement, element/parameter, and
  `registerAsset` consumers through A2. Popup SWAP is currently absent.
- R2/Agent must provide integrated guarded whole/per-step Undo, including the
  later-history scan, A→B→A protection, and v2 `undo_steps`/`undo_of` records.
- Runtime must expose authoritative v2 `/commits` history with pinned/cursor-safe
  reads and complete labels, steps, merge/read metadata, publisher, command and
  undo records. The App cannot establish this from its current DTOs alone.
- Integration must provide exact full Agent/Runtime SHAs and the required farm
  seed/project. No new API, route, selector, launcher, or test budget is
  invented by this handoff.

## Runner registration

The central suite configuration currently contains:

```text
full-e2e-three-products  npm run test:e2e:three-products
e2e-m1-gesture           npm run test:e2e:three-products -- --grep 'M1 real'
```

There is no P2-specific or P3-specific named suite. The existing
`e2e-m1-gesture` selector is not P2-only: it discovers the three tests whose
titles contain `M1 real` (the move journey, Gate-5 journey, and dependency
conflict case). The future farm owner must register or otherwise document the
appropriate P2/P3 qualification entry after the v2 cases exist. This worker did
not modify `suites.conf`, the selector, the launcher, or the test budget.

## Evidence collected here

Static checks for this correction:

- `git status --short --branch` — App clean before and after correction.
- `git show -s --format='commit=%H tree=%T branch=%D' HEAD` — recorded
  `8b979bd2139c96e029dbc42be9a47f4309c8ee37` and tree
  `e5cde440ce2f31bd0e20dbf2bb7d9d5cbd9d09da`.
- `git -C /home/user/work/runtime show -s --format='commit=%H tree=%T branch=%D' HEAD`
  — recorded the Runtime commit/tree above for static API inspection only.
- `sed`/`rg` reads of PLAN v2.1 §3, the second FAIL review, and current
  `design/commit-v2.md` §§1,7 — verified defaults, dependencies and exact history
  wire names. `nl`/`rg` reads of App `timeline-commit-types.ts:68,80-94`,
  `three-products.spec.ts:803-832,1050,1115-1136,1186,1239,1352,1888-1900,1990-2006,2070`,
  and Runtime `server.py:535-545`, `service.py:2502-2529`,
  `timeline_commit_store.py:282-322` — confirmed the v1 DTO/status inventory,
  corrected journey citations, fixture reset, and existing cursor-bound API.
- `cat playwright.three-products.config.ts` and
  `rg -n 'full-e2e-three-products|e2e-m1-gesture|P2|P3'` against central
  `tests/suites.conf` — confirmed the existing runner and missing P2/P3 named
  registration; no configuration changed.
- `git diff --check` — passed; App source/test diff is empty.

Earlier list-only evidence retained from the prior handoff/review (not rerun
for this correction):

- `npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts tests/e2e/local/three-products.selected-param-dev.spec.ts`
  — listed 14 tests in 2 files; list-only, no execution.
- `npx playwright test --config playwright.three-products.config.ts --grep 'M1 real' --list`
  — listed 3 tests in 1 file; list-only, no execution.

Typecheck and lint are N/A because there is zero App source/test delta. No
browser, localhost, live socket, Runtime, Agent, farm, full, acceptance, or
heavy suite was run. No P2/P3 acceptance credit is claimed by this handoff.
