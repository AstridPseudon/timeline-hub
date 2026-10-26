# D141 frozen ordinary Farm handoff

Status: `PASS_SOURCE / NOT_READY_ON_THIS_VENUE`.

The production receiver is source-bound to Agent
`28e56cacb42d3da85b02e5b3543895b44f3d0f70`/tree
`2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`, Runtime
`6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`/tree
`ac5b862744bece65b2e30565db1777bacd60da28`, App
`867cb2737af1b46dc608c7cd37c349e920fe9422`/tree
`2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`, and Composition
`635f4de06fda22a85fc2e4cfc764d0153a4c9f40`/tree
`5ab5191a296980a0a6bcd1178ab6902d6478a148`.

Command-file identity: `ops-d140-farm/commands.md`, SHA-256
`f6804f6b4ad52b0108169e8b125b238307f82764ad835e95404da214286fd7f3`, 12,309
bytes, mode 0644. Its normal route is the D139a installed-schema route; it
uses the existing `p4-d73-pinned-launch.sh` only after all pre-body gates.

The expected received kit is `ops-child-custody/make-child-venv`, SHA-256
`fd83c9e2017f75fb0d76a2d633d4a63aed090df37c4d7417b03152e7a4fc22b5`, 111171
bytes, mode 0755. The actual Farm received-maker path and installation receipt
are UNBOUND. This hash is not a fabricated receipt.

## Ready-to-send sequence

Bind every exact Farm-owned path and authenticated receipt first, then send the
following complete sequence from `commands.md`:

1. Run `D140_PHASE=pre-child ops-d140-farm/receive-farm.sh --check-only`.
   It must list every missing row and return `NOT_READY`/exit 1 until all
   genuine inputs exist. Do not proceed on a partial result.
2. Send exactly one normal request:

   ```sh
   "$NORMAL_REQUEST_ROUTE" venv-agent-child-d140 "$AGENT_SHA" \
     --source-carrier "$AGENT_CHECKOUT" "$RUNTIME_CHECKOUT" "$RUNTIME_SHA" \
     --dependency-wheelhouse "$DEPENDENCY_SEED" \
     --schema-installed-distribution "$SCHEMA_INSTALLED_DISTRIBUTION" \
     --schema-source-manifest "$SCHEMA_SOURCE_MANIFEST"
   ```

   Bind the actual returned child Python/bootstrap, manager manifest, and
   request-scoped output roots. No package index, mirror, old child, alternate
   schema, or `--farm-schema-source` substitution is allowed.
3. Run `D140_PHASE=post-child ... --check-only`; stop unless `READY`.
4. Run the existing child import checker with the authenticated historical
   `4c/ab1e` census as supporting input only and the four existing roots from
   `commands.md`. A fresh result must list all unconditional-required misses,
   diagnostics, and optional/plugin misses. Nonzero stops the sequence; it is
   not relabelled as a current D141 census without a new receipt. No App
   execution is required for Agent core.
5. Run fresh D134 positive and poison controls. Positive must exit 17 with
   exactly one counter line; poison must be the positive manifest with only
   `agent_sha` replaced by forty zeroes, fail nonzero before the stub, and leave
   zero counter lines. Neither result exists yet.
6. Only after those gates pass, invoke the existing D124 core route once with
   the exact 22 unfiltered roots in `commands.md` (no `-k`, marker, collect-only
   or other filter). Retain durable XML/JUnit, raw runner output, actual runner
   exit, request manifest/runmanifest, start/stop witness, disk witness, and
   KEEP root before cleanup; then run the post-launch check-only census.

For a ready venue, the remaining command blocks are exactly these (with all
bindings supplied by the Farm owner):

```sh
test -f "$POSITIVE_COUNTER" && test ! -s "$POSITIVE_COUNTER"
test -f "$POISON_COUNTER" && test ! -s "$POISON_COUNTER"
set +e
"$IMPORT_CHECK_ROUTE" \
  --child "$CHILD_PYTHON" \
  --launcher "$D73_LAUNCHER" \
  --root "$AGENT_CHECKOUT/astrid" \
  --root "$AGENT_CHECKOUT/astrid_runtime_client" \
  --root "$RUNTIME_CHECKOUT/runtime_protocol" \
  --root "$RUNTIME_CHECKOUT/packages/python/astrid_runtime_client" \
  --census-file "$CANONICAL_CENSUS" \
  --output "$RAW_ROOT/d140-child-imports.json"
imports_rc=$?
set -e
if [ "$imports_rc" -ne 0 ]; then
  "$P4_PYTHON" - "$RAW_ROOT/d140-child-imports.json" <<'PY'
import json
import sys
report = json.load(open(sys.argv[1], encoding="utf-8"))
print("IMPORT_NOT_READY mandatory=%d diagnostic=%d" % (
    len(report.get("missing_installed_distributions", [])),
    len(report.get("missing_census_modules", []))), file=sys.stderr)
PY
  printf '%s\n' "IMPORT_NOT_READY: checker rc=$imports_rc; exact owner must resolve classified misses" >&2
  exit "$imports_rc"
fi
test "$(python3 - "$RAW_ROOT/d140-child-imports.json" <<'PY'
import json
import sys
print(json.load(open(sys.argv[1], encoding="utf-8")).get("status", ""))
PY
)" = passed

set +e
P4_STUB_COUNT="$POSITIVE_COUNTER" P4_D73_MANIFEST="$P4_D73_MANIFEST" \
  P4_D73_EVIDENCE="$P4_D73_EVIDENCE" P4_D73_REQUEST_ID=d140-positive \
  "$D73_DRY_ROUTE" "$P4_D73_MANIFEST" dry -- "$POSITIVE_CONTROL"
positive_rc=$?
set -e
test "$positive_rc" = 17
test "$(wc -l < "$POSITIVE_COUNTER")" = 1

set +e
P4_STUB_COUNT="$POISON_COUNTER" P4_D73_MANIFEST="$POISON_MANIFEST" \
  P4_D73_EVIDENCE="$P4_D73_EVIDENCE" P4_D73_REQUEST_ID=d140-poison \
  "$D73_DRY_ROUTE" "$POISON_MANIFEST" dry -- "$POISON_CONTROL"
poison_rc=$?
set -e
test "$poison_rc" -ne 0
test "$(wc -l < "$POISON_COUNTER")" = 0

start_stop="$STARTSTOP_ROOT/$P4_D73_REQUEST_ID.start-stop.txt"
raw_log="$RAW_ROOT/$P4_D73_REQUEST_ID.launcher.log"
junit="$JUNIT_ROOT/$P4_D73_REQUEST_ID.xml"
printf 'start=%s\n' "$(date --iso-8601=seconds)" > "$start_stop"
df -P "$OUTPUT_ROOT" > "$DISK_ADMISSION"
set +e
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH="$(dirname "$NODE_BIN"):/usr/local/bin:/usr/bin:/bin" \
  VIRTUAL_ENV="$(dirname "$(dirname "$P4_PYTHON")")" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" \
  ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$KEEP_ROOT" \
  P4_D73_REQUEST_ID="$P4_D73_REQUEST_ID" CORE_ROUTE="$CORE_ROUTE" /bin/bash --noprofile --norc -c \
  'exec "$CORE_ROUTE" "$1" run -- -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml="$2" tests/editing_conformance tests/sdk tests/timeline tests/core/timeline tests/core/test_timeline_element_orphan_cleanup.py tests/core/test_timeline_element_publication.py tests/core/test_timeline_element_publication_runtime.py tests/core/rendering/test_timeline_visualize_cli_grammar.py tests/core/rendering/test_local_schema.py tests/packs/timeline tests/packs/rendering/test_composition_package.py tests/packs/rendering/test_live_scene_composition.py tests/packs/rendering/test_render_export_task_adapter.py tests/packs/rendering/test_timeline_filmstrip_cards.py tests/packs/rendering/test_timeline_filmstrip_execution.py tests/packs/video_editing/test_runtime_publication_chain.py tests/stage1/test_cold_launch_autobootstrap.py tests/test_installer_schema.py tests/test_installer_sources.py tests/test_installer_bootstrap_schema.py tests/test_timeline_clip_replacement.py tests/v10/test_timelines_create.py' \
  core-route "$P4_D73_MANIFEST" "$junit" > "$raw_log" 2>&1
core_rc=$?
set -e
printf 'stop=%s\nrc=%s\n' "$(date --iso-8601=seconds)" "$core_rc" >> "$start_stop"
df -P "$OUTPUT_ROOT" >> "$DISK_ADMISSION"
test -s "$raw_log" && test -s "$junit" && test -s "$start_stop" && test -s "$DISK_ADMISSION"
test -f "$KEEP_ROOT/$P4_D73_REQUEST_ID.manifest"
test -f "$KEEP_ROOT/$P4_D73_REQUEST_ID.runmanifest"
test -d "$RETAINED_ROOT"
test "$core_rc" = 0
D140_PHASE=post-launch FARM_D73_RECEIPT="$KEEP_ROOT/$P4_D73_REQUEST_ID.manifest" \
  FARM_D73_RECEIPT_SHA256="$P4_D73_MANIFEST_SHA256" \
  ops-d140-farm/receive-farm.sh --check-only
```

## Honest unbound venue inputs

The following remain Farm-owned UNBOUND inputs: Farm `FARM_ORCH_ROOT` and
normal producer custody; received maker and normal requester/import-checker
paths; installed `banodoco-timeline-schema==0.0.2` dist-info, exact 18-row
RECORD (12 hashed plus six named unhashed rows), PEP 610 direct URL and trusted
manifest; schema carrier/installation summary; authenticated normal source
checkout receipts (Agent/Composition local receipts exist but are not Farm
execution evidence; Runtime/App receipt files are absent); normal child,
registration, provision report, child receipt, child Python/bootstrap and
source/client/schema markers; a fresh current-tuple import census; central
service and suite; D73 launcher/manifest/input receipt, Node v20.19.4, profile,
normal request/import/dry/core routes; dependency seed; disk admission,
retained root, output/JUnit/raw/start-stop/KEEP roots; fresh D134 controls and
counters; and D124 post-launch XML, raw runner log, actual runner exit,
start/stop and disk witnesses, request/run manifests, and durable KEEP.

Import, D134 positive/poison, and D124 core have not run. Main Runtime full and
pristine are not Farm jobs. After the sole Farm cut core, the conditional
pristine-five rule is: rerun pristine Agent
`8b6ed2116fd1803d24b2be5bc08bd9490407fe4a` and pristine Runtime
`fa9cd5464a8b37b02f971de375e56be846cd69e2` only for IDs in Main's five-node
list that also fail Farm cut core, in the same Farm child-environment kind,
before REG classification. It is not a blanket five-node run or a new gate.

