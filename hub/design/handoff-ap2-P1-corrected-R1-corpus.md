## P1 corrected-provider requalification

Result: **NOT MERGEABLE: 1 failed, 41 passed.** The corrected d8e1578 packet was run against the actual new Agent R1 provider at `28b9b966206d7f19c8fc2212d662797e7024ea1c` (not old `8a66`). The sole failure is stale membership removal: the provider returns `value_conflict`, while the contract and packet require `selection_changed`.

### Exact revisions and source verification

- providerSHA: `28b9b966206d7f19c8fc2212d662797e7024ea1c`
- test-sourceSHA: `d8e1578bd9f717eb975addb50c2654de70815475`
- The 15 allowed packet blobs under `tests/sdk/fixtures/p1_feasibility/**` and the three requested tests were verified with `git hash-object` against the corresponding d8e1578 tree entries. Existing fixture bytes already matched; only the missing request corpus and two tests were imported.
- No product, schema, generated, pin, lock, launcher, report, skip, or xfail files were changed in the worktree. Existing `runtime_abi` fixture was used.

### Scenario dispositions

- `trim-internal-clip-window`: accepted; direct real-provider execution and canonical output assertions pass.
- `created-track-and-clip-list-inserts`: accepted; list creation, opaque values, and inverse pass.
- `params-absent-to-explicit-values`: accepted; absent/null distinctions and shared-alias preservation pass.
- `params-null-to-object`: accepted; explicit null guard and opaque sibling preservation pass.
- `params-remove-and-preserve-opaque`: accepted; remove guard, explicit null sibling, and opaque preservation pass.
- `disjoint-field-merge`: direct service execution passes and preserves both fields, but reports legacy `rebased` as recorded by the detached/old Runtime fixture. This is not v2 `merged` evidence and does not prove Runtime HTTP/App H3.
- `same-field-refusal`: stale same-field edit is refused as `value_conflict`; pass.
- `ordered-list-move-and-order-refusal`: base move is accepted; stale move is refused as `selection_changed`; stale removal is refused as `value_conflict` instead of required `selection_changed` (the one failing assertion).

The packet retains all success/refusal, absent/null, opaque, order, membership, and history/inverse assertions. The corpus continues to record Runtime HTTP publication and App/UI H3 as pending; no detached result is promoted to that evidence.

### Exact commands and logs

Pytest acceptance command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
```

Result: `1 failed, 41 passed, 1 warning in 5.57s`, exit `1`.

- Full pytest log: `/tmp/ap2-P1-corrected-R1-corpus-pytest.log`
- Ruff command: `/root/.local/bin/ruff check tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py` — passed, exit `0`; log `/tmp/ap2-P1-corrected-R1-corpus-ruff.log`.
- Mypy command: `/root/.local/bin/mypy --follow-imports=silent tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py` — passed, exit `0`; log `/tmp/ap2-P1-corrected-R1-corpus-mypy.log`.
- Diff check: `git diff --check` — passed, exit `0`; log `/tmp/ap2-P1-corrected-R1-corpus-diff-check.log`.

### Remaining owner need

Agent R1 owns the remaining fix: check ordered-collection membership/order dependencies before the item-value guard, while preserving `value_conflict` for stale same-field edits. Requalify this exact d8e1578 packet after that repair. Runtime HTTP/App H3 and v2 `merged` acceptance remain unverified; no full, browser, heavy, or socket suite was run.

## Independent requalification review (2026-10-23)

Result: **PASS on exact assembly/report accuracy only; NOT MERGEABLE while red.**

The review read contract `design/commit-v2.md` §§2–4, the current `design/BOARD-HEADER.md`, and this handoff. Corpus base `0e91cc9f3397c425758331ad5a94765bb3a6b0ef`, provider `28b9b966206d7f19c8fc2212d662797e7024ea1c`, and packet `d8e1578bd9f717eb975addb50c2654de70815475` are the stated revisions. All 15 packet blobs are byte-identical to d8e (15 checked, 0 mismatches); all product bytes are exact at provider 28b; and the corpus commit contains only the three intended test/fixture additions. The packet source is exact at d8e, with no skip/xfail/fails weakening markers.

The mandated pytest command reproduced `1 failed, 41 passed, 1 warning in 5.38s`, exit 1. The sole red is stale ordered-list membership removal returning `value_conflict` instead of required `selection_changed`; same-field `value_conflict` and order `selection_changed` remain passing. Ruff, mypy, and `git diff --check` passed. Logs are `/tmp/ap2-P1-corrected-R1-corpus-{pytest,ruff,mypy,diff-check}.log`.

The existing report is truthful: the disjoint-service `rebased` result remains partial old-fixture evidence only, with no new v2 `merged`, Runtime HTTP, App, or H3 claim. No full/browser/heavy/socket suite was run. This review PASS is not mergeability or full P1 completion; re-run the unchanged d8e packet after the Agent R1 precedence repair.

## Membership requalification (2026-10-23)

Result: **PASS: 42 passed, 1 warning.** The unchanged corrected packet was
re-run against the new committed Agent R1 membership repair at
`e6f7167d6171638f0bfcd5b9f88ae04f05b7b64c` (parent
`28b9b966206d7f19c8fc2212d662797e7024ea1c`), not old `8a66`.

- providerSHA: `e6f7167d6171638f0bfcd5b9f88ae04f05b7b64c`
- test-sourceSHA: `d8e1578bd9f717eb975addb50c2654de70815475`
- All 15 permitted packet blobs match d8e tree hashes exactly. Only the three
  absent packet paths were imported; no product/schema/generated/pin/lock/
  launcher/skip/xfail file changed. Existing `runtime_abi` was used.
- `trim-internal-clip-window`, `created-track-and-clip-list-inserts`,
  `params-absent-to-explicit-values`, `params-null-to-object`, and
  `params-remove-and-preserve-opaque`: accepted and all real output,
  absent/null, opaque, alias, and inverse assertions pass.
- `disjoint-field-merge`: direct service preservation passes, but the detached
  Runtime fixture reports legacy `rebased`; this is not v2 `merged` or Runtime
  HTTP/App H3 evidence.
- `same-field-refusal`: `value_conflict`; pass.
- `ordered-list-move-and-order-refusal`: base move accepted; stale order move
  and stale membership removal both return `selection_changed`; pass.

Acceptance command and logs:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-app2-native/bin/python -m pytest -q tests/sdk/test_p1_doc_patch_provider.py tests/sdk/test_p1_doc_patch_requests.py tests/sdk/test_p1_case_corpus.py
```

Result: `42 passed, 1 warning in 5.11s`, exit `0`.

- `/tmp/ap2-P1-membership-requalification-pytest.log`
- `/tmp/ap2-P1-membership-requalification-ruff.log`
- `/tmp/ap2-P1-membership-requalification-mypy.log`
- `/tmp/ap2-P1-membership-requalification-diff-check.log`

Ruff, mypy, and `git diff --check` each passed with exit `0`. No full/browser/
heavy/socket suite ran. Agent R1 product merge eligibility remains
Agent-owned; Runtime HTTP publication, App/UI H3, and v2 `merged` acceptance
remain unverified.
