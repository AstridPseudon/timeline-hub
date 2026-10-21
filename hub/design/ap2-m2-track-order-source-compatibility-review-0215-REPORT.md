# App2 M2 track-order source compatibility review

## Disposition

**Bounded SOURCE ACK for the media-only parent track reorder shape.** The
committed Agent source recipe matches App2's existing media-only serializer
consumer. This ACK covers source compatibility only; it does not authorize
App activation, Runtime qualification, generation, pinning, freezing, fallback
deletion, or a lane-order migration.

## Exact Agent source reviewed

I reviewed the immutable synced Agent ref
`remotes/hub/timeline/agent/tl/agt-m2-track-order-restart-finish` (also
`hub/timeline/agent/tl/agt-m2-track-order-restart-finish`), not a dirty
checkout:

- commit: `c1ae9e93d31c1c091b93c952ae803059a890bf61`
- tree: `a54be6e2269e191c032496b3b73cfcf761d7402e`
- parent source recipe commit: `a8604a8ca0619ccb4702b8709be3af5885f36ace`
- schema blob: `c0c28e55349493bf26b999b6052c97518c7e1549`
- schema: `astrid/core/timeline/schema/edit-command.schema.json`, draft
  2020-12; operation `track.reorder`, version `1`, `select: "parent"`

The schema requires `args.order` and `args.expected_order`, each a unique
array of `parent/track:<id>` references, with no extra arguments. The handler
uses the existing ordered-collection primitives and writes only the virtual
`parent::track_order` address; no `track_order` persistence leaf is created.

## Contract checks

| Requirement | Result |
|---|---|
| Complete raw parent permutation plus `expected_order` | Pass. Capture selects `collection.tracks`; execution requires the current order to equal `expected_order`, then checks equal length, unique membership, same-owner identity, and complete permutation before arranging rows. |
| Raw row, null/false/zero, opaque, clips, root/config retention | Pass. `arrange()` reorders existing raw rows without rebuilding them. The committed conformance fixture asserts exact reordered rows and preserves null, false, zero, opaque data, clips, parent siblings, and `config.app.timelineDataLanePlacement`. |
| Serialized reload, inverse, redo | Pass. The focused test JSON-reloads the bundle and record, replays, inverses, and re-inverses to the exact prior bundle. |
| Disjoint label rebase | Pass. A `track.set` label edit rebases across the reorder and retains both the label and final order. |
| Changed-order and identity refusal | Pass. A stale order and an identity rename refuse before writing. |
| Strict changed-order / ABA refusal | Pass. The test rejects both direct intervening order writes and a real away-then-back `A -> B -> A` recorded history. |
| Lane shape | Pass, bounded. Extra `lanes` arguments are refused by the command schema and focused test. This is correct: App's lane branch also writes `config.app.timelineDataLanePlacement` and must remain outside this media-only command atomically. |

## App2 consumer mapping

The reviewed App integration tree is `692765846fef511047445fecef3e55ec8bb6a5bf`
(tree `e615c0a3aafca34504ba3544560de3887e4de38d`). In
`src/tools/video-editor/hooks/useTimelineTrackManagement.ts`, the
`handleMoveTrack` branch with no `lanes` computes a new
`resolvedConfig.tracks` array and sends the existing `type: 'config'` mutation.
The existing commit serializer then routes this through
`serializeResolvedTimelineEdit` -> `serializeForDisk`, which preserves the
track array order and existing track payload fields. No new persisted field,
store, Runtime DTO, or endpoint is needed to carry the Agent command.

The smallest future App adapter is row-local and should use the already
available command-session/outbox seam:

1. Verify the displayed/raw parent basis and capture
   `expected_order = current.resolvedConfig.tracks.map(track =>
   \`parent/track:${track.id}\`)`.
2. Apply the existing media-only `moveTrackWithinKind` result and emit the
   corresponding complete `order` array with `track.reorder@1`.
3. Submit that command through the existing session/outbox and retain the
   current serializer until command-consumer proof is complete.
4. Refuse native capture for any lane-bearing invocation (including a mixed
   track/data-lane reorder); leave the existing atomic lane serializer path
   intact until a separate carrier covers both authored collections.

This is an adapter around the current handler, not a new DTO/store/API. The
current App source has no reorder-specific command port yet, so activation
still requires that small App-owned adapter and its command-session preview /
recovery proof; no activation is claimed by this review.

## Evidence

- Exact committed Agent source, extracted without checkout, focused test:

  ```text
  PYTHONPATH="$TMP/src:/home/user/work/runtime" \
    /home/user/work/venv-app2-native/bin/python -m pytest -q \
    "$TMP/src/tests/editing_conformance/test_recipe_track_order.py"
  ```

  Result: **3 passed**, exit 0. Pytest emitted two existing unknown-config
  warnings for `timeout` and `timeout_method`; no test was skipped or weakened.

- App focused source controls:

  ```text
  node_modules/.bin/vitest run --no-cache \
    --config config/testing/vitest.config.ts --maxWorkers=1 \
    --no-file-parallelism \
    src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts \
    src/tools/video-editor/commands/genericPatchCapture.test.ts
  ```

  Result: **2 files, 46 tests passed**, exit 0.

No full suite, browser journey, Runtime live/provider test, generated artifact
qualification, or retry/idempotent acceptance test was run. Those remain
required before any App activation or pin/freeze decision.

## Worktree changes

No App production files were edited. This review produced only this report,
the requested commit-message file, and the completion marker.
