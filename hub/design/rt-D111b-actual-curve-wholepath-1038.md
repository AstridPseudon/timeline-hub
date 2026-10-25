# D111b actual curve whole-path investigation

Decision: **HELD**. This is an independent read-only handback against exact base `85639c2941dbb8fd62439700f4a16b1cdf654136` (fix1016). No product, test, pin, or generated-file changes were made.

## Result

Fix1016 cleared the generic read/deepcopy cost but not the growth gate. The trustworthy aggregate is `_read` 24.721185059 s -> 6.007234940 s and deepcopy calls 2058 -> 448. Receipt/readback bytes remained equal and source-document/source-store counts remained 0. The remaining per-request observation is 15 -> 498 history-entry calls while distinct entries grow 3 -> 10. The measured endpoint 0.264527529 s -> 1.828706732 s (6.91x, 1.5x limit, FAIL) is confounded: the diagnostic hashes/JSON-measures every returned value, and the final store callables account for only 0.240382864 s of the 1.828706732 s wrapped port read. This does not establish an uninstrumented production endpoint curve.

The exact sequence is:

`distinct entries: 3, 4, 5, 6, 7, 8, 9, 10` -> `entry calls: 15, 33, 63, 108, 171, 255, 363, 498`.

The sequence is real call-path evidence, not a conclusion that the diagnostic wrapper's wall time is production time.

## Production path

App's structural save creates a `doc.patch` command at `shotTimelineDataProvider.ts:1124-1142`; the generated client serializes and POSTs `/v1/projects/{project}/timelines/{timeline}/commit` with `Idempotency-Key` at `generated.ts:202-204`. Runtime validates detached body/path identity and delegates at `service.py:2447-2461`, then creates a request-private `RequestCommitPort` at `service.py:2508-2515`.

Agent's production commit reads base closure, head, and base history at `astrid/sdk/timeline/commit.py:1227-1231`. The `doc.patch`/merge path may rebase and call `_records` plus `patch_boundary`; reservation checking is then performed at `commit.py:1395-1399`. Thus some historical growth is necessary: these checks authenticate the exact base/current chain, prior records, and revision boundaries.

The remaining repeated work is in `RequestCommitPort._ancestor` (`timeline_commit_port.py:225-244`). Each call starts from observed/base roots and walks backward through `_history_entry_view` until its target. `revision_closure` caches closures only (`:257-286`); it does not memoize an already traversed request-local publication path. Therefore several provider reads can revisit the same ancestry. This explains 15 -> 498 without repeating the settled positional-source-hydration finding.

Runtime's store cache is not an unauthenticated shortcut. `history_read_scope` keeps SQL/CAS inputs live and checks them before/after dependent reads (`timeline_commit_store.py:501-529`). `_verify_accepted` rechecks live ledger/history rows, dependency ordering, replay proofs, and inputs before publishing proofs (`:601-695`). `_history_entry_view` performs membership checks and re-verifies accepted cache hits (`:1009-1055`), while `_history_view` rebinds the exact through entry and checks the chain (`:1083-1132`). The existing cache is detached, and `RequestCommitPort._read` deepcopies returned values (`timeline_commit_port.py:210-216`), preserving mutation isolation.

The C0 surface checked is the full request/response contract: request `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, `commands`, `label`, `steps` (each `id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge`, `reads`, `dry_run`, and `Idempotency-Key`; accepted/merged responses carry `canonical_document`, `receipt`, `head`, `effects`, `bindings`, and `dependencies`. Conflict responses retain `head` and `reason`; invalid responses retain `code`, `path`, and `hint`; dry-run leaves durable state unchanged. The observed App request is the `doc.patch` subset of this contract, not a reduced alternate API.

## Safe bounded handback

An already verified request-private traversal result is safely reusable only within the same request, exact project/timeline/publication-revision pair, and unchanged authenticated `history_read_scope`. Per-public-call authorization and membership/revocation checks must remain. So must `_HistoryReadInputs` checks, store-version checks, CAS byte/hash checks, and `_verify_accepted` live-row/ledger/replay validation. Reuse must be invalidated by acceptance writes, unrelated transaction changes, rollback/refusal, close/restart, DB/WAL/CAS/version changes, or failed verification; proofs must never cross requests. This is the bounded remaining cost and safety boundary, not a new trust seam or implementation plan.

## D94 distinction and measurement limits

D94 warm is a repeated history-only GET after acceptance/restart: its N=3..22 samples stayed at 27 SQL with zero digest/decode work. D111b exercises the App POST -> Runtime -> Agent commit lifecycle, ancestry/reservation reads, and canonical readback. D94 therefore neither validates nor invalidates this native whole-path curve. D112a baseline equivalence is a different task and cannot imply a required D111b flat curve.

Prior 123/132/53/2/7 controls and the separate strict 39+1 parent-failure scope were retained, not rerun. Native XML is absent because the central recipe did not enable `--junitxml`; the raw exit/log is retained and no XML was synthesized. No App/P4/full/native-body/source acquisition/record fabrication was done, and no private payloads, URLs, credentials, or raw stack export are included.

## Checks

Source SHA-256, Python AST parsing of four production Python files, prior/raw JSON validation, `git diff --check`, and exact worktree cleanliness passed. Targeted tests/type/lint are N/A for this read-only task; prior controls are evidence retained from the earlier worker. Sanitized evidence is in `workers/rt-D111b-actual-curve-wholepath-1038/evidence/`; the machine-readable report is the adjacent `.json`.

Recommended next step is for the assigned sole author/orchestrator to decide whether this bounded request-local traversal cost warrants a separately authorized implementation/measurement task. No second diagnostic round was run.
