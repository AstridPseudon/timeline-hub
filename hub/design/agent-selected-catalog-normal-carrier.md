# Agent selected-catalog normal admission carrier

Status: **PASS for an existing project-owned normal pack; BLOCKED for the
hosted system/builtin source unless App supplies an already-admitted
project-owned tuple.** No Agent product files were changed.

## Exact result

The supported carrier is the existing project-pack admission and retained
document-input path:

```python
admit_project_pack(
    realm: str,
    project: str,
    *,
    client=None,
    collection="default",
) -> dict[str, Any]
```

The existing CLI entry points are:

```text
python3 -m astrid.core.element.cli project-pack init \
  --realm <realm> --project <project> [--collection <owner>]
python3 -m astrid.core.element.cli project-pack admit \
  --realm <realm> --project <project> [--collection <owner>]
python3 -m astrid.core.element.cli project-pack resolve \
  --realm <realm> --project <project> --pack <packId> \
  --element <id> --kind <effect|animation|transition> --revision <sha256:...>
```

`init` must precede `admit`. `admit` is explicit and may create a new
immutable admission, or backfill the existing admission's `snapshot_object`
through the same flow when the local source closure still matches. It does
not rebind old timeline records or silently select the latest admission.

## Identity and read tuple

For the requested descriptor, the tuple must be carried exactly as received
from Agent admission:

```text
owner:    <admission.pack_id> == elementRef.packId
id:       audio-reactive-colour
kind:     effect
revision: the full 64-hex sha256 revision returned by admission
```

The peer supplied only the display prefix
`rendering/effect/audio-reactive-colour@sha256:8e3a…`. This note deliberately
does not expand that prefix or substitute another revision. The current main
Agent rendering source computes `sha256:5e566b1a94381b45c5af4d8afbdf3b010444405e923c39dd1354bc670b650f5d`,
which is not the requested source. The frozen R4 builtin catalog contains
`sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e`,
also a different source. Neither is evidence for `8e3a…`.

The containing project document supplies the exact `DocumentPin`:

```json
{
  "document_id": "<row.document_id>",
  "version": <row.version>,
  "content_digest": "sha256:<digest of row.content>"
}
```

Agent's existing `resolve_admitted_element()` returns this binding as
`binding.projectId`, `binding.documentId`, `binding.documentVersion`, and
`binding.contentDigest` (`astrid/core/element/project_packs.py:704-731`).
Map those fields to the `DocumentPin`; App must not hash a document body or
choose a first/latest admission. The selected admission's
`snapshot_object.object_id` is the only object ID for the exact
`owner/id/kind/revision` tuple.

## Existing path, end to end

1. `admit_project_pack()` validates the configured project-pack document and
   source closure, copies every declared file into the immutable local
   snapshot, and preserves `.build-receipt.json`
   (`astrid/core/element/project_packs.py:392-488`).
2. It serializes the portable snapshot (sorted path/hash/bytes plus the build
   receipt), imports it through the existing managed media/CAS import, and
   records the returned `{object_id, digest, size, media_type}` in the same
   project-pack document admission (`:488-500`). The document remains the
   source of the admission identity; the CAS object is the retained bytes.
3. Agent/App2 carry the exact pin in the existing selected-PARAM command:

   ```json
   {
     "op": "clip.set-params",
     "args": {
       "values": {"<parameter>": "<value>"},
       "clear": [],
       "schema_source": {
         "document_id": "<exact>",
         "version": 1,
         "content_digest": "sha256:<exact>"
       }
     }
   }
   ```

   `schema_source` is an existing optional `DocumentPin`, not a new DTO.
4. The generated retained reads already exposed by the SDK are:

   ```python
   client.get_project_verified_document(project_id, pin)
   client.get_project_verified_document_object(project_id, pin, object_id)
   ```

   Their generated routes are respectively:

   ```text
   GET /v1/projects/{project_id}/document-inputs/verified
   GET /v1/projects/{project_id}/document-objects/verified
   ```

   The second request repeats the exact pin and adds the selected
   `snapshot_object.object_id`. Runtime returns the retained `VerifiedDocument`
   and closed `VerifiedDocumentObject`; Agent's
   `admitted_element_snapshot_descriptor()` validates the admission, closure,
   build receipt, descriptor, and bytes
   (`astrid/core/element/project_packs.py:678-701`).

5. The normal provider consumes only that verified pair. It records the pin
   and snapshot descriptor as command dependencies and uses the exact source
   again for retry, inverse, redo, and replay. No local source, build cache,
   renderer, browser catalog, or re-discovered latest admission is consulted.

## Reproducible ephemeral proof

The existing fixture `retained_pack` is test-only. It creates a temporary
Runtime realm/project/timeline, seeds a project pack, calls the real
`packs.admit_project_pack()` with a Runtime-backed test client, reads the
project document and its CAS bytes, and submits a native PARAM request whose
provider must consume only the selected snapshot object. Temporary source,
artifact, RealmStore, document, and CAS state are all under pytest's `tmp_path`.

Exact command run from this Agent worktree:

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
/home/user/work/venv-agent/bin/python -m pytest -q -rs \
  -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_selected_schema_runtime.py::test_native_params_reads_only_the_exact_selected_object
```

Result: **1 passed in 2.35s**. The proof is the same normal source/admission,
managed CAS, project document, exact pin, exact object read, and provider
validation path App2/Runtime must use. It is intentionally not a browser,
hosted, installed-host, renderer, or full-suite claim.

## System-pack constraint and smallest peer question

`admit_project_pack()` is for a project-owned source binding. Its document
requires `astrid.project-pack/v1`, `source_binding_key: project-packs`, a
project-scoped relative manifest, and an owner-qualified project-pack
admission. The built-in/system rendering source (`pack:rendering`, or the
hosted builtin) is not that project-owned source. Giving it a guessed
`packId`, copying the builtin revision, or making App's browser catalog stand
in for the admission would violate the existing custody contract.

Therefore the exact hosted `8e3a…` descriptor is **not yet a qualified
carrier** from the evidence supplied here. The smallest peer question is:

> Can App2/Viewing provide the exact full `packId` plus full 64-hex revision
> and `DocumentPin` from an actual prior Agent `admit_project_pack()` for this
> `audio-reactive-colour` effect, or is `8e3a…` a system-pack source that must
> remain visibly unsupported until an owner-approved system-pack carrier
> exists?

Until that answer is yes, App2 must keep the selected-PARAM write refused with
the draft preserved. Do not substitute builtin `2a9b…`, invent a project-pack
owner, re-admit inside save, or add a route/DTO/manifest.

## Evidence boundaries

- Peer input: `peer-app-to-runtime-20261020T2027Z-selected-catalog-normal-carrier.md`.
- Viewing report: `handoff-vw-m3-d10-selected-catalog-normal-producer-report.md`;
  93 targeted checks passed and hosted `runtimeOrigin() !== ''` disables the
  virtual admission module and `/api/astrid-element-admissions`.
- No product code, public API, endpoint, schema, or test was changed here.
- No browser, installed-host, renderer, full, or live-hosted suite was run.
