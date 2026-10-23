# A4 provider witness report

No production files, tests, schemas, pins, or branches were changed. `DONE` and the required commit message were written.

## Existing provider

The existing registered command that preserves raw video timing/transition fields is:

```json
{
  "schema_version": 1,
  "op": "clip.swap-media",
  "version": "1",
  "select": "parent/clip:<existing-id>",
  "args": {
    "old_media": "<Runtime MediaSelection>",
    "media": "<Runtime MediaSelection>"
  },
  "intent": {"ownership": "parent"}
}
```

Source:

- Registration: `astrid/sdk/timeline/commands.py:93-96`
- Callable: `capture_parent_swap_media(bundle, select, old_media, media, verified_media=...)` at `astrid/sdk/timeline/native_occurrence_media_commands.py:284-290`
- Handler: `parent_swap_media` / `_swap` at `.../native_occurrence_media_commands.py:220-263`

`_swap` invokes `_clip(..., raw_window=True)`. Therefore:

- omitted `hold` with authored `from`/`to`, and explicit `hold: null`, are used only for validation; the original row remains unchanged;
- positive subminimum holds are accepted when finite and greater than zero; no `.05` floor is introduced;
- incoming `transition` is accepted because transition rejection applies only when `raw_window=False`;
- timing fields, transition, opaque fields, and other row content are not rewritten; the normal write is the asset replacement.

Created IDs:

- same asset alias: no created IDs;
- new alias: `parent/asset:<new asset>` may be created;
- no new clip is created.

Relevant reads/guards include the target clip, parent clip collection, registry bindings, output FPS/source-window state, affected alias consumers, and payload media mirrors. Writes are limited to registry binding/mirrors and the selected clip’s `asset`.

## Important limitation

`clip.add-media` is the existing parent birth command, but it is not equivalent for this requested case:

- registration: `astrid/sdk/timeline/commands.py:103`
- handler: `astrid/sdk/timeline/native_parent_media_commands.py:25-52`
- it calls `_clip(..., raw_window=False)` at line 32;
- `_clip` requires a positive finite `hold` and rejects non-null `transition` at `native_occurrence_media_commands.py:146-187`.

Thus there is no existing registered provider that performs a *new after-anchor parent video birth* while preserving omitted/null hold and incoming transition semantics. The smallest missing migration is a birth-path semantic that reuses the existing raw-window behavior while still creating the parent clip. This is a semantic gap, not justification for `doc.patch`, a fabricated default, or a new unapproved operation.

The old behavior evidence is recorded in `agent-A4-raw-map-1837.md:133-142`; it explicitly marks incoming transition, missing/null hold, and subminimum after-anchor birth parity as uncovered by current `clip.add-media`.

## Runtime-backed selected-media authority

Existing real Runtime-backed fixture:

- `tests/editing_conformance/test_commit_runtime_parent_media.py`
- Runtime setup: `media_realm()` at lines `88-185`
- authentic Runtime selection retrieval: lines `150-159`
- ordinary execution: `test_ordinary_birth_or_ordered_replacement_accept_reload_inverse_redo_retry` at lines `195-197`, calling `ordinary_roundtrip()` lines `200-289`
- request invocation: `body()` lines `31-36`, `commit()` lines `39-44`
- ordinary command shape: `birth()` lines `57-70`

The fixture settles Runtime-managed outputs named `old`, `new`, and `unrelated` as `video/mp4`, with filenames such as `new.mp4`. The bytes are synthetic test bytes, not production media:

- `new`: `sha256:11507a0e2f5e69d5dfa40a62a1bd7b6ee57e6bcd85c67c9b8431b36fff21c437`
- `old`: `sha256:cba06b5736faf67e54b07b561eae94395e774c517a7d910a54369e1263ccfbd4`

Runtime returns the authoritative five-field selection:

```json
{
  "asset": "...",
  "generation_id": "...",
  "variant_id": "...",
  "object_id": "sha256:<64 hex>",
  "catalog_digest": "sha256:<64 hex>"
}
```

Authority and controls:

- selector resolution: Runtime `timeline_commit_port.py:826-855`;
- project/association/lifecycle/task/attempt provenance: `:865-919`;
- CAS digest/size/media-type verification: `:1006-1015`;
- catalog digest revalidation: `:1018-1020`;
- Agent exact verified-input matching and positive metadata checks: `astrid/sdk/timeline/_media_inputs.py:8-19`;
- Agent captures both `old_media` and `media` through `port.selected_media`: `astrid/sdk/timeline/commit.py:964-968`;
- acceptance revalidates captured media: Runtime `timeline_commit_port.py:493-518`.

Missing, foreign, stale, wrong-object, wrong-catalog, and occupied-identity controls are covered by existing test IDs including:

- `test_invalid_media_or_reserved_identity_refuses_before_accept_and_writes`
- `test_runtime_rejects_obsolete_scalar_shape_before_reads_and_writes`
- `test_exact_old_source_tuple_survives_new_primary_variant_and_replacement_inverse`

The raw timing test `test_parent_raw_window_and_incoming_transition_survive_without_normalization` in `test_recipe_parent_media.py:175-194` is detached Agent evidence only; it is not Runtime credit.

## V2 receipt/steps

The existing commit provider preserves the established V2 request metadata, canonical document, records, bindings, dependencies, history, undo steps, preview `would_status`, and structured refusals. Provider preparation and `port.preview/accept` occur at `astrid/sdk/timeline/commit.py:1172-1195`.

No tests were run, per the brief’s source-only instruction.