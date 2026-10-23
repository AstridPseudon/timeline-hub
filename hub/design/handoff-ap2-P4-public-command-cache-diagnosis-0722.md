# P4 public command canonical-source diagnosis

Disposition: **diagnosis PASS; product functionality FAIL/unfixed; P4 NOT DONE**.
Agent owns the correction (PLAN G2/G3, consuming R1). This is a bounded read-only
source diagnosis, not a behavior qualification. No product, test, fixture,
schema, pin, generated, launcher, configuration or operations file changed.
No tracked report artifact was added. No plan/contract decision was changed.

## Exact source and retained failures

- Stage/sourceSHA: `dd0bd73e2cef92cdca8213d26e175e350b484af6`, tree
  `e762ea942c4139b97f782a1882e7de3453b42cb8` (this worktree).
- Current Agent integration inspected: `4edc4b321cae5cfc58252d7ed89e3f0408238646`,
  tree `f17b84c48bae3461dd11cedb8719bd17495a8210`; clean when inspected.
- `git diff --exit-code HEAD 4edc4b321cae5cfc58252d7ed89e3f0408238646 -- astrid/sdk`
  returned 0, no output: **the whole SDK subtree is identical**. A separate
  byte/AST witness also checked nine relevant working files against integration.
  Integration's changed `astrid/core/timeline/authoring_bundle.py` concerns
  retention of unchanged legacy missing media selectors. It cannot supply the
  missing key: `document_from_bundle:304` reads it before calling the compiler.
  The differing P4 test inventory does not repair the callable SDK route.
- Retained service artifacts under `$ORCH/tests/`:
  `ap2-P4-ten-canonical-boundary-return-0703-p4-v2-http-nodes-1023071347-20774/log.txt`
  reports **1 failed, 1 warning in 3.32s**;
  `ap2-P4-ten-canonical-boundary-return-0703-p4-v2-http-nodes-1023071551-30589/log.txt`
  reports **1 failed, 1 warning in 3.52s**. Both fail at the first
  `opened.command`, test line 310, after seed/restart/ordinary open and exact
  canonical/physical-source assertions. The second traceback shows `calls=[]`:
  the note commit has not reached the HTTP submission boundary.
- Log SHA-256 respectively:
  `71f0ea34da8c767071101a79069c52a15d8c92d6f12dd757909f4753b367c686` and
  `3231734522e77ce3f207eeaba670711dee19b00228794becfa54c7381f0c05cc`.
  These are retained results, not reruns by this worker.

Here `$ORCH` is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`.

## Existing production route and failure

All line references below are identical at the stage and inspected integration
unless explicitly stated otherwise.

1. `astrid/sdk/timeline/commit_session.py:237-254`: public `timeline.open()`
   opens `TimelineSession`, reads its durable exact base pair, then calls
   `fetch_bundle` with **revision only**. `Timeline._adopt:44-51` deep-copies
   that public bundle into both `.bundle` and `._command_bundle`.
2. `Timeline.command:106-120` checks pending/flight and base freshness, captures
   free edits, then calls `_append:79-104`. Line 83 immediately executes
   `self._command_bundle`; there is no verified source hydration here.
3. `commands.py:182-232` validates/copies the input and dispatches the registered
   handler. `_doc_patch.py:335` constructs `Closure`; its constructor at
   113-117 calls `commit.document_from_bundle`. `commit.py:304` unconditionally
   reads `bundle['source_mapping']['_runtime_document']`. Ordinary open did not
   populate it. The uncaught `KeyError` precedes provider submission and is a
   genuine product gap, not a test oracle mismatch.
4. Free edits follow `_capture_free_edits:71-77` -> G3 emitter -> `_append`.
   Parent-only note emission succeeds, as the retained run demonstrates. Child
   edits additionally call `Closure(before)` in `emitter.py:171-181`; some child
   allocations do so at 225-226. They need canonical source **before emission**,
   so an `_append`-only fix is incomplete for the promised free-edit surface.
5. `Timeline.commit(fn):188-197` fetches each evaluation's revision without its
   publication, then constructs another Timeline. Initial evaluation and
   conflict re-evaluation have the same gap. Each working Timeline's `_basis`
   is its evaluation pair; using the durable session's older base during a
   conflict re-evaluation would hydrate the wrong boundary.
6. On success `commit_session.py:128-135` already adopts
   `bundle_from_document(result['data']['canonical_document'])`, including
   merged changes. That happens too late to help the first staged patch.

## Existing authenticated read and outbox boundaries

`store.fetch_bundle:641-656` already forwards an optional `publication_id` to
`client.timelines.open_bundle`. `_remote_timeline.py:27-221` is the existing
canonical read route; no new endpoint is needed. It checks parent, shot and
internal owner/scope/revision responses (67-139), projects immutable image
fields (140-168), and only hydrates private source on an **explicit exact
revision/publication pair** (169-208). That branch finds the matching history
receipt, verifies the revision and receipt ID, obtains its canonical document,
or uses the verified immutable parent's retained manifest for bootstrap/legacy
receipts, and calls `bundle_from_document`. `commit.py:77-151,154-166` verifies
canonical fields, payload digests, exact closure identities, links and manifest.
The remote branch compares the hydrated source projection to the actual closure
read and checks retained manifest equality before attaching the private source.
Do not bypass or replace these checks; do not rebuild retained pins from an
editable/public bundle. Ordinary revision-only public reads remain unhydrated.

`TimelineSession._bundle`, `sync.py:193-206`, already chooses that exact-pair
read if pending/extra commands include `doc.patch`. `commit_many:338-345` uses
it before local capture. This existing behavior is bypassed by Timeline's
earlier preview execution. Calling `_bundle` wholesale from `_append` would
also risk discarding locally staged edits unless they are preserved/replayed.

The Python outbox has **no `base_document` field**: `outbox.py:18-60` persists
JSON; `sync.py:160-179` initializes scope/base/pending/flight; `submit:472-501`
freezes commands/options/evaluation; `_flush:514-527` persists the exact
body/key/count/fence. Successful acknowledgements advance the pair at 559-570;
ambiguous failures retain the flight. A canonical `base_document` is a verified
read result, not something this outbox currently stores or can reconstruct.
The passing single-edit test's local `base_document` at
`test_p4_cli_sheet_v2_runtime.py:125-143` comes from that exact-pair read and
is used for an expected provider plan; it does not hydrate a Timeline handle.

## Why the single HTTP case passes

The existing single CLI/sheet test uses `TimelineSession` and a native move
(`test_p4_cli_sheet_v2_runtime.py:75-105`), which executes without requiring
the generic patch Closure cache. Runtime's provider loads its own verified
canonical closure via `commit._load:422-429`. Its full accepted/request/receipt/
show/history pass therefore does not exercise the broken `Timeline.command`
preview path. The ten-note case does exercise it. Existing mocked SDK vectors
also pre-populate `generated.bundles` with `bundle_from_document` (e.g.
`test_timeline_open_commit.py:35`, `test_p4_commit_v2.py:47-49`), so their success
cannot establish the ordinary public-open boundary. No such fixture was changed
or executed here.

## Smallest owner correction

Agent should join its existing verified canonical read to the Timeline's local
emission/execution boundaries in `commit_session.py`, using the handle's exact
`_basis` revision/publication pair and its already-bound client/scope. Obtain
the immutable canonical source through `fetch_bundle(..., revision_id=...,
publication_id=..., client=...)`; retain that authenticated source privately
for execution and child emission. Preserve `.bundle`'s ordinary-open shape,
working aliases, authored draft edits, earlier local commands, step numbering,
guards and the original evaluation pair. Hydrate copies used for emission on
both sides consistently: emitter provenance equality at 262 rejects a source
metadata change introduced on just one side. Avoid turning private hydration
itself into a free edit via the `.bundle != ._command_bundle` comparisons.

Cover initial open, direct command, helper/free edits, function evaluations at
returned conflict pairs, and reopened sessions. Reuse authenticated source
already available after acceptance where valid. An initial-open-only fix misses
the function path; an `_append`-only fix misses child emission. No R1 weakening,
schema change, alternate transport, synthetic canonical document, public cache
requirement, new persistence ledger or test expectation change is needed.

This is a correction outline, not an implemented or tested patch. Exact private
state placement is an Agent implementation choice within these constraints.

## Checks, limits and acceptance handoff

Executed during this task:

- `python3 /tmp/w-f9e13dec0c/source_witness.py` — exit 0; nine byte-identical
  source checks plus AST checks of both missing publication calls, raw
  `_command_bundle` construction/execution, existing lower-level exact-pair
  patch hydration, Closure's cache requirement, and absence of an SDK session
  `base_document` key. Source-only evidence; no product imports or test bodies.
- `git diff --exit-code HEAD 4edc4b321cae5cfc58252d7ed89e3f0408238646 -- astrid/sdk`
  — exit 0, no SDK differences.
- `git status --short` here and at `/home/user/work/agent` — empty at inspection.
- `sha256sum` on the two retained failure logs — values recorded above.

Relevant source SHA-256: `commit_session.py`
`277d0136aaa6f6d256e3e392f831f027d9c90802e7dac6aecffc5bba4b012fe9`;
`_remote_timeline.py`
`05a00ba3af343eba2a5970f7ad047c0008d6f4c4bee745767dd3d71d7cc2ac67`;
`commit.py`
`7776e31c83a7f0fc58965141b5863548c7cd4bb60f58f5c827848254c810eb3b`.
Remaining per-file SHA-256 values are emitted by the retained source witness.

No behavioral tests were run: no source was changed, retained failures already
locate the seam, and the brief prohibits unchanged reruns. No HTTP/body/service/
socket/browser/build/full/request invocation was made. No blockage to diagnosis;
product acceptance remains blocked on the Agent correction and its verification.

Recommended commands for the owner **after its correction**, not run here:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_open_commit.py tests/sdk/test_timeline_open_commit_v2.py tests/sdk/test_timeline_sync.py tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_p4_commit_v2.py
```

Existing hydrated fake-transport vectors alone are insufficient: owner regression
coverage must consume ordinary authenticated public reads and verify retained
pair/digest/guard rejection, child free-edit emission, and conflict re-evaluation
at the returned head. Keep all promised effects and original tests.

For the owning orchestrator's central service, after review/staging, use the
existing named suite with the worker that holds the corrected product and
reviewed original proof (no duplicate service or new suite):

```sh
R=$("$ORCH/bin/request-test" <corrected-owner-worker> p4-v2-http-nodes --files "tests/editing_conformance/test_p4_ten_note_v2_runtime.py") && "$ORCH/bin/wait-test" "$R"
```

Then separately qualify the reviewed rerun proof and retain the single CLI/sheet
case. The current integration does not contain the staged ten-note/rerun proof
inventory, so source presence must be reconciled by its owners before selecting
those nodes. Preserve authentic seed/restart and ordinary-open/cache assertions.
Acceptance remains PLAN P4/G2/G3/R1 and contract §§1-5,7: complete v2 request
api_version/scope/base pair/commands/label/steps patch+reads/merge/reads/dry_run/key;
accepted and merged whole canonical/head/digest/receipt/effects/bindings/
dependencies/history/undo_steps; structured conflict and invalid replies;
ten notes as one commit with per-step undo/redo, conflict rerun, and show/history.
No full suite is requested or recommended by this diagnosis.
