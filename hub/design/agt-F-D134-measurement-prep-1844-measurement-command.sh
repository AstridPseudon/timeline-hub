#!/usr/bin/env bash
set -eu

# D134 measurement is conditional and must be dispatched by MAIN only after
# 20:00Z.  This recipe intentionally has no fallback route or package setup.
: "${D134_CLOCK_GATE:?MAIN must bind D134_CLOCK_GATE=OPEN at/after 20:00Z}"
: "${D134_CUSTODY_E2E_AT_20Z:?MAIN must bind the genuine 20:00Z custody verdict}"
: "${D134_DISPATCH:?MAIN must bind D134_DISPATCH=AUTHORIZED}"
test "$D134_CLOCK_GATE" = OPEN
test "$D134_CUSTODY_E2E_AT_20Z" = NOT_GREEN
test "$D134_DISPATCH" = AUTHORIZED

: "${AGENT_CHECKOUT:?MAIN must bind the frozen Agent checkout}"
: "${RUNTIME_CHECKOUT:?MAIN must bind the frozen Runtime checkout}"
: "${APP_CHECKOUT:?MAIN must bind the frozen App checkout}"
: "${COMPOSITION_CHECKOUT:?MAIN must bind the frozen Composition checkout}"
: "${P4_D73_MANIFEST:?MAIN must bind an existing exact-tuple D73 manifest}"
: "${P4_D73_EVIDENCE:?MAIN must bind the existing D73 evidence directory}"

test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD)" = a4e016b6a9f91fbe372672bdcf382c630bf59186
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD^{tree})" = 60d45288145414ee4702fcce61af7c7810c2a3df
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD)" = 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD^{tree})" = de2954a0ceadb4455903d9abdfec3b773318a50f
test "$(git -C "$APP_CHECKOUT" rev-parse HEAD)" = d8a1cd40b866c49c0ab415682391f0ec87a7a8e7
test "$(git -C "$APP_CHECKOUT" rev-parse HEAD^{tree})" = dd2afd6c5c7a1ac73feaac4390cc64d7f31fe7b9
test "$(git -C "$COMPOSITION_CHECKOUT" rev-parse HEAD)" = 635f4de06fda22a85fc2e4cfc764d0153a4c9f40
test "$(git -C "$COMPOSITION_CHECKOUT" rev-parse HEAD^{tree})" = 5ab5191a296980a0a6bcd1178ab6902d6478a148
test "$(git -C "$AGENT_CHECKOUT" remote get-url origin)" = https://github.com/peteromallet/astrid-agent
test "$(git -C "$RUNTIME_CHECKOUT" remote get-url origin)" = https://github.com/banodoco/banodoco-workspace-runtime
test "$(git -C "$APP_CHECKOUT" remote get-url origin)" = https://github.com/banodoco/reigh-app
test "$(git -C "$COMPOSITION_CHECKOUT" remote get-url origin)" = https://github.com/peteromallet/timeline-composition
test -z "$(git -C "$AGENT_CHECKOUT" status --porcelain --untracked-files=all)"
test -z "$(git -C "$RUNTIME_CHECKOUT" status --porcelain --untracked-files=all)"
test -z "$(git -C "$APP_CHECKOUT" status --porcelain --untracked-files=all)"
test -z "$(git -C "$COMPOSITION_CHECKOUT" status --porcelain --untracked-files=all)"

exec env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full /bin/bash --noprofile --norc -c \
  'exec "$0/tools/p4-d73-pinned-launch.sh" "$1" run -- -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$2/agent-core-full.xml" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$P4_D73_EVIDENCE"
