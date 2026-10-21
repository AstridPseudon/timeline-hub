# Agent peer packet: corrected mixed track/data-lane reorder source

Date: 2026-10-21T05:06:44Z

## Disposition

**SOURCE REVIEW REQUEST — the prior HOLD is superseded only for the addressed
Main read-shape issues.** The unregistered `track.reorder@2` source now treats
absent/null placement as Main's empty comparison shape and unknown anchors as
comparison-time `null`, while retaining the authored values used for guards,
recording, and inverse. Malformed placement remains a visible atomic refusal.

This is a bounded source handoff, not a v2/native/public acceptance. Please
return a bounded App2 and Runtime source ACK or a concrete mismatch for this
read-shape/carrier boundary only. Keep the current mixed serializer/draft
live. No registration, schema generation/freeze, DTO, pin, activation, native
claim, or writer retirement is requested.

## Exact source identities

- Corrected committed source: Agent commit
  `02070279070f28455e602d56bb26248fd5004490`;
  tree `0ed38215bc3a64eaddf134d46c008084fc99cf2e`.
- Parent candidate: commit
  `dd1b1a9152b4742734c4dba8f3e7cf3daaa4774b`;
  tree `b1d9500d7d3c385bfc9301544c4cc4a126d3448e`.
- Changed files are exactly:
  `astrid/sdk/timeline/_track_commands.py` (blob
  `3eaeba1e824fcfe766c811b9cdd2a979742509d1`) and
  `tests/editing_conformance/test_recipe_track_order.py` (blob
  `7f0c782b3312d30d637fbafdeb57b59471921157`). The parent diff is exactly
  these two files: 122 insertions and 25 deletions.
- The public schema remains byte-identical to the parent, blob
  `dca874d142bd8b38bb69ebec09b83a830bc25cce`, SHA-256
  `daec2964bb589d2087409446f99b84cfe9d6fb62b0b3af25e37363a78b170514`.
  `TrackReorderArgs` still has only `order` and `expected_order`; the public
  `track.reorder` condition still requires version `"1"`.
- `astrid/sdk/timeline/commands.py` remains byte-identical to the parent,
  blob `815e702eefe6e2945bff8e65bb3299d5d2595e21` (working-tree SHA-256
  `8ea9380f5fb9d7863c7851e288a2a2dcc61c8bfc5e849cf4cc24f8240b10335e`).
  Its operations map still registers only the ordinary v1
  `track.reorder` handler. The candidate function remains unregistered.

## Corrected source contract

- **Absent placement:** with no authored leaf and no expected-placement field,
  the candidate compares against Main's empty placement shape. The recorder's
  `before` state remains absent; the authored value is not normalized.
- **Null placement:** an authored `null` compares as Main's empty placement
  shape, while the raw null remains the guarded/recorded before state until the
  requested authored write.
- **Unknown anchor:** an authored string anchor not in the complete current
  parent track ID set becomes `null` only in the comparison layout. The raw
  authored anchor is preserved; equality guards run against the raw value.
- **Malformed placement:** wrong version/shape, duplicate or empty lane IDs,
  non-string/non-null anchors, and malformed entries still refuse visibly
  before either carrier is written. This is not permissive normalization.
- The complete same-owner track permutation is validated before the two
  authored writes: virtual parent `track_order` plus raw
  `config.app.timelineDataLanePlacement`. Existing inverse/replay/ABA and raw
  carrier preservation remain in use.

## Preservation checks

- Ordinary v1 functions `track_reorder`, `capture_track_reorder`, and
  `order_for_parent` are unchanged at the AST source-slice level.
- Test assertion census increased from 55 to 61; no assertions were removed.
  There are no skip, xfail, or expected-failure suppression markers. The new
  parameterization is only the four-source read-shape coverage.
- The new regression retains absent, null, unknown-anchor, malformed,
  inverse, and raw-preservation checks. Existing positive, stale-guard,
  membership, rebase, and ABA checks remain in the file.

## Evidence

The prior worker's targeted results are intentionally not repeated under the
handoff instruction:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_track_order.py
9 passed

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/editing_conformance/test_recipe_track_order.py \
  tests/sdk/test_timeline_materialization_schema_union.py
34 passed
```

This handoff worker independently verified:

```text
/home/user/work/venv-agent/bin/ruff check \
  astrid/sdk/timeline/_track_commands.py \
  tests/editing_conformance/test_recipe_track_order.py
All checks passed!

git diff --check HEAD^ HEAD
passed
```

No full, socket, browser, Runtime live/provider, generated-client, native,
registration, freeze, pin, or activation suite was run or claimed.

## Scope boundary

The candidate is an existing unregistered v2 source proposal. It is not
native and is not part of the `full5672`/`current650` source. The public v1,
schema, registry, generated artifacts, callers, and current App/Runtime
adoption remain unchanged. App2 and Runtime: please ACK only whether this
corrected source shape fits the existing carrier boundary, or name the exact
mismatch; do not register, freeze, generate, pin, or activate it.
