# Runtime R2r current original-nine proof — 1626

## Outcome

PASS: one original Agent 67ba nine was run against the exact integrated Runtime
checkout. The command exited 0 with `9 passed in 15.69s`.

Runtime:

- commit `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`
- tree `9b07545cac9a8bbafb16246aaa6f72050ef7cffe`
- `runtime_protocol/timeline_commit_port.py` SHA256
  `0d44b5a5e1e0374239df461cb5094ff4fe5bb70761233efd4e3a65c2b29b0859`
- `runtime_protocol/timeline_commit_store.py` SHA256
  `b1cfdceefc533220ea9a5478f61a971109d1cc2d70fa2c7a76341ffa977f2246`

Agent:

- commit `67ba416bca813f4931b557f6f2ca2abf935d7d35`
- tree `172916ee683f5bda5274c0db49eb9d21825fb2ef`
- original test bytes SHA256
  `75ccd026898b241d2241f5c058342aeb728e3a70f039a8701343b55f6fc648f6`
- original test AST identity
  `be9a7dce79a3fbe8be453a0dcb8f4c0a8d33eb35cbe8fd6e34d0194bfe5206ea`
- provider `_commit_patch.py` SHA256
  `162e813a35513c831cd99af4b8ec1ce147d9be72e5f4cb036d97adf7109e74ed`

Both worktrees were clean. The observed module origins in every phase report
were the current Runtime worktree and the pinned Agent worktree, not an
ordinary integration checkout or installed substitute.

## Command

Run once from Runtime worktree `/home/user/work/wt/rt-R2r-current-pair-proof-1626`:

```bash
PYTHONDONTWRITEBYTECODE=1 ORIGINAL9_EVIDENCE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-current-pair-proof-1626/evidence/original9 ASTRID_RUNTIME_CHECKOUT=$PWD ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-67ba416b PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-history-sequential-1543:/home/user/work/wt/agt-pin-67ba416b:$PWD:$PWD/packages/python /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p original9_observer /home/user/work/wt/agt-pin-67ba416b/tests/editing_conformance/test_doc_patch_sequential_rebase.py
```

The prior worker observer source was used unchanged:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-history-sequential-1543/original9_observer.py`

Observer SHA256:
`77c2a39cd671c8d4c5c826cb3afab19c3ad7812c636ee793fb825e39defcaf2b`.

Full pytest stdout SHA256:
`fb72387e2ca5c89846433d25fb27f9e9c29a23ea3054fee8f49a8bccfaa603cf`.

## Acceptance matrix

- 9/9 test nodes passed.
- 27/27 phase reports passed: setup, call, and teardown for each node.
- The four positive current/moved × declared/no-read combinations passed with
  expected accepted/merged behavior.
- All five strict negatives passed and executed: field, consulted, membership,
  source, continuation.
- Four previews had null receipts and no database writes, with the expected
  accepted/merged `would_status`.
- 23 durable observer records were written to the permanent evidence directory
  before validation; each has request, prepared data, provider original/plan,
  replay bindings, and a pre-validation database hash. Sixteen include the
  detached capture object and fifteen include returned outcomes; the remaining
  records are preserved pre-validation refusal captures.
- All per-node reports retain full longrepr fields and before/after module
  origin stdout. Credential-key scan is clean: zero findings.
- No deselection, skip, xfail, test-body retry, or second original-nine run.

## Evidence custody

Permanent evidence root:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-current-pair-proof-1626/evidence/original9/`

It contains the complete flat pytest phase reports (`pytest-report-*.json`),
all observer capture/outcome records (`original9-capture-*.json`), and full
stdout (`../original9-pytest.log`). The source report is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-current-pair-proof-1626/report.md`

## Scope and recommendation

This is readonly qualification evidence, not a merge authorization. No product,
test, fixture, pin, schema, generated client, Git ref, host, browser, socket,
daemon, or public-history file was changed. No full suite, native suite,
browser/daemon journey, provisioning, or host test was run, as excluded by the
brief. Retain the held historical ancestry and route this report to the
orchestrator’s independent review; do not create a new review gate solely for
this proof.
