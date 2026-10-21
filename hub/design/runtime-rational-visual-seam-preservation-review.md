# Runtime rational-FPS visual-seam preservation review

Date: 2026-10-21 UTC  
Verdict: **APPROVE** (candidate only; no merge, pin, release, or public adoption)

## Reviewed identities

- Immutable Main014 reference: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`,
  tree `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Producer branch: `tl/rt-m2-rational-visual-seam-normal-path-classify`,
  commit `60a919a22f42f0b5b0a246ce84cb43e9f46c2106`, tree
  `4fc4c0fdbe1a2d78061a4b83d480d758a6a69d13`, parent exactly `95bd...`.
- The qualified `95bd` pin target and its artifacts were not modified.

## Decision

APPROVE the bounded source as a post-014 follow-up. The producer fixed a real
normal managed-render admission refusal: authored `config.output.fps` can be a
raw JSON rational mapping or two-integer list, and the visual seam previously
sent either form through scalar-only `finite()`.

The exact product diff is three files:

- `runtime_protocol/timeline_inspection.py`: the existing bounded `_fraction`
  helper accepts only the exact `{numerator, denominator}` mapping spelling in
  addition to its existing two-integer list/tuple spelling.
- `runtime_protocol/visual_seam.py`: `_fps()` uses `_fraction` only for local
  mapping/list seam-clock evaluation; scalar values still use the unchanged
  `finite()` path. The authored value is never rewritten.
- `tests/test_visual_seam_admission.py`: rational positive cases, authored-byte
  preservation, and invalid FPS refusals. Existing strict timing tests and
  admission/custody/immutability assertions are unchanged.

No protocol/schema/generated-client/DTO/store-writer/API files changed; no new
writer, scene dependency, endpoint, or persisted field was introduced. The
Runtime artifact manifest remains current, with all 76 Main014 artifacts
unchanged.

## Actual live caller and preservation checks

The live consumer is Runtime's existing
`RealmStore._freeze_managed_render_inputs()` path, reached from
`RealmStore.create_task()` for a managed `rendering.render` task. It loads the
persisted pinned parent/child closure and calls the existing
`admit_closure(..., materialize=True)` boundary. A live isolated control using
the producer tree admitted authored `[30000, 1001]`, produced the converted
seam report FPS, and preserved `[30000, 1001]` in the materialized snapshot.

Commit acceptance still validates and persists the canonical document without
calling the visual seam. The Agent provider's authored parent payload remains
the source of the persisted bytes. Existing publication code may record seam
diagnostics, but its own comment and control flow keep them advisory: findings
do not gate an otherwise valid save or render admission. The changed code adds
no renderer/scene import or save-path dependency.

The actual changed caller is therefore the local seam consumer in
`runtime_protocol/visual_seam.py`; `runtime_protocol/store.py`, the commit
store, provider, DTOs, and published contract remain unchanged.

## Guard evidence

The producer tests cover both accepted wire forms and reject `True`, zero,
negative, positive infinity, and zero-denominator mapping/list values. Source
inspection confirms the scalar path rejects strings and null, while `_fraction`
rejects malformed mappings/lists, booleans, null, negative values, and
zero-denominator pairs without clamping or accepting arbitrary coercions. One
additional isolated probe for the missing malformed mapping case also refused
with `ValidationError`.

Exact evidence:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP/tests:$TMP" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_visual_seam_admission.py::test_render_materialization_still_rejects_invalid_timing \
  tests/test_visual_seam_admission.py::test_render_materialization_accepts_raw_rational_fps \
  tests/test_visual_seam_admission.py::test_render_materialization_rejects_invalid_fps \
  tests/test_direct_render_admission.py::test_direct_managed_render_admission_freezes_snapshot_before_claim \
  tests/test_timeline_native_inspection.py::test_generic_fraction_still_rejects_null
14 passed in 0.87s

python scripts/artifact_manifest.py --check
contract/artifacts.json is current

git diff --check 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c \
  60a919a22f42f0b5b0a246ce84cb43e9f46c2106
passed
```

The live managed-render control and malformed-mapping probe both passed on an
isolated archive of `60a919a...`. No full suite, browser, pixel/audio render,
or live-socket suite was run. The live control proves Runtime's managed
admission boundary and snapshot custody, not Agent-over-HTTP integration or
renderer output parity.

## Delivery boundary

Stage `60a919a...` as a post-014 Runtime follow-up only after the orchestrator
chooses adoption. Keep the qualified `95bd` source/tree and all Main014
artifact identities immutable; this review is not a semantic freeze or public
consumer pin.
