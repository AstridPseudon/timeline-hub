Implemented portable, deeply frozen `{bundle, command}` capture bases. Cloning and JSON roundtripping preserve original guards; sequential B captures A’s returned `.bundle`.

Matched Agent’s final published corrections: parent intent, exact materialization ownership guards, recorded mirrors, and retained-input dependencies. Added a retained fixture checker/regenerator. No UI/hooks/outbox/client changes.

Validation passed:

```bash
npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/clipMoveCapture.test.ts
```

**78 passed.**

```bash
npx eslint src/tools/video-editor/commands/clipMoveCapture.ts src/tools/video-editor/commands/clipMovePrimitives.ts src/tools/video-editor/commands/clipMoveCapture.test.ts
git diff --check
```

Both passed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-m1-core-integration-fix /home/user/work/venv-agent/bin/python src/tools/video-editor/commands/fixtures/clip_move_parity.py
```

**28/28 exact commands, bundles and records verified**, including shared-materialization replay.

Targeted TypeScript checking passed with temporary mapping to the client worker’s official DTO; temporary files were removed.

Decision: synchronous hashing is limited to Agent’s existing identity/pin semantics because the gesture port is synchronous. No new dependencies or wire fields.

No known parity delta against Agent’s final published correction source. Next: integrate Agent/client branches and mount the session API. Full/browser/runtime acceptance remains unverified; M1 readiness is not claimed.

Commit message written to `ORCH/workers/app-m1-capture-review/commit-msg`.