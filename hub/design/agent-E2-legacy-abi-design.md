# E2/D81: ABI1 retirement with a net-line budget

Status: design-only, non-gating, and behind every critical row.  This is an
owner-review proposal for a post-ZIP follow-up.  It authorizes no product
change, current wiring, tuple change, history rewrite, or deletion today.

Verdict: READY FOR OWNER REVIEW as a conditional, net-negative design.  The
line reduction is defensible only if the post-ZIP implementation keeps the
existing Runtime history/acceptance authority, converts only facts that are
already authenticated, and classifies every missing fact as `legacy_unknown`.
If the owner does not approve that existing-authority status projection, the
verdict becomes NOT READY: the measured candidate deletion is not enough to
justify a new trust surface.

## Evidence boundary and identities

The Agent inventory is from `tl/integration` at
`22d00393f7d944f1d01505637ca00b1995c3e158`.  The Runtime inventory is from the
actual integration checkout `/home/user/work/runtime` at
`44917baf5976d6a655d582fafc63fde7b6cb242d`.  The frozen R4 source identities
were read with `git show` only: SDK
`11caf1d9de291d76f491cf69f7942606b7471d7a` and Runtime
`31c7ac3a00f7a205f507bf5bd4d4625628d429bd`.  The current integration sources,
not the frozen branches, are authoritative for this inventory.

The named `/home/user/peteromallet/astrid-agent/docs/projects/timeline-r4/`
directory and `/tmp/.../scratchpad/luna/reports/` directory were absent in this
environment.  Available Timeline Hub controls used as design references were:

* `hub/design/commit-v2.md` (C0, §§1–5 and §7), including exact retry,
  head-pair, source, publisher, previous-value, read/order/range, ABA, and undo
  rules;
* `hub/design/runtime-D61-abi-boundary-1410.json`;
* `hub/design/rt-D61-1422-boundary-facts.json`;
* `hub/design/rt-D61-1422-private-execution-seam.json`;
* `hub/design/peer-runtime-to-agent-20261024T1531Z-D62-MERGED.md`;
* `hub/design/agt-R2-D62-remaining-whole-path-1546.md`; and
* `hub/design/E-PLAN.md`, owner-approved 24 Oct 19:55Z and trimmed 20:02Z.

The required source-only inventories were run against Agent `astrid tests` and
Runtime `runtime_protocol tests` source trees.  No test bodies were collected
or executed, and no HTTP, browser, full, performance, install, or environment
suite was run.

## C0 and modern schema lock

C0 uses version-1 wire/schema markers inside the modern v2 contract.  The
modern request retains `api_version: 1`, each command's `schema_version: 1`,
the canonical document's `schema_version: 1`, and recorder/records
`schema_version: 1`.  These values are not ABI1 labels and are not retirement
targets.  The complete request remains `api_version`, `project_id`,
`timeline_id`, `base_revision_id`, `base_publication_id`, `commands`, `label`,
`steps` (each step has `id`, `label`, `intent`, `tags`, `command_ordinals`,
`patch`, and optional `reads`), `merge` (`fields` or `atomic`), optional
request `reads`, `dry_run`, `source`, `rationale`, and `group_id`, plus the
HTTP `Idempotency-Key`.

Replies remain `accepted` or `merged` with canonical closure, records,
effects, bindings, history, and receipt; `preview` with `would_status` and a
null receipt; `conflict` with head and reason; and `invalid` with code, path,
hint, and suggested command.  Exact existing legacy retries return their
original envelope, including historical `rebased`; a new ABI1 mutation is
refused after the owner-approved cutover.

Stable schema-1 fields, `Recording`, `prepared_records`, and
`HistoryEntry.recorder_abi` visibility are retained.  No schema/client/
generated-file change is proposed by E2.

## What ABI1 means

These states remain distinct:

1. **Genuine prechange history.**  Accepted event and history metadata both
   lack `recorder_abi`; Agent defaults a missing field to ABI1 only in the old
   read/replay seam at `astrid/sdk/timeline/commit.py:1005–1014`.  Runtime
   preserves the legacy interpretation at
   `runtime_protocol/timeline_commit_store.py:296–304`.
2. **Authenticated ABI1.**  Runtime accepted the edge with an authenticated
   `recorder_abi: 1` pair.  It is a server fact, but it does not prove that
   physical provenance is complete; Runtime explicitly permits missing
   physical provenance at `runtime_protocol/timeline_commit_auth.py:451–465`.
3. **Stripped or incomplete v2.**  A v2-shaped submission has only some
   physical bindings retained, while the current classifier at
   `runtime_protocol/timeline_commit_store.py:1230–1235` uses “any physical
   binding”.  That is not completeness authority and must not be reused by
   migration.

`legacy_unknown` records an honest absent or unprovable fact.  It never proves
that a request was complete and never authorizes inverse.  A contradictory
original is `tampered_or_inconsistent`, not an excuse to infer ABI1.  No
synthetic v2 facts are added, and no old receipt, event, request/idempotency
row, record, canonical document, publisher, or source attribution is changed.

## Full inventory and caller map

The companion TSV is the machine-readable inventory.  The important retained
boundaries are:

### Agent

* `astrid/sdk/timeline/_recording.py:71–87,246–280` is the shared recorder
  core.  Modern v2 uses it through `commit.py:1421–1437`; retain it.
* `astrid/sdk/timeline/_commit_preview.py:7–22,25–90` builds shared schema-1
  records and original/landing captures used by modern v2; retain it.
* `astrid/sdk/timeline/commit.py:661–704` reads contiguous history and
  schema-1 records; retain the history read and make status explicit before
  inverse.
* `astrid/sdk/timeline/commit.py:770–930` contains native fork restoration.
  Its physical-binding checks remain the proof for eligible converted records;
  only the ABI1/native allowance listed in the budget is removable.
* `astrid/sdk/timeline/inverse.py:757–784` is the v1 inverse read/create
  reconstruction.  It is removable only after the migration status says the
  entry has complete physical facts; unknown entries refuse inverse.
* `astrid/sdk/timeline/_step_undo.py:10–50,87–128` supplies whole and
  per-step selection and later-history guards.  The no-step fallback is removed
  only after status is available; the guards are retained.
* `astrid/sdk/timeline/native_word_anchor.py:136–170,173–281` and
  `native_occurrence_fork.py:14–36` are source/document compatibility, not
  recorder authority; retain them until a separate document migration.
* Production callers are
  `astrid/sdk/timeline/sync.py:313–330,530–570`,
  `astrid/sdk/timeline/commit_session.py:163–250`,
  `astrid/sdk/timeline/store.py:457–498`,
  `astrid/sdk/_remote_timeline.py:225–268`, and provider
  `astrid/sdk/timeline/commit.py:1160–1444`.  They retain the exact request/key
  retry path.  The eventual migration read occurs before constructing
  `timeline.inverse`; E2 proposes no wiring now.

### Runtime

* `runtime_protocol/timeline_commit_store.py:45–105` intentionally leaves old
  requests byte-compatible.  Keep the exact-retry and historical projection
  behavior; only the new-submit ABI1 acceptance can be retired after the
  cutover.
* `runtime_protocol/timeline_commit_store.py:202–304` verifies old status,
  receipt, event, metadata, and record commitments.  Keep it unchanged for
  immutable replay.
* `runtime_protocol/timeline_commit_auth.py:290–315` derives omitted
  `track.create` allocation claims.  This is a true ABI1 submission branch and
  is removable once new v2 commands carry their authoritative claim and old
  entries are replay-only.
* `runtime_protocol/timeline_commit_auth.py:451–475` skips missing physical
  provenance for ABI1 records.  The six-line conditional is removable only
  after unknown old entries cannot enter new acceptance validation.
* `runtime_protocol/timeline_commit_store.py:1214–1272` accepts and publishes
  the mutation.  Only the “any physical binding” ABI classifier at
  `:1230–1235` is a target; the accepted/merged/rebased reply branches remain
  for exact history and retries.
* `runtime_protocol/timeline_commit_store.py:1424–1445` commits the immutable
  metadata/event pair.  Retain it; migration appends a separate commitment.
* `runtime_protocol/timeline_commit_store.py:442–529,477–529,624–648`,
  `timeline_commit_baseline.py:257–264,284–340`, and
  `timeline_commit_inputs.py:245–260` preserve history, the explicit
  `legacy_unknown` baseline, and source verification.  Retain them.
* `runtime_protocol/timeline_commit_types.py:90–104` and generated client
  `packages/python/astrid_runtime_client/timeline_commit_types.py:90–104`
  retain schema 1, optional `recorder_abi`, and `rebased`/`merged`.  No client
  deletion is proposed.

The Runtime tests that establish authority boundaries are
`tests/test_timeline_recorder_abi_authority.py:112–203,420–438`,
`tests/test_timeline_recorder_abi_authority.py:84–108,227–249,353–438`, and
`tests/test_timeline_commit_contract.py:497–529,786–852,901–907`.  Agent
structural evidence is
`tests/sdk/test_timeline_legacy_inverse_bindings.py:40–113`,
`tests/sdk/test_timeline_commit_provider.py:402–430,438–449,449–499,511–567,547–567,870–920,1120–1247`,
`tests/sdk/test_timeline_commit_provider_runtime.py:15–113,125–205,197–205,205–292`,
`tests/sdk/test_p1_doc_patch_provider.py:210–297,359–505`, and
`tests/sdk/test_timeline_occurrence_delete_provider.py:83–114`.  These are
source citations only in this task.

## Minimal one-time migration proposal

Runtime performs one migration per timeline after the ZIP and owner approval;
Agent and clients do not write migration facts.  It uses the existing history
authority and verifier over immutable `timeline_commit_history` rows,
`records_json`, accepted event payload/hash chain, idempotency receipt/request
hash, exact base/landing closures, and retained source objects.  It adds no
custody system, DSL, code generator, registry, ledger, or extra trust surface.

For each publication, compute a deterministic digest over the original row,
receipt, event, and closure pins.  Reverify the original before writing an
append-only conversion projection keyed by
`(project_id, timeline_id, original_publication_id, original_event_hash)`.
The projection records the original digest, source publisher, migration actor
from authenticated execution context, base/landing pair, copied known records,
status, and an explicit unknown-facts set.  It is exposed through the existing
history read only after owner approval; E2 proposes no new public route.

Statuses are:

| Status | Allowed facts | Undo |
|---|---|---|
| `already_v2` | Existing authenticated v2 records and mode pair; reverify only | Existing whole/per-step gates |
| `converted_abi1` | Exact authenticated ABI1 facts copied into the projection; no absent field is filled | Whole commit only when every gate below passes; per-step also needs complete step facts |
| `legacy_unknown` | Honest missing mode, record, closure, source, codec, physical, owner, order, read, or range fact, with reason | Refuse whole and per-step inverse/redo |
| `tampered_or_inconsistent` | Event/metadata mismatch, changed source digest, impossible closure, or contradictory original | Quarantine/refuse; owner investigation |

An ABI1 entry is `converted_abi1` only if the existing authenticated facts
already prove the complete inverse inputs, including physical source/owner/
order facts where the modern gate requires them.  The migration never creates
physical bindings from final bytes.  An otherwise plausible legacy record with
missing physical or source facts is `legacy_unknown`; this deliberately trades
old undo convenience for a safe, line-reducing cutover.

Migration is one transaction per publication with a durable cursor in
publication/project-sequence order.  A checkpoint stores the source digest and
last completed publication.  Restart rereads and compares the digest; a crash
before commit leaves no projection, and a crash after commit is an exact
idempotent replay.  Partial migration is visible and safe: converted entries
use their recorded gates, unknown entries remain readable but undo-ineligible,
and the final cutover refuses any unclassified row.  Rollback aborts the
projection/checkpoint only; it never deletes or rewrites original history,
rolls back user documents, or replays an old request.

## Existing production caller and undo gate map

E2 proposes no implementation today.  The eventual read/undo map is:

1. `sync.py:313–330,530–570` persists and retries the exact body/key through
   the existing commit client.  It must not reconstruct a changed old request.
2. `store.py:457–498` and `_remote_timeline.py:253–268` retain exact
   revision/publication head pairs and immutable history reads.
3. `commit.py:1229–1299` reads the server-owned status, target entries,
   boundaries, source closures, `recorder_abi`, and step facts before building
   `AcceptedRecords` and choosing whole or selected steps.
4. `_step_undo.py:23–128` and `inverse.py:757–905` remain the gate set for
   complete records, previous values, source restoration, selections, and later
   history.  In the post-cutover implementation, the legacy reconstruction is
   called only for a status-authorized converted entry; unknown/tampered status
   refuses before inverse.

Whole-commit undo requires verified original receipt/event/idempotency
commitments; authenticated scope and publisher; base and landing closures;
exact before/after writes and derived writes; source, owner, allocation,
membership/order, materialization, and inverse-stage facts; and a complete
later-history scan that rejects writes including A→B→A.  Per-step undo also
requires authoritative step patches, command ordinals, dependencies, causal
derived-effect attribution, and a safe selected-step range.  Every refusal is
fail-closed; no receipt, event, request, binding, or final document is rewritten
to make it pass.

## Source-grounded line budget

The following are current source line counts at the pinned integration SHAs,
counted from the exact ranges inspected read-only.  They are not future
implementation measurements.  The candidate ranges are true ABI1 conditionals
or their direct ABI1 dispatch; shared schema-1 and immutable-history ranges are
excluded.

| Repo/file and exact current range | Current lines | Proposed post-cutover action |
|---|---:|---|
| Agent `astrid/sdk/timeline/commit.py:884–888` | 5 | Delete native ABI1 fork allowance; complete physical proof remains |
| Agent `astrid/sdk/timeline/commit.py:1007–1009` | 3 | Delete missing-ABI1 default/acceptance; read explicit migration status |
| Agent `astrid/sdk/timeline/inverse.py:757–784` | 28 | Delete v1 inverse read/create reconstruction after eligible entries are status-authorized |
| Agent `astrid/sdk/timeline/inverse.py:850–852` | 3 | Delete ABI1 inverse dispatch |
| Agent `astrid/sdk/timeline/inverse.py:880–882` | 3 | Delete non-physical binding fallback; unknown entries refuse |
| Agent `astrid/sdk/timeline/_step_undo.py:23–30` | 8 | Delete no-step whole-inverse fallback; retain guarded step/whole machinery |
| Runtime `runtime_protocol/timeline_commit_auth.py:290–315` | 26 | Delete omitted `track.create` claim derivation |
| Runtime `runtime_protocol/timeline_commit_auth.py:451–456` | 6 | Delete missing-physical ABI1 acceptance branch |
| Runtime `runtime_protocol/timeline_commit_store.py:1230–1235` | 6 | Replace “any physical binding” classifier with the already-v2 post-cutover path; one line may remain |
| **Candidate range total** | **88** | **Approximate removable budget: 87 lines** |

The one-line difference is the required constant modern classification after
the cutover.  This is an approximate deletion budget, not a claim that a future
formatter will preserve line numbers.

Estimated additions, implementation estimate only:

| Addition | Estimated lines | Reason |
|---|---:|---|
| Permanent existing-history status projection/read and explicit cutover refusal | 16 | Reuse existing verifier/history authority; no route or new custody |
| Permanent pre-inverse status gate and unknown/tampered refusal | 10 | Keep production caller behavior fail-closed |
| Permanent v2-only acceptance simplification and conformance hooks | 8 | Remove ABI1 branch without weakening current guards |
| **Permanent subtotal** | **34** | Estimated future code, not measured design time |
| One-time source scan, digest verification, and classification | 12 | Reuse existing acceptance/replay verification |
| One-time transaction cursor, resume/idempotency, and partial state | 10 | One publication transaction; no source rewrite |
| One-time unknown/tamper report and final unclassified-row check | 8 | Honest refusal and owner review input |
| **One-time-tool subtotal** | **30** | Estimated future tool code |
| **Total additions** | **64** | Permanent plus one-time tool |

Proposed net budget: approximately **87 removable − 64 added = 23 fewer
lines**.  This is the smallest design that is plausibly net-negative while
preserving immutable history and using existing authority.  If implementation
needs more than 64 added lines, or needs a new custody/trust surface, the
owner must mark E2 NOT READY rather than accepting a positive or unmeasured
change.

Dependencies are C0's existing contract and gates, the Runtime history/event/
receipt verifier, the existing Agent inverse gates, an owner-approved
post-ZIP status projection, and a complete producer audit.  No dependency is a
schema/client/generated-file regeneration, pin, registry, ledger, upstream,
M5, credential, or denied-route change.

## Limits and post-ZIP proof

This design task proves only that the cited source and caller paths exist at
the recorded SHAs, the TSV citations agree with this document, the line budget
is source-grounded, and the Agent worktree is clean with both
`git diff --exit-code` and `git diff --cached --exit-code`.  It does not prove
the future migration, its implementation, a new authority, or runtime
behavior.

The implementation/review estimate is **34 permanent worker-hours plus 18
one-time migration-tool worker-hours, 52 worker-hours total**.  This is an
implementation estimate, not measured design time.  Risk is **high**: the
largest risks are misclassifying stripped v2 as ABI1, losing exact retry
identity, or treating schema 1/shared recorder fields as removable.  The
owner must reject the patch if it introduces synthetic facts or a new trust
surface.

The actual proposed POST-ZIP proof is the same P1–P5 and affected core gates,
plus: old exact retries after restart and changed-body idempotency refusal;
migration crash before/after commit, resume, partial migration, unknown,
tamper, and source-digest mismatch cases; safe whole-commit and per-step
inverse; A→B→A refusal; immutable receipt/event/request/idempotency/record and
canonical-document bytes; and source, owner, order, read, previous-value, and
range guards.  It must also prove accepted/merged/preview/conflict/invalid
reply behavior and the complete C0 request field set, including
`Idempotency-Key`.  Source-only path checks in this document are acceptance of
the design task, not the implementation proving gate.  No HTTP/browser/full/
performance/install/environment behavior is claimed here.
