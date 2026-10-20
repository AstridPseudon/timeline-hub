#!/usr/bin/env bash
set -euo pipefail

ROOT=/home/user/work/wt/vw-m3-sdk-retained-scene-proposal-final-gate
OWN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-sdk-scene-existing-retention-join
PY=/home/user/work/venv-agent/bin/python
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT"
export ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules
export ASTRID_NODE_EXECUTABLE="$NODE"

cd "$ROOT"
SCRATCH=$(mktemp -d /tmp/vw-m3-sdk-retained-review.XXXXXX)
mkdir -p "$SCRATCH/astrid/sdk/timeline" "$SCRATCH/tests/sdk"
cp "$ROOT/astrid/sdk/timeline/check.py" "$SCRATCH/astrid/sdk/timeline/check.py"
patch -s -p1 -d "$SCRATCH" < "$OWN/owner-sdk.patch"

set +e
"$PY" - "$SCRATCH" <<'PY'
import importlib.util
import sys
from pathlib import Path

import pytest

scratch = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location(
    "astrid.sdk.timeline._check_proposal_review", scratch / "astrid/sdk/timeline/check.py"
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

from astrid.sdk.timeline_checkout import Checkout

for name in ("_on_screen", "_retained_on_screen"):
    setattr(Checkout, name, getattr(module._CheckMixin, name))

raise SystemExit(pytest.main([
    "--basetemp=" + str(scratch / "proposal-tests"),
    "-q", "--tb=short", "-p", "no:cacheprovider", "-o", "addopts=",
    str(scratch / "tests/sdk/test_retained_scene_check.py"),
    str(Path.cwd() / "tests/sdk/test_scene_save_core.py"),
]))
PY
STATUS=$?
set -e
find "$SCRATCH" -depth -type f -delete
find "$SCRATCH" -depth -type l -delete
find "$SCRATCH" -depth -type d -empty -delete
exit "$STATUS"
