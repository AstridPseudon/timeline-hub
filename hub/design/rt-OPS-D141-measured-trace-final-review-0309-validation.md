# OPS D141 validation

## Candidate and controls

The reviewed composition candidate is commit `88bb53f12f9f05aaae3357badc431e7f04cd8559`, tree `1dfcf8e66d972999ecde7f42699e9cda85fe5b7d`, with a clean worktree. The actual private control harness completed successfully:

```text
python3 -I ops-d141-measured-floor/controls/real-controls.py       PASS (exit 0)
bash -n ops-d141-measured-floor/bin/test-run                      PASS
python3 -I [AST parse of all five controls]                      PASS
ruff check --no-cache ops-d141-measured-floor/controls/*.py       PASS
git diff --check                                                 PASS
```

The real-control run covered the exact held IDs from review 0235, exact SAME P5 identity, bare/suffix/wrong-job P5 refusals, targeted15, floors, D89d formula, reciprocal heavy admission, 4GB stop, strict provenance/path/owner/source/job/command/suite checks, and continuous 5-second trace/reaping/exit/cancel behavior. The held IDs were refused before artifact or launch. The exact P5 and targeted15 controls passed with four trace rows each.

The candidate preserves snapshot, cache, and lease handling. No mirrored control, test weakening, or source-selection shortcut was introduced. No live request, body, queue, install, network, browser, or full suite was run.

## Real caller trace

The read-only source chain is:

```text
request-test -> full TEST ID + request file + pending queue entry
  -> dispatcher-daemon -> test-run <FULLID>
  -> candidate admission/receipt validator
  -> source/job/repo/suite/command checks and measured-floor decision
  -> snapshot/cache/lease handling
  -> body sampler and 5-second KEEP trace
  -> final append/validation, reaping, exit/cancel handling
```

The candidate's exact-ID guards close both 0235 findings: the two held full IDs are rejected before any launch/artifact, while the same `runtime-d141-p5-cut-1026013331-6934` identity is accepted only with repo `runtime` and suite `d141-p5-cut`. The old held IDs are not enabled.

## App applicability

This is the blocking applicability finding. Final App source `520d7e4fc12a03392afaed3f486aba34a2b5c319` / tree `70ad390c56b0e45d9279b4179598b6cdbad9ed65` defines D66 through the unique selector suite `p2-automatic-child-placement`, and `d66-plain-stack.mjs` derives or accepts a unique submit-suite name. It does not define `full-e2e-timeline`. The candidate's passing `app/full-e2e-timeline` row is therefore a synthetic private control route, not proof of the real final App first-placement route.

The exact final App registered row, source command, and command hash are absent from the reviewed evidence. The older 0213/867cb273 binding cannot be reused for final 520d. Runtime P5 and Runtime targeted15 are source-control-ready; the App source input is not established, so the whole kit is not ready. No row rename, preflight, request, body, or reissue was performed.

## C0 contract review

`/home/user/work/runtime/contract/commit-v2.md` was read as the full C0 contract. The review confirms preservation of the exact base pair, ordered command transaction, required labels and step fields for new producers, semantic/doc.patch separation, optional reads, merge field/atomic modes, exact idempotency body, and dry-run behavior. It also preserves patch closure, physical-identity aliases, guarded previous values, ordered list operations, collection membership/order conflicts, later-head CAS/rebase, accepted/merged receipts, conflict actual-head reasons, structured invalid details, refused categories, and unchanged preview semantics (would-status only, null receipt, no writes/history/idempotency/head). Undo remains guarded against later history including A-to-B-to-A; meta namespaces and preservation remain constrained by the contract.

