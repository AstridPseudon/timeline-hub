# R2r nested-range independent review — PASS

Reviewed source `f054966472590c961755fafa835e3036ba697867` against base
`9ce4242bc01f100bab9efc51032a73985cefb2b2`, PLAN C0 §5 / R2r, the Runtime
source report and handoff, and the Agent nested packet plus independent review.

## Findings

- PASS: the product diff is limited to `runtime_protocol/timeline_commit_auth.py`,
  `tests/test_timeline_inverse_stage_authentication.py`, and the 140,275-byte
  `tests/fixtures/timeline_nested_inverse_1543.json`. No store, port, provider,
  contract, schema, generated client, pin, or public v2 shape changed.
- PASS: `_inverse_stage_inherited` derives multiple ordered partitions only from
  the store-authenticated immediate inverse history entry. It retains one
  outward publication/step/command identity, requires complete non-overlapping
  native/effect coverage, and checks exact reversed native captures and canonical
  before/after observations. The existing one-range path remains unchanged.
- PASS: no provider stage image/dict is trusted, no history is invented, and no
  byte-equal alias is retargeted. Existing ownership, pin, digest, read, ABA /
  ancestry, foreign/future/self, and no-write guards remain in the exercised
  suite.
- PASS: fixture custody is explicit. The fixture SHA-256 is
  `8798a4b3a66b6922367add8cae44183a112dea54e4ec15b4e67a47ae7e8b6a13`; its
  history contains the accepted recorded publication
  `txn-75285c95600949c8b1267a71f8e71a9d` with matching receipt. The `prepared`
  object has no receipt and is an auth-only inverse projection, not a production
  PreparedCommit or public-redo result.
- PASS: the retained-fact causal check is old RED / new GREEN, and the original
  auth-helper/test AST, frozen-77 equality, and diff checks pass.

The Agent independent review remains a separate known limit: its strict positive
stops at the unchanged competing-selected-media compiler refusal. It does not
invalidate this Runtime-owned authentication seam.

## Tests and checks

- `PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_read_basis.py tests/test_timeline_source_duplicate_authority.py tests/test_timeline_source_document_boundary.py`
  — **241 passed**.
- Same five files with `-m integration` — **56 passed, 185 deselected**.
- Focused store/tamper run (`-k 'nested_inverse_authenticates_boundaries_without_durable_forgery or actual_nested_inverse_authenticates_complete_retained_boundaries or actual_nested_inverse_forgeries_refuse_losslessly'`) — **32 passed, 85 deselected**. This covers the real-store positive, 10 full-SQL no-write refusals, the retained positive, and 20 retained tamper cases.
- Extra boundary probe (boolean range, duplicate ordinal, inverse-op shape, and
  tampered retained source fact) — **4/4 rejected** with `invalid_records`.
- `ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py` — **clean**.
- Scoped Pyright comparison artifacts reviewed from the source qualification:
  **6 baseline / 6 current**, exact diagnostic identities equal, **0 added / 0
  removed**; all six are pre-existing test `reportOptionalSubscript` findings.
- Source-integrity script — **pass**: old RED, new GREEN, original AST unchanged,
  frozen 77/77 equal. `git diff --check` — **pass**.

## Limits

This is a Runtime source-authentication review only. I did not run public redo,
full suites, browser/native/daemon/provisioning/benchmark runs, or modify Agent
representation. The source candidate still requires the Agent one-outward-step
two-range representation and independent qualification of the separate compiler
cause before any orchestrator-authorized public redo.
