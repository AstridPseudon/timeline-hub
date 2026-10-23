# G5 restructure c271 qualification — 1924

## Result

**DRAFT ONLY / P1 NO-GO.** The one permitted c271 node reached the actual
Agent/Runtime service path and failed during redo. This is not a qualification
PASS and no integration or source repair was made.

The causal owner is Agent `astrid/sdk/timeline/_step_undo.py:157`, where
`compile_mirror()` raises `CommandError("nested inverse compiler observation
differs from native history", kind="history_unavailable")`. Runtime only
propagated that provider refusal through its execution/service boundary; no
Runtime cause is assigned.

## Identity and guards

- Agent source: `89c38c9355f5d4bcc68597ec74e4729435a7a07a`, tree
  `b050d29ec63cad9aaaf536427451d8079293f24c`.
- Runtime checkout: `/home/user/work/wt/rt-pin-2a9e347f`, commit
  `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree
  `f79a2355cfb39d9ada7721978bd20d5702105778`.
- Locked c271 body: lines 570–689,
  `c2711a2d10765828694ee1906d75bdf62a91ed6ac0bbef8e4cb0d823e48ec30d`,
  matched current source and the 89c source.
- Repository `git diff --check`, `git diff --quiet`, and status were clean.
  No product, test, fixture, helper, Runtime, pin, schema, Git ref, or shared
  dependency was changed.

The corrected observer and child hook were copied into the worker-owned
evidence area and adapted only for the current body, source roots, runtime
commit, packet paths, and the corrected `_event` compatibility call. The
initial direct preflight entrypoint reported a false historical-body mismatch;
the corrected wrapper preflight was run before the body and passed. No body was
run during the false preflight.

## Exact commands and results

Preflight archive/service boot (corrected observer wrapper): **PASS** — current
Agent/Runtime identities, authentic archive SHA-256
`2915bd4ac0d46954d19c30f87a517b82074218699978e650fab03fcba81b72d3`, backup
verify/restore, service/project/timeline boot, c271 body lock, and credential
scan `[]`.

Collection-only, once, unfiltered and without `-m integration`:

```text
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f G5_AGENT_ROOT=$PWD G5_EVIDENCE_ROOT=<worker>/evidence/collect PYTHONPATH=<worker>/evidence:$PWD:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only -p g5_corrected_observer tests/sdk/test_timeline_restructure_guarded_runtime.py::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
```

Result: **1 test collected in 0.70s**.

The single permitted body command was:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f G5_AGENT_ROOT=/home/user/work/wt/agt-G5-restructure-qualified-1924 G5_EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-qualified-1924/evidence/actual G5_CHILD_OBSERVER_LOG=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-qualified-1924/evidence/actual/child-observer.jsonl G5_EXPECTED_AGENT_COMMIT=89c38c9355f5d4bcc68597ec74e4729435a7a07a G5_EXPECTED_RUNTIME_COMMIT=2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-qualified-1924/evidence:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-qualified-1924/evidence/hook:/home/user/work/wt/agt-G5-restructure-qualified-1924:/home/user/work/wt/rt-pin-2a9e347f /usr/bin/timeout -k 15 120 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -p g5_corrected_observer tests/sdk/test_timeline_restructure_guarded_runtime.py::test_restructure_whole_inverse_redo_and_intervening_overlap_refusal
```

Its terminal pytest summary
was not emitted by the harness channel, but the durable observer captured the
actual refusal and complete underlying trace. The execution facts are:

- Forward `timeline.restructure` accepted; its canonical/receipt assertions
  were reached.
- Whole `timeline.inverse` accepted; its complete inverse assertions were
  reached.
- Redo `timeline.inverse` refused before `redone` was assigned, with the exact
  Agent stack ending at `_step_undo.py:157`.
- Later intervening-overlap and no-write assertions were **not reached**.
- Public refusal details were preserved: `status=refused`, HTTP/status 409,
  `code=history_unavailable` in the failure details, `path=[]`, exact
  `base/current` pair equal to the head, hint `Refresh the timeline history
  before retrying`, suggested command `timeline history`, and
  `conflicts=[]`.
- The refusal made no write: SQL dump, head, and history were unchanged.

The child observer recorded 151 durable rows: 70 seam entries, 68 seam exits,
10 wrapper installations, 2 seam exceptions, 1 child boot, and no observer
failures. It checked 126 distinct loaded module origins across 15,632 available
hash observations with zero mismatches. `runtime_protocol.auth` and
`runtime_protocol.timeline_commit_auth` were loaded from the actual 2a9e
checkout and matched the configured source hashes. The actual exception was:

```text
CommitRejected: nested inverse compiler observation differs from native history
  astrid/sdk/timeline/commit.py:1050
  astrid/sdk/timeline/_commit_patch.py:973
  astrid/sdk/timeline/_step_undo.py:330
  astrid/sdk/timeline/_step_undo.py:304
  astrid/sdk/timeline/_step_undo.py:199
  astrid/sdk/timeline/_step_undo.py:218
  astrid/sdk/timeline/_step_undo.py:188
  astrid/sdk/timeline/_step_undo.py:157
```

The complete compressed packet archive is worker-owned at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-restructure-qualified-1924/evidence/g5-c271-complete-packets.tar.gz`,
8.8 MiB, SHA-256
`502266a70f0d1a3cb21d354e9cce01245acb39ea014649fe528039e997de1e8c`.
The flat file inventory and per-file hashes are in the companion packet
manifest.

## Allowed post-run checks

- Observer/hook `py_compile`: **PASS**.
- Observer AST parse: **PASS**.
- c271 AST body hash: **PASS**.
- Source-clean and `git diff --check`: **PASS**.
- Prior identical-draft quality evidence reused as directed: Ruff `2148/2148`
  and private mypy `1911/1911` from the current G5 quality reports; not rerun.
- No full suite, original FOUR, first-node, browser, HTTP, P1/P4, provider
  matrix, source retry, public redo retry, or Runtime patch was run.

## Decision / next step

Per the settled plan, retain this candidate as draft and keep P1 NO-GO. Dispatch
the Agent inverse owner with this causal packet if repair is authorized; do not
attribute the refusal to Runtime and do not rerun or weaken the unchanged c271
body in this qualification lane.
