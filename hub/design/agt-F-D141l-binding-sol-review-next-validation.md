# Validation

All commands were read-only against the author packet, current source tuple,
and harmless isolated controls. No live service was requested or run.

| Command | Result |
|---|---|
| `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-sol-next/evidence/check-source.py check` | exit 0; `control_status=PASS`; `pair_status=BLOCKED_U2_003_NATIVE_CUSTODY`; admission 10; lifecycle 38 |
| `bash -n` on author controller, cut, pristine, tiny-controls and positive-stub | exit 0 |
| Python AST on author `binding-source.py` and `check-source.py`; JSON parse of source-manifest/readiness/admission-derivation | exit 0 |
| source-manifest SHA readback for all 11 listed operational files | all PASS |
| `bash /tmp/.../agt-F-D141l-binding-sol-next/evidence/controller-continuation.sh check` | exit 0; `status=BLOCKED_U2_003`, request-test not called, rows not installed, native both members heavy at 4,700,000,000 |
| Composition `git rev-parse HEAD HEAD^{tree}` and clean status | `6a2d1c22ec800229812f4d756d7198aece8111ed`, `57f68e1fad9c84ce0c0a2fa10f9a2f8defb1a847`, clean |
| current Agent/Runtime/App/Composition tuple readback | Agent `ecdc242e`/`d362fe9d`; Runtime `95d98f03`/`78df31d6`; App `82e9e13d`/`6a6e49eb`; Composition `635f4de0`/`5ab5191a` in integration worktree; review base is the explicit Composition `6a2d1c22`/`57f68e1f` |
| registered `agent agent-core-full` rows in current ORCH `tests/suites.conf` | count 1; it is the retained historical 0309 row and was not mutated |
| original launcher tiny controls | positive exit 17/call 1; Agent-SHA-only poison exit 1/call 0 |

The checker’s fixture/native association controls are not live admissions. The
current packet has no request ID, result directory, JUnit, runmanifest or
terminal exit from a new service. Product lint/typecheck are N/A because the
reviewed files are operational evidence shell/Python, not product sources; no
behavioral pytest nodes or full suite were rerun.

The author trace has real disclosed gaps and remains non-qualification evidence.
This review’s own five-sample trace is in `disk-trace.txt`; minimum available
space was 4,552,992 KiB (>4,000,000,000 bytes) and no stop was reached.
