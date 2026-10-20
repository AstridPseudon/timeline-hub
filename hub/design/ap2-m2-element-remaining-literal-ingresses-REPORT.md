# ap2-m2 element remaining literal ingresses — blocked report

## Result

No App source was changed. The requested bounded family was selected as the
literal transition apply/update/remove ingress in
`ElementsLibraryPanel`/`runtime/element-adapter.ts`. The exact required
native tuple was inspected before coding:

| peer | commit | tree |
| --- | --- | --- |
| Agent | `8130a401bf44a518d5a40ae274d398b8c560be55` | `236c3e57e0265c52b81ba8085de3193026176bff` |
| Runtime | `2c4ac180c2220bdad966bc01e95ad230e99ce26a` | `7ab412cc4bcbe517efcfa806e092336390312e18` |
| App Composition | public `0.0.13`, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |

The native registry has `clip.set-element`, `clip.set-params`, `clip.set`,
`clip.add`, `clip.delete`, and `track.create`. It has no native transition
SET/update operation. `clip.set` accepts `hold` writes and explicit clears,
including `transition`, but its closed `values` shape does not accept a
transition payload. `clip.set-element` only replaces an existing element
reference with the same element id/kind/owner and cannot clear the reference.

That surface cannot represent the current transition behavior without a
lossy cast or a fabricated command:

- apply writes the destination clip's exact `elementRef` and `transition`
  payload after same-track adjacency and duration-fit checks;
- update changes the destination `elementRef`, transition type/revision,
  duration, and optional params;
- remove clears both `transition` and `elementRef` from the destination clip.

The current implementation is at
`src/tools/video-editor/components/ElementsLibraryPanel.tsx:124-156` and
`src/tools/video-editor/runtime/element-adapter.ts:355-426`. The native Agent
implementation at `astrid/sdk/timeline/_clip_scalar_commands.py` confirms
that `clip.set-element` only writes `elementRef` after requiring an existing
reference, while `clip.set` has no transition SET shape. The published
Runtime schema at `tests/fixtures/published-command-schemas/agent-0a0ac7ba.json`
contains the same closed command definitions.

Using `clip.set-element` for transition apply/update would omit the authored
transition payload. Using `clip.set` clear for remove would leave the
`elementRef`. Using `clip.add`/`clip.delete` would create/remove a separate
overlay row and change Main behavior. All three are therefore rejected by
the settled rules.

## Exact peer prerequisite

Agent/Runtime must first publish and qualify an official native transition
recipe on the exact paired tuple (or an explicitly approved successor), with
no App-side command cast. The recipe must provide:

1. atomic apply/update of the destination clip's incoming transition and
   exact element identity/revision, with the existing adjacency, shortest
   clip, frame-duration, parent/occurrence ownership, and canonical incoming
   semantics;
2. atomic remove that clears the transition and its associated element
   reference together;
3. original accepted target/order/membership and read/selection/binding
   footprints, opaque-field preservation, and unchanged-write recording;
4. deterministic inverse, replay, and retry using the original command and
   guards; and
5. an exact Agent validation/execute record, bundle, inverse/replay golden
   plus matching Runtime generated schema/artifacts for Agent `8130a401`,
   Runtime `2c4ac180`, and App public13.

Once that prerequisite exists, App can route the existing panel operation
through the current session/outbox port, retain visible unsafe-input refusal
and draft preservation, then qualify mounted positive/refusal, exact retry,
guarded undo, native records/bundle/inverse/replay, and zero legacy traffic.
The transition adapter/provider and other element families remain open; no
ledger row was marked deleted.

## Verification

The focused existing App behavior lane passed unchanged:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs ./node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/runtime/element-adapter.test.ts src/tools/video-editor/components/ElementsLibraryPanel.test.tsx src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/elementOverlayCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

Result: **5 files, 99 tests passed**. The first equivalent invocation without
the repository's runner preload failed at config load because this config
uses `__dirname` under the runner loader; it did not modify the tree or
dependencies. No full suite, browser, localhost, socket, install, pin, or
shared dependency operation was run.

