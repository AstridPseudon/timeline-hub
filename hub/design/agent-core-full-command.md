# D108a: `agent-core-full` source-only publication

Status: published for MAIN execution. This is the sole Agent full-core route.
The Agent worker did not collect, execute, submit, register, or write a body.

## Binding source and immutable tuple

MAIN binds these variables through the normal request-checkout path. They are
not the mutable `/home/user/work/{agent,runtime,app,composition}` worktrees:

```sh
AGENT_CHECKOUT='<immutable checkout returned by MAIN request-checkout>'
RUNTIME_CHECKOUT='<immutable checkout returned by MAIN request-checkout>'
APP_CHECKOUT='<immutable checkout returned by MAIN request-checkout>'
COMPOSITION_CHECKOUT='<immutable checkout returned by MAIN request-checkout>'
P4_D73_MANIFEST='<MAIN-owned existing manifest path>'
P4_D73_EVIDENCE='<MAIN-owned existing evidence directory>'
```

Exact fixed guards:

```text
Agent commit:   070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2
Agent tree:     6056414359ae9fce08d999d54cbecf719fda33c3
Runtime commit: 1daca2a33f6d7b10053e07c539a54843e3984e19
Runtime tree:   a522511414947e48e317a5e5c2103483b121a750
```

Runtime `runtime.lock` must name the Runtime commit above. APP_CHECKOUT and
COMPOSITION_CHECKOUT are the App and Composition roles captured once by MAIN's
existing request-checkout receipts; this document does not invent their missing
full paths or SHAs. The existing D73 manifest carries and verifies all four
checkout SHA/tree/path tuples.

The existing provider/schema ABI is:

```text
python=/home/user/work/venv-agent/bin/python
venv=/home/user/work/venv-agent
schema=/home/user/work/venv-agent/lib/python3.13/site-packages
node=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
node_version=v20.19.4
profile=<existing immutable profile bound by MAIN; no profile creation>
schema_digest=sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b
composition_version=0.0.14
profile_lock_sha=f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d
profile_archive_sha=819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234
profile_registry_sha=d609b44b37d724358a33405e9d8539008fd1ac30bc2f0d9746575c3fbadaac96
```

## Exact expanded command

This is the existing row-181 command with only path-sensitive bindings made
explicit. The launcher, manifest format, preflight, and provider binding are
existing artifacts. MAIN supplies genuine immutable checkout and evidence paths;
the JUnit path is under MAIN's evidence directory.

```sh
set -eu
: "${AGENT_CHECKOUT:?MAIN must bind immutable Agent checkout}"
: "${RUNTIME_CHECKOUT:?MAIN must bind immutable Runtime checkout}"
: "${APP_CHECKOUT:?MAIN must bind immutable App checkout}"
: "${COMPOSITION_CHECKOUT:?MAIN must bind immutable Composition checkout}"
: "${P4_D73_MANIFEST:?MAIN must bind the existing D73 manifest}"
: "${P4_D73_EVIDENCE:?MAIN must bind the existing evidence directory}"
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD)" = 070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD^{tree})" = 6056414359ae9fce08d999d54cbecf719fda33c3
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD)" = 1daca2a33f6d7b10053e07c539a54843e3984e19
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD^{tree})" = a522511414947e48e317a5e5c2103483b121a750
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
  ASTRID_REMOTION_PROJECT_DIR='<MAIN manifest profile path>' \
  ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node \
  ASTRID_TEST_NODE_MODULES='<MAIN manifest profile path>/node_modules' \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full /bin/bash --noprofile --norc -c \
  'exec "$0/tools/p4-d73-pinned-launch.sh" "$1" run -- -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$2/agent-core-full.xml" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py' "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$P4_D73_EVIDENCE"
```

The `python` field is the existing launcher manifest binding; the launcher
executes `/home/user/work/venv-agent/bin/python -P`. The profile value and its
node_modules path remain manifest-bound, not fabricated here.

## Expanded root inventory and source-consistency finding

The selector argv above expands to these actual roots, in order:

```text
tests/editing_conformance
tests/sdk
tests/timeline
tests/core/timeline
tests/core/test_timeline_element_orphan_cleanup.py
tests/core/test_timeline_element_publication.py
tests/core/test_timeline_element_publication_runtime.py
tests/core/rendering/test_timeline_visualize_cli_grammar.py
tests/core/rendering/test_local_schema.py
tests/packs/timeline
tests/packs/rendering/test_composition_package.py
tests/packs/rendering/test_live_scene_composition.py
tests/packs/rendering/test_render_export_task_adapter.py
tests/packs/rendering/test_timeline_filmstrip_cards.py
tests/packs/rendering/test_timeline_filmstrip_execution.py
tests/packs/video_editing/test_runtime_publication_chain.py
tests/stage1/test_cold_launch_autobootstrap.py
tests/test_installer_schema.py
tests/test_installer_sources.py
tests/test_installer_bootstrap_schema.py
tests/test_timeline_clip_replacement.py
tests/v10/test_timelines_create.py
```

The old handoff/manifest metadata says `root_count=23`, but the exact row 181
command, `-core-roots.txt`, and root inventory contain 22 actual selector roots
(the `total` inventory key is not a selector). No 23rd path exists in the
provided source, and no path is invented here. Agent `070dfc` includes the
released D110 test under `tests/sdk`; adding that file as another selector would
change the existing recipe and duplicate collection. MAIN must reconcile any
central count field against the byte inventory before installing the row.

## Existing row recipe and path substitutions

The existing source recipe is the row-181 form below. MAIN substitutes only the
named checkout/evidence bindings; the root argv and launcher remain unchanged:

```text
agent OWN-REHEARSAL-SUITE env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 P4_D73_MANIFEST=/tmp/.../own-rehearsal.manifest P4_D73_EVIDENCE=/tmp/.../evidence P4_D73_REQUEST_ID=own-rehearsal-corrected /bin/bash --noprofile --norc -c 'set -eu; test "$(git -C /home/user/work/agent remote get-url origin)" = https://github.com/peteromallet/astrid-agent; test "$(git -C /home/user/work/runtime remote get-url origin)" = https://github.com/banodoco/banodoco-workspace-runtime; test "$(git -C /home/user/work/app remote get-url origin)" = https://github.com/banodoco/reigh-app; test "$(git -C /home/user/work/composition remote get-url origin)" = https://github.com/peteromallet/timeline-composition; exec /home/user/work/agent/tools/p4-d73-pinned-launch.sh "$P4_D73_MANIFEST" run -- -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$P4_D73_EVIDENCE/OWN-REHEARSAL-SUITE.xml" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py'
```

Substitute `/home/user/work/agent`, `/runtime`, `/app`, and `/composition` with
`AGENT_CHECKOUT`, `RUNTIME_CHECKOUT`, `APP_CHECKOUT`, and `COMPOSITION_CHECKOUT`
from MAIN's normal request-checkout. Substitute the old manifest/evidence/request
id with MAIN's existing `P4_D73_MANIFEST`, `P4_D73_EVIDENCE`, and
`agent-core-full`; substitute the launcher with
`$AGENT_CHECKOUT/tools/p4-d73-pinned-launch.sh`. Do not create a launcher,
credential, scope, profile, checkout, install, or registry writer.

The four source receipts are the D73 Agent/Runtime/App/Composition
SHA/tree/path tuple. The old qualified Runtime receipt is the immutable
`1daca` tuple above; MAIN captures App and Composition once through the same
route. The old Agent source receipt was
`b27ff3449ec4d9b5e14ac25b8f5a18c1999c21f6` / tree
`972188c76ed7a9e8f41d1baf6768673de2596efc`, replaced for this run by the
released `070dfc` source.

## Baselines and result accounting

The prior pre-fix collection was exactly `9268` tests, 409 source files, exit 0,
with inventory aggregate SHA256
`7ac5cdd0bfa2b811f9a0a4fb719d9a28ef6080d2bb879ed29fe54fc1a6882b69`. This is
only a baseline. MAIN determines the final count and result; no current count
is guessed or prefiltered.

The upstream 924 baseline is:

```text
path=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D60-snapshot-return-1342/evidence/upstream-full-9244377.xml
sha256=2941565205663912985f766210bfead7db42264976fabee7dc899d03d4f4657f
counts=12396 passed, 91 failed, 14 errors, 16 skipped, 566 subtests; root total 13083
```

## Preflight, central row, and ownership

The existing parsed preflight form is required once by MAIN:

```text
positive-once(body17): parse the published row, submit exactly once, require nonzero control exit 17 and body_count=1
poison-zero: parse the poison input through the same existing entrypoint, require nonzero exit (2) and body_count=0
```

These are central registry proofs, not a new local helper or gate. MAIN alone
installs the parsed central registry row, proves CAS plus positive-once and
poison-zero, and submits the full body. The Agent worker writes no body and does
not perform collection. The published command is distinct from the actual
parsed row: this document publishes the source recipe, while MAIN's existing
registry machinery parses, installs, and proves the row it actually used.

## Production Timeline commit contract reminder

The production caller remains the registered `commitTimeline/provider` seam:
Timeline commit/session, RuntimeCommitService provider, remote
`commit_timeline`, and NativeSheet use the same existing seam. The v2 request is:

```text
api_version=1, project_id, timeline_id, exact base_revision_id/base_publication_id,
commands[{schema_version,op,version,select,args}], label,
steps[{id,label,intent,tags,command_ordinals,patch,optionalreads}],
merge=fields|atomic, optionalreads, Idempotency-Key, dry_run, source, rationale, group_id
```

Replies are `accepted|merged` with canonical document/base+landing,
`merge_mode`, receipt, records, bindings, effects, dependencies, steps, history,
and undo_steps; conflicts return reason/head; invalid requests return
code/path/hint/suggestedcommand; preview returns `would_status` and null receipt.
Historical rebased retries remain exact.
