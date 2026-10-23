# G5 child review — 1917

## Verdict

**PASS for the 1907 observational diagnosis; P1 remains NO-GO and there is no G5 merge.**
The earlier 1902 `internal_error` was a harness failure before the actual Runtime provider/commit path, not evidence of a Runtime product regression. The corrected bounded node reached and completed both ordinary SDK `TimelineSession.move` commits, then failed at the Agent retained-history lookup. That identifies the next Agent history boundary, but does not prove a product defect: fixture/history expectation remains a live alternative.

No production, test, Runtime, observer installation, schema, pin, environment, or shared-dependency file was changed. The 1917 lane owns the ordinary Agent historical-basis source review in parallel; this report does not create a competing author or approval gate.

## Harness diagnosis

The 1848/1902 observer called `_event(service, project, timeline, request=body)` at `g5_preflight_observer.py:410`, omitting the required `name`. The original-valid-node packet records the resulting `TypeError: _event() missing 1 required positional argument: 'name'` while Runtime was in `runtime_protocol/server.py:311`; it records no provider, port, store, or coordinator execution for that request. Therefore the old 1902 `1 PASS / 3 FAIL` result cannot assign that failure to Runtime.

The corrected shim is external and minimal. Its AST has only the base observer import, `_event` compatibility wrapper, and direct delegation from all three pytest hooks (`pytest_configure`, `pytest_runtest_setup`, `pytest_runtest_teardown`). It does not call a product method, replace a product result, inject state, or claim success. `g5_corrected_observer.py`, the original observer, and the child hook all compile and parse. The four original test-body locks are `all_match=true`; the target body remained the exact original.

The corrected child log has one durable boot packet, nine wrapper-install records, and 13 seam-entry/13 seam-exit records. The provider-loader entry/exit is present. It also has one non-product `observer-install-failure` during module-level metadata logging (`__qualname__` on a partially initialized provider module); this is a qualification limit on observer setup, not a product exception. The corrected run itself has no `runtime.server.error` and no seam exception.

Do not collapse the evidence files into one execution: `original-first-node.jsonl` and `original-valid-node.jsonl` are separate bounded launch records, while `original-corrected.jsonl` is one pytest node whose body made **two** move commits. The corrected log shows both coordinator/provider/store sequences entering and exiting with `accepted`; it does not show one-body/one-commit semantics.

## Corrected first-node result and ownership

The bounded corrected command recorded by 1907 was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 \
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-2a9e347f \
ASTRID_AUTHENTIC_LEGACY_ARCHIVE=/home/user/timeline-hub/hub/design/g5-sdk-authentic-capture-20261023-b6069d1d.tar.gz \
G5_AGENT_ROOT=/home/user/work/wt/agt-G5-child-cause-1907 \
G5_EVIDENCE_ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence \
G5_CHILD_OBSERVER_LOG=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence/original-corrected.jsonl \
G5_EXPECTED_AGENT_COMMIT=89c38c9355f5d4bcc68597ec74e4729435a7a07a \
G5_EXPECTED_RUNTIME_COMMIT=d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b \
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence/hook:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence:/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence:/home/user/work/wt/agt-G5-child-cause-1907:/home/user/work/wt/rt-pin-2a9e347f \
/usr/bin/timeout -k 15 720 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider \
-p g5_corrected_observer -m integration \
tests/sdk/test_timeline_checkout_history_runtime.py::test_checkout_reload_undo_cli_redo_uses_retained_history
```

Recorded result: **1 failed in 20.73s**, at `tests/sdk/test_timeline_checkout_history_runtime.py:148`, `assert restored_basis is not None`. Both preceding `TimelineSession.move` calls were accepted, with complete provider/port/store/coordinator entry/exit packets and no Runtime public error. The next observed boundary is Agent `astrid/sdk/timeline_sheet.py:find_version`, which returns `None` after checking local/exported/history/base candidates and Runtime history. This is a source-backed precise owner for follow-up, not a proven product cause; the packet does not establish whether the mismatch is Agent history behavior or a fixture/test expectation. No recovery, undo/redo continuation, or source fix was attempted. The earlier 1902 private capture remains unavailable; no recovery claim is made.

The production caller remains the ordinary SDK checkout/move/history path in the unchanged test body. No `internal_error` should be reclassified as a Runtime bug from the public 1902 result.

## Runtime identity qualification limit

The corrected child boot and seam packets show:

```text
Agent actual/configured:   89c38c9355f5d4bcc68597ec74e4729435a7a07a
Runtime actual HEAD:       2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d
Runtime tree:              f79a2355cfb39d9ada7721978bd20d5702105778
Runtime configured env:    d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b
```

Thus the 1907 command used the 2a9e checkout but set `G5_EXPECTED_RUNTIME_COMMIT=d9e2`; the expected string is not proof that the child ran d9e2. Actual loaded module origins are under `/home/user/work/wt/rt-pin-2a9e347f/runtime_protocol`, including `runtime_protocol/auth.py`, `timeline_commit_auth.py`, server, service, execution, port, provider, and store. The package directory is therefore source-backed as the child origin, although the exact runtime `runtime_protocol.__path__` object was not emitted by the hook and is not independently claimed beyond that filesystem-origin evidence.

Static git/source comparison shows the relevant loaded files match actual 2a9e. Most also happen to be byte-identical to d9e2 (`__init__.py`, `auth.py`, server, service, execution, port, provider, and store). **`runtime_protocol/timeline_commit_auth.py` differs:** actual/2a9e SHA-256 begins `3b812936efaa`, while d9e2 begins `9a009f155c7c`; 2a9e is the commit parent/current source actually loaded. The 1907 flat table claiming those hashes as “= Runtime d9e2” is therefore too strong and must be corrected to “matches the actual 2a9e source; stable unchanged modules also match d9e2.” This is a qualification limit, not evidence of a Runtime fault in this run.

## C0/evidence limits

The durable case packets retain accepted canonical-document data, full receipt data, records, bindings, effects, dependency manifests, history/head/SQL views where available, and the original request/base/project/timeline/dry-run fields. The unchanged body-lock and source checks preserve the ordinary caller and request construction. However, the corrected single node does not independently exercise every C0 variant. In particular, this review does not claim fresh proof of merged/refused replies, dry-run null receipt, or every structured error (`code`, `path`, `head`, `hint`, suggested command), nor does it claim that every label/step/read/merge/key field is present in the move request itself. Those remain prior qualified evidence, not new corrected-node execution evidence.

## Checks run for this review

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m py_compile \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence/g5_corrected_observer.py \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-four-preflight-1848/evidence/g5_preflight_observer.py \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-child-cause-1907/evidence/hook/sitecustomize.py PASS
AST parse plus corrected-hook delegation audit                  PASS
body-lock report-all.json (`all_match=true`)                    PASS
credential scan (`findings=[]`)                                PASS
git diff --check (review worktree)                              PASS
git status --short (review worktree)                            CLEAN
```

No prohibited original FOUR/first-node/c271/9/full/browser/HTTP/new-service probe was run by this review. No full suite was requested. P1 remains **NO-GO**; no G5 merge or approval is recommended from this packet alone.
