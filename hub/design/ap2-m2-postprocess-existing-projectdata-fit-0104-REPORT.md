# Postprocess shader project-data fit check

## Decision

**NO FIT for the existing private392 carrier.** No dormant postprocess member
was prepared. The existing `project-data.write` member can preserve raw leaf
data, but it is an extension-owned opaque-data carrier and does not retain or
recheck the selected postprocess shader authority. Using it for this host-owned
root would allow a shader identity change that the real postprocess validator
must refuse.

## Main authored root

Main stores one postprocess shader at:

```text
parent.config.app.shaderPostprocess
```

The root is a `TimelinePostprocessShaderMetadata` object. Its required identity
fields are `scope: "postprocess"`, `extensionId`, `contributionId`, and
`shaderId`. Its optional authored fields are `label`, `uniforms`, `keyframes`,
`textures`, `enabled`, `sourceHash`, and opaque `metadata`. `config.app` is a
host-owned application metadata map, not an extension-data namespace.

The actual source/schema authority is the selected registry record, looked up
by `shaderId` and `ownerExtensionId`, with matching `contributionId` and a
`postprocess` pass. The existing domain path
`assignTimelinePostprocessShader` also enforces the one-postprocess-shader
scope and refuses replacement of an occupied scope with another shader.

## What the existing carrier does and does not preserve

The current helper maps a project-data operation as:

```text
project-data.write(target, key, value, replace)
  -> parent.config.app[target][key] = value
```

Therefore `target: "shaderPostprocess"` is syntactically accepted and reaches
the right object, but only by treating the host root name as an extension ID.
It preserves existing sibling values, opaque JSON, object-key order, and
absent optional fields when replacing an existing leaf. It cannot remove a key
that becomes absent, because the private392 carrier is replace-only and has no
delete member.

Those lossless leaf properties are not enough: the command records only the
project-data leaf and container claims. It has no selected registry record,
shader source/schema pin, `sourceHash` authority, or postprocess-scope
validation. Passing the real extension ID instead would write the wrong path,
`config.app[extensionId]`, rather than `config.app.shaderPostprocess`.

## Executable counterexample

Added the focused test-only counterexample:

`src/tools/video-editor/commands/postprocessShaderProjectDataFit.test.ts`

It verifies both facts in two tests:

1. Replacing the existing `shaderId` leaf through the carrier preserves the
   raw root, opaque sibling, key order, absent `enabled`, and replay result.
2. `assignTimelinePostprocessShader` refuses changing `shader.postGrade` to
   `shader.postVignette` with `shader_scope_occupied`, while
   `captureProjectDataMember` accepts the same leaf write and produces the
   mismatched root.

This is the precise validation bypass that prevents a dormant row-local member
from being safe. No old ShaderInspector builder was reused or merged.

## Smallest existing-carrier extension request

Keep the existing `project-data.write` operation rather than inventing a new
operation, but add a closed host-root/authority variant for this one root. It
must:

- address `config.app.shaderPostprocess` explicitly instead of interpreting
  `shaderPostprocess` as an extension namespace;
- require the selected registry authority for
  `{extensionId, contributionId, shaderId, scope}` and the postprocess schema;
- preserve the existing replace-only leaf claims and raw sibling/order/absence
  behavior; and
- recheck that authority and occupied-scope identity during replay/acceptance,
  refusing stale or unknown selected sources before any write.

Until that existing-carrier extension is available and qualified, the live
ShaderInspector config writer must remain unchanged.

## Live callers and ownership

- `src/tools/video-editor/components/ShaderInspector/ShaderInspector.tsx:255-301`
  is the live legacy producer. The postprocess branch writes the whole
  `resolvedConfig.app.shaderPostprocess` root at lines 293-301.
- `src/tools/video-editor/commands/projectDataMember.ts:299-354` is inert in
  this worktree; no non-test production caller was found.
- `src/tools/video-editor/commands/genericPatchCapture.ts:129-161` does not
  classify `project-data.write` as supported.
- `src/tools/video-editor/hooks/useTimelineOps.ts:270-274` routes only
  classified native generic patches; project-data remains on the guarded
  fallback path.
- `src/tools/video-editor/commands/commitSession.ts:954-986` constructs the
  generic port but has no project-data dispatch.

Clip-local `clip.app.shader` remains out of scope. Preview, player, and render
ownership were not changed.

## Verification

Passed in the assigned App worktree:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/postprocessShaderProjectDataFit.test.ts
1 file, 2 tests passed

node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/postprocessShaderProjectDataFit.test.ts src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/lib/timeline-domain.shaders.test.ts
3 files, 23 tests passed

node_modules/.bin/eslint src/tools/video-editor/commands/postprocessShaderProjectDataFit.test.ts --ext ts --max-warnings 0
passed

node_modules/.bin/tsc --noEmit --pretty false
passed

git diff --check
passed
```

Reused, without repeating, the existing private392 Agent floor evidence:
the approved seam-private392 review records 17 focused Agent project-data
tests and the matching App helper evidence. No full suite, browser,
localhost, socket, pin, activation, Runtime mutation, or shared-file change
was performed.
