# Gate 6 existing native-port preflight

## Purpose and source of truth

This is a cheap, source-and-mounted-test preflight for the three remaining
automatic, popup, and public Trim proofs. It does not qualify a browser proof,
does not activate a dormant port, and does not add a hook, product flag, ready
state, selector, timeout, budget, or graph edge. The source base is the
integrated App tree at `1490fbfe9` (the automatic admission guard and dormant
popup port are already present).

The preflight must mount the existing command/provider assembly and inspect the
port that the trigger already owns. A missing port and a port method that
refuses are different results; retain that distinction. Do not infer either
one from a zero network request.

## Trigger map

| Proof | Actual trigger and caller | Assembly owner and real port | Existing observation | Cheap mounted preflight |
| --- | --- | --- | --- | --- |
| Automatic placement | The `Generate image` button in `EditorImageGeneration` opens `ImageGenerationModal`; the approved submit calls `timelinePlacement.prepare(...)`, then the prepared client submits the task. The caller identity is `session.imageGeneration` / `ImageGenerationPlacement`, with `ownerRef: occurrence:<id>` and an explicit lane. | `VideoEditorProvider` creates `RuntimeOperationHost`, binds it through `bindEditorImagePlacementHost`, and passes it through `useTimelineSave` → `useTimelineCommandSession` → `createTimelineCommandSession`. The native port is `imageGeneration`; its existing wake observers are `taskEventsReady` and `subscribe`. | The existing mounted UI test already observes `IMAGE_PLACEMENT_UNAVAILABLE` as `role=status`, and a refused preparation as `role=alert`. The existing real proof observes operation traffic and POSTs in `auto-real-proxy.spec.ts`. | Run the existing production binding fixture in `commitSession.placement.test.ts`: mount the real `RuntimeOperationHost`, bind the operation, call `session.imageGeneration.prepare({ ownerRef, lane, anchor })`, and verify the reservation precedes the task POST. Use `EditorImageGeneration.test.tsx` for the mounted modal/port gate. This is a preflight only; it is not the actual journey. |
| Popup ADD | No current App2 caller invokes native occurrence ADD. `AstridTravelRoute` renders `LocalTimelineShotBrowser`; `ShotTimelinePreview` mounts a nested `VideoEditorProvider`, but the popup path passes only `ShotTimelineMediaProvider`, not `occurrenceAddMedia`. Therefore the caller identity is **not available** in the current tree. | The dormant carrier is real: the nested `VideoEditorProvider` owns the command session, `useTimelineCommandSession` returns `occurrenceAddMediaPort`, `useTimelineState` forwards it as `editorOps.occurrenceAddMedia`, and the provider publishes it. The port contract is `capture({ ownerRef: occurrence:<id>, row, media, current })` → `finish(basis, verified)` → `submit({ command, preview })`; the command is `op: occurrence.add-media`. | `VideoEditorProvider.test.tsx` observes `data-testid="occurrence-add-media-port-state"` as mounted. `useTimelineCommandSession.test.tsx` observes the existing clean-save refusal and zero outbox commits. The popup route has DOM identity attributes for canonical occurrence/project/shot/revision, but no port readiness or caller observation. | Use the existing mounted `scoped()` command-session fixture and the existing provider port probe to establish carrier presence and refusal behavior. This cannot qualify ADD: until an App2 caller is wired, there is no trigger-to-port join to exercise. Do not treat the media provider’s `prepareMediaImport` or selection reads as the native ADD caller. |
| Public Trim | `ClipSourceWindowFields` is the real caller. On source-field focus/pointer/key/paste it calls `captureClipTrimEdit`; on the discrete value commit it calls `submitClipTrimEdit`. The command must be `op: clip.trim`, `select: parent/clip:<clipId>`. | The public `VideoEditorProvider` owns the command session; `useTimelineSave` creates `clipTrimPort` in `commitSession`, and `useTimelineState` forwards it as `editorOps.clipTrim`. The native write is the existing timeline commit port. | The existing public trace proves the click completed, local status became `dirty`, and no commit POST followed; its retained error context includes the non-GET trace and console/page-error checks. That observation proves “no commit request,” not whether the carrier was absent, stale, or refused. The parent trim observer in `parent-trim-command.spec.ts` retains commit POST body/key/status/response and legacy paths. | Use the existing mounted command-session fixture (`useTimelineCommandSession.test.tsx`’s `mounted()` helper) with the real `commands.clipTrimPort`; inspect the port before invoking the existing `captureClipTrimEdit`/`submitClipTrimEdit` path. A missing port, a synchronous guard error, and an enqueued `clip.trim` intent are three separate outcomes. No browser-visible readiness exists today, so this mounted check is the required preflight boundary. |

## Exact request and failure evidence to keep

For each trigger, retain one ordered record for every non-GET request, not only
the expected commit:

```text
method, pathname, idempotency-key, raw request body, response status,
raw/JSON response body (with credentials redacted), and request order
```

The automatic proof already supplies this split through `operation`, `requests`,
`responses`, `failures`, `pendingFailures`, and `auto-http-failures.json` in
`auto-real-proxy.spec.ts`. The expected non-GET sequence is the bound operation
request, `POST /v1/tasks`, and the final
`POST /v1/projects/<project>/timelines/<timeline>/commit`; task, managed-output,
and media-selection reads remain useful surrounding evidence but are GETs.
Keep the task POST body and idempotency key byte-for-byte with the durable
placement continuation.

For Trim and popup ADD, the native write is
`POST /v1/projects/<project>/timelines/<timeline>/commit`. Retain its exact
body, key, status, response, and the `legacy` path list. A zero commit POST is
evidence only when paired with the mounted port result.

After any failure, retain all of the following from the existing observers and
mounted surface:

- error-level console messages, `pageerror`, and `requestfailed` method/path/failure text;
- the visible error context: automatic `role=status`/`role=alert`, Trim’s source-field `role=alert`, or the popup caller’s existing context once a caller exists;
- the mounted port result: missing versus present, exact synchronous/asynchronous error text, and the owner identity (`occurrence:<id>` or `parent/clip:<id>`);
- the relevant outbox snapshot: owner id, pending request, intents, placement continuation, conflict/outcome, and whether any commit was enqueued;
- the canonical trigger identity already present in the DOM or fixture (project, timeline, occurrence/shot/revision, lane, clip id), without inventing a new diagnostic surface.

Interpretation is intentionally narrow:

* Automatic is preflight-ready only when the bound operation is current, the
  placement port prepares, and the durable reservation is visible before
  `POST /v1/tasks`.
* Popup is not preflight-ready for a proof: its carrier is mounted, but the
  current route has no native occurrence-ADD caller.
* Trim is not preflight-ready for a proof until the mounted check distinguishes
  an available `clipTrim` port and a refused capture/submit from the already
  observed zero-POST browser symptom.

---

## Bounded status note

Trim failclosed eb51 mergeddf4, seek e1c0 merged2b85, callerless popup999 integrated5ff, automatic02ac integrated1490; source proofs aren't browser proofs.

