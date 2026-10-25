# D140 Farm commands

These are manager commands, not execution evidence. They are run by the Farm
owner only after `receive-farm.sh --check-only` returns `READY` and every
receipt binding is re-read under its normal receiving route. If any gate is
missing, stop with `NOT_READY` and its owner.

## 1. Normal child request — exactly once

The schema pair is the D139a authenticated installed distribution plus its
trusted manifest. Do not use `--farm-schema-source`, a package index, a mirror,
or a legacy retained child.

```sh
"$NORMAL_REQUEST_ROUTE" venv-agent-child-d140 "$AGENT_SHA" \
  --source-carrier "$AGENT_CHECKOUT" "$RUNTIME_CHECKOUT" "$RUNTIME_SHA" \
  --dependency-wheelhouse "$DEPENDENCY_SEED" \
  --schema-installed-distribution "$SCHEMA_INSTALLED_DISTRIBUTION" \
  --schema-source-manifest "$SCHEMA_SOURCE_MANIFEST"
```

The normal route must return the registered child receipt. Bind its actual
`bin/python` as `CHILD_PYTHON`; it must be the maker-selected interpreter and
must not be replaced by Main's interpreter.

## 2. Registered child import census

Run the existing checker inside the registered child, with the authenticated
canonical census. Its 1,146-row `4c/ab1e` packet is supporting evidence only;
the result must report unconditional-required failures separately from the
12 diagnostic missing rows and the five optional/plugin misses. It must not
be relabelled as a current `41ad/f103` census without a named new receipt.

```sh
"$IMPORT_CHECK_ROUTE" \
  --child "$CHILD_PYTHON" \
  --launcher "$D73_LAUNCHER" \
  --root "$AGENT_CHECKOUT/astrid" \
  --root "$AGENT_CHECKOUT/astrid_runtime_client" \
  --root "$RUNTIME_CHECKOUT/runtime_protocol" \
  --root "$RUNTIME_CHECKOUT/packages/python/astrid_runtime_client" \
  --census-file "$CANONICAL_CENSUS" \
  --output "$RAW_ROOT/d140-child-imports.json"
```

## 3. D73 dry controls — positive then poison

Use fresh counter paths supplied in the census. The positive parsed-row stub
must exit `17` after exactly one call. The poison manifest changes only
`agent_sha` to forty zeroes; it must fail nonzero before the stub and leave its
counter at zero. These are pre-body controls, not a body result.

```sh
set +e
P4_STUB_COUNT="$POSITIVE_COUNTER" P4_D73_MANIFEST="$P4_D73_MANIFEST" \
  P4_D73_EVIDENCE="$P4_D73_EVIDENCE" P4_D73_REQUEST_ID=d140-positive \
  "$D73_LAUNCHER" "$P4_D73_MANIFEST" dry -- "$POSITIVE_CONTROL"
positive_rc=$?
set -e
test "$positive_rc" = 17
test "$(wc -l < "$POSITIVE_COUNTER")" = 1

set +e
P4_STUB_COUNT="$POISON_COUNTER" P4_D73_MANIFEST="$POISON_MANIFEST" \
  P4_D73_EVIDENCE="$P4_D73_EVIDENCE" P4_D73_REQUEST_ID=d140-poison \
  "$D73_LAUNCHER" "$P4_D73_MANIFEST" dry -- "$POISON_CONTROL"
poison_rc=$?
set -e
test "$poison_rc" -ne 0
test "$(wc -l < "$POISON_COUNTER")" = 0
```

`POISON_MANIFEST` is an actual manager-rendered copy of the authenticated D73
manifest with only `agent_sha=0000000000000000000000000000000000000000`.
Do not hand-edit a production manifest or silently recapture a changed head.

## 4. One unfiltered Agent core body

Only after the registered child, import census, positive and poison controls,
disk admission, profile, manifest and service gates pass, invoke the existing
launcher once. Preserve JUnit, raw runner output, start/stop/disk evidence and
the `KEEP` directory before harness cleanup. Do not count membership in an
unrelated historical suite and do not invent a PASS total.

```sh
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH="$(dirname "$NODE_BIN"):/usr/local/bin:/usr/bin:/bin" \
  VIRTUAL_ENV="$(dirname "$(dirname "$P4_PYTHON")")" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" \
  ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full /bin/bash --noprofile --norc -c \
  'exec "$0/tools/p4-d73-pinned-launch.sh" "$1" run -- -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$2/agent-core-full.xml" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$P4_D73_EVIDENCE"
```

The selector above is exactly 22 roots and has no marker, `-k`, row filter or
other prefilter. The production caller continues to use the normal receiving
route and the existing C0 request/reply fields; this packet adds no product
caller, provider, schema, client, pin, Store, queue or registry behavior.
