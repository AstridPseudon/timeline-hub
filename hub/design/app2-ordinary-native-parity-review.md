# App ordinary native capture — current-root/native parity review

## Verdict

**REQUEST CHANGES for both the 281-line helper diff and the proposed shared
patch.** The helper's bounded behavior is supported by focused tests and a
native Agent probe, but it is not a current-root-applicable change. The shared
patch is not an applicable implementation and must not be approved or applied
wholesale.

## Identities and scope

- Candidate helper/test diff: `071e27d10090902b835657bfd75238b107c18174`
  (`tl/ap2-m2-ordinary-native-batch`), compared with old source base
  `55e7e217b4adc2c57315e22ce0bebfc36a436ffa`; exactly two added files and 281
  added lines.
- Current App reference root: `b1ef4b9b910ba72375c34cf319692f90d22edc25`.
- Proposed shared patch:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-m2-ordinary-native-batch-shared.patch`.
- Native acceptance used the read-only `agent-ordinary` archive from
  `ap2-m2-native-parity-environment` and `/home/user/work/venv-app2-native`.
  The fixed producer pair recorded by the source handoff is Agent
  `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` (tree
  `75354d38c898729bac09619679f5421faba319ed`) and Runtime
  `2c4ac180c2220bdad966bc01e95ad230e99ce26a` (tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`).

## What passed

The candidate's focused historical App lane passed:

```text
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism \
  src/tools/video-editor/commands/genericPatchCapture.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.test.ts \
  src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.test.ts \
  src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx \
  src/tools/video-editor/commands/commitSession.test.ts
```

Result: **6 files, 206 tests passed**.

The helper's mixed patch test proves the all-or-refuse boundary before owner
resolution: a patch containing supported label/hold operations plus
`project-data.write` raises `GenericPatchRefusal`, resolves no owner, and does
not execute a member. Its capture test also proves the original patch/bundle
are unchanged, owner references are stable, declaration order is sorted by
the public `order` field with input-index tie breaking, and one command list
is produced. The projection test proves an immutable local projection and
preserves unrelated display state/data-lane identity.

The exact TypeScript-produced mixed native command list was then serialized
from `captureGenericPatch` and checked by the frozen Agent implementation:

```text
node --import tsx -e "...document(); ...authoringBundleFromDocument(document());
  ...captureGenericPatch(...track.update order:2, clip.update order:1)..."
  > /tmp/ap2-ordinary-native-ts-produced.json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AG" \
  /home/user/work/venv-app2-native/bin/python - /tmp/ap2-ordinary-native-ts-produced.json
```

Result: both generated commands passed `validate_command`; native `execute`
passed atomically with ordinals `[0, 1]`, command order `clip.set -> track.set`,
and writes `parent/clip:x::hold` then `parent/track:V1::label`. The resulting
values were hold `1.23456789` and label `""`.

The direct native mixed-batch check also passed:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AG" \
  /home/user/work/venv-app2-native/bin/python -
```

It submitted a valid `track.set` followed by unsupported `project-data.write`;
native execution refused the batch and left the input bundle unchanged.

## Why approval is withheld

1. `git apply --check` of the proposed shared patch against an archive of
   current root `b1ef4b9b...` fails at `commitSession.ts`,
   `useTimelineCommandSession.ts`, and `useTimelineState.ts`.
2. Current root has no `src/tools/video-editor/commands/genericPatchCapture.ts`
   and no `clipScalarCapture.ts`; the candidate helper imports the latter at
   `genericPatchCapture.ts:4`. The old helper therefore cannot compile at the
   current root. This is the exact deleted dependency called out in the
   handoff, not a hypothetical concern.
3. The patch context assumes current-root APIs that are absent or reshaped,
   including `clipScalarPort` wiring. Applying the textual patch would require
   silently reconstructing an older session shape, which would violate the
   current-root requirement.
4. This is source/helper evidence only; it does not retire the live snapshot
   writer. `useTimelineOps` on current root still has the label special case
   and snapshot `commitData` path. No current-root writer migration was
   claimed here.

## Minimal repair required

Re-port the helper against current root, or narrow the change to an explicitly
current-root seam. The repair must provide a real current-root clip scalar
capture/execute implementation (or use an already-present current-root native
producer), update the actual `commitSession`/command-session/state APIs rather
than the stale patch context, and rerun the same focused lane. It must retain
the pre-resolution all-or-refuse check, stable owner binding, sequential
records, one `commands[]`/outbox intent, immutable projection, and exact retry
body/key. Do not copy `clipScalarCapture.ts` or the old shared patch wholesale,
and do not delete the remaining snapshot writers until all ordinary operation
families have native producers as required by the handoff.

## Not run / proof limits

- No full, browser, localhost, socket, e2e, package installation, dependency
  change, pin change, shared-environment mutation, or product edit was made.
- The passing Vitest lane runs against the candidate's historical dependency
  closure, not current root; it proves helper behavior, not integration.
- Native proof covers the generated track-label + positive-hold command pair
  and atomic refusal. It does not prove Runtime HTTP acceptance, outbox retry,
  current-root compilation, or live writer retirement.
