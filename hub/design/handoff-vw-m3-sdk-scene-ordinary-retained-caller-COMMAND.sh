#!/usr/bin/env bash
set -euo pipefail
OWN=$(cd -- "$(dirname -- "$0")" && pwd)
ROOT=/home/user/work/wt/vw-m3-sdk-scene-ordinary-retained-caller
PRIOR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-sdk-scene-existing-retention-join
PY=/home/user/work/venv-agent/bin/python
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT"
export ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules
export ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
cd "$ROOT"
SCRATCH=$(mktemp -d "$OWN/.qualification.XXXXXX")
trap 'rm -rf -- "$SCRATCH"' EXIT
mkdir -p "$SCRATCH/astrid/sdk/timeline" "$SCRATCH/tests/sdk"
cp astrid/sdk/timeline/check.py "$SCRATCH/astrid/sdk/timeline/check.py"
patch -s -p1 -d "$SCRATCH" < "$PRIOR/owner-sdk.patch"
cat >> "$SCRATCH/tests/sdk/test_retained_scene_check.py" <<'PY'


@pytest.mark.parametrize('working', [False, True])
@pytest.mark.xfail(strict=True, reason='D09: ordinary Checkout.check must acquire retained original inputs without a manual _scene_inputs tuple')
def test_ordinary_check_activates_public_node_without_manual_handoff(tmp_path, monkeypatch, root, working):
    checkout, request, workspace, snapshot, reads = source(tmp_path, monkeypatch, root, working=working)
    # Preserve the real prepared pair, inherited host source and workspace.
    # Remove only the prior proposal's test-only injection. This is a more
    # favorable environment than the ordinary CLI, which has no host handoff.
    del checkout._scene_inputs
    transport = scene_answers.host_frames_at
    observed = []

    def observe(props, basis, frames):
        answers = transport(props, basis, frames)
        observed.append(answers)
        return answers

    monkeypatch.setattr(scene_answers, 'host_frames_at', observe)
    report = checkout.check()
    assert observed, 'ordinary check never reached public Node; prior _scene_inputs setup is necessary'
    assert report.valid and not report.blocking
PY
"$PY" - "$SCRATCH" <<'PY'
import importlib.util
import sys
from pathlib import Path

import pytest

from astrid.sdk.timeline_checkout import Checkout

scratch = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location(
    'astrid.sdk.timeline._ordinary_scene_audit', scratch / 'astrid/sdk/timeline/check.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
for name in ('_on_screen', '_retained_on_screen'):
    setattr(Checkout, name, getattr(module._CheckMixin, name))
raise SystemExit(pytest.main([
    '--basetemp=' + str(scratch / 'tests-tmp'),
    '-q', '--tb=short', '-rx', '-p', 'no:cacheprovider', '-o', 'addopts=',
    str(scratch / 'tests/sdk/test_retained_scene_check.py'),
    'tests/sdk/test_scene_save_core.py',
]))
PY
git diff --check
test -z "$(git status --porcelain)"
