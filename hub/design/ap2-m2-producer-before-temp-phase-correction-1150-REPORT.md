# App producer `before` phase-correction report

## Result

Added the same-directory sidecar harness:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132/outer-controls-run.phase-corrected-1150.py`

The original harness remains unmodified and byte-identical:

- old `outer-controls-run.py` SHA-256: `ff1ae8404f39d765b01429ce706fa0affb6a163b632c20506a9705f103ec7234`
- new sidecar SHA-256: `a4b3f89d9f15f9fbd095e5b6b658605807f7b0099e8337f0cb4dea11ebdf662e`

## Exact patch

```diff
@@
-  temps=[json.loads(l) for l in (case/'temps.jsonl').read_text().splitlines()]
+  temp_log=case/'temps.jsonl'
+  temps=([json.loads(l) for l in temp_log.read_text().splitlines()]
+         if label!='before' or temp_log.exists() else [])
   leaked=[p for p in temps if Path(p).exists()]
   if label=='before':
-   assert len(leaked)==1 and Path(leaked[0]).name.startswith('tl-ap2-producer-existing-'),leaked
+   assert not temps and not leaked,(temps,leaked)
   else:assert not leaked,leaked
```

This is the only changed behavior. `ROOT`/`ORCH` are still derived from the sidecar’s physical directory, and no source/helper/pin/version, launch stub, or artifact-closure file was rebound or recopied.

## Phase/control mapping

| Phase | Retained assertions | Corrected temp assertion |
|---|---|---|
| `before` | early source-hash refusal, status 1, one custody shell, zero child, zero build stub, no packet | absent temp log is an empty event list; exact `temps_created=0` and `temps_leaked=0`; no fake event is created |
| `after` | unchanged four-shell dispatch, child/build, retained packet bytes/checksum, cleanup | original temp parsing and no-leak assertion unchanged |
| `absent-output` | unchanged refusal/retention-failure, dispatch, cleanup, and no complete packet assertions | original temp parsing and no-leak assertion unchanged |
| `copy-failure` | unchanged retention copy-failure, dispatch, cleanup, and incomplete-packet assertions | original temp parsing and no-leak assertion unchanged |
| `success` | unchanged status, dispatch, cleanup, and no-packet assertions | original temp parsing and no-leak assertion unchanged |

The `before` refusal precedes the runner’s `mktemp`, so requiring a later-stage leaked directory was stale and contradicted executed code. This is a process-harness conversion only; the D01 ordinary-batch ledger row remains `OPEN`.

## Validation

- `python3 ...` static checker using `compile()`, `ast.parse()`, exact unchanged-line comparisons, and SHA-256 checks: **PASS** for original and sidecar; only the two intended temp/assertion hunks differ.
- `diff -u0 outer-controls-run.py outer-controls-run.phase-corrected-1150.py`: **PASS**; output contains only the missing temp-log handling and `before` zero-temp assertion.
- App worktree `git status --short`: **clean**.
- No preflight, five controls, build, browser, socket, service, full suite, install, or actual producer execution was run, as required. Those behaviors remain unverified until the manager obtains the independent delta approval and requests the cheap preflight plus five controls.
