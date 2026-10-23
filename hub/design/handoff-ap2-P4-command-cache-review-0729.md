# P4 command-cache review (0729)

Disposition: **PASS diagnosis / FAIL product-unfixed / P4 not done.** Independent review of Sol0722 confirms the retained 20774 and 30589 failures are genuine source failures, not an oracle or transport mismatch.

## Confirmed source cause

At `astrid/sdk/timeline/commit_session.py:237-254`, public `Timeline.open()` obtains the durable exact base pair but calls `fetch_bundle` with revision only. `:44-51` copies that unhydrated public bundle into `_command_bundle`; `:79-104` executes staged commands locally. A `doc.patch` reaches `_doc_patch.py:334-336` and `Closure` (`:111-117`), then `commit.py:298-305` requires `source_mapping["_runtime_document"]`. The first ten-note command therefore raises `KeyError` before submission. The retained 20774/30589 logs both show this at test line 310; 30589 records no submitted calls.

The current `tl/integration` is `d24da4af0`, and `git diff --exit-code 4edc4b321 d24da4af0 -- astrid/sdk` is clean. The review snapshot also matches `4edc4b321` across `astrid/sdk`. No current product fix exists.

## Boundary and correction

Ordinary public reads deliberately omit private source: `store.py:641-651` forwards `publication_id` only when present; `_remote_timeline.py:63-67` requires an exact pair for hydration and `:169-208` verifies receipt, canonical document, scope, digest/manifest equality before attaching `_runtime_document`. The existing exact-pair route is already used by `sync.py:193-206` for pending `doc.patch` work, but `Timeline.command` previews too early.

Agent owns the minimal fix in the Timeline/session path (G2/G3 consuming R1): privately retain or fetch the authenticated exact-pair bundle for the handle's `_basis`, before command execution and before G3 child free-edit emission. Child emission is source-dependent at `emitter.py:171-210` and `:213-238`. Function conflict re-evaluation also needs exact-pair hydration: `commit_session.py:178-196` fetches a conflict's revision without its publication. Preserve each returned pair, public caller shape, outbox/step/guard semantics, and all v2 request/reply fields.

No synthetic cache, public exposure, guard bypass, alternate transport, new persistence, fixture/test expectation, schema, pin, generated file, or Runtime/App change is recommended.

## Proof limits

The single HTTP CLI/native move remains independently passing because it uses `TimelineSession` plus native `capture_move` (`tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py:75-105`), while the provider independently loads its verified closure (`commit.py:422-429`). It does not exercise the broken generic `Timeline.command`/`doc.patch` preview. No unchanged service or behavioral test was rerun in this readonly review. P4 acceptance remains blocked on Agent's correction and targeted/central proof of ten-note one-commit, per-step undo/redo, conflict rerun, and show/history.

Exact retained log hashes:

- 20774: `71f0ea34da8c767071101a79069c52a15d8c92d6f12dd757909f4753b367c686`
- 30589: `3231734522e77ce3f207eeaba670711dee19b00228794becfa54c7381f0c05cc`
