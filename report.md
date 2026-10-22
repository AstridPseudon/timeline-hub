# C0 contract review

Result: **PASS** for this review. This is a review result only; C0 approval remains with the orchestrator.

## Scope and findings

Compared `contract/commit-v2.md` on `tl/rt-C0-contract` (`58f9f1bd5`) with `tl/integration`, PLAN.md §2 (all seven points), and the shared design copy. The contract covers:

- request base/commands/label/steps, `fields`/`atomic`, declared reads, conservative omitted-read behavior, and publisher-bound idempotency/retry;
- closure roots and alias normalization, absent versus explicit null/remove, ordered identity lists, refusal of id-less element addressing, stable created IDs/reservations, and sequential previous-value guards;
- field/item, collection membership/order, and atomic-scope conflicts, including equal-value A→B→A history;
- accepted/merged/conflict/invalid/refused outcomes, structured error details, and server-side dry-run with no durable effects;
- guarded whole/per-step inverse commits, later-history/dependency scans, merged inverse landing-head preservation, and redo;
- `meta` placement, namespace/value/size/depth limits, opaque preservation, and renderer/reference isolation; and
- labels, steps, requested/effective merge mode, reads, authoritative Runtime publisher, receipts, history pagination, legacy entries, and no history for non-accepted outcomes.

No contract contradiction or missing implementable detail was found that warrants FAIL. The document explicitly records the known downstream adoption seams: current Runtime uses `rebased` while C0 requires `merged`, and current coordinator validation admits only `conflict`/`refused`; generated schemas, coordinator/port, provider, undo, metadata, and history tasks are named as owners rather than silently claiming they already work.

Read-only consistency checks against Runtime `timeline_commit_store.py` / `timeline_commit_execution.py` at `cc7410a1f` and Agent `commands.py` / `commit.py` at `a086cc6d...` (plus frozen R4 Agent refs) were consistent with the stated extension model: Runtime retains request hashing, authorization, acceptance transaction, CAS, preview/accept split, publisher binding, closure validation, receipts, and history; Agent retains recorded reads/writes/created identities, bounded three-attempt commit/CAS retry, history traversal, inverse inputs, and the existing preview branch. No product files were changed.

## Required evidence

All commands were run from `/home/user/work/wt/rt-C0-review`.

- Exact JSON/example and shared-copy command from the contract: **PASS** — both files parsed 17 JSON blocks and had 7 required headings; byte equality passed.
- Exact Runtime fixture/digest command from the contract: **PASS** — digest, receipt/result equality, step partition, ordered-list transitions, merged preservation, preview, structured errors, ABA, meta preservation, and whitespace assertions passed.
- `git diff --check tl/integration...HEAD`: **PASS**.
- `python3 -m pytest -q tests/test_timeline_commit_contract.py tests/test_timeline_commit_type_generator.py`: **34 passed** in 16.98s. One warning: the active pytest did not recognize the repository's `timeout` option; no test failed.
- Config inspection: `pyproject.toml` defines pytest settings but no separate lint/typecheck command or Makefile gate. **Lint/typecheck: N/A (no configured targeted command)**. The targeted type-generator test invokes `tsc` and passed.

Not run: full suite, browser journey, localhost/live-socket tests, and any product implementation tests; C0 is documentation-only and the task explicitly does not require those gates.

## Decision / next step

No repair or commit is requested. The orchestrator should make the C0 approval decision, then downstream owners should adopt the explicitly called-out schema/status/coordinator changes before consumers send v2 input.
