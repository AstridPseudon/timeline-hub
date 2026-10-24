Prepared the bounded P2 repair in **caller-publication.py and caller-custody.json only**. Commit message and `DONE` are written; the harness will commit.

- Fixed stale tree literal `2deab1a1494fbccfce5e9235412bacb8a949c0cd` → `1094bf3662c785e4b21eddf7e3ae980da79b1af1`.
- Authenticated Agent head `333b44b1a1b8be72d4d101391b7636c508419109`, exact079 parent, clean detached checkout, approved 18-line source/234-line test delta, and 3,418 protected blobs.
- Normal receipt: `$ORCH/queue/done/checkout-agent-333b44b1a1b8be72d4d101391b7636c508419109`; SHA256 `fad9e905e1ebf658215887dd84ad01e7ed2014366d0fbaecf56b3a6fa5388d96`.
- Also repaired four encoded Remotion-origin bindings. Its authentic retained0258 receipt records079; the old guard incorrectly compared that origin with333b. All checks remain enforced.

App source `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`, tree `542b772e6deed676b917f857708445b7d37a5aa8`, parents, C0 production path, 60 guards, H36 diagnostics, stages and original bodies remain unchanged. Child1016/key188546, Runtime37eb, Remotion0258 and graph819acf were verified in place.

Private candidate: `/tmp/w-b620d40126/candidate/`

- `current-draft.rows`: `2e04e3d9c7dd636674017cbe8202182eda4bf8fff39d6d49424e1ae6025055bc`
- `prepared.json`: `306442912ef1bf567df9bf10090901ee7067b33e992046b68cb9878fce9e0b06`

Commands and results (`S=/tmp/w-b620d40126`):

- `TMPDIR="$S/candidate" python3 caller-publication.py` — PREPARED.
- `python3 "$S/check-shell.py"` — read-only source/client/tree block passed; seven negatives refused, including stale tree/head.
- `python3 "$S/check-publication.py"` — existing14 fault matrix plus eight source/receipt/client/backend/delta/protected-count/registry faults refused.
- `python3 "$S/check-identity.py"` — exact source and preserved-byte comparisons passed.
- `PYTHONPYCACHEPREFIX="$S/pycache" python3 -m py_compile caller-publication.py "$S/candidate/decoded-bench-guard.py"` — passed.
- `python3 -m json.tool caller-custody.json` and `bash -n` on original/new decoded/wrapped shells — passed.
- `git diff --check` — passed; exactly two changed files.

P3 remains `23226c274dbdbb8750f009cb89d7920db40eb49513af906df7b4f76d9a7a3bf0`. All247 outsiders remain `9acf76fafd09c0e4ecd89be6288402f8557dcb17c3a70f492ce9ae56d241e2e8`. Pure1036 tests/types/lint evidence is reused by exact identity.

No blockers. Installed actual26414 and shared registry remain untouched. No installation, service request, socket allocation, setup, build, backend or browser execution occurred; **no live credit**. Next: independent cumulative review, then separate worker-only installation before an authorized meaningful run.