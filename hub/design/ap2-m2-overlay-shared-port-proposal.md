# M2 literal overlay shared-port proposal

This is an unapplied, four-file maximum proposal. It consumes the approved
literal existing-element session port; it does not create a second store,
framework, generic command submit API, DTO, serializer, or direct Runtime
POST. The App Provider's automatic-host join remains App-owned.

## 1. `src/tools/video-editor/commands/elementGesture.ts`

Add beside the existing literal `ElementCapturePort` types:

```ts
import type { TimelineData } from '../lib/timeline-data.ts';
import type { TimelinePatch } from '@/sdk/video/timeline/patch.ts';
import type { EditCommand, JSON } from '@/integrations/runtime/timeline-commit-types.ts';
import type { AuthoredBundle } from './clipMovePrimitives.ts';
import type { OutboxBasis } from './commitOutbox.ts';

export type ElementOverlayOperation =
  | { kind: 'create'; row: Record<string, JSON>; track?: Record<string, JSON> }
  | { kind: 'delete'; select: string };

export type ElementOverlayCaptureBasis = {
  readonly operation: ElementOverlayOperation;
  readonly bundle: AuthoredBundle;
  readonly commands: readonly EditCommand[];
  readonly localGeneration: number;
  readonly localBasis: OutboxBasis;
  readonly previewVersion: number;
};

export type PreparedElementOverlay = {
  commands: EditCommand[];
  preview: TimelinePatch;
};

export interface ElementOverlayCapturePort {
  capture(input: { current: TimelineData; operation: ElementOverlayOperation }): ElementOverlayCaptureBasis;
  finish(basis: ElementOverlayCaptureBasis): PreparedElementOverlay;
  submit(input: PreparedElementOverlay): void;
}
```

Add `elementOverlay: ElementOverlayCapturePort` to the existing
`ElementCapturePort`/session surface (or, if the literal port is already a
composite surface, add it as its one nested member). Do not create another
context or store.

## 2. `src/tools/video-editor/commands/commitSession.ts`

Import the approved helper and the types above:

```ts
import {
  captureElementOverlay,
  captureElementOverlayDelete,
  finishElementOverlay,
} from './elementOverlayCapture.ts';
import type {
  ElementOverlayCaptureBasis,
  ElementOverlayCapturePort,
  ElementOverlayOperation,
  PreparedElementOverlay,
} from './elementGesture.ts';
```

Add this beside the existing literal element port, reusing the same `bundle`,
`known`, `displayHead`, `localGeneration`, `lastIntent`, `prepared`,
`assertReady`, and `enqueue` closures:

```ts
const elementOverlay: ElementOverlayCapturePort = {
  capture({ current, operation }) {
    assertReady();
    if (current.head?.projectId !== options.scope.projectId
      || current.head.timelineId !== options.scope.timelineId
      || current.head.headRevisionId !== displayHead.revisionId
      || current.head.headPublicationId !== displayHead.publicationId) {
      throw new Error('Displayed timeline does not match the raw authoring basis');
    }
    const captured = operation.kind === 'create'
      ? captureElementOverlay(bundle, { row: operation.row, track: operation.track })
      : captureElementOverlayDelete(bundle, operation.select);
    return Object.freeze({
      operation: copy(operation),
      bundle: captured.bundle,
      commands: captured.commands,
      localGeneration,
      localBasis: lastIntent ? { after: lastIntent } : { head: copy(known.head) },
      previewVersion: current.configVersion,
    });
  },
  finish(basis) {
    assertReady();
    if (basis.localGeneration !== localGeneration) {
      throw new Error('Timeline changed during the element overlay edit');
    }
    const result = finishElementOverlay(basis);
    const preview: TimelinePatch = {
      version: basis.previewVersion,
      source: 'timeline.native-element-overlay',
      operations: result.commands.map((command) => command.op === 'track.create'
        ? { op: 'track.add', target: String((command.args as { row: { id: string } }).row.id),
            payload: copy((command.args as { row: Record<string, JSON> }).row) }
        : command.op === 'clip.add'
          ? { op: 'clip.add', target: String((command.args as { row: { id: string } }).row.id),
              payload: copy((command.args as { row: Record<string, JSON> }).row) }
          : { op: 'clip.remove', target: command.select ?? '' }),
    };
    const preparedOverlay: PreparedElementOverlay = {
      commands: result.commands,
      preview,
    };
    prepared.set(JSON.stringify(result.commands), {
      payload: { commands: result.commands, before: basis.bundle, after: result.bundle, preview },
      generation: localGeneration,
      basis: basis.localBasis,
    });
    return preparedOverlay;
  },
  submit(input) {
    assertReady();
    const key = JSON.stringify(input.commands);
    const entry = prepared.get(key);
    if (!entry || entry.generation !== localGeneration || entry.payload.before !== bundle
      || !equal(input.preview, entry.payload.preview)) {
      throw new Error('Element overlay was not captured by this session or the timeline changed');
    }
    prepared.delete(key);
    enqueue({ ...entry.payload, preview: input.preview }, input.preview, entry.basis);
  },
};
```

The actual implementation must preserve the existing `prepared` payload's
`displayBasis` handling if the literal element port has already factored that
field into its helper. `track.create` and `clip.add` remain one grouped intent.

Return `elementOverlay` from `createTimelineCommandSession` beside the existing
`port` and `trackLabelPort`.

## 3. `src/tools/video-editor/hooks/useTimelineCommandSession.ts`

Apply the same legacy-clean barrier as the literal element port:

```ts
const overlayPort = session.elementOverlay;
session.elementOverlay = {
  capture(input) {
    if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element overlay');
    return overlayPort.capture(input);
  },
  finish(basis) {
    if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element overlay');
    return overlayPort.finish(basis);
  },
  submit(input) {
    if (!latest.current.legacyClean()) throw new Error('Wait for earlier timeline saves before editing an element overlay');
    overlayPort.submit(input);
  },
};
```

Expose the same property from the hook and include it in
`TimelineCommandSessionSurface`. Recovery remains the existing outbox replay;
it must not recapture from the acknowledgement/display projection.

## 4. `src/tools/video-editor/hooks/useTimelineState.ts`

Expose the port through the already-existing chrome command-session object:

```ts
commandSession: save.commands.enabled ? {
  state: save.commands.state,
  retry: save.commands.retry,
  recover: save.commands.recover,
  useLatest: save.commands.useLatest,
  keepLabelChanges: save.commands.keepLabelChanges,
  elementOverlay: save.commands.elementOverlay,
} : undefined,
```

`ElementsLibraryPanel` and the selected-clip delete callback read this through
`useTimelineChromeContextSafe()`. This avoids any Provider automatic-host
construction change. App applies the existing Provider join only if its current
branch requires forwarding the already-existing chrome surface.
