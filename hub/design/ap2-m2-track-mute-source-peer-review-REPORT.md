# AP2 M2 track mute private source review

Disposition: **ACK — bounded Agent source only.** No source mismatch was found
for Agent `45201ef4fdb330635ed99035f6eded65f07f88b4` and schema
`6826fc7d8cec337f6c015db21b0a223ec4a438a18204e4e07f6fca91f594c0b7`.

This ACK is not generation, pin adoption, Runtime/App activation, or approval
to replace `full392`/`public013`. No product files, wire/endpoint/provider/
store, public artifact, or dependency was changed.

## Findings

- Main `track.update` accepts boolean `muted` in merge mode and changes only
  that supplied leaf; an absent authored leaf remains absent. Main rejects a
  new `null`. Main replace mode reconstructs the track from structural fields
  and clears mutable siblings, so it is not a mute-clear operation. The
  current public `TimelinePatchOperation.clear` only names clip leaves; there
  is no public track clear.
- The candidate extends the existing closed `track.set` carrier only. Its
  schema accepts raw boolean `values.muted` and explicit `clear: ["muted"]`,
  while rejecting null/non-boolean values, unknown fields, overlap, duplicate
  clears, and non-empty intent. `track_set` calls the existing leaf
  write/clear recorder; it does not replace the track row.
- Capture records the exact raw `muted` state (`absent` or present value) in
  `expect`/`writes` and preserves same-value writes and explicit clears. The
  target is the stable `parent/track:<id>` or
  `occurrence:<id>/track:<id>` identity. Parent capture pins `base_parent`;
  occurrence capture additionally reads/binds the occurrence and shot/source
  owner. The existing fixed `scalar.target`/`scalar.owner` bindings remain in
  force.
- Existing inverse/replay machinery is applicable without a new path: leaf
  writes carry before/after tagged states, same-property intervening writes
  and A→B→A are guarded, while a disjoint label write can replay. The
  candidate’s focused tests cover exact presence/inverse, stale same-property
  refusal, disjoint label replay, occurrence owner binding, closed args, and
  opaque sibling preservation. Existing track-set/label conformance covers
  ABA undo, exact replay, identity ambiguity, ordering, and label behavior.
- Existing label set/clear forms remain accepted and their handler is
  unchanged apart from the intended schema extension. Raw leaf mutation also
  preserves label/kind/role/opacity/volume/app/unknown siblings and track
  collection order; no destructive replace interpretation is introduced.

## App boundary for any later consumer

The current App native carrier and `trackLabelCapture` remain label-only, and
the current generic classifier still admits only parent label-only merge for
`track.update`. That is correct for this source-only review. A future paired
consumer may emit only a merge-shaped boolean mute set through the generated
matching Runtime/Agent contract. It must not reinterpret App `mode: "replace"`
as mute clear. Native clear may be exposed only when the consumer explicitly
represents clear; broader destructive replacement stays unsupported unless
all affected fields are represented and guarded.

Future Composition work must retain the agreed floors: raw absence versus
`false`, exact owner/track binding, label compatibility, opaque/order
preservation, and guarded inverse/rebase behavior.

## Evidence

- Candidate inspection via frozen ref: only the schema, `_scalar_commands.py`,
  and the new focused test file changed; `git diff --check` passed. Candidate
  schema hash verified as `6826fc7d8cec337f6c015db21b0a223ec4a438a18204e4e07f6fca91f594c0b7`;
  scalar source hash verified as
  `84b09f7fa0a0a6ae824bc64ca4e8e7e54ae4cce5e73e759bfcfff1cb231cea91`.
- Decisive App controls (unchanged source tree):

  ```text
  node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
    src/tools/video-editor/lib/timeline-patch.test.ts \
    src/tools/video-editor/commands/genericPatchCapture.test.ts \
    src/tools/video-editor/hooks/useTimelineOps.test.ts
  => 3 files passed, 362 tests passed
  ```

- Agent focused tests were inspected but not executed: the Agent candidate is
  frozen in another repository and no private copy was made. No full,
  browser, socket, Runtime, generation, dependency, or public/private pin
  suite was run.

