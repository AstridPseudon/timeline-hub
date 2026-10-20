#!/usr/bin/env bash
set -euo pipefail
OWN=$(cd -- "$(dirname -- "$0")" && pwd)
ROOT=/home/user/work/wt/vw-m3-sdk-scene-existing-retention-join
PY=/home/user/work/venv-agent/bin/python
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH="$ROOT"
export ASTRID_TEST_NODE_MODULES=/home/user/work/wt/vw-m1-ssr-snapshot/remotion/node_modules
export ASTRID_NODE_EXECUTABLE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
cd "$ROOT"
SCRATCH=$(mktemp -d "$OWN/.qualification.XXXXXX")
trap 'rm -rf -- "$SCRATCH"' EXIT
"$PY" -m pytest --basetemp="$SCRATCH/owned-tests" -q --tb=short -p no:cacheprovider -o addopts= \
  tests/packs/rendering/test_prepared_scene_query.py \
  tests/packs/rendering/test_scene_answers.py tests/packs/rendering/test_scene_host.py \
  tests/sdk/test_scene_save_core.py tests/sdk/test_scene_caller_preservation.py
# Apply the owner patch only in private scratch. Load the exact proposed methods
# into the existing Checkout class; the actual worktree SDK stays untouched.
mkdir -p "$SCRATCH/astrid/sdk/timeline" "$SCRATCH/tests/sdk"
cp astrid/sdk/timeline/check.py "$SCRATCH/astrid/sdk/timeline/check.py"
patch -s -p1 -d "$SCRATCH" < "$OWN/owner-sdk.patch"
"$PY" - "$SCRATCH" <<'PY'
import importlib.util
import sys
from pathlib import Path

import pytest

from astrid.sdk.timeline_checkout import Checkout

scratch = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location(
    'astrid.sdk.timeline._check_proposal', scratch / 'astrid/sdk/timeline/check.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
for name in ('_on_screen', '_retained_on_screen'):
    setattr(Checkout, name, getattr(module._CheckMixin, name))
raise SystemExit(pytest.main([
    '--basetemp=' + str(scratch / 'proposal-tests'),
    '-q', '--tb=short', '-p', 'no:cacheprovider', '-o', 'addopts=',
    str(scratch / 'tests/sdk/test_retained_scene_check.py'),
    'tests/sdk/test_scene_save_core.py', 'tests/sdk/test_scene_caller_preservation.py',
    'tests/sdk/test_timeline_transaction.py', 'tests/sdk/test_timeline_publish_connection.py',
    'tests/sdk/test_timeline_commit_provider.py', 'tests/sdk/test_workspace_client_timeline_commit.py',
    'tests/packs/rendering/test_verified_source.py',
]))
PY
/home/user/work/venv-agent/bin/ruff check --no-cache astrid/core/timeline/scene_answers.py \
  tests/packs/rendering/test_prepared_scene_query.py "$SCRATCH/tests/sdk/test_retained_scene_check.py"
git diff --check
