# D124 next Farm input: unfiltered agent-core-full command

Source-only derivative of the qualified 1336 packet.

This packet binds the actual merged Agent and released Runtime sources for the
next batch; it does not claim a Farm checkout, child environment, profile, D73
manifest, receipt, counter, or execution result.

The prior Farm `0b586e4b/42aad0e9` core and `9ea67534/369ffa7c` host14 inputs
remain immutable and are not retargeted. This packet is the next batch only.
The child maker's refusal of unowned local distribution metadata is preserved:
there is no retry, substitution, overlay, or bypass here.

## Actual source tuple

| role | caller-bound source | commit | tree | parents |
| --- | --- | --- | --- | --- |
| Agent | `AGENT_CHECKOUT` | `a4e016b6a9f91fbe372672bdcf382c630bf59186` | `60d45288145414ee4702fcce61af7c7810c2a3df` | `61fefc6983f4413f1d1964b149bbaf5eadb8d2f0 96df3f5b4862b1c267e3816237bae8a64b5dc31f` |
| Runtime | `RUNTIME_CHECKOUT` | `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344` | `de2954a0ceadb4455903d9abdfec3b773318a50f` | `7070f1378d1917fcce69857ebd33cd2b3015568b ef4728a1c07b7d3909d5027fbf1e673f6aec0030` |
| App | `APP_CHECKOUT` | `d8a1cd40b866c49c0ab415682391f0ec87a7a8e7` | `dd2afd6c5c7a1ac73feaac4390cc64d7f31fe7b9` | `34d4644589970274a5252c0f7c68b6288eb0b0b4` |
| Composition | `COMPOSITION_CHECKOUT` | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `7a95a40b07ea0d273e17afb69dbc3456b603f2bc` |

The Agent merge contains the reviewed union commit
`16bbd56dbf016bcddeafa891291129efcfa87196` (tree
`70fcd38844e7d93cdf97e4aebaf248d3736a312a`) and the independently reviewed
host fallback `96df3f5b4862b1c267e3816237bae8a64b5dc31f`. The Agent
`runtime.lock.json` names Runtime `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.

## Preserved canonical identities

These identities are unchanged from the qualified 1336 packet except for the
intended Runtime lock provenance and the current Agent source tuple:

- canonical-15 source identity: `6e8ae0142655eb7a6d10083d2d3ae5d434b5c94e`;
- schema digest: `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`;
- canonical schema digest: `3654ca3c68f5b3d2022ee91f532aa388b198033d6ae54cda8d8b25cecf739815`;
- Runtime bundle digest: `e4da5c0edc728869a7e78b5820b36f0a0756e1891af64a4f8c0fc37d705196e1`;
- Remotion tree: `b01dca9b3b24f54093c20b7c5657316f997725db`;
- schema source `astrid/core/timeline/banodoco_schema.py` blob:
  `1b3f12da05da3bb89fa76881184eefdf8232e076`;
- existing launcher `tools/p4-d73-pinned-launch.sh` blob:
  `2844cec15b97fa995ecaf120961fc891b8e13b1c`, SHA-256
  `cec561761cb90adbe94dbcc1b1f6b62afb107f1a90e079c6ce2b823405a072d1`;
- existing D73 maker `tests/suites.conf.candidate.request.md` blob:
  `fbde96168dca681a76cff1526c23b8d0b74001eb`, SHA-256
  `782fb81cea67ce71b785dd5dbf891bb1d32df74c136425d83d53e938bdf8b51c`.

The launcher and maker are reused unchanged. No generated, schema, client,
registry, pin, or launcher source is added by this packet.

## Exact unfiltered core selector

The existing metadata inventory is 23 entries; the selector argv has exactly
22 roots. The live-scene composition root and integration roots remain in the
argv. There is no marker, `-k`, row filter, default filter, or other prefilter.
The command below is source-reviewable only; the production caller supplies
all bindings and invokes the existing registered launcher unchanged.

~~~sh
set -eu
: "${AGENT_CHECKOUT:?caller must bind the actual merged Agent checkout}"
: "${RUNTIME_CHECKOUT:?caller must bind the released Runtime checkout}"
: "${APP_CHECKOUT:?caller must bind the captured App checkout}"
: "${COMPOSITION_CHECKOUT:?caller must bind the captured Composition checkout}"
: "${P4_D73_MANIFEST:?caller must bind the D73 manifest made by the existing maker}"
: "${P4_D73_EVIDENCE:?caller must bind Farm-owned evidence}"
: "${P4_PYTHON:?caller must bind the manifest-selected Python}"
: "${P4_NODE:?caller must bind the manifest-selected Node}"

test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD)" = a4e016b6a9f91fbe372672bdcf382c630bf59186
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD^{tree})" = 60d45288145414ee4702fcce61af7c7810c2a3df
test "$(git -C "$AGENT_CHECKOUT" rev-list --parents -n 1 HEAD)" = 'a4e016b6a9f91fbe372672bdcf382c630bf59186 61fefc6983f4413f1d1964b149bbaf5eadb8d2f0 96df3f5b4862b1c267e3816237bae8a64b5dc31f'
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD)" = 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344
test "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD^{tree})" = de2954a0ceadb4455903d9abdfec3b773318a50f
test "$(git -C "$RUNTIME_CHECKOUT" rev-list --parents -n 1 HEAD)" = '5e9ad1c6f74241d8771d3284fdd2ce7a214fd344 7070f1378d1917fcce69857ebd33cd2b3015568b ef4728a1c07b7d3909d5027fbf1e673f6aec0030'
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
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD:tests/suites.conf.candidate.request.md)" = fbde96168dca681a76cff1526c23b8d0b74001eb
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD:astrid/core/timeline/banodoco_schema.py)" = 1b3f12da05da3bb89fa76881184eefdf8232e076
test "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD:runtime.lock.json)" = e4f7e2db58ce73bbe69c1ae07566ba56b360bf47
test "$(awk -F= '$1 == "agent_sha" {print $2}' "$P4_D73_MANIFEST")" = a4e016b6a9f91fbe372672bdcf382c630bf59186
test "$(awk -F= '$1 == "runtime_sha" {print $2}' "$P4_D73_MANIFEST")" = 5e9ad1c6f74241d8771d3284fdd2ce7a214fd344
test "$(awk -F= '$1 == "app_sha" {print $2}' "$P4_D73_MANIFEST")" = d8a1cd40b866c49c0ab415682391f0ec87a7a8e7
test "$(awk -F= '$1 == "composition_sha" {print $2}' "$P4_D73_MANIFEST")" = 635f4de06fda22a85fc2e4cfc764d0153a4c9f40

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

## Existing production contract seam

The registered `agent-core-full` caller remains unchanged. It sends the full C0
request: `api_version`, `project_id`, `timeline_id`, `base_revision_id`,
`base_publication_id`, `commands[{schema_version,op,version,select,args}]`,
`label`, `steps[{id,label,intent,tags,command_ordinals,patch,optional reads}]`,
`merge` (`fields` or `atomic`), `reads`, `Idempotency-Key`, `dry_run`, `source`,
`rationale`, and `group_id`.

Accepted or merged replies retain `canonical`, `base`, `landing`, `receipt`,
`records`, `bindings`, `effects`, `dependencies`, `history`, and `undo_steps`.
Conflicts retain `reason` and `head`; invalid requests retain `code`, `path`,
`hint`, and `suggested_command`; previews retain `would_status` and a null
`receipt`. Existing authentication, privacy, and no-write semantics remain
unchanged. This packet introduces no source or caller change.
