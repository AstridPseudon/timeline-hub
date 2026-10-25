# Commands and results

All worktree commands used cwd `/home/user/work/wt/app-D124-activation-wholepath-sol-1425`.

1. `git show af5fe0:scripts/testing/sitecustomize.py`, `git show 4b4e0558:scripts/testing/sitecustomize.py`, `git show 9d75477:scripts/testing/sitecustomize.py` and corresponding `tests/e2e/local/support/harness.ts` reads, hashed with SHA256: PASS; both source files identical across the three refs. Absolute source paths and hashes are in evidence/facts.json. Both protected test files were read only.

2. Existing startup guard only, no daemon/sockets/sink/trace hook. Executed via a Python subprocess wrapper with the environment below (equivalent standalone command shown):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-D124-activation-wholepath-sol-1425/scripts/testing:/home/user/work/wt/rt-pin-5e9ad1c6:/home/user/work/wt/agt-pin-070dfc5e ASTRID_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-D124-helper-final-review-1315-helper.py /home/user/work/venv-runtime/bin/python -c 'import json, sitecustomize
try:
    sitecustomize._start_capture()
except SystemExit as exc:
    print(json.dumps({"exception_class": type(exc).__name__, "message": str(exc), "callsite": "scripts/testing/sitecustomize.py:_start_capture:51", "source": "existing helper basename guard", "normal_startup_exit": 78}))'
```

The caller had no ASTRID_P2_COMMIT_PHASE_CAPTURE opt-in. PASS: subprocess exit 0, stderr empty; caught exact SystemExit recorded in evidence/first-exception.json. The automatic startup path itself was not monkeypatched or changed; its exit-78 behavior is source-proved.

3. Existing offline D66 resolver, no daemon/sockets:

```bash
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_PYTHON=/home/user/work/venv-agent/bin/python D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D124-helper-final-review-1315/evidence/p2_commit_phase_capture.py D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760 PYTHONDONTWRITEBYTECODE=1 /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --input-type=module -e 'import { p2CommitPhaseCaptureConfig } from "./tests/e2e/local/support/harness.ts"; import path from "node:path"; import { tmpdir } from "node:os"; const config = p2CommitPhaseCaptureConfig(path.join(tmpdir(), "d124-offline-config")); console.log(JSON.stringify({ helper: config.helper, sha256: config.helperSha256, basename: path.basename(config.helper), witness: "offline config only; no daemon started" }));'
```

PASS, exit 0: required basename and exact SHA accepted. This is not fresh activation credit. The retained prior helper was then copied byte-exactly to this worker's own evidence/p2_commit_phase_capture.py and independently hashed.

4. Retained 1354 capture read privately with Python json/hashlib: PASS, 102 rows / 30758 bytes / mode 0600, genuine phase summaries and sampling metadata. Only structural metadata saved to evidence/retained-1354-witness.json; no raw capture, stack, request key or id copied.

5. `git diff --check`: PASS, exit 0. `git status --porcelain`: PASS, empty. No App source edits. ESLint/TypeScript: N/A. Python helper tests: not run (no helper repair).

6. `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --version`: v20.19.4. `/home/user/work/venv-runtime/bin/python --version` and `/home/user/work/venv-agent/bin/python --version`: both Python 3.13.16.

7. Requested exact normal/reviewed two-control commands: NOT RUN. They need sockets and therefore central execution under the orchestrator rule. Registry inspected: app targeted invokes Vitest, e2e-harness runs different files, and no exact Node two-control named suite exists. No invalid request was submitted and no registry modified. Exact proposed central commands are in activation-recipe.md. Async clarification requested; fresh activation remains unqualified.

Historical results, not current reruns: 1354's canonical-basename reviewed control passed 2 / 40 skipped; 1402 and 1414 normal controls passed 2 / 40 skipped; their reviewed design-basename controls failed endpoint readiness. Those historical results are distinguished from every current check above.
