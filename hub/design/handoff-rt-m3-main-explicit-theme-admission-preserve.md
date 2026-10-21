# Runtime Main explicit-theme admission preservation

## Corrected current disposition

This remains an ordinary-carrier proof only. Runtime `95bd3c5` is unchanged;
Main infrastructure touched for this investigation: **NONE**. The proof does
not qualify the raw `params.timeline_ref` probe, canonical Theme acceptance, or
physical parity. The old custody REQUEST CHANGES report is superseded because
its positive fixture was misidentified as a current SDK caller. Preserve the
historical red positive and passing foreign/tamper negative; do not merge or
xfail the invalid fixture. See the canonical-caller reconciliation for the
exact source names and abandoned branch dispositions.

## Result

No Runtime product change is required. Runtime `95bd3c5` already preserves the
upstream Main ordinary file-input path for an explicit Theme. The current
Timeline canonical managed-render freeze must remain strict and must not be
changed to admit arbitrary extra objects.

## Exact source boundary

- Runtime current source: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Runtime upstream Main reference: `origin/main` at
  `b535646faaad2f8ae7968dfe0f4fa3057f960264`.
- Both current Runtime and `origin/main` retain
  `RealmStore._freeze_managed_render_inputs()` as the canonical
  `timeline_ref` admission boundary. It derives ordered IDs from the
  canonical timeline registry and rejects a supplied list that differs from
  that canonical order. This is correct closure protection, not a Theme
  source selector.
- The upstream ordinary invocation has no `params.timeline_ref`: the named
  `inputs.theme` descriptor is retained in the opaque task spec and the
  ordinary Runtime input path validates project association and exact ordered
  `input_object_ids`/`execution_request.inputs` identity.

## Executable proof

Using `RuntimeService` and its normal `ingest` API, a distinguishable JSON
Theme was imported into project CAS with `media_type=application/json` and
`original_name=theme.json`. A normal `rendering.render` task was admitted with
the named `inputs.theme` descriptor and matching ordered CAS IDs. The admitted
readback preserved the descriptor and ordered object ID. The existing
`deployment_binding_from_task()` projected exactly one immutable
`InputBinding(name="theme", object_id=<id>, digest=<id>)`; a direct CAS read
matched the authored bytes byte-for-byte.

No Runtime resolver or Theme interpretation is involved: GenericHost
materializes the already-authorized named input as `theme.json` and Agent's
existing resolver remains the sole Theme merge point.

Existing direct-neighbor tests preserve the refusal boundaries: foreign
project objects, conflicting/duplicate descriptors, and reordered
`execution_request.inputs` are rejected; capture authority tests preserve
candidate/closure checks and no-write refusal.

## Actual integration gap and deferred proposals

The missing forwarding is upstream of Runtime's ordinary carrier. App's
managed export path currently does not forward its resolved Theme (and its
`theme_id` slug is not authority). Agent/App/Viewing must preserve the Main
ordinary invocation's named `inputs.theme` descriptor and its digest in the
existing admission manifest. Viewing may only consume the existing admitted
named materialization; it must not add slug lookup, browser/hash authority,
another transport, or a second resolver.

Do not add the Theme object to canonical `timeline_authority` media closure,
relax the exact `timeline_ref` list, accept an unowned descriptor, or treat an
inline JSON value as provenance. Explicit invalid, foreign, missing, or
tampered descriptors must continue to refuse visibly rather than fall back to
the default Theme.

The new ThemeDocument, `app.astrid.themeSource`, private preparation, and
delegation proposals are explicitly **DEFERRED** per the owner ruling.
