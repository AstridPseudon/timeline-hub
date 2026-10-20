# App2 element native repair evidence

Date: 2026-10-20
Agent source: frozen `agent-ordinary` at Agent 310e5484, from `app2-native-parity-environment.md`.

## Source repair

- Removed the copied scalar read loop from `commands/elementCapture.ts`.
- Read both `elementRef` and `element_ref` explicitly, matching the native handler even when the first alias is present.
- Removed the local selected-pack PARAM/element schema synthesis. Selected project-pack element and PARAM capture now refuse with `selected project pack capture requires authoritative Agent schema capture`; the input bundle is not mutated and no basis/command is returned.
- Literal element and PARAM capture paths remain unchanged in behavior, including opaque fields.

## App tests

Command:

```sh
node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts \
  --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/elementCapture.test.ts \
  src/tools/video-editor/commands/clipParamsCapture.test.ts
```

Result: **2 files, 135 tests passed**.

## Native exact-command probe

The probe loaded the existing frozen native fixture
`tests/editing_conformance/fixtures/recipe_m2_clip_set_element.json`, used its
bundle and target, removed only the selected-pack `packId` and
`schema_source` to exercise the bounded literal path, then generated the
command and record with the repaired TS producer. That exact TS-produced
command was submitted unchanged to Agent `validate_command` and `execute`.

Command shape submitted:

```json
{
  "schema_version": 1,
  "op": "clip.set-element",
  "version": "1",
  "select": "occurrence:occ-1/clip:picture-1",
  "args": {
    "elementRef": {
      "id": "reveal",
      "kind": "effect",
      "revision": "sha256:f29d84a00776ffaa8578fbbb80f7654ee34b83c763162c265811180d99ded4bd"
    }
  },
  "intent": {},
  "resolved": ["occurrence:occ-1/clip:picture-1"],
  "reads": [
    {"ref": "occurrence:occ-1/clip:picture-1", "path": ["id"]},
    {"ref": "occurrence:occ-1", "path": ["occurrence_id"]},
    {"ref": "occurrence:occ-1/shot", "path": ["shot_id"]},
    {"ref": "occurrence:occ-1/clip:picture-1", "path": ["elementRef"]},
    {"ref": "occurrence:occ-1/clip:picture-1", "path": ["element_ref"]}
  ],
  "selections": [],
  "bindings": {
    "scalar.owner": "occurrence:occ-1",
    "scalar.target": "occurrence:occ-1/clip:picture-1"
  },
  "created": [],
  "expect": {
    "occurrence:occ-1/clip:picture-1::elementRef": {
      "state": "present",
      "value": {"id": "reveal", "kind": "effect", "revision": "draft-reveal"}
    }
  },
  "authorship": {"occurrence:occ-1/clip:picture-1::elementRef": "direct"}
}
```

Probe command:

```sh
node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs \
  /tmp/element-native-probe.ts |
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary \
/home/user/work/venv-app2-native/bin/python -c '...native validate_command/execute and deep comparisons...'
```

Result:

```text
validate: accepted
execute: accepted
command_exact: true
record_exact: true
bundle_exact: true
```

The native and TS read paths were identical, in this order:
`clip.id`, `occurrence.occurrence_id`, `occurrence/shot.shot_id`,
`clip.elementRef`, `clip.element_ref`. This is native acceptance and deep
field parity, not TS self-consistency only.

Native recipe command:

```sh
PYTHONPATH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary \
/home/user/work/venv-app2-native/bin/python -m pytest -q -c /dev/null -p no:cacheprovider \
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary/tests/editing_conformance/test_recipe_clip_set_element.py
```

Result: **30 passed in 1.81s**.

No full, browser, socket, Runtime, or live authenticated App suite was run.
