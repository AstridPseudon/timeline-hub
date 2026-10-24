#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(git rev-parse --show-toplevel)"
cd "$SOURCE_ROOT"

BENCH=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e
SITE="$BENCH/lib/python3.13/site-packages"
PY="$BENCH/bin/python"
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
BROWSER=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
FFMPEG=/usr/bin/ffmpeg
FFPROBE=/usr/bin/ffprobe
COMPOSITION="$PROFILE/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz"
RUNTIME="$SITE"

test -x "$PY"
test -d "$SITE"
test -x "$NODE"
test -x "$BROWSER"
test -x "$FFMPEG"
test -x "$FFPROBE"
test -f "$PROFILE/package-lock.json"
test -f "$COMPOSITION"
test "$(sha256sum "$PROFILE/package-lock.json" | awk '{print $1}')" = f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d
test "$(sha256sum "$COMPOSITION" | awk '{print $1}')" = 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234
test "$(sha256sum "$NODE" | awk '{print $1}')" = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
test "$(sha256sum "$BROWSER" | awk '{print $1}')" = 85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95
test "$(sha256sum "$FFMPEG" | awk '{print $1}')" = ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41
test "$(sha256sum "$FFPROBE" | awk '{print $1}')" = 272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f

echo "SOURCE_ROOT=$SOURCE_ROOT"
echo "SOURCE_HEAD=$(git rev-parse HEAD)"
echo "SOURCE_TREE=$(git rev-parse HEAD^{tree})"
echo "SOURCE_BODY_SHA256=$(sha256sum tests/packs/video_editing/test_runtime_publication_chain.py tests/test_installer_service_repair_integration.py tests/test_conftest_environment.py)"
echo "RUNTIME_ENV=$RUNTIME"
echo "PROFILE=$PROFILE"
echo "PROFILE_LOCK_SHA256=$(sha256sum "$PROFILE/package-lock.json" | awk '{print $1}')"
echo "COMPOSITION_ARCHIVE=$COMPOSITION"
echo "COMPOSITION_ARCHIVE_SHA256=$(sha256sum "$COMPOSITION" | awk '{print $1}')"
echo "NODE=$NODE"
echo "NODE_SHA256=$(sha256sum "$NODE" | awk '{print $1}')"
echo "BROWSER=$BROWSER"
echo "BROWSER_SHA256=$(sha256sum "$BROWSER" | awk '{print $1}')"
echo "FFMPEG=$FFMPEG"
echo "FFMPEG_SHA256=$(sha256sum "$FFMPEG" | awk '{print $1}')"
echo "FFPROBE=$FFPROBE"
echo "FFPROBE_SHA256=$(sha256sum "$FFPROBE" | awk '{print $1}')"
echo "PROVISION_REPORT_SHA256=$(sha256sum "$BENCH/.provision-report" | awk '{print $1}')"
echo "IMPORT_ORIGINS_SHA256=$(sha256sum "$BENCH/.astrid-import-origins" | awk '{print $1}')"
echo "DISTRIBUTION_METADATA_SHA256=$(sha256sum "$BENCH/.astrid-distribution-metadata" | awk '{print $1}')"
echo "AGENT_RECORD_SHA256=$(sha256sum "$SITE/astrid-0.1.0.dist-info/RECORD" | awk '{print $1}')"
echo "RUNTIME_RECORD_SHA256=$(sha256sum "$SITE/astrid_runtime-0.1.0.dist-info/RECORD" | awk '{print $1}')"
echo "AGENT_DIRECT_URL=$(cat "$SITE/astrid-0.1.0.dist-info/direct_url.json")"
echo "RUNTIME_DIRECT_URL=$(cat "$SITE/astrid_runtime-0.1.0.dist-info/direct_url.json")"
echo "ORIGINS_I_BEGIN"
"$PY" -I -c 'import astrid, astrid_runtime, astrid_runtime_client, runtime_protocol; print(astrid.__file__); print(astrid_runtime.__file__); print(astrid_runtime_client.__file__); print(runtime_protocol.__file__)'
echo "ORIGINS_I_END"

# The managed c886 entry has no Agent wheel artifact.  The older D13 carrier
# points at ef851 and is deliberately not reused or relabeled as c36.
D13_WHEEL="$BENCH/wheelhouse/astrid-0.1.0-py3-none-any.whl"
if test -f "$D13_WHEEL"; then
  echo "D13_UNEXPECTED_WHEEL=$D13_WHEEL"
else
  echo "D13_NOT_READY missing field=agent_wheel path=$D13_WHEEL"
  echo "D13_NOT_READY managed c886 has RECORD/direct_url only; no c36 wheel carrier"
fi

COLLECTED="$($PY -P -m pytest -q -o addopts= -p no:cacheprovider --collect-only \
  tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0] \
  tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[True-1] \
  tests/test_conftest_environment.py::test_bootstrap_environment_is_accepted_by_the_remotion_probe_context)"
printf '%s\n' "$COLLECTED"
test "$(printf '%s\n' "$COLLECTED" | grep -Ec '^tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids\[(False-0|True-1)\]$')" = 2
test "$(printf '%s\n' "$COLLECTED" | grep -Fc 'tests/test_conftest_environment.py::test_bootstrap_environment_is_accepted_by_the_remotion_probe_context')" = 1

HOME_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/env-misc-0020-home.XXXXXX")"
mkdir -p "$HOME_ROOT"
export HOME="$HOME_ROOT"
export PATH="$(dirname "$NODE"):$BENCH/bin:/usr/bin:/bin"
export PYTHONDONTWRITEBYTECODE=1
export ASTRID_HOST_EXECUTION_PROFILE=installed
export ASTRID_PACK_HOST_PYTHON="$PY"
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SITE"
export ASTRID_REMOTION_PROJECT_DIR="$PROFILE"
export ASTRID_NODE_EXECUTABLE="$NODE"
export ASTRID_TEST_NODE_MODULES="$PROFILE/node_modules"
export ASTRID_REMOTION_BROWSER_EXECUTABLE="$BROWSER"
export ASTRID_FFMPEG_EXECUTABLE="$FFMPEG"
export ASTRID_FFPROBE_EXECUTABLE="$FFPROBE"
export PYTHONPATH="$SOURCE_ROOT"

"$PY" -P -m pytest -q -o addopts= -p no:cacheprovider \
  tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[False-0] \
  tests/test_installer_service_repair_integration.py::test_repair_restarts_real_runtime_for_failed_service_and_preserves_healthy_pids[True-1] \
  tests/test_conftest_environment.py::test_bootstrap_environment_is_accepted_by_the_remotion_probe_context

echo "PROFILE_AFTER_LOCK_SHA256=$(sha256sum "$PROFILE/package-lock.json" | awk '{print $1}')"
echo "PROFILE_AFTER_COMPOSITION_SHA256=$(sha256sum "$COMPOSITION" | awk '{print $1}')"
