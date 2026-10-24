## Verdict

**FAIL for R5-full-occupancy completion/wiring.** The delta is only an offline preparation helper; it is not connected to the original historical-reuse fixture or production caller path. R5 remains held and provider-qualified status is unverified.

## Findings

- Base: `fad2ddd1eb84f73a2155590ade81a7c51ec50695`
- Candidate: `60fedb573`
- Delta: one test file, `+119` lines; no product/runtime changes.
- All pre-existing function bodies are AST-identical: **23/23**.
- Collection: **18 cases** total, comprising the two new offline cases plus all original cases, including missing-head and inline/reference distinctions.
- New helper correctly shapes:
  - five-key `source_ref`;
  - `source_occurrence_id`;
  - `occurrence.place-shared`, `select: parent`;
  - destination-only `created`;
  - dry-run/idempotency fields.
- It uses synthetic IDs and performs no authenticated source lookup, physical historical-pin verification, media/null/opaque/closure validation, CAS, retry, or Runtime/provider call.
- Callgraph proves `_historical_shared_request` is called only by the new offline test at lines 301 and 312. The original historical fixture at `tests/test_timeline_legacy_occupancy.py:597-658` still uses `timeline.inverse` and never invokes it.

Exact missing hook: wire the carrier into `test_legacy_historical_reuse_keeps_newer_global_shot_head` after its real source document/occurrence setup, using the reviewed Agent-provided authenticated source reference. Do not fabricate source authority or run this until the Agent handoff is reviewed.

## Checks

- Exact new offline nodeids: **2 passed**
- Collection-only: **18 collected**
- `py_compile`: passed
- AST/property/callgraph mapping: passed; original bodies unchanged and helper reachability confirmed
- `git diff --check`: passed
- Ruff (`ruff 0.16.8`): failed with **4 pre-existing diagnostics**, reproduced against the parent file; no new Ruff issue was introduced.
- Pyright: actual checked file count **1**, with **11 unresolved-import diagnostics** because the Agent checkout is unavailable. No qualifying parent/final normalized comparison was possible; the author’s absolute-path/config attempt is not accepted as proof.

I did not run original provider bodies, HTTP tests, full-file tests, full suites, checkout/provision/retry, or use the author’s socket-failure run as evidence.

The staged Agent worktree `/home/user/work/wt/agt-G4-historical-sharing-sol-0226` is absent. No tracked files were modified. Commit message and `DONE` marker were created.