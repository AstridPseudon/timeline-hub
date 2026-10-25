# Validation and decision

## Exact source inventory

The 14 selected nodes are the exact `managed_edge_fixture` rows from the reviewed D134 partition: four video-unplace parameterizations, six M2 auto-placement provider/replay parameterizations, and four M2 placement create/unplace provider/replay nodes. The current source bytes, AST hashes, and canonical fixture-input hashes are recorded in `source-manifest.json`.

The authored input includes:

- parent occurrences `occ-a` and `occ-b`, with `occ-a` at 8000 ms for 10000 ms and `occ-b` at 10000 ms for 10000 ms;
- the source shot's existing item `item-1`, its exact old media ID, `opaque_literal`, text binding, metadata and unknown fields;
- internal clips at `[1,3)` and `[5,7)`; for video, source window `[2,6]`, hold 4, speed 2;
- the exact image/video selection and verified-media records used by the callers;
- all original capture, inverse, retry, no-write, refusal and sibling/parent preservation predicates.

No authored value, root, topology, media identity, opaque field, pin, CLI/input, inverse input or assertion was changed.

## Caller and guard trace

The three files reach Runtime through `commit_timeline`/`commitTimeline` and use the Agent registered provider. Their setup currently uses a whole-shot `doc.patch` after a semantic birth. C0/R1 rejects that patch because changing shot item correspondence is a managed closure edge. The registered alternatives do not provide an equivalent:

- `occurrence.create` creates the occurrence and an empty shot;
- `shot.set` is limited to name/settings;
- `occurrence.add-media` creates a clip and registry binding but does not create shot items;
- `placement.create`/`placement.unplace` operate on occurrence-owned clips;
- `media.admit` only authenticates media inputs.

Therefore a replacement would necessarily omit `item-1`, invent history/allocation, or rewrite authored topology. Each violates the task's preservation rule. The exact outcome is `UNAPPLIED`, not a fake fixture or a guard workaround.

## D104

The five D104 conditions are mapped in `predicate-map.json`. Conditions 1 and 3 are evidenced; condition 2 describes the intended setup-only boundary but cannot be completed; condition 4 prevents changing the shared `inputs()` seed without a broader caller audit; condition 5 is not met because no supported migration exists and no protected review/meaningful proof was run.

## Scope controls

Only read-only inspection and static validation were performed. No pytest integration body, full suite, localhost/browser/socket run, fresh measurement, product/shared-fixture/Runtime/schema/pin/generated/seed change, retirement, REG closure, or behavior/core credit was attempted.
