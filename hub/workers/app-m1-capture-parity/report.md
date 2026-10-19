Implemented `captureClipMove(bundle, select)` → opaque basis, `finishClipMove(basis, on)` → `{command, bundle, record, previewAt}`, and detached `executeClipMove`. Sequential B uses A’s returned authored bundle; finish preserves original guards.

Validation passed:

- `npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/commands/clipMoveCapture.test.ts` — **54 passed**.
- `npx eslint src/tools/video-editor/commands/clipMoveCapture.ts src/tools/video-editor/commands/clipMovePrimitives.ts src/tools/video-editor/commands/clipMoveCapture.test.ts` — passed.
- `npx tsc -p /tmp/app-m1-capture-parity-tsconfig.json` — passed using the client worker’s official generated DTO artifact through temporary path mapping.
- `git diff --check` and explicit added-file whitespace checks — passed.

Python verification invocation — **18/18 exact commands, bundles and records passed**:

```bash
PYTHONPATH=/home/user/work/wt/agt-m1-core /home/user/work/venv-agent/bin/python - <<'PY'
import json
from astrid.sdk.timeline.capture import capture_move
from astrid.sdk.timeline.commands import execute
f = json.load(open('src/tools/video-editor/commands/fixtures/recipe_m1_move.json'))
for case in [f, *f['cases']]:
    command = capture_move(case['bundle'], case['select'], case['on'])
    plan = execute(case['bundle'], [command])
    assert command == case['command'], case['name']
    assert plan.bundle == case['after_bundle'], case['name']
    assert plan.records[0] == case['record'], case['name']
PY
```

Agent source and regeneration command are recorded in `clipMoveCapture.test.ts`. The implementation follows executable Agent semantics, including occurrence ownership intent on parent moves despite differing handoff prose. FPS fractions exceeding safe browser integer precision fail closed.

Next: merge the client DTO artifact and wire the session/UI adapter. Provider, drag and full/browser integration remain unverified; none were run. Commit message written to the assigned path; temporary files removed.