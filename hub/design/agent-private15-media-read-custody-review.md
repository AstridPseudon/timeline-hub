# Agent private15 media authority repair

## Disposition

Repair the media-authority boundary in reviewed Agent commit
`5869c0cb058d63e6097a0eea20e502a2042f3e0f` only. The prior review correctly
blocked the arbitrary callable lookup and the silent identity-conflict
acceptance. The implementation must use the already-reviewed D13
`WorkspaceClient` media adapters from source `7b3e1205` / compose
`65c87dd5`, as carried by `tl/agt-m2-d13-final95-current-cut-ready`; it must
not introduce another media API, a fabricated verifier, or a new authority
source.

## Exact authenticated adapter

Baseline `6efc815` is missing the two normal-client adapters. Port only this
unchanged `WorkspaceClient` hunk, including both operation allow-list entries:

```python
def get_project_media_selection(self, project_id: str, selection: Mapping[str, Any]) -> Any:
    """Read one exact Runtime-selected project media pin."""
    return self._call_generated("get_project_media_selection", project_id, selection)

def get_project_verified_media(self, project_id: str, selection: Mapping[str, Any]) -> Any:
    """Read the Runtime verifier result for one exact media pin."""
    return self._call_generated("get_project_verified_media", project_id, selection)
```

The normal generated-client contract remains unchanged and is the authority
for the request/response shape:

```text
get_project_media_selection(project_id, MediaSelectionQuery) -> MediaSelection
get_project_verified_media(project_id, MediaSelection) -> VerifiedMedia

MediaSelectionQuery =
  {asset, generation_id, variant_id}
  | {association_id, object_id, version}

MediaSelection =
  {asset, generation_id, variant_id, object_id, catalog_digest}

VerifiedMedia =
  {selection, media_type, size, duration_seconds?, width?, height?}
```

The generated methods retain the existing authenticated loopback Runtime
transport, credential, project scope, and normal client/factory construction.
The voiceover helper must receive that normal `WorkspaceClient` (or the
existing typed facade that owns it); it must not search `client`, `_remote`,
`_transport`, `_generated`, or arbitrary `getattr` results for a callable. If
the normal adapter is unavailable, raise the existing voiceover error and
keep the private managed result refused. Do not accept a test-installed
callable as Runtime authority.

## Exact selection and verification rules

Replace `_runtime_method()` with direct calls to the two fixed adapters. Keep
the current/private host context and the existing managed-output association
as the selector source. Do not trust a mutable client field or a caller
supplied MIME, byte size, duration, or selection.

`_media_selector()` must fail closed unless exactly one selector form is
present and internally consistent:

- association form: nonempty `association_id`, `object_id` digest, and
  integer `version >= 1` (lifecycle version may supply the same value);
- legacy form: nonempty `asset`, `generation_id`, and `variant_id`.

If both selector forms or duplicate identity fields are present, every known
claim must agree with the exact Runtime result; a conflict in legacy identity,
`digest`, or lifecycle version is a refusal. Never prefer one form and
silently drop the other. If both `object_id` and `digest` are present they
must be the same digest. Boolean versions are invalid.

After the selection read, require the exact five-field `MediaSelection` and
require the returned selection to equal the selector’s bound identity. Bind
the requested project, generation, variant, asset, association, object, and
version to the response wherever those fields are available. Contradictory
project/source/output identity is a refusal, including a foreign project,
generation or variant, asset mismatch, object mismatch, association mismatch,
or catalog-digest mismatch. Do not overwrite or discard conflicting claims.

After the verified-media read, require `verified.selection` to equal the
Runtime selection, `media_type == "audio/wav"`, a positive integer `size`,
and a finite positive intrinsic `duration_seconds`. Read the selected object
bytes through the existing managed media surface and require both exact byte
length and `sha256(payload) == selection.object_id`. Runtime’s intrinsic
duration remains authoritative for retiming; manifest/caller duration is
never authoritative. Runtime authorization, lifecycle, completed-settlement,
catalog, and CAS failures remain visible and fail closed.

The private managed path therefore succeeds only after the real normal
client reaches both existing Runtime reads and the byte/hash/size checks
pass. There is no normal private native success without the reviewed pin and
actual combined Agent/Runtime source.

## Bounded regression coverage

Keep all existing public `22` positive behavior expectations, the public
`bound.publish(...)`/receipt path, original revision/publication pair checks,
Runtime-duration retiming, proposal digest versus outer producer identity,
and private managed no-publish behavior. Add one meaningful negative for each
affected behavior, without broad reruns:

1. install a forged/different-project selection-shaped result behind an
   otherwise real-looking output and assert refusal before proposal/native
   success;
2. supply contradictory generation/variant/object (and association/digest)
   identity claims and assert refusal rather than silent preference; and
3. return mismatched verified duration or size, or same-size bytes with a
   different hash, and assert refusal with no accepted private result.

The tests must exercise the fixed normal-client adapter boundary; a fake
callable injected through an arbitrary attribute is not positive evidence.
Do not encode a passing behavior as refusal, inject a fake positive, bypass
Runtime health, or claim normal requester outbox/retry/guarded-undo proof.

## Explicitly separate prerequisites

The `host64f` action optional-output correction is separate and must not be
folded into this media repair. Composition still requires the real
`astrid.core.execution.executor._action_context` host/runner composition;
the missing module in both base and candidate means the fixture’s
`trusted_execution_context` attribute is not evidence. Do not add an import
shadow or fake C3d positive. Until that composition exists, private managed
proposal/native qualification remains held while the media boundary itself
is repaired as above.

## Evidence boundary

The Runtime source already proves the corresponding selection and verified
media service checks (project ownership, exact selector identity,
managed/completed association, catalog metadata, intrinsic duration/size,
and CAS bytes). This document records how the Agent must reach that exact
authority. It does not claim that the current rejected commit reaches it,
nor claim live Runtime, native, browser, render, requester-outbox, or full
suite qualification.

No repository documentation is changed by this repair. The only intended
artifact is this design/review file.
