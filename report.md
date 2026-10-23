# R2r current-fixture proof — PASS

## Scope

Scoped dependency-cleared proof for `rt-R2r-current-fixture-proof-0534` only.
No product, test, schema, generated client, pin, artifact, or fixture edits were
made. The required fixture, helper, and acceptance-test objects are byte/object
identical to `be5848e17`.

## Exact reviewed inputs

- Runtime actual integration snapshot: `85dafdf46742b02ae5e4a300656cd6f5d68f0d4d`,
  tree `80c3da43addffdbfb2aa95bac06e2abd5e011146`; parents are
  `495769531de8d79d27a2d8022851d75b92f04ebe` and
  `675a249de6afcf69ba9c987484e32719a4e19be5`.
- Agent exact reviewed pin: `736cfdd15a83c9d22bfcc1269967d3b319eae9a8`,
  tree `4d9bd5076e76a895ba026234d3db77b50e94507a`, clean detached checkout at
  `/home/user/work/wt/agt-pin-736cfdd1`.
- Both source trees were read-only archived into the private harness scratch
  directory `/tmp/w-f278ae18d3/exact-snapshot-85dafdf-736cfdd` before testing.
- Imported origins were exactly the private archives:
  `runtime_protocol` from `.../runtime/runtime_protocol/__init__.py`,
  `astrid` from `.../agent/astrid/__init__.py`, and
  `astrid_runtime_client` from `.../agent/astrid_runtime_client/__init__.py`.

## Acceptance

Command:

```text
cd /tmp/w-f278ae18d3/exact-snapshot-85dafdf-736cfdd/runtime
timeout 45 env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/tmp/w-f278ae18d3/exact-snapshot-85dafdf-736cfdd/runtime ASTRID_CHECKOUT=/tmp/w-f278ae18d3/exact-snapshot-85dafdf-736cfdd/agent PYTHONPATH=/tmp/w-f278ae18d3/exact-snapshot-85dafdf-736cfdd/runtime:/tmp/w-f278ae18d3/exact-snapshot-85dafdf-736cfdd/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_acceptance.py::test_real_provider_two_projects_keep_local_ids_and_commit_authority_isolated
```

Result: **PASS — 1 passed in 11.38s**.

This preserves and exercises the original two-project local-ID/scope checks,
baseline snapshot and history/receipt checks, exact idempotent retry, own
inverse/restore, and forged foreign-scope/refusal/no-write controls in the
unchanged node. The unchanged legacy text `elementRef` remains untouched; the
native move targets `music-bed`.

The independent Agent evidence was reused as directed, not duplicated: the
peer Agent 0524 handoff records 69 Agent checks plus the original create/render
2 checks passing on this reviewed source, with new/modified/target-invalidated
reference guards retained. This result is therefore scoped to reviewed Agent
`736cfdd15` plus Runtime `85dafdf46`; it is not a qualification claim for the
broader current Agent home checkout.

## Identity and preservation checks

- `tests/fixtures/precut-two-projects-v31.tar.gz`: SHA-256
  `1275d53a94b3aa03bfad8d5c2eb2aa26da5766c8d95a7c1453a23acf106cef64` in both
  `be5848e17` and the tested head; Git object
  `3b4d17d19f21c2bc5a1f402d1576c729862cea0f` in both.
- `tests/project_isolation_fixture.py` object is
  `dd41ddbefd65fb67101e232746b72c3038eec18e` at both base and head.
- `tests/test_timeline_commit_acceptance.py` object is
  `f5a4ba547d5185168fa9b4ac9671ddf72469a933` at both base and head.
- Frozen `contract/artifacts.json`, schemas, clients, TypeScript package, and
  `runtime.lock.json` have no path changes from `be5848e17` to `85dafdf46`.
- `git diff --check` passed for the Runtime integration snapshot, Agent pin,
  and this worker worktree. The actual Runtime and Agent checkouts remained
  clean at their recorded identities after the run.

## Limits / next step

No broader Runtime/Agent suites, browser, native-render, crash, or duplicate
known isolation runs were performed. Lint/type checks are N/A for this
read-only proof. The first wrapper attempt used unavailable `/usr/bin/time` and
did not execute pytest; the exact command above was then run successfully.
