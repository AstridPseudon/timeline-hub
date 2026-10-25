# F-final / D54a pristine-upstream core preparation

Preparation only. No checkout, profile, venv, Store, source install, launcher,
registry, core/full/browser/P4/render/wheel/ZIP command, or central test request
was executed by this worker. The command below is the existing published normal
route from design/agent-core-full-command.md; selector order, launcher flags,
PYTHONNOUSERSITE=1, and --timeout=45 are preserved verbatim.

Pristine-gate status: NOT EXECUTABLE from the named upstream object because the
five route roots and D73 launcher are classified as
`UNKNOWN_MISSING_UPSTREAM_SELECTOR`. This artifact records the proposed command
and its first-return mapping only; it does not claim a gate pass or zero count.

## Existing normal route (MAIN-bound inputs)

MAIN must bind genuine immutable paths for all six inputs. The fixed guards in
the retained document are historical; for this final comparison MAIN would
bind the named upstream objects in source-manifest.json and must re-check every
path/tree before any request. This worker does not rewrite the published route
or fabricate a replacement launcher.

~~~sh
set -eu
: "${AGENT_CHECKOUT:?MAIN must bind immutable Agent checkout}"
: "${RUNTIME_CHECKOUT:?MAIN must bind immutable Runtime checkout}"
: "${APP_CHECKOUT:?MAIN must bind immutable App checkout}"
: "${COMPOSITION_CHECKOUT:?MAIN must bind immutable Composition checkout}"
: "${P4_D73_MANIFEST:?MAIN must bind the existing D73 manifest}"
: "${P4_D73_EVIDENCE:?MAIN must bind the existing evidence directory}"
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD)" = 886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD^{tree})" = f53cc8426ccef8760021ef6207303bce7b80e777
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD)" = dbcdb97c50afc72bd5e2599cb7ead0fe56bc7c4f
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD^{tree})" = 904d3d90d8235d4a27f2d5a8cbf88298d5ec0210
test "$(git -C "$AGENT_CHECKOUT" remote get-url origin)" = https://github.com/peteromallet/astrid-agent
test "$(git -C "$RUNTIME_CHECKOUT" remote get-url origin)" = https://github.com/banodoco/banodoco-workspace-runtime
test "$(git -C "$APP_CHECKOUT" remote get-url origin)" = https://github.com/banodoco/reigh-app
test "$(git -C "$COMPOSITION_CHECKOUT" remote get-url origin)" = https://github.com/peteromallet/timeline-composition
exec env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full /bin/bash --noprofile --norc -c \
  'exec "$0/tools/p4-d73-pinned-launch.sh" "$1" run -- -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$2/agent-core-full.xml" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py' "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$P4_D73_EVIDENCE"
~~~

The existing parsed preflight is the same launcher in dry mode. MAIN must supply
the existing positive and poison controls and fresh counter paths; these names
are intentionally not guessed here:

~~~sh
: "${MAIN_POSITIVE_CONTROL:?MAIN must bind the existing positive parsed-row control command}"
: "${MAIN_POSITIVE_COUNTER:?MAIN must bind the positive control counter path}"
: "${MAIN_POISON_CONTROL:?MAIN must bind the existing poison input for the same control entrypoint}"
: "${MAIN_POISON_COUNTER:?MAIN must bind the poison control counter path}"

set +e
env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-positive \
  P4_STUB_COUNT="$MAIN_POSITIVE_COUNTER" /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$MAIN_POSITIVE_CONTROL"
positive_rc=$?
set -e
test "$positive_rc" != 0
test "$positive_rc" = 17
test "$(wc -l < "$MAIN_POSITIVE_COUNTER")" = 1

set +e
env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-poison \
  P4_STUB_COUNT="$MAIN_POISON_COUNTER" /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$MAIN_POISON_CONTROL"
poison_rc=$?
set -e
test "$poison_rc" != 0
test "$(wc -l < "$MAIN_POISON_COUNTER")" = 0
~~~

Expected output is owned by MAIN's genuine evidence path only:
$P4_D73_EVIDENCE/agent-core-full.xml. No output was created here.

## C0 production request contract (reference only)

No C0 request was constructed or submitted. The final caller must use the
existing public shape, with no public-shape change:

~~~json
{
  "api_version": 1,
  "project_id": "<exact>",
  "timeline_id": "<exact>",
  "base_revision_id": "<exact>",
  "base_publication_id": "<exact>",
  "commands": [{"schema_version": "<exact>", "op": "<exact>", "version": "<exact>", "select": "<exact>", "args": {"<exact>": "<exact>"}}],
  "label": "<exact>",
  "steps": [{"id": "<exact>", "label": "<exact>", "intent": "<exact>", "tags": [], "command_ordinals": [], "patch": {}, "reads": {}}],
  "merge": "fields",
  "reads": [],
  "dry_run": false,
  "source": "<exact>",
  "rationale": "<exact>",
  "group_id": "<exact>"
}
~~~

The HTTP request carries `Idempotency-Key: <exact>` as header metadata; it is not
a JSON body property. For example, the transport metadata is:

~~~http
Idempotency-Key: <exact>
Content-Type: application/json
~~~

The body uses the exact step field `reads`. Merge may be fields or atomic.
Accepted/merged replies carry canonical/base/
landing, merge_mode, receipt, records, bindings, effects, dependencies, history,
and undo_steps. Conflicts carry reason and head; invalid requests carry code,
path, hint, and suggested_command; preview carries would_status and a null
receipt.



