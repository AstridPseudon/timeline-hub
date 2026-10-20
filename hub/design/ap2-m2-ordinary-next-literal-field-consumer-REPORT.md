# AP2 M2 ordinary next literal field consumer

Status: **blocked on the existing Agent/Runtime carrier contract; no App source change made.**

## Scoped family

The one family inspected was `track.update.muted` (ordinary track mute). This is
the smallest remaining literal field with a direct Main compiler behavior and a
clear semantic boundary. Existing label/hold/move/trim/structural producers were
not changed.

## Current Main behavior

The live entry is `useTimelineOps.apply`, used by extension/proposal patch
acceptance. `track.update` is validated and compiled by
`src/tools/video-editor/lib/timeline-patch.ts`:

- merge `{ muted: true|false }` changes only the top-level authored
  `track.muted` field and preserves other fields;
- replace `{ muted: true }` starts from the structural `id/kind/label` base,
  so omitted mutable fields such as `opacity`, `volume`, `role`, `app`, and
  unknown authored siblings are removed;
- there is no track-level `clear` member in the public `TimelinePatch`
  operation shape. Treating replace as a mute clear would therefore drop
  unrelated authored state.

The current native classifier admits label-only track updates and the already
qualified ordinary clip families. `track.update { muted }` remains unsupported,
so the existing snapshot producer remains reachable. Mixed supported/unsupported
batches continue to refuse atomically before owner resolution in the native
path; that behavior must stay until this family has a matched carrier.

## Exact carrier finding

The exact current Agent 8130 schema has `TrackSetArgs.values` containing only
`label`, with `clear` containing only `label`. Exact Runtime 2c4 generated
contract types carry the same restriction. The existing `track.set` carrier
therefore cannot represent top-level `track.muted`.

`clip.set-params` is not a substitute: it writes `clip.params.*`, targets clips,
and cannot preserve the meaning of a top-level track mute. Mapping mute to an
opaque params key or a snapshot diff would silently change semantics.

## Concrete Agent/Runtime peer contract request

Extend the **existing** `track.set` carrier only; do not add an operation, DTO,
endpoint, or App-side no-op. The bounded field is exactly top-level authored
`track.muted`.

Accepted native command forms should be:

```json
{
  "schema_version": 1,
  "op": "track.set",
  "version": "1",
  "select": "parent/track:<raw-id>",
  "args": {"values": {"muted": true}, "clear": []},
  "intent": {}
}
```

and the explicit clear form:

```json
{"values": {}, "clear": ["muted"]}
```

The existing label forms and their behavior must remain unchanged. Reject
set/clear overlap, duplicate clears, unknown fields, non-boolean values, and
non-empty intent. App admission should accept only a merge-mode
`track.update` carrying the boolean `muted` member until a public existing
clear representation is specified; it must not reinterpret `mode: replace` as
a mute-only clear because Main replace has broader destructive semantics.

Required capture and acceptance semantics:

| Item | Required contract |
| --- | --- |
| Before | Read the stable `parent/track:<raw-id>` identity and the exact raw `muted` state (`absent` or present boolean). Preserve the existing parent source dependency and target binding used by `track.set`. |
| Declared intent | `{}`. No ripple, ownership, follow, or inferred track selection. The App adapter resolves the displayed track to one stable parent-track identity before capture. |
| After set | Same raw track object except `muted: true` or `muted: false`. |
| After clear | Same raw track object with only `muted` absent. |
| Read guards | Stable target identity, captured before-state at `track.muted`, the existing parent source pin, and the existing target binding. A changed target or before value refuses visibly. |
| Opaque preservation | `label`, `kind`, `role`, `opacity`, `volume`, `app`, unknown keys, and all parent config/track siblings survive byte-for-byte. Do not replace or normalize the track object. |
| Retry/undo | Use the existing `track.set` records, expectations, inverse, replay, and one-command batch/outbox path. A mixed batch remains all-or-refuse. |

Runtime 2c4 must publish the matching generated schema/client acceptance for
this extension of the existing carrier before App adoption. Until that paired
contract exists, this App worker should not add a producer/member for mute.

## Evidence

Focused current-App neighbors:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/lib/timeline-patch.test.ts \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts
=> 3 files, 359 tests passed
```

Source inspection was read-only against App `e245a4791`, Agent 8130 source/schema,
and Runtime 2c4 generated contracts. No full, browser, socket, Runtime HTTP,
dependency, pin, or Git operation was run. A standalone `tsx` classification
probe was not usable because the shared Composition install lacks the currently
imported `computeMediaTrim` export; this did not modify the worktree or shared
dependencies. Classification was verified from the existing classifier source
and the passing generic-patch tests instead.

The App worktree remains clean. No commit is proposed for product code; this
report is the handoff requested by the missing official carrier.
