# D140 Farm commands

These are manager commands, not execution evidence. Run the receiver in two
input phases: `D140_PHASE=pre-child receive-farm.sh --check-only` admits only
preexisting inputs; after the normal child request, run
`D140_PHASE=post-child receive-farm.sh --check-only` with the produced child,
manager manifest, controls, and output roots. After the launcher, use
`D140_PHASE=post-launch` to check request-scoped retained results. A missing gate is finite
`NOT_READY`; do not continue or substitute another route.

The ordinary D139a installed-schema request is the default Farm route and does
not require the historical Farm distribution source or receipt. If the existing
`FARM_REQUIRED=1` selector is used for the special Farm profile, the receiver
requires its full distribution and retained-authority closure. The requester
and maker still refuse an installed-schema request combined with Farm flags;
keep that guard and do not substitute the D139a carrier.

The receiver never starts a body. The post-child census authenticates the
registered child, tuple receipts, key/value D73 input manifest, exact poison
comparison, and durable output roots before the sequence below.
The existing `p4-d73-pinned-launch.sh` route is the only launcher named here.

## 0. Pre-child census

```sh
D140_PHASE=pre-child ops-d140-farm/receive-farm.sh --check-only
```

The pre-child census must not require `CHILD_PYTHON`, `CHILD_BOOTSTRAP`, a new
D73 manifest/evidence directory, fresh controls, or post-child output roots.

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
`bin/python` as `CHILD_PYTHON` and its maker-selected bootstrap as
`CHILD_BOOTSTRAP`; neither may be replaced by Main's interpreter or a copied
venv. Then render the manager input manifest, bind its consistency digest and run
the post-child census. Stop unless it is `READY`. This phase requires no
launcher-created retained manifest, request-id, runmanifest or exit files.

```sh
D140_PHASE=post-child ops-d140-farm/receive-farm.sh --check-only
```

## 2. Registered child import census — mandatory stop gate

Run the existing checker inside the registered child, with the authenticated
canonical census. Its historical 1,146-row `4c/ab1e` packet is supporting evidence only;
the result must report unconditional-required failures separately from the
12 diagnostic missing rows and the five optional/plugin misses. It must not
be relabelled as a current D141 `28e56/6a011` census without a named new receipt.

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
```

The checker’s nonzero exit is never ignored. Mandatory and diagnostic misses
remain separately reported, but either leaves the sequence on a finite hold;
no control or core call follows a checker failure.

## C0 wire names retained by the receiving handoff

The frozen Runtime `6a011d58` `contract/schemas/timeline-commit.json` request is the
actual ABI: `api_version`, `project_id`, `timeline_id`,
`base_revision_id`, `base_publication_id`, `commands`, optional `label`,
`steps`, `merge`, `reads`, `dry_run`, `source`, `rationale`, and `group_id`.
Each requested step uses `id`, `label`, `intent`, `tags`,
`command_ordinals`, `patch`, and optional `reads`; accepted steps may also
contain `dependencies`. The request is carried by the existing normal route
with its `Idempotency-Key` header; this packet does not rename or synthesize
that contract.

The accepted result uses `status` (`accepted`, `rebased`, or `merged` in the
C0 acceptance shape), `base_revision_id`, `base_publication_id`,
`previous_revision_id`, `previous_publication_id`, `accepted_revision_id`,
`rebased_onto`, `canonical_document`, `document_digest`, `commands`,
`id_map`, `provider_version`, `compiler_version`, `merge_mode`, `steps`, and
`publisher` (plus optional `source`, `label`, `rationale`, `group_id`). The
mutation envelope is `{data: CommitAccepted, receipt: MutationReceipt}`;
history entries separately include `receipt` and nested `records`/`Recorder`.
Conflict/refusal
details use `base`, `current`, and `conflicts`; the current head is a
`HeadPin` with `revision_id` and `publication_id`. `canonical_document` is
not a synonym for a generic canonical/base/landing field, and history is a
separate `HistoryPage` shape.

`merge` is `fields` or `atomic`; omitted request `reads` with `doc.patch`
requires conservative atomic scope guards. Steps partition command ordinals
in execution order; submitted patches assert effects and accepted patches
contain the provider's complete effects and dependencies. The base remains
the revision/publication pair. Runtime owns authorization, idempotency,
CAS, rebase, attribution and guarded whole/per-step undo. Exact-key retries
return the original authenticated reply; historical `rebased` replies retain
their spelling, while new v2 disjoint-head acceptance uses `merged`.

The preview envelope is `{data: CommitPreview, receipt: null}`. Its data has
`status: preview`, `would_status: accepted|merged`, both base IDs,
`evaluated_head`, `canonical_document`, `document_digest`, `commands`, `id_map`,
`provider_version`, `compiler_version`, and optional `merge_mode`/`steps`.
Preview writes no history or publication. Failure uses `http_status`, `code`,
`message`, and `details`; details have `status: conflict|refused|invalid`,
`reason`, nullable `base`/`current`, and `conflicts`, with structured
`code`, `path`, `hint`, `suggested_command` where applicable. Each conflict
has `kind`, `ref`, `path`, `base`, `theirs`, `ours`, `choices`. These shapes
remain exactly C0 and the D141 schema bytes equal the historical f103 schema;
Farm receipt custody changes no wire field or authority rule.

## 3. D73 dry controls — positive then poison

Use fresh counter paths supplied in the census. The positive parsed-row stub
must exit `17` after exactly one call. The poison manifest changes only
`agent_sha` to forty zeroes; it must fail nonzero before the stub and leave its
counter at zero. These are pre-body controls, not a body result.

```sh
test "$P4_D73_EVIDENCE" = "$KEEP_ROOT"
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

D140_PHASE=post-launch P4_D73_REQUEST_ID=d140-positive \
  FARM_D73_RECEIPT="$P4_D73_EVIDENCE/d140-positive.manifest" \
  FARM_D73_RECEIPT_SHA256="$P4_D73_MANIFEST_SHA256" \
  ops-d140-farm/receive-farm.sh --check-only
```

`POISON_MANIFEST` is an actual manager-rendered copy of the authenticated D73
manifest with only `agent_sha=0000000000000000000000000000000000000000`.
Do not hand-edit a production manifest or silently recapture a changed head.

## 4. agent-core-full — one unfiltered Agent core body with durable evidence

Only after the registered child, import census, positive and poison controls,
disk admission, profile, manifest and service gates pass, invoke the existing
launcher once through the bound `CORE_ROUTE`. The existing launcher writes its
request-scoped manifest, request id, runmanifest and body/preflight logs under
`P4_D73_EVIDENCE`; bind that variable to `KEEP_ROOT`. The outer route captures
raw stdout/stderr in `RAW_ROOT`, pytest writes XML to the exact `JUNIT_ROOT`
path, and the route writes start/stop and `df` witnesses to `STARTSTOP_ROOT`
and `DISK_ADMISSION` before returning. Re-read `RETAINED_ROOT` before cleanup.
Declarations without these files are not evidence.

```sh
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
test -s "$raw_log"
test -s "$junit"
test -s "$start_stop"
test -s "$DISK_ADMISSION"
test -f "$KEEP_ROOT/$P4_D73_REQUEST_ID.manifest"
test -f "$KEEP_ROOT/$P4_D73_REQUEST_ID.runmanifest"
test -d "$RETAINED_ROOT"
test "$core_rc" = 0
D140_PHASE=post-launch FARM_D73_RECEIPT="$KEEP_ROOT/$P4_D73_REQUEST_ID.manifest" \
  FARM_D73_RECEIPT_SHA256="$P4_D73_MANIFEST_SHA256" \
  ops-d140-farm/receive-farm.sh --check-only
```

The selector above is exactly 22 roots and has no marker, `-k`, row filter or
other prefilter. The production caller continues to use the normal receiving
route and the existing C0 request/reply fields; this packet adds no product
caller, provider, schema, client, pin, Store, queue or registry behavior.
