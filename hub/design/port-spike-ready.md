# Timeline R4 M0 port spike ready

The disposable Agent worktree is ready for the recipe worker to exercise the
import-clean R4 APIs read-only. The recipe worker must not edit this worktree.

Worktree: `/home/user/work/wt/agt-m0-spike`  
Branch: `tl/agt-m0-spike`  
Base: `tl/integration` / `e51595c6`  
Frozen source: `origin/codex/handover-timeline-r4-20261019-candidate-sdk`

## Import result

The full `astrid.sdk.timeline` package walk imported 58 module candidates with
0 failures using system Python:

```text
cd /home/user/work/wt/agt-m0-spike
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 - <<'PY'
import importlib, pkgutil
package = importlib.import_module('astrid.sdk.timeline')
names = [item.name for item in pkgutil.walk_packages(package.__path__, package.__name__ + '.') if not item.ispkg]
failures = []
for name in names:
    try:
        importlib.import_module(name)
    except Exception as exc:
        failures.append((name, type(exc).__name__, str(exc)))
print(f'import candidates: {len(names)}')
print(f'failed: {len(failures)}')
raise SystemExit(bool(failures))
PY
```

## Module list for read-only recipe work

Minimal timing/editing surface:

```text
astrid/sdk/timeline/commands.py
astrid/sdk/timeline/compiler.py
astrid/sdk/timeline/continuous.py
astrid/sdk/timeline/inverse.py
astrid/sdk/timeline/model.py
astrid/sdk/timeline/rebase.py
astrid/sdk/timeline/sequence_fit.py
astrid/sdk/timeline/transitions.py
astrid/core/timeline/compatibility.py
astrid/core/timeline/cut_index.py
astrid/core/timeline/motion_curves.py
```

Available adjacent modules for read-only probes:

```text
astrid/sdk/timeline/music_beds.py
astrid/sdk/timeline/music_lane.py
astrid/sdk/timeline/transcript_binding.py
astrid/sdk/timeline/transcript_commands.py
astrid/sdk/timeline/transcripts.py
astrid/sdk/timeline/story.py
astrid/sdk/timeline/shot_groups.py
astrid/sdk/timeline/graph_commands.py
astrid/sdk/timeline/drafts.py
astrid/sdk/timeline/restore_commit.py
astrid/core/timeline/audio_envelope.py
astrid/core/timeline/chapter_storage.py
astrid/core/timeline/copy_sync.py
astrid/core/timeline/music_bed.py
```

The full path classification, current-main seams, and exact test evidence are
in [`port-manifest.md`](./port-manifest.md).

## Evidence already exercised

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 -m pytest -q \
  tests/sdk/test_timing_compiler.py tests/sdk/test_timing_cycles.py \
  tests/core/timeline/test_motion_curves.py \
  -k 'not generated_python_and_typescript_are_fresh'
```

Result: `69 passed, 1 deselected, 2 warnings in 4.52s`.

The original-main comparison was `195 passed, 1 failed, 17 deselected, 6
warnings`; the single failure needs unavailable font measurement support. The
remaining classified R4 results and logs are in `port-manifest.md`.

## Read-only recipe command

```text
cd /home/user/work/wt/agt-m0-spike
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD python3 - <<'PY'
from astrid.sdk.timeline import compiler, model, sequence_fit
print(compiler.__name__, model.__name__, sequence_fit.__name__)
PY
```

Use system Python until the orchestration environment publishes
`agent-env-ready.md`; then use the shared dependencies-only interpreter with
`PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python`. Do not install into
that environment and do not run git mutations. This spike does not claim that
Runtime, App, or Composition integration is complete.
