# G5 retained-draft restore diagnosis (readonly)

Date: 2026-10-23. Reviewed tree: `d32f87b838cdd58d4ac0539c152e8cd0ff9ea091`,
parent/current pre-G5 base: `bda966e9c491e1fa4b683cda8913dddeaa14c63d`.
Runtime qualification pin: `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`.

## Verdict

P1 remains **NO-GO**. The retained four-case run is real evidence: 2 passed,
2 failed in 27.13s. The retained-draft failure is not explained by a harmless
publication-id normalization. The observed `draft.document()` is the prior
accepted-move/current authoring snapshot (parent revision
`authoring-parent-revision-99d2d01b77f19dc4264c7bc8a0d8b86a6a15ebb9ae8c9b7f473d980de13f3f89`, digest
`sha256:286c41f1f99457f5dc3f26eb04fcbd02f9e455dce967e82e39f09994a49f2696`),
not the restored source closure. Its payload differs too.

The strongest source-backed cause is a local current-head/source-boundary bug:
after restore, `_reset_base()` performs an unpinned normal read. `fetch_bundle()`
then tries to infer a unique publication from the revision. Restore intentionally
lands the original accepted revision under a new publication, so that revision
is no longer unique. The read can refuse; `_reset_base()` catches the exception,
leaves the prior accepted-move bundle on disk, and retires draft history. This
matches the retained actual revision/digest/payload. The exact exception and
full request/closure packet were lost, so this is an evidence-backed inference,
not a claimed capture.

No source repair or test edit was made. Do not fix this by stripping metadata,
retargeting equal-bytes, or fabricating accepted history.

## Retained facts, source inferences, and lost evidence

Retained facts:

- ORIGINALFOUR used the authentic archive and Runtime `d9e2a71e...`; result was
  2 passed / 2 failed.
- `test_retained_restore_does_not_reopen_consumed_draft_steps` reached a
  successful restore: `accepted_revision_id == original.base_parent.revision_id`
  and `restore.receipt.receipt_id != accepted.receipt.receipt_id`.
- The final full-document assertion failed. The retained diff shows actual
  `base_parent` revision/digest/payload differ from `Checkout(original)`.
- The joined G5 commit changes exactly four paths: the three validation/provider
  files and `tests/editing_conformance/test_authenticated_legacy_restore.py`.
  It does not change `sync.py`, `store.py`, `publish.py`, or the retained test.
- The other ORIGINALFOUR failure is the independent inverse-range refusal;
  this diagnosis does not assign it to the draft-reset boundary.

Source inferences:

1. `TimelineSession.restore()` queues one `timeline.restore` command and flushes
   through the ordinary outbox/commit route. `_flush()` sends the current base
   pair, command, `dry_run`, source, and optional metadata; it does not send a
   caller-supplied document.
2. `_ack()` requires the accepted canonical document and checks
   `accepted_revision_id == canonical_document.parent_revision.revision_id`.
   It separately requires a fresh receipt ID, so same revision/new publication
   is a legitimate accepted outcome.
3. `Checkout._reset_base()` calls `fetch_bundle()` with neither revision nor
   publication, replaces the in-memory bundle, writes it without an undo step,
   and retires history. On read failure it catches the exception and returns
   without replacing the bundle, while still retiring history.
4. `fetch_bundle()` first opens the normal current bundle. If no publication is
   present, it scans history and requires exactly one row matching the revision.
   It cannot distinguish the original publication from the new restore
   publication when both carry the accepted historical revision.
5. The normal reader is a deterministic projection: Runtime parent/child image
   rows are reduced to canonical field sets, then `open_authoring_bundle()` maps
   them to `base_parent`, `base_parent_payload`, placements, and source mappings.
   That projection can explain authoring representation differences, but not a
   different parent payload from the intended restored closure.

Lost:

- The original full per-case request, accepted reply, SQL/history snapshots,
  prepared provider input, canonical records/bindings/effects/dependencies,
  module-origin capture, and the exact exception from the second reset.
- The deleted `/tmp/w-a525d31f0b` packet and private Runtime artifacts. They are
  not reconstructed here and no original test body was rerun.

## Exact causal seam

The likely sequence is:

`original R0/P0` → local draft steps → ordinary move accepts `Rmove/Pmove` →
first `_reset_base()` succeeds and persists `Rmove/Pmove` → restore is submitted
at `Rmove/Pmove`, but the authenticated source is `R0/D0` → Runtime accepts
canonical revision `R0` with new publication `Prestore` → second unpinned
`_reset_base()` reads current `R0`, then revision-only history matching sees
`P0` and `Prestore` → unique-publication check fails → old `Rmove` bundle stays
on disk. The retained actual generated `Rmove` identity and changed payload are
consistent with that last step.

This is a local stale-snapshot/source-boundary classification (a), not merely
faithful current-head normalization (b). The normal reader's projection is
legitimate when it is given the exact current `(revision, publication)` pair;
the current reset path does not preserve that pair. Missing exact authenticated
closure (c) prevents claiming whether the accepted restore canonical document
itself was exact, but the successful accepted revision assertion and G5 source
path support it; the lost packet prevents stronger ownership proof.

## Old/new call seams and G5 scope

Pre-G5 and G5 have the same `TimelineSession.restore()` → `_flush()` →
`client.timelines.commit()` → Runtime acceptance seam and the same
`Checkout._reset_base()` → `store.fetch_bundle()` path. `git diff
d32f87b83^ d32f87b83 -- astrid/sdk/timeline/{sync,store,publish}.py` is empty.

The actual G5 provider seam is in `commit.py`: the draft passes the authenticated
restore closure as `baseline`, includes inverse sources plus restore closures in
`source_bundles`, and passes provider restoration records into final timing
validation. It then still emits the canonical document through the normal
`document_from_bundle()` path. That is the intended caller path; it does not
provide local draft hydration or a second writer.

The smallest source repair, if the manager approves implementation after a
causal capture, is to make the reset/current read use the authoritative current
head pair (preferably the accepted reply's `accepted_revision_id` plus
`receipt.receipt_id`, or the current history head pair) when calling
`fetch_bundle()`. Do not infer publication identity from revision-only matching.
This is a source repair proposal, not an applied change.

## Faithful oracle boundary

The current `assert draft.document() == Checkout(original).document()` is too
strong for publication identity: a successful restore must create a new
publication. But it must not be weakened until the stale-snapshot problem is
resolved. A meaningful regression should first prove the post-reset current
read has:

- restored parent revision and content digest equal to the requested `R0/D0`;
- restored parent/child payload and closure pins equal to the authenticated
  source closure after the normal authoring projection;
- `base_parent.publication_id == Prestore` and different from `P0`; and
- no retained local draft undo/redo steps.

Only then should the oracle compare canonical content/projection separately
from publication identity. The observed `Rmove` digest/payload must remain a
failure, not be normalized away.

## C0 request/reply inventory

Normal restore request emitted by current Agent source:

```json
{
  "api_version": 1,
  "project_id": "<scope>",
  "timeline_id": "<scope>",
  "base_revision_id": "<current head revision>",
  "base_publication_id": "<current head publication>",
  "commands": [{"schema_version": 1, "op": "timeline.restore", "version": "1",
                "select": null, "args": {"revision_id": "<R0>",
                                           "content_digest": "<D0>"}}],
  "dry_run": false,
  "source": {"via": "python"}
}
```

For this caller, `label`, `steps`/full step patches, request `reads`, `merge`,
`rationale`, and `group_id` are omitted; the ABI/default contract normalizes
missing metadata. The HTTP idempotency key is the persisted flight key. Restore
is sole-command and exact-head guarded.

On success C0 requires `{data, receipt}`. `data` includes status (`accepted` or
`merged`), base pair, previous pair, accepted revision, `rebased_onto`, full
`canonical_document`, document digest, normalized commands, `id_map`, provider
and compiler versions, complete steps/patches, effective merge mode, publisher,
and echoed source/label/rationale/group annotations when supplied. The receipt
is authoritative and its `receipt_id` is the new publication. Authenticated
history retains records/commands, physical bindings, authored and derived
effects, dependencies, and `undo_steps`; those exact fields are not in the
surviving packet. A restore has no undo target (`undo_steps` is not evidence to
invent here).

Dry-run would use the same request with a fresh key and `dry_run: true`; success
is `status: preview` with `would_status`, evaluated head, candidate canonical
document/digest, commands, id map, steps and merge mode, with no receipt/history
write. Refusals must retain `http_status`/transport `code`/message and structured
`details.status`, semantic error `code`, `path`, `head/current`, `hint`, and
`suggested_command`. None of the lost per-case reply/error fields is asserted.

## Test-body hashes and evidence

The retained test bodies were not changed. Current source hashes:

- `test_checkout_reload_undo_cli_redo_uses_retained_history` lines 128–160:
  source SHA-256 `cc761fb486d617cdecf4dd6c7ac40486073b50d693c28fcacff0b370b4f4deeb`,
  AST SHA-256 `f2a95ff5f3ae236097cf339fd7c3053df53c24256d7913be6875bede8267f7aa`.
- `test_retained_restore_does_not_reopen_consumed_draft_steps` lines 245–293:
  source SHA-256 `b1c4e31aa6e20c16a90e20ac53d98d21fbe043c1cbfc1aee09a4557cdb6472aa`,
  AST SHA-256 `8e60a62f573bdc277433bb7fb2fba3738240b99a7106828976e68a1630a254f5`.
- Neither function has a decorator; the module-level integration marker is
  unchanged (`pytestmark = pytest.mark.integration`, source SHA-256
  `cef7f773ba983abbab18d3fedff66bb85806f063456038e8bd00c0562718af00`). The
  reviewed D21 source lock for the first body is
  `cc761fb486d617cdecf4dd6c7ac40486073b50d693c28fcacff0b370b4f4deeb`.

Evidence citations and excerpt hashes are permanent in the worker evidence
directory. Credential scan found no credential-shaped matches in those new
evidence files. No tests were run for this readonly report.

## Recommendation

Keep G5 draft-only and P1 NO-GO. Dispatch one manager-controlled causal capture
that preserves the restore request, accepted reply/receipt, current history head
pair, normal `open_bundle`/`fetch_bundle` response, and reset exception without
recreating the lost packet. If it confirms the duplicate-revision lookup above,
repair the source current-pair handoff, then add the meaningful regression with
separate content/projection and publication assertions. Do not dispatch an
independent approval or weaken the existing equality first.
