# D134 CLI22 source assessment — root-045

## Verdict

`FAIL_SOURCE_ASSESSMENT`.

The exact authored route in `tests/editing_conformance/test_native_batch_ingress.py:141-151` is:

```text
edit commands-file film FILE --project PROJECT --json
  --base-revision-id REV --base-publication-id PUB [optional flags]
```

Current `COMMANDS` registers `edit` as one ordinary parser (`cli.py:3624-3650`) and no nested `commands-file`; `build_parser` no longer calls `configure_native_edit_parsers` (`cli.py:3958-3972`). The parser therefore rejects the command-list file before a handler or Runtime call. This is the approved G5 retirement recorded by `dba6e4e7a80f5d7b88b2f8718644ac72dcbe9de6`.

## Current supported ingress comparison

| Route | Source proof | Why it is not a faithful replacement |
|---|---|---|
| `timelines commit REF --project P --file DOCUMENT -m LABEL --idempotency-key K [--dry-run]` | `cli.py:3596-3608`; `cli_native.py:55-161` | Requires a detached document bundle (`project_id`, `timeline_id`, `base_parent`, `parent`, `placements`, `shots`). It does not accept the authored JSON list of EditCommands or CLI base flags. It computes a bundle diff through `Timeline`/G3, forcing a new `doc.patch`/semantic envelope and new step metadata. Repackaging the list by executing it or synthesizing a document changes authored input and refusal semantics. |
| `timelines apply REF SHEET --project P [--dry-run]` | `cli.py:3510-3529`, `3810-3815`; `timeline_sheet.py:587-606,720-881` | Accepts the cut-sheet grammar, not the JSON command list. NativeSheet reconstructs commands from rows, limits editable fields, and uses `session.commit_many` with sheet-generated steps. It cannot preserve arbitrary original commands, `expect` versus `reads`, malformed/envelope/media refusal cases, or the original file-route bytes. |
| Python `TimelineSession.commit_many` / `queue_many` | `sync.py:302-369`; `sync.py:490-601` | A genuine batch/queued ingress with durable outbox and exact retry exists for Python callers. It is not a supported CLI invocation and has no commands-file parser/file-retention/no-write admission boundary. Treating it as the CLI replacement would change the tested ingress. |
| `timelines edit` ordinary route | `cli_native.py:176-323`; `cli.py:3624-3650` | Supports individual semantic move/trim and other detached editing flags; it has no raw batch-file argument. |

The current document path does preserve important C0 mechanics once a valid detached document exists: `commit_session.py:12-19,87-127,163-254` delegates free bundle changes to the G3 emitter, and `sync.py:525-601` freezes/retries the exact outbox flight. That does not prove source fidelity for this retired file ingress because the original command list never reaches that path.

## Why the old test family remains behavioral

The test file deliberately retains the original command-list input and predicates. It covers one real batch publication and reload/guarded inverse; captured versus uncaptured commands; explicit original base pins; raw request idempotency; lost ACK/restart with disjoint, relevant, ABA, and delete-recreate peers; file byte retention; no recapture after restart; stale boolean-vs-number claims in `expect` and `reads`; atomic refusal/no Runtime call for claims, late-invalid, media, empty, and envelope damage; preview with null receipt and the same command list; and original-pair behavior after a peer advances the head. The finite member map in `predicate-map.json` records each exact case and the live seam.

These purposes cannot be credited as conserved by `commit --file` or `apply`: those routes require different authored source formats and derive a different request. The shared worker's unchanged mutableRuntime reproduction was not repeated and is not treated as qualification.

## Recommendation

Do not restore the `commands-file` spelling in this review. The current Agent CLI/G3-G5 owner must either provide and qualify a new supported CLI batch/file contract that explicitly conserves this family, or formally retire/re-specify the root-045 behavioral family under an orchestrator decision. No test expectation, authored input, route, or scope was changed here.
