# M2 producer native-carrier source handoff

## Result

No existing Agent carrier covers the full live transcript/Scene producer
update. The smallest legitimate reuse is `clip.add` for a *fresh complete
parent clip row* only. It cannot carry the later regeneration/alignment update
through the current native path. `clip.set-params` is not a substitute: it
writes under `params`, not host clip fields, and must not be used to hide
ownership or provenance.

This is a source contract handoff only. No App production code, Agent source,
DTO, store, endpoint, pin, activation, browser, socket, or full-suite work was
done.

## Sources checked

- App ownership repair approved by safety review 0212: commit `9a5e9ed6c`,
  tree `d1483e3edfbc3b8b0db2615cb719c08c2902cc44`.
- Current committed Agent source: `tl/integration` commit
  `04fdd64205b4a2365e50455bd3ac81b027c617f3`, tree
  `88eb6b87ed41150a74f6f5da219d4f56f87d864d`.
- App integration under review: commit
  `692765846fef511047445fecef3e55ec8bb6a5bf`, tree
  `e615c0a3aafca34504ba3544560de3887e4de38d`.

## Exact live producer members

### Transcript caption regeneration

`buildTranscriptCaptionPatch` emits, per deterministic caption ID:

- optional `track.add`: `kind`, `label`, and optional `before`;
- new `clip.add`: `track`, `at`, `clipType: "text"`;
- `clip.update` with `track`, `at`, `hold`, `x`, `y`, `width`, `height`,
  `text` (`content`, `fontSize`, `color`, `bold`, `align`), `label`,
  `mode: "merge"`, and the host app payload
  `{ managedBy: extensionId, __generated__: generatedMeta }`;
- regenerate-only `clip.remove` for stale clips whose existing generated
  metadata identifies this extension/contribution and transcript schema.

`generatedMeta` is the existing host provenance object: extension and
contribution identity plus the versioned source/output fingerprints, source
schema/item/revision, generator version, and conflict policy. It is not a
generic clip parameter.

The repaired source keeps the existing behavior that an occupied deterministic
ID is updated only when it is owned by the active transcript extension. A
foreign-owned or user-authored same-ID clip is not targeted.

### Scene Phase Markers

Both fresh-shot builders emit, per shot:

- `clip.add`: `track`, `at`, `clipType: "hold"`, and existing
  `app.managedBy`;
- `clip.update`: `hold`, `label`, existing `app.managedBy`, and
  `mode: "merge"`.

The existing alignment builder emits only owned targets. A same-track batch is
`clip.move { at }` plus `clip.update { hold }`; a cross-track/unresolved batch
uses `clip.move { track, at }` plus `clip.update { hold, mode: "merge" }`.
Foreign-owned and user-authored clips are filtered before these operations are
constructed and remain byte-for-byte unchanged.

The approved `d148` controls prove fresh producer output -> existing compiler
-> serialized reload/reader -> second owned regeneration/alignment, while
preserving the protected clips. They do not claim the mounted route is
accepted.

## Current rejection point

In `src/tools/video-editor/commands/genericPatchCapture.ts`, the native
classifier accepts structural `clip.add`, exact hold-only `clip.update`, and
the `{ values, clear }` scalar shape. The transcript update and fresh Scene
update are neither shape. A producer batch containing the supported add and
one of those updates is therefore `mixed`.

`useTimelineOps` sends every non-`unsupported` classification to the generic
capture port. `captureGenericPatch` rejects the unsupported member before
owner resolution or command submission; `GenericPatchRefusal` reports every
member, including “Not submitted because another patch member was refused”.
The batch does not fall through to the snapshot writer. This is the required
draft-preserving whole-batch refusal.

The existing compiler can preserve arbitrary `clip.update` fields, including
`app`, but that does not create a corresponding Agent command. The current
Agent registry has `clip.add`, `clip.set`, `clip.set-params`,
`clip.set-element`, `clip.move`, and related commands; it has no host-field
`clip.update` command.

## Existing Agent carrier fit

- `clip.add@1` is a parent-owned complete literal row requiring `id`,
  `clipType`, `track`, `at`, and `hold`. Its schema permits additional JSON,
  so `text`, `label`, and `app` can be carried on a fresh row. This is the only
  real fit, and only for creation if the producer supplies the complete row.
- `clip.set@1` permits only `values.hold` and clears for `hold`, `asset`, or
  `transition`. It cannot write `managedBy`, `__generated__`, `text`, label,
  geometry, or the producer's host update payload.
- `clip.set-params@1` explicitly writes top-level keys below `clip.params`.
  It cannot represent host ownership/provenance and is forbidden as a
  provenance disguise.
- `clip.set-element@1` changes an existing element reference only; `clip.move`
  moves timing only. Neither carries the missing host fields.

Therefore there is no honest existing carrier for transcript regeneration or
Scene alignment updates. The concrete gap is source-owned Agent support for
the exact host-field update set above, with no guessed wire shape. The fresh
row portion may reuse `clip.add`; it must not be presented as coverage of the
update portion.

## Executable source witness

This was run against the current committed Agent source with no source edits:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/agent \
  /home/user/work/venv-app2-native/bin/python - <<'PY'
from astrid.sdk.timeline.commands import CommandError, validate_command

command = {
    'schema_version': 1, 'op': 'clip.set', 'version': '1',
    'select': 'parent/clip:caption-1',
    'args': {'values': {
        'app': {'managedBy': 'transcript-lane', '__generated__': {'extensionId': 'transcript-lane'}},
        'text': {'content': 'hello'}, 'label': 'hello',
    }, 'clear': []},
}
try:
    validate_command(command)
except CommandError as exc:
    print('REFUSED:', exc)
PY
```

Observed:

```text
REFUSED: Additional properties are not allowed ('app', 'label', 'text' were unexpected)
```

The same witness also validated a full-row `clip.add` carrying `app`, `text`,
and `label`, confirming the narrow creation-only fit. It did not claim command
execution because that additionally requires a real active output track.

## Contract request ready for Agent

> **Agent source request — M2 transcript/Scene producer carrier**
>
> Please review the current `clip.add`/`clip.set`/`clip.set-params` carriers
> against the live producer batches. Confirm the bounded mapping for a fresh
> complete parent row through existing `clip.add` (including literal `hold`,
> `text`/label/geometry where present, and `app.managedBy` plus transcript
> `__generated__`), or return **NO-FIT** for that portion if the current
> capture path cannot preserve it. Separately, return **NO-FIT** for the
> existing-clip update portion unless an existing carrier genuinely records
> these exact host fields: transcript `text`, label, geometry, timing,
> `managedBy`, and `__generated__`; Scene `hold`, label, and `managedBy`.
> Do not use `clip.set-params` to carry host ownership/provenance and do not
> invent an unreviewed operation or wire field. Any accepted mapping must
> preserve deterministic IDs, record the ownership/provenance reads and
> writes, survive reload, and permit exactly the second owned regenerate or
> alignment. Foreign-owned and user-authored targets must be excluded and
> remain byte-for-byte unchanged. If any member is unsupported or ambiguous,
> refuse the whole batch before capture/submit and leave the App draft intact.
> Return the exact source files, schema/registry identity, and a focused
> executable refusal/positive witness; this is a source contract only, not
> App activation or a public pin.

## Callers and evidence

No caller implementation changed in this handoff. The affected live callers
remain:

- `renderTranscriptAsCaptions` -> `buildTranscriptCaptionPatch`;
- `createShotsFromMarkers` -> `buildCreateShotsPatch` or
  `buildCreateEmptyShotsPatch`;
- `moveExistingShotsToMarkers` / `alignShotsToTransitions` /
  `ScenePhaseMarkersPanel` -> `buildAlignShotsPatch`.

Reused approved focused evidence (not repeated here): the exact repaired
source run covered 8 files and **494 tests passed**, plus targeted ESLint and
`git diff --check`. No browser, localhost, Runtime socket, activation, or full
suite was run. The current route remains unqualified until a compatible
source carrier exists and the normal mounted route proves accepted revision,
reload, retry identity, second owned action, and protected foreign/user
preservation.

The exact approved focused request was:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-ownership-active-route-repair-0210 targeted --files "src/tools/video-editor/dev/transcript-lane/__tests__/transcriptLane.test.tsx src/tools/video-editor/dev/transcript-lane/__tests__/fixtureProvider.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/ScenePhaseMarkersOverlay.test.tsx src/tools/video-editor/dev/scene-phase-markers/__tests__/panel-transition.test.tsx src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/lib/timeline-reader.test.ts src/tools/video-editor/lib/managed-object-guard.test.ts"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-producer-ownership-active-route-repair-0210-targeted-1021021546-4131
```

Result: **8 files, 494 tests passed**. This result belongs to the approved
`d148` source candidate and was not rerun as a broad repeat in this handoff.
The only command executed for this handoff was the local Agent validator
witness above; it exited successfully after printing the expected refusal and
creation-only schema acceptance.
