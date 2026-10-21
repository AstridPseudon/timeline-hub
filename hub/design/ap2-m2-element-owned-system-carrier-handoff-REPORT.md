# AP2 M2 element-owned system carrier handoff

## Disposition

**Producer gap; hold App2 activation and issue the Agent peer request below.**

The current source tree has no existing authorized producer/result-field pair
that can carry a retained global/system declaration pin to App2. The valid
project-owned carrier must not be reinterpreted as system ownership.

The target identity is:

```text
packId=rendering
id=audio-reactive-colour
kind=effect
revision=sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387
```

The hosted built-in is a different source and must never be substituted:

```text
packId=rendering
id=audio-reactive-colour
kind=effect
revision=sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e
```

Neither revision is an admission pin by itself.

## Existing seams checked

### App

* `src/tools/video-editor/runtime/admitted-elements.ts:41-66` gates the
  admission route to local development/project-pack admission. Hosted mode
  does not obtain an admission document from this route.
* `src/tools/video-editor/runtime/admitted-elements.ts:128-135` exposes exact
  `id`, `packId`, `kind`, `revision`, schema, defaults, and authoring metadata,
  but no `DocumentPin` and no retained `snapshot_object`.
* `src/tools/video-editor/runtime/pinned-element-source.ts:5-28` performs an
  exact saved-ref lookup and returns catalog/draft metadata only. It cannot
  establish historical admission authority.
* The existing native timeline carrier is sufficient once a legitimate source
  is supplied: `clip.add`/`clip.set-element` accepts the owner-qualified ref
  and `args.schema_source` (`DocumentPin`). The App test
  `tests/e2e/local/three-products.selected-param-dev.spec.ts:57,74,89,110`
  proves this for a retained project pack, not for a system/builtin source.
* `agentToolInvocationService.ts` is the M10 generic `ToolResult`/proposal
  bridge. Its artifact promotion metadata is not Agent managed invocation
  authority and has no declaration pin/object field. It cannot be used as a
  replacement carrier.

### Agent managed invocation and result

* The existing private action is
  `rendering.timeline_visualize`, reached by
  `astrid/sdk/invocation.py:_invoke_internal_result` and the existing
  `rendering.timeline_visualize` preflight. The settled private
  `scene_only` precedent is therefore the only plausible action to examine.
* `astrid/sdk/invocation.py:766-786` calls `prepare_filmstrip`, freezes the
  timeline capture, and adds `metadata.element_resources` plus an
  `element_resource_binding_hash`.
* `astrid/sdk/invocation.py:1003-1074` resolves an exact registry/pack
  declaration and hashes declared resource bytes. This is derived resource
  metadata, not a retained Runtime document pin or snapshot object; it does
  not produce `document_id`, document `version`, `content_digest`, or an
  admitted `snapshot_object.object_id`.
* The managed preflight at `astrid/sdk/invocation.py:4272-4334` forwards the
  frozen capture through the existing authority context/filmstrip authority
  object. That authority is for the timeline capture and its source revision,
  not a system declaration admission.
* `astrid/sdk/results.py:158-179,275-293` exposes generic
  `InvocationResult.raw_result` and `InvocationResult.outputs`. The current
  filmstrip result is a bundle/scene answer with timeline/render provenance;
  no existing result value contains the required declaration `DocumentPin`
  and retained snapshot object. There is no App bridge that turns generic
  managed outputs into declaration authority.

### The tempting project-pack producer is disqualified

`astrid/core/element/project_packs.py:392-505` is a real authorized producer:
it captures an immutable source closure, publishes a project document, and
attaches a CAS `snapshot_object`. The validator at `:536-586` requires the
verified project document to be scoped to the project and requires the
owner-qualified reference; `:611-675` independently verifies the immutable
bytes/build receipt. This is exactly the right proof for a project-owned
overlay, and exactly the wrong authority for claiming the system/builtin
`rendering` pack as project-owned.

The Agent f83 source ACK and the existing selected-schema tests therefore
support the existing `schema_source: DocumentPin` carrier only for an actual
owned overlay. They do not qualify normal project-pack admission as a system
declaration producer.

## Private-mode decision

Do **not** apply the settled private-internal-mode precedent here. The same
managed invocation and result types are present, but the same capture
authority does not contain a system declaration admission, and the same
result fields do not contain its `DocumentPin`/object identity. Treating
`metadata.element_resources`, a browser/catalog revision, `snapshot_label`,
or the hosted built-in revision as that pin would be fabricated authority.
Adding a new DTO, endpoint, provider/store, manifest, or App-side carrier
would violate the settled M2 boundary.

## PEER REQUEST — Agent-owned unit

Please qualify **one existing authorized Agent producer action** for the exact
`rendering/effect/audio-reactive-colour@sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387`
declaration, or return an explicit no-carrier result.

The action may reuse the existing private managed
`rendering.timeline_visualize`/capture authority only if that authority
already opens a legitimate global/system declaration admission. It must not
turn `admit_project_pack` into system ownership. Use one existing result field
(the current candidate is the generic `InvocationResult.raw_result` mapping;
do not add a public DTO or a new result type) to expose the exact captured
record containing all of:

```json
{
  "elementRef": {
    "packId": "rendering",
    "id": "audio-reactive-colour",
    "kind": "effect",
    "revision": "sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387"
  },
  "schema_source": {
    "document_id": "<actual retained system document>",
    "version": "<actual captured version>",
    "content_digest": "<actual captured content digest>"
  },
  "snapshot_object": {
    "object_id": "<actual retained object id>",
    "digest": "<same object digest>",
    "size": "<actual size>",
    "media_type": "application/json"
  }
}
```

The field names above describe the acceptance witness; they are not a request
to add a new public schema. If the existing managed result cannot carry this
record without adding a new field or authority store, stop and report
`NO-CARRIER` instead of inventing one.

### Acceptance witness requested from Agent

1. Invoke the named existing action against a real capture/admission of the
   exact 8e identity; do not use browser catalog state or a hash computed by
   App.
2. Assert the returned existing result field contains the exact owner/id/kind/
   revision, a `DocumentPin` whose digest is the opened document content, and
   a `snapshot_object.object_id` read from that admission.
3. Assert the retained read validates the same `(DocumentPin, object_id)` and
   the source bytes/build receipt resolve to the exact declaration. This is
   the system analogue of the existing project-owned witness in
   `tests/sdk/test_timeline_selected_schema_runtime.py:82-100`.
4. Add negative witnesses: the `2a9b...` built-in revision, a latest/builtin
   substitution, a browser/catalog-only revision, and a normal project-pack
   document used as system ownership must all refuse.
5. Return the exact serialized result sample and source/test locations to
   App2. App2 can then feed the existing native `schema_source` carrier; no
   App/Runtime source change is part of this request.

Until that witness exists, App2 must hold the hosted/system overlay path.

## Verification and scope

No product source was changed. This was a read-only source/report
investigation; no generation, pin/adoption, render, browser, socket, full
suite, or central `request-test` run was performed. Working-tree check:

```text
git status --short --branch
## tl/ap2-m2-element-owned-system-carrier-handoff...hub/tl/integration
```

The product worktree is clean. The report is the only deliverable from this
worker.
