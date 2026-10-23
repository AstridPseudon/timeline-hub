# G5 retained-draft diagnosis review (readonly)

Date: 2026-10-23. Reviewed exact G5 `d32f87b838cdd58d4ac5939c152e8cd0ff9ea091` as
checked out here (the full object is `d32f87b838cdd58d4ac016f...` in the brief's
short form; Git resolved `d32f87b83` to `d32f87b838cdd58d4ac4f3d...`), parent
`bda966e9c491e1fa4b683cda8913dddeaa14c63d`. The exact resolved commit is
`d32f87b83` / tree `d389da2cd99c6f5dcef6924b446b3d3243b84d1b`; no worktree
changes were made.

## Verdict

**FAIL as written; PASS only for the narrowed static-chain claim.**

The draft correctly identifies a real source hazard: `Checkout._reset_base()`
performs an unpinned `store.fetch_bundle()` read; `fetch_bundle()` fills a
missing publication by requiring one history row for the returned revision; a
historical revision reused by a restore publication can make that lookup
ambiguous. It also correctly keeps P1 **NO-GO**, requires a new publication,
and refuses to normalize away the observed content/digest mismatch.

The draft overstates that hazard as the retained run's actual cause. The
retained log contains the final full-document mismatch, but not the second
reset's request, response, history rows, exception, or the accepted canonical
closure. Therefore the exact dynamic cause remains **LOST**. The report must
not say that the reset did fail, or that the old moved snapshot was definitely
kept, merely because the source permits that path.

It also names a nonexistent `store.load_bundle`; the exact owner boundary is
`astrid/sdk/timeline/publish.py:_PublishMixin._reset_base` calling
`astrid/sdk/timeline/store.py:fetch_bundle`. The G5 commit changes only
`_commit_timing_validation.py`, `commit.py`, `validation.py`, and the added
authenticated-restore test; it does not alter sync/store/publish.

## What is proven, inferred, and lost

Proven from source and retained evidence:

- The G5 tree is the exact four-path join above. `git diff d32f87b83^ d32f87b83`
  has no sync/store/publish change.
- The retained 1738 run was once executed against Runtime
  `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`: **2 passed, 2 failed in
  27.13s**. The restore case reached accepted historical revision equality and
  a fresh receipt, then failed the full document comparison. The printed
  actual base parent had generated revision
  `authoring-parent-revision-99d2d01b77f19dc4264c7bc8a0d8b86a6a15ebb9ae8c9b7f473d980de13f3f89`
  and digest `sha256:286c41f1f99457f5dc3f26eb04fcbd02f9e455dce967e82e39f09994a49f2696`,
  versus the original `a3e671256f1c42b8837d3e118c97b21b`, publication
  `txn-11c90075be6c4c8bb9e2627366f0fe4f`, digest
  `sha256:b6069d1ddccc0279e871b142773b63b73b107ebf9d0adc11ab73832b69097afb`.
- `_reset_base()` catches any exception from `fetch_bundle`, retires local
  draft history, leaves `self.bundle` untouched, and records the old-base note
  ([`publish.py:406-414`](../../../../../../home/user/work/wt/agt-G5-restore-draft-review-1758/astrid/sdk/timeline/publish.py:406)).
- `fetch_bundle()` opens the normal bundle without a publication, then scans
  history and refuses unless exactly one row matches its revision
  ([`store.py:451-488`](../../../../../../home/user/work/wt/agt-G5-restore-draft-review-1758/astrid/sdk/timeline/store.py:451)).
  Its explicit-publication branch hydrates the exact pair, so pair-addressed
  hydration is a distinct, guarded path.
- The normal authoring projection deliberately constructs `PARENT_IMAGE_FIELDS`
  from revision, digest, and payload; publication is not part of that image.

Static inference, not retained dynamic proof:

`Rmove/Pmove` → unpinned reset → restore of historical `R0` under `Prestore` →
second unpinned reset → revision-only history match sees `P0` and `Prestore`.
That chain would refuse at the uniqueness guard and leave `Rmove/Pmove`, and
is consistent with the retained generated revision/digest/payload. It is not
the only explanation: the unpinned read could have succeeded and the normal
projection or canonical restore closure could still have produced the observed
content mismatch.

Lost evidence:

- the original per-case request/response, second-reset exception, SQL/history
  rows, prepared provider input, canonical records/bindings/effects/deps, and
  accepted restore closure;
- the temporary packet/private Runtime artifacts from the 1738 run.

The 1738 preflight's exact head pair came from a direct Runtime baseline/DB
verification, not from the normal Agent reader response. Do not call that
reader evidence or reconstruct the missing packet.

## Current-read publication check

The draft's stronger claim—“normal current read returned the actual head
publication and the reader dropped it”—is **not supported and is false for the
reviewed source path**:

1. Frozen Runtime inspection computes/returns `revision_id`, `head_revision_id`,
   parent digest, and snapshot digest; its result has no `publication_id`
   ([runtime `timeline_inspection.py:552-565,751-758`]).
2. Agent `RemoteTimelines.open_composition()` copies that response into
   `native_inspection`; its public `summary` also omits publication.
3. `_remote_timeline.open_bundle()` reads the revision from that result, then
   builds the parent image from `PARENT_IMAGE_FIELDS`, which excludes
   publication. `store.fetch_bundle()` subsequently performs the revision-only
   history scan.

The public `history()` route does expose an exact `head` pair. That is the
smallest existing source seam for a future repair: for the *unrequested
current-head* case only, use and validate `history.data["head"]` before exact
publication hydration; keep explicit historical revision reads strict and
pair/digest guarded. This is an Agent SDK fix candidate, not a Runtime finding.

## Oracle boundary

`TimelineSession.restore()` sends the requested historical revision and digest
through the ordinary commit route. `_ack()` requires the canonical parent
revision to equal `accepted_revision_id` and separately requires a fresh receipt
ID. Thus a successful restore necessarily has a new publication even when the
accepted revision is the old revision.

The oracle must therefore separate:

- exact restored canonical authored content, parent/child closure, manifest and
  content digest (after the normal authoring projection); and
- identity: accepted revision may equal `R0`, while accepted publication must
  be new and distinct from `P0`.

The observed generated revision, changed digest, and changed payload are not a
publication-only mismatch and must remain a failure until the current-pair or
closure cause is captured. Do not strip metadata, retarget equal bytes, or
weaken the full old-pair assertion blindly.

## C0 request/reply inventory (schema, not a recovered packet)

The production caller is Agent `TimelineSession.restore()` → `_flush()` →
`client.timelines.commit()` → Runtime, followed by
`Checkout._reset_base()` → `store.fetch_bundle()` → public Runtime reads. It is
not detached provider evidence and not a public Runtime write route.

The restore request contains `api_version`, `project_id`, `timeline_id`, the
exact `base_revision_id`/`base_publication_id` pair, `commands`, `dry_run`, and
`source`; the command is the sole `timeline.restore` command with its target
revision and content digest. The v2 envelope remains capable of carrying
`label`, `steps` (each `id`, `label`, `intent`, `tags`, `command_ordinals`,
`patch`), `reads`, `merge` (`fields|atomic`), `declaredreads`, `key`,
`rationale`, and `group_id`; this restore caller omits optional metadata unless
the persisted outbox already contains it.

Accepted/merged replies retain canonical `data` and full receipt, including
status, base/previous/accepted revision-publication identities,
`rebased_onto`, canonical document and digest, normalized commands, id map,
provider/compiler versions, steps/patches, merge mode, publisher, and echoed
source/label/rationale/group annotations when present. History/receipt records
retain bindings, authored and derived effects, dependencies, `undo_steps`, and
the canonical/full receipt. Dry-run retains `preview` plus
`preview.would_status`, evaluated head, candidate canonical document/digest,
commands, id map, steps, and merge mode, with no receipt/history write.
Refusals retain structured `code`, `path`, `head/current`, `hint`, and
`suggested_command` (plus transport status/details). No lost case-specific
value is asserted here.

## Owned next step

Keep G5 draft-only and P1 NO-GO. Dispatch one manager-controlled causal capture
at the Agent SDK boundary that records, without reconstructing history: the
restore request, accepted canonical reply/receipt, history head pair, the
normal `open_bundle`/`fetch_bundle` result, and the second-reset exception.

If it confirms the duplicate-revision lookup, the smallest owned fix is in
`store.fetch_bundle()` for the unpinned current-head path: obtain the exact
`history` head pair, verify its revision matches the opened current revision,
then hydrate with that pair. Preserve explicit historical revision uniqueness,
canonical authored-content equality, digest checks, and all C0 guards. If the
capture instead shows a successful read with a wrong closure, dispatch the
corresponding Agent reader/projection owner; do not edit the oracle first.

No source, test, Runtime, schema, pin, Git, daemon, browser, HTTP, body rerun,
dependency, environment, permission-gate, or merge change was made.

## Evidence hashes

Source extract hashes and citations are in the worker evidence directory. The
reviewed Agent full-file hashes include:

```text
publish.py                 f8cd74076fce10d35a7a97778b6628aa3f41e8909389f93780ab49d1cc731f2c
store.py                   3eedf2c651f91bf0e74b3fc9aba08a6e610a463796c450446c1364792dbe4e3f
_remote_timeline.py        05a00ba3af343eba2a5970f7ad047c0008d6f4c4bee745767dd3d71d7cc2ac67
remote.py                  d36ecb5aecf6576515c7c59b127c878638cd13b16f77b24381f7a3da63f1cea0
sync.py                    3e9ccf0aafa1b7fe0718fcd8c05b35d50fc137d2a81b7ec6ff709943b0100a7f
commit.py                  f4272228f5c663d2f586aa5cc4f8ef2486aad4e4d38ca99e9433b6a991e53dbd
retained test              02cd704852b9da1b76c58253eaf90e74177202cce97fa585c4ab722e8a3b4df
```

Credential-shaped scan of the new evidence files: 0 matches. No tests were
run; this was a readonly source review.
