# Agent pristine initialization — source handoff

Worker `agt-m2-pristine-initialize-native`, base `43d567f9d972386dc4cf585fbacc3ad9afc56bdd`.
Harness assigns final commit after exit. This is an Agent source candidate, not
a frozen generated release or App/bootstrap-writer retirement.

## Exact App meaning and capture

Verified actual App main `44f0b9ca9d0247d909f86f56955a04ef6c18a2aa`:
`src/tools/video-editor/lib/defaults.ts:4-44` and
`src/integrations/runtime/createDefaultTimeline.ts:50-82` agree with integration.
Initializer is `timeline.init`, version `1`, select `parent`, empty intent.
Closed args require name (string, including App's explicit empty string), slug
(nonempty string), and output (all five keys required):

```json
{"name":"Main","slug":"main","output":{"resolution":"1280x720","fps":30,"file":"output.mp4","background":null,"background_scale":null}}
```

This v1 covers App defaults only, not arbitrary output settings. Slug is the
existing App result, not guessed/normalized by Agent. Writes, in order, are
`parent.config.output`, `parent.name`, `parent.slug`, `parent.registry.assets`.
Every original write address is ABSENT. Last value is `{}`, creating the real
raw `parent.registry.assets` container inside the already-existing `{}` registry.
Never `config.registry`; never replace parent/config/registry roots.

Use the actual immutable empty accepted document:

```python
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.capture import capture_track_create
from astrid.sdk.timeline.native_initialize import capture_initialize

bundle = bundle_from_document(accepted_document)
calls = [capture_initialize(bundle, name=name, slug=slug, output=app_output)]
for row in full_app_tracks:  # V1, then A1; full defaults.ts rows, unchanged.
    local = execute(bundle, calls).bundle
    calls.append(capture_track_create(local, 'parent', row))
# Persist original base revision/publication pair, calls, exact request and key.
# Commit all three in one normal Runtime request.
```

Full track defaults remain `label`, `scale:1`, `fit:contain`, `opacity:1`,
`blendMode:normal`, plus id/kind. Theme/theme_overrides/generation_defaults stay
ABSENT. Captured selectors/reads/write expectations are ordinary recorder
claims, verified by the provider. Initializer uses `resolved: []` like parent
track.create: parent is not a ScopedId. No invented ref/schema widening.

## Pristine authority, inverse and retry

Provider uses existing authenticated `history_entry(base_publication_id)`, its
revision match, `intent == bootstrap`, `previous is None`, and exact
`head == {base_revision_id, base_publication_id}`. Repeat the pair check on every
CAS retry before replay. Handler additionally records/guards the complete raw
empty parent, empty clips/tracks/order, absent output/name/slug/assets, and
requires no placements or shots. Unknown/legacy/opaque content refuses unchanged.
There is no caller-authoritative pristine flag and no missing port seam.

Undo uses ordinary authenticated records; reversing the entire init+V1+A1 batch
restores the exact bootstrap document, including `{}` vs `{assets:{}}` and
null vs absence. Redo is inverse-of-inverse. Fresh initialization after any
accepted edit or undo is denied even if bytes/revision equal the original.
Direct deterministic capture/replay alone does not authorize publication.

Accepted exact retry stays Runtime-ledger-first. Real Runtime test restarts,
undoes init, then patches both engine execute and provider commit to raise:
retry returns the original accepted envelope and does not move the current head.
Changed payload under that key is refused. Provider race regression accepts
another track create→undo between precheck and CAS, then refuses initialization
on the equal-byte later publication.

## Golden and complete additive successor

`tests/editing_conformance/fixtures/pristine_initialize.json` contains actual
Main/default payload plus all three exact captures and recorder records.
Fixture raw SHA-256:
`214566e2a8ea7127ac5d27389ff4da5bedefd12b13155c89454b4719bda47b63`.

Schema is full frozen S2 `26ef2bbb` (48 definitions / 22 op conditions), with
only TimelineInitArgs and its condition added: **49 definitions / 23 conditions**.
No replacement by the old 43-definition base. Retains producer/consumed,
retained-element, numeric, inverse/restore definitions. Permanent test removes
precisely init additions and compares the full canonical S2 digest
`344be9aa869ec5d2ce24ba3f0fc7adf60ec185e00f6495801873d9a9f4c6c19b`.
New raw schema SHA-256:
`e29c4542a79e5c2098251ac3ff80a47883d08878b79592aa920f1e3321274159`.
Manager must freeze this complete additive successor before normal generation.
Pins/ABI/HTTP/table/journal/coordinator unchanged. Base lacks producer.guard's
handler; only its existing S2 schema is retained here, not its other worker's code.

## Results and remaining repair pair

Final focused tests: 32 passed / 2.95s (init conformance, provider and composed
schema); real Runtime in-process test: 1 passed / 2.54s, archived pinned Runtime
`94114269d1ce23ab3224d7eca5a85138ce2b5fed`; earlier neighbor selections:
156 passed / 14.78s and 305 passed / 41.01s. Changed Python Ruff and diff checks
pass. Exact commands and limitations: worker `notes/report.md`. No full/full*,
make check, browser, live socket, actual App or HTTP Door run was requested/run.

Remaining cross-owner pair: Runtime supplies constrained same-ID headless
repair/public admission; App persists original workflow intent BEFORE create,
then exact init batch/base/request/key BEFORE commit and resumes on verified
history. Current test uses existing Agent Outbox to demonstrate durable caller
intent at create→init and lost-ACK boundaries, not App implementation. Preserve
old App publisher and all positive repair/create/retry tests until normal frozen
successor generation and real Door/App reload, undo, retry, zero-legacy-traffic
qualification pass. This worker cannot repair a headless shell and adds no bypass.
