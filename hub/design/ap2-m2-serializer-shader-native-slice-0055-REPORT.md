# App2 M2 ShaderInspector serializer slice

## Result

Prepared a dormant, row-local `buildShaderInspectorPatch` seam in
`src/tools/video-editor/commands/shaderInspectorCapture.ts` with focused
success/refusal coverage. It uses only existing App patch families:

- clip shader metadata → `clip.update` with `payload.app.shader`;
- postprocess shader metadata → `app.update` at the existing
  `shaderPostprocess` root;
- scope mismatch, blank clip identity, and invalid patch versions refuse before
  a target or operation is guessed.

The builder is intentionally not wired into `ShaderInspector.tsx`,
`useTimelineCommit`, `useTimelineOps`, preview, player, or render paths. The
current UI producer remains the existing `applyEdit({ type: 'config', ... })`
producer at `ShaderInspector.tsx:289-301`. No shared HOME-owned file was
changed, and no serializer deletion or activation is claimed.

## Authored versus derived/advisory

The authored film state is the shader assignment and its editable values:
clip-local/postprocess scope and identity, uniform values, explicit enabled
state, keyframes, and existing texture bindings. These affect the visual film
and must remain attached to their raw `app` roots.

Registry diagnostics, registry defaults, the fallback label, `sourceHash`, and
inspector bookkeeping (`uniformPreset` and `inspectorCompareMode`) are
derived/advisory inspection state. The current producer can include those
fields in the config mutation, but this slice does not reinterpret them as
Agent params or infer a native edit from registry metadata.

The dormant builder passes the supplied shader object through unchanged, so
null/false/opaque metadata and field absence are not normalized or dropped.

## Agent literal mismatch

No existing Agent command fits both shader roots. The smallest executable
literal showing the mismatch is:

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

Agent `clip.set-params` records/writes `parent/clip:clip-1.params.shader`;
ShaderInspector reads/writes `parent/clip:clip-1.app.shader`. The postprocess
root has no clip selector at all. Adding `schema_source` does not repair this:
without a selected project-pack element Agent refuses
`schema_source requires a selected project pack element`; with one, PARAM
still writes `params.*`, not either shader `app` root. No selected-schema PARAM
reuse or arbitrary metadata-to-params inference was made.

## Smallest Agent contract request

Agent needs one narrowly scoped, root-aware command contract for the existing
authored shader roots: `clip.app.shader` and parent
`config.app.shaderPostprocess`. The contract should use stable clip/root
selectors and explicit set/clear semantics, capture exact original authority
for the addressed raw root, and record:

- raw root presence versus absence, including `null`, `false`, empty values,
  and opaque nested fields;
- unrelated `app` roots as preserved rather than inferred;
- guarded inverse/replay that restores the exact original root or its absence;
- refusal when the original root/authority or target identity is unavailable or
  changed.

It must not be represented as selected-schema PARAM unless the target is
actually a selected project-pack element with genuine retained original
schema authority. The request names no new operation here; Agent owns the
operation/recording shape. Until that contract exists and is qualified, this
producer remains on the legacy config serializer path.

## Ownership and decisions

- App2 owns the ShaderInspector/serializer row-local producer work.
- HOME owns shared command/session/door/outbox/core files and preview/player/
  render paths; none were edited.
- The current serializer-consumer-cut report says the three serializer
  consumers remain live and no deletion is safe. This slice therefore stages
  only a dormant producer seam and does not remove
  `serializeResolvedTimelineEdit` or any mutation variant.

## Verification

Passed:

```sh
TMPDIR=/tmp/ap2-m2-serializer-shader-native-vitest-cache \
  npx vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/shaderInspectorCapture.test.ts \
  src/tools/video-editor/components/ShaderInspector/ShaderInspector.test.tsx
```

Result: **2 files, 15 tests passed, exit 0**.

```sh
npx eslint \
  src/tools/video-editor/commands/shaderInspectorCapture.ts \
  src/tools/video-editor/commands/shaderInspectorCapture.test.ts \
  --max-warnings 0
```

Result: passed, exit 0.

```sh
git diff --check
```

Result: passed.

Not run: full suite, browser, localhost, socket, Runtime/Agent gate, or
preview/player/render qualification, as explicitly out of scope.

## Remaining blocker / next step

The row is not native-ready and the serializer consumer is not cut-ready. The
next step is an Agent-owned root-aware shader command contract and a paired
App capture/session seam that retains exact raw-root authority, followed by
the normal native acceptance/reload/inverse/retry proof. Only after that
qualification can ShaderInspector be wired away from the config mutation.
