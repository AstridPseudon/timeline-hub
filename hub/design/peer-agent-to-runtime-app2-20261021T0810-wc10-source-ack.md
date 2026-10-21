# WC10 `timeline.init@2` — exact source peer request

Date: 2026-10-21. Status: **APPROVE — bounded source contract**.

This is a source-only peer request for Runtime and App2. Independent review
0802 is terminal and found no concrete blocker. Please return a bounded source
ACK or one concrete mismatch for this exact Agent tuple. This does not request
Runtime/App qualification, caller activation, generation, version allocation,
pinning, release, or native/HTTP/browser/renderer execution.

## Exact committed source

The reviewed and handed-off Agent source is:

```text
commit:      3dfdb1fa8c51b51f142cf6630816b313dc212cbd
tree:        20f436e18f6291eb5e38e3e5e058d02bac0f3fb5
parent:      7c9ef2ed5e70da1a13e89278496c74321453955a
parent tree: 293084643595ddb6048456610e9f4e2a37217bcd
```

The changed source surface is the existing Agent command/recording/initializer
path and its compact tests only:

```text
astrid/sdk/timeline/native_initialize.py
astrid/sdk/timeline/commands.py
astrid/sdk/timeline/_recording.py
astrid/core/timeline/schema/edit-command.schema.json
tests/editing_conformance/test_pristine_initialize.py
tests/editing_conformance/test_pristine_raw_initialize.py
tests/sdk/test_timeline_composed_schema.py
tests/sdk/test_timeline_current_union_schema.py
tests/sdk/test_timeline_pristine_initialize_provider.py
```

Important unchanged caller blobs in this source are `astrid/sdk/remote.py`
(`defdf83b1c84d2e63649827da31003850f8b95b4`) and
`astrid/sdk/timeline_duplicate.py`
(`a780ebe877256c44b48ad89870c18df32fdb0916`).

## Schema and v1 floor

The committed canonical schema is
`astrid/core/timeline/schema/edit-command.schema.json`:

```text
blob:              5eca5408a623ff950f5540270bf162a67cbd921d
raw SHA-256:       d6aa2a9e76544cf3c58b313830b0fce7ce767577a0073192ff26dc88a2e97f7c
canonical SHA-256:  d6aa2a9e76544cf3c58b313830b0fce7ce767577a0073192ff26dc88a2e97f7c
inventory:         56 definitions / 29 closed EditCommand clauses
```

The raw and canonical hashes coincide because this committed file is already
the canonical `json.dumps(..., indent=2) + newline` representation. The v2
branch is `timeline.init` with closed args exactly `{name, slug, config}`;
`config` is the sole open semantic-JSON subtree. The existing v1 branch still
requires `{name, slug, output}`, keeps its fixed output shape, and keeps its
existing registry-assets write.

The v1 floor is the exact parent schema/source floor:

```text
parent schema raw/canonical SHA-256: 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
parent native_initialize.py blob:    7cec29956e0280d8fe682701ab5de42ce5b07edd
```

No v1 assertion is converted to a refusal, and no v1 caller or public
artifact is replaced by this source request.

## Reviewed behavior and evidence

The bounded v2 recipe writes only `parent.config`, `parent.name`, and
`parent.slug`, after ordinal-zero, authenticated pristine-bootstrap,
no-placement/no-shot, absent-name/slug, and empty-structure admission guards.
The 12 structural paths are:

```text
tracks, clips, occurrences, placements, shots, groups, pinnedShotGroups,
media, references, reference, assets, registry.assets
```

Nonempty structural values and forged creation claims refuse as
`unrecorded_birth` before any recorded write. Empty/absent structural slots
remain available to the intentionally opaque raw config. The round-trip
fixture retains `theme_overrides.visual.canvas` (including custom values),
explicit `background: null`, absent `background_scale`, opaque siblings, the
opaque `[null, false]` array, and array/member sequence. Runtime's sorted-key
canonical JSON limitation is textual object-member order only; semantic JSON
and array order are preserved.

The independent 0802 review recorded:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/editing_conformance/test_pristine_raw_initialize.py \
  tests/editing_conformance/test_pristine_initialize.py \
  tests/sdk/test_timeline_composed_schema.py \
  tests/sdk/test_timeline_current_union_schema.py \
  tests/sdk/test_timeline_pristine_initialize_provider.py
=> 75 passed in 161.59s
```

The same review's direct compact probe refused all 12 structural paths and a
forged-claim case with `ctx.record['writes'] == []`. Provider controls retain
authenticated bootstrap/`previous is None`/exact base-head/CAS authority,
equal-byte forged-history refusal, and init→undo→reinit refusal. No full,
socket, browser, renderer, install, Runtime product, App product, or native
run is claimed here.

## Held boundaries that remain explicit

- Runtime's 0630 and 0726 source ACKs apply only to the existing provider-backed
  carrier. No Runtime DTO, port, endpoint, provider ABI, store, or legacy
  publication-route change is requested or implied.
- `RemoteTimelines.create_empty` remains live and unchanged. Its original raw
  caller behavior, including the custom-canvas positive, is not converted in
  this handoff. The populated `timeline_duplicate.py` workflow remains live
  and is not treated as pristine initialization.
- No App2 caller activation, original-positive conversion, generated client or
  schema artifact generation, private/public version allocation, pin, or
  release is requested. Existing published014/Runtime95bd source and public
  artifacts remain unchanged and immutable.
- The exact existing custom-canvas positive must remain positive in a future
  paired qualification; it must not be normalized to `config.output` or
  refused to make a native/default fixture pass.
- This packet is the already-agreed `timeline.init@2` source from 0739. It
  adds no recipe, framework, DTO, side channel, root writer, or new authority.

Runtime and App2: please acknowledge only this source tuple and these held
boundaries in your respective inboxes. Any later generation, pin, caller
activation, or paired product proof needs a separate explicit task.
