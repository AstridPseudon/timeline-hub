# App2 to Agent: shader root consumer contract request

Date: 2026-10-21
Scope: documentation-only handoff from the completed shader-source0055 and
postprocess392-no-fit0104 reports. This is a peer request, not a production
change, test change, new operation proposal, or activation request.

## Current Main contract, with executable source proof

App persists two host-owned authored shader roots. The types explicitly define
the storage locations and the full metadata shape:

- `src/tools/video-editor/types/index.ts:314-363` documents
  `clip.app.shader` and `config.app.shaderPostprocess`. The common authored
  fields are `extensionId`, `contributionId`, `shaderId`, optional `label`,
  `uniforms`, `keyframes`, `textures`, `enabled`, `sourceHash`, and opaque
  `metadata` (`:335-345`); texture bindings are structured refs (`:328-333`).
- `src/tools/video-editor/components/ShaderInspector/ShaderInspector.tsx:255-301`
  is the live producer. For a clip it copies the resolved clip, preserves
  existing `app` siblings, and writes the complete `nextShader` at
  `currentClip.app.shader` (`:280-289`). For postprocess it preserves other
  config-app keys and writes the complete `nextShader` at
  `resolvedConfig.app.shaderPostprocess` (`:293-301`).
- `src/tools/video-editor/lib/timeline-domain.ts:480-506` validates the
  required root identity (`scope`, `extensionId`, `contributionId`, `shaderId`)
  and reads the two roots. `:541-589` assigns clip or postprocess metadata;
  occupied-scope replacement is refused by the existing domain validator.
- `src/tools/video-editor/lib/timeline-patch.ts:963-980,1706-1745` shows the
  existing `app.update` consumer path. A postprocess payload is recognized only
  at target `shaderPostprocess`, then passed through
  `assignTimelinePostprocessShader`; the existing occupied-scope diagnostic is
  emitted before the update proceeds.

The current producer still sends the whole resolved config through the legacy
`applyEdit({ type: 'config', ... })` path. The shader-source0055 report staged a
dormant row-local capture seam but deliberately did not wire it into that
producer or into session, preview, player, or render paths. The serializer row
therefore remains open.

## Exact Agent mismatch and existing carriers

The smallest executable Agent command demonstrating the clip mismatch is:

```json
{
  "schema_version": 1,
  "op": "clip.set-params",
  "version": "1",
  "select": "parent/clip:clip-1",
  "args": {
    "values": {
      "shader": {
        "scope": "clip",
        "extensionId": "com.example.shader",
        "contributionId": "wash",
        "shaderId": "wash",
        "uniforms": {"intensity": 0.75}
      }
    },
    "clear": []
  }
}
```

On current Agent, `astrid/sdk/timeline/_scalar_commands.py:68-95` makes
`clip.set-params` write `parent/clip:clip-1.params.shader`, not
`parent/clip:clip-1.app.shader`. The same implementation rejects
`schema_source` without a genuinely selected project-pack element at
`:81-88`; with a selected element, the authority is for `params.*`, not for a
host-owned shader root. `astrid/sdk/timeline/commands.py:64-72` confirms that
the current registry has `clip.set-params` but no shader-root operation.

For postprocess, the existing App project-data carrier is mechanically close
but semantically not fit as currently defined:

- `src/tools/video-editor/commands/projectDataMember.ts:298-338` captures a
  `project-data.write` command with `target`, `key`, `value`, and replace mode.
- `:270-286` applies it as
  `parent.config.app[target][key] = value`, preserving existing sibling JSON,
  opaque values, object-key order, and absent optional fields when replacing a
  leaf. It is replace-only and has no delete/absence member.
- Therefore `target: "shaderPostprocess"` reaches the right App key only by
  treating a host root name as an extension namespace. The record does not
  retain or recheck the selected registry record, source/schema authority,
  `sourceHash` authority, or the one-postprocess-scope identity. The completed
  0104 counterexample showed that the carrier can accept a `shaderId` leaf
  change while `assignTimelinePostprocessShader` refuses the corresponding
  occupied-scope replacement.

The existing-carrier fit is consequently narrow and explicit:

1. Clip root: use the existing clip scalar/capture family only as the carrier
   family, but it must gain an Agent-owned root-aware form that writes
   `clip.app.shader`; it must not be represented as selected-schema PARAM.
2. Postprocess root: extend the existing `project-data.write` carrier with a
   closed host-root/authority case for `config.app.shaderPostprocess`; do not
   create a second DTO or a generic shader builder. Agent owns the command and
   recording shape, subject to the acceptance below.

## Preservation and classification requirements

The consumer contract must preserve, exactly and in order:

- root presence versus absence, including an absent root, `null`, `false`,
  empty values, and opaque nested metadata;
- all unrelated `app` siblings and their original order;
- the selected source/registry identity and its authority, rather than
  rebuilding it from `shaderId` or a UI registry lookup;
- `uniforms`, `keyframes`, `textures`, `enabled`, `sourceHash`, and opaque
  `metadata`, including texture-binding values and field absence;
- exact inverse/replay behavior, restoring the original root or its absence;
- guarded refusal when the target identity, original authority, selected source,
  or occupied postprocess scope is unavailable or changed.

Agent should classify the fields, rather than treating all metadata as
advisory: shader scope and registry identity (`extensionId`, `contributionId`,
`shaderId`, and the selected source/schema authority) are core validation
inputs; visual authored values and bindings are authored state; labels,
diagnostics, registry defaults, fallback labels, inspector bookkeeping such as
`uniformPreset`/`inspectorCompareMode`, and similar registry-derived values are
advisory or derived unless the existing normal API proves otherwise. This
packet makes no security-bug claim. The 0104 result is a semantic no-fit in the
current carrier; a security finding would require normal API evidence beyond
this source-only counterexample.

## PEER REQUEST TO AGENT

Please review this exact packet and return a bounded ACK or a concrete mismatch
for the existing carrier families. If accepted, define and qualify the
smallest root-aware Agent contract for both `clip.app.shader` and
`config.app.shaderPostprocess`, retaining Agent ownership of operation and
recording details. Minimum acceptance is executable proof of:

1. set and explicit clear/absence for each root;
2. exact preservation of opaque fields, key order, unrelated roots, selected
   source identity, and texture bindings;
3. core identity/authority validation, including occupied postprocess scope;
4. guarded inverse/replay and stale-authority refusal; and
5. normal native acceptance, reload, retry, and undo evidence before App
   rewires `ShaderInspector` or retires the legacy config writer.

Please identify the exact Agent source SHA/tree and focused controls in the ACK.
Runtime can then provide the bounded counterpart ACK for the agreed existing
carrier. Until both are qualified, keep the current legacy producer, keep the
generic shader builder unmerged, and keep the whole serializer row OPEN.

## Evidence and limits

This packet did not modify production or test code and did not rerun the
shader-source0055 15-control or postprocess392 23-control sets. The completed
reports record the following evidence:

- shader-source0055: `npx vitest run --no-cache --config
  config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism
  src/tools/video-editor/commands/shaderInspectorCapture.test.ts
  src/tools/video-editor/components/ShaderInspector/ShaderInspector.test.tsx`
  — 2 files, 15 tests passed; ESLint and `git diff --check` passed.
- postprocess392-no-fit0104: Vitest focused run — 1 file, 2 tests passed;
  three-file Vitest run — 3 files, 23 tests passed; ESLint, `tsc --noEmit`,
  and `git diff --check` passed.

No full suite, browser, localhost/socket, Runtime/Agent gate, pin, activation,
or preview/player/render qualification was performed for this documentation
packet.
