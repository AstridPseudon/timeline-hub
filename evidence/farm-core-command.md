# D124 Farm input: corrected agent-core-full command

Source-only derivative of the preserved D124 input packet from worker 1330.
The core Agent target is corrected to the owner-approved
0b586e4b56cffbcd066ea8792adf46b660f5395a normal binding/captured-redo join.
The earlier b545b616a41388e24d6f2a59b7b45c26cb057d2c tuple remains historical
preparation evidence and is not relabeled as this target.

This is a Farm controller handoff, not an execution claim. Farm must obtain a
new normal checkout and child/profile receipts for 0b586e4b; no receipt is
claimed here.

## Captured immutable tuple

| role | Farm checkout binding | commit | tree | parent guard |
| --- | --- | --- | --- | --- |
| Agent | <FARM_NORMAL_CHECKOUT_AGENT_0B586E4B> | 0b586e4b56cffbcd066ea8792adf46b660f5395a | bb23455ea5f38120c251a91f4a4afeeb1ea3d5ce | 0b586e4b56cffbcd066ea8792adf46b660f5395a 225fccb77e59d9ab8dc456feaff910625d2d12f8 c474325862e5d45aaf97906fd09f560fb65ffe0b |
| Runtime | <FARM_NORMAL_CHECKOUT_RUNTIME_42AAD0E9> | 42aad0e92f6da8ea83dd0a382a87e3acd12651b0 | 085a5be70b56353deb41ae7d743336a4ccb7f29c | 42aad0e92f6da8ea83dd0a382a87e3acd12651b0 369ffa7c00bd3d45c610fac7651ff79e7a283a1a |
| App | <FARM_NORMAL_CHECKOUT_APP_D8A1CD40> | d8a1cd40b866c49c0ab415682391f0ec87a7a8e7 | dd2afd6c5c7a1ac73feaac4390cc64d7f31fe7b9 | d8a1cd40b866c49c0ab415682391f0ec87a7a8e7 34d4644589970274a5252c0f7c68b6288eb0b0b4 |
| Composition | <FARM_NORMAL_CHECKOUT_COMPOSITION_635F4DE0> | 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 | 5ab5191a296980a0a6bcd1178ab6902d6478a148 | 635f4de06fda22a85fc2e4cfc764d0153a4c9f40 7a95a40b07ea0d273e17afb69dbc3456b603f2bc |

The App and Composition SHA/tree pairs are the original Farm capture and are
unchanged. The values above were read with git rev-parse from authoritative Git
objects; Farm must verify them again on actual normal receipts.

## Farm-owned pending inputs

These are intentionally unresolved. The Farm lead must request them through the
existing normal routes, then render the D73 manifest/evidence from those
receipts. Do not use the historical b545 checkout, an old 070dfc manifest, or
the existing 9cd3dbe8/1d9ddba5 near-match profile.

~~~text
P4_D73_MANIFEST=<FARM_GENERATED_D73_MANIFEST_FROM_0B_NORMAL_RECEIPTS>
P4_D73_EVIDENCE=<FARM_OWNED_D124_CORE_EVIDENCE_DIRECTORY>
P4_PYTHON=<NORMAL_CHILD_VENV_PYTHON_RECEIPT_KEYED_TO_0B586E4B_AND_42AAD0E9>
P4_NODE=<NORMAL_PROFILE_NODE_RECEIPT_FOR_V20.19.4>
P4_PROFILE=<NORMAL_RUNTIME_PROFILE_RECEIPT_KEYED_TO_0B586E4B_AND_42AAD0E9>
MAIN_POSITIVE_CONTROL=<LEAD_EXISTING_PARSED_POSITIVE_CONTROL>
MAIN_POSITIVE_COUNTER=<LEAD_FRESH_POSITIVE_COUNTER_PATH>
MAIN_POISON_CONTROL=<LEAD_EXISTING_PARSED_POISON_CONTROL>
MAIN_POISON_COUNTER=<LEAD_FRESH_POISON_COUNTER_PATH>
~~~

The exact Farm lead request is the existing checkout route, with no new
checkout implementation:

~~~sh
"$ORCH/bin/request-checkout" agent 0b586e4b56cffbcd066ea8792adf46b660f5395a 'D124 corrected D73 core Agent target'
~~~

The lead must request the normal runtime profile and child venv keyed to the
new Agent SHA and unchanged Runtime SHA, then verify those receipt keys in the
generated manifest. Profile targets remain Node v20.19.4, Composition 0.0.14,
archive 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234,
profile lock f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d,
profile registry d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96,
and schema digest
sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b.
These are validation targets, not locally observed profile receipts.

## Corrected source and launcher identity

The existing launcher is still the only launcher:

~~~text
<FARM_NORMAL_CHECKOUT_AGENT_0B586E4B>/tools/p4-d73-pinned-launch.sh
~~~

Its Git blob is 2844cec15b97fa995ecaf120961fc891b8e13b1c and its SHA-256 is
cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1 at both
b545 and 0b586e. The target remotion tree is
b01dca9b3b24f54093c20b7c5657316f997725db; the timeline/schema tree is
8729690bef06784028a0474ad55b811fea52406d; and
astrid/core/timeline/banodoco_schema.py is blob
1b3f12da05da3bb89fa76881184eefdf8232e076 at both commits. The runtime lock
blob is also invariant (e3b3e2ac385ae1d9a025c81d75811f9dacd4f0fc). No new
Remotion, schema, launcher, generated, or pin input is needed.

The target-specific source delta is the owner-approved merge:
225fccb77e59d9ab8dc456feaff910625d2d12f8 plus captured-redo parent
c474325862. Farm should retain normal binding and captured-redo source
receipts for this target; this worker does not author host code.

## Exact unfiltered core selector

The metadata inventory remains 23; the actual selector argv has exactly 22
roots. It includes the live-scene composition root and has no marker, -k, row,
or prefilter exclusion.

~~~sh
set -eu
: "${AGENT_CHECKOUT:?Farm must bind the new normal Agent 0b586e checkout}"
: "${RUNTIME_CHECKOUT:?Farm must bind the captured Runtime checkout}"
: "${APP_CHECKOUT:?Farm must bind the captured App checkout}"
: "${COMPOSITION_CHECKOUT:?Farm must bind the captured Composition checkout}"
: "${P4_D73_MANIFEST:?Farm must generate the D73 manifest from receipts}"
: "${P4_D73_EVIDENCE:?Farm must bind its owned evidence directory}"
: "${P4_PYTHON:?Farm must bind the normal child-venv Python receipt}"
: "${P4_NODE:?Farm must bind the normal Node v20.19.4 receipt}"

test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD)" = 0b586e4b56cffbcd066ea8792adf46b660f5395a
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD^{tree})" = bb23455ea5f38120c251a91f4a4afeeb1ea3d5ce
test "$(git -C "$AGENT_CHECKOUT" rev-list --parents -n 1 HEAD)" = '0b586e4b56cffbcd066ea8792adf46b660f5395a 225fccb77e59d9ab8dc456feaff910625d2d12f8 c474325862e5d45aaf97906fd09f560fb65ffe0b'
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD)" = 42aad0e92f6da8ea83dd0a382a87e3acd12651b0
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD^{tree})" = 085a5be70b56353deb41ae7d743336a4ccb7f29c
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
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD:tools/p4-d73-pinned-launch.sh)" = 2844cec15b97fa995ecaf120961fc891b8e13b1c
test "$(sha256sum "$AGENT_CHECKOUT/tools/p4-d73-pinned-launch.sh" | awk '{print $1}')" = cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1
test "$("$P4_NODE" --version)" = v20.19.4
test "$(awk -F= '$1 == "agent_sha" {print $2}' "$P4_D73_MANIFEST")" = 0b586e4b56cffbcd066ea8792adf46b660f5395a
test "$(awk -F= '$1 == "runtime_sha" {print $2}' "$P4_D73_MANIFEST")" = 42aad0e92f6da8ea83dd0a382a87e3acd12651b0
test "$(awk -F= '$1 == "app_sha" {print $2}' "$P4_D73_MANIFEST")" = d8a1cd40b866c49c0ab415682391f0ec87a7a8e7
test "$(awk -F= '$1 == "composition_sha" {print $2}' "$P4_D73_MANIFEST")" = 635f4de06fda22a85fc2e4cfc764d0153a4c9f40
! grep -Fq 070dfc "$P4_D73_MANIFEST"
! grep -Fq b545b616 "$P4_D73_MANIFEST"

NODE_BIN=$(dirname "$P4_NODE")
VENV_ROOT=$(dirname "$(dirname "$P4_PYTHON")")
exec env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH="$NODE_BIN:/usr/local/bin:/usr/bin:/bin" \
  VIRTUAL_ENV="$VENV_ROOT" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full /bin/bash --noprofile --norc -c \
  'exec "$0/tools/p4-d73-pinned-launch.sh" "$1" run -- -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$2/agent-core-full.xml" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py' "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$P4_D73_EVIDENCE"
~~~

The command is source-reviewable only and is not run by this worker.

## Existing parsed-row controls

Farm must run the existing controls once before any body, with separate fresh
counters. These controls are required inputs/expectations, not observed
results here.

~~~sh
: "${MAIN_POSITIVE_CONTROL:?lead must bind the existing parsed positive control}"
: "${MAIN_POSITIVE_COUNTER:?lead must bind the fresh positive counter}"
: "${MAIN_POISON_CONTROL:?lead must bind the existing parsed poison control}"
: "${MAIN_POISON_COUNTER:?lead must bind the fresh poison counter}"

set +e
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" PATH="$(dirname "$P4_NODE"):/usr/local/bin:/usr/bin:/bin" \
  VIRTUAL_ENV="$(dirname "$(dirname "$P4_PYTHON")")" \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-positive P4_STUB_COUNT="$MAIN_POSITIVE_COUNTER" \
  /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$MAIN_POSITIVE_CONTROL"
positive_rc=$?
set -e
test "$positive_rc" != 0
test "$positive_rc" = 17
test "$(wc -l < "$MAIN_POSITIVE_COUNTER")" = 1

set +e
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" PATH="$(dirname "$P4_NODE"):/usr/local/bin:/usr/bin:/bin" \
  VIRTUAL_ENV="$(dirname "$(dirname "$P4_PYTHON")")" \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-poison P4_STUB_COUNT="$MAIN_POISON_COUNTER" \
  /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$MAIN_POISON_CONTROL"
poison_rc=$?
set -e
test "$poison_rc" != 0
test "$(wc -l < "$MAIN_POISON_COUNTER")" = 0
~~~

Expected accounting is positive parsed once (exit 17, one counter line) and
poison zero (nonzero exit, zero counter lines). The production caller retains
the complete C0 seam: request api_version, project_id, timeline_id,
base_revision_id, base_publication_id, commands, label, steps, merge, reads,
Idempotency-Key, dry_run; replies accepted/merged canonical head and receipt,
records, bindings, effects, dependencies, history, undo_steps; conflict
reason/head; invalid code/path/hint/suggested command; and preview
would_status with null receipt.
