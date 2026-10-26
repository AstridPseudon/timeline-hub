# U3/D141 independent source review

## Verdict

FAIL SOURCE. One proved upstream behavior regression requires owner return before normal merge: the App no longer swaps the live AgentChat panel for the scripted tour panel while the editor tour is running. This is separate from whole-cut readiness; generated manifest/vendor inputs are also still provisional.

## Substantive finding

`src/tools/video-editor/components/AgentChat/AgentChat.tsx:227-255` in the candidate calls `useAgentChatBridge`, checks only `isTimelineAgentSessionsAvailable`, and renders `AvailableAgentChatPanel`. It does not import `TourChatPanel` or `useEditorTourRunning`.

Frozen upstream `7ca61bb3280beca21d98a854af266a382f7ce5df` has the corresponding imports at lines 56-59 and the gate at lines 167-180:

```text
const tourRunning = useEditorTourRunning();
if (tourRunning) return <TourChatPanel isExpanded={isExpanded} />;
return <AvailableAgentChatPanel ... />;
```

The current-parent side of the automatic merge retained the newer unified `AgentChatMenu`/availability implementation but dropped this independent tour gate. That is not an intentional test replacement: the candidate retains `TourChatPanel.tsx` and its protected suite, and production `BrowserTourEditor` still mounts the scripted panel directly. The direct protected behavior test makes the loss observable: live session hooks were called during the tour, the scripted composer/transcript did not appear, and all 13 TourChatPanel tests failed.

## Predicate census review

The author census covered 15 affected files, 428 test declarations, and 1,495 static assertion statements, with no reviewer or author edits to test files. All 1,455 current-parent test paths and 1,322 frozen-upstream test paths were retained in the WIP. Exact-token differences were reviewed in one pass:

- Current-parent-only tokens absent from the WIP: `PaneControlTab.test.tsx` (the old `w-[10px]` grip assertion), `RuntimeConnectionPanel.test.tsx` (the two old responsive placement assertions), `TimelineEditorShellCore.test.tsx` (the seven old 420px/pane-band padding assertions), and `cardPlacement.test.ts` (the old bottom-dock top coordinate). These map to frozen-upstream source replacements: bottom-grip orientation, unified gate-layer placement, 360px/regular-padding shell geometry, and centered empty-card placement. They are intentional upstream replacements, not deleted live purpose.
- Frozen-upstream-only exact assertions: 11 in `AgentChat.test.tsx`. The five missing upstream titles are `does not auto-create when unengaged (pane unlocked, no markEngaged)`, `opens the new-chat menu on the chat's agent models from "Change model for new chats"`, `reports the header overlay open while the chat menu, the model line or the new-chat picker is open`, `starts a new chat with the open chat's agent from the + button`, and `starts the default agent from + with no model, so the service repeats its remembered model`. Source comparison shows these are superseded by the candidate's voice-aware engagement predicate and unified `AgentChatMenu`/model-picker architecture; the current tests preserve the corresponding live purpose under the new API. They are not evidence of equivalence by title alone, and the separate missing tour gate above is a real regression.
- `TourChatPanel.test.tsx` itself is retained and unchanged from the automatic WIP merge. Its 13 failures are therefore not an allowed weakening or an expected generated-file dependency.

No tests were skipped, deleted, weakened, or xfailed.

## Non-regressed source paths reviewed

The candidate's only changes from WIP4572 are the five conflict paths: manifest, TourChatPanel source, RemotionPreview source, position-keys vendor source, and vendor provenance. TourChatPanel retains the upstream reply/conversation spotlight grouping while retaining the current AgentChatMenu API. RemotionPreview retains both preview-revision delivery and the upstream playerControls/fullscreen transport union. The v2 persisted save path remains present: localSaveSession rebuilds base-pinned requests from the durable outbox; DataProvider calls generated `commitTimeline`; generated types retain commands, steps, reads, merge mode, accepted/merged/preview envelopes, structured conflict/invalid errors, receipts, dependencies, history, and undo steps. No legacy overwrite route was added by this resolution.

## Deferred generated qualification

The author evidence remains valid and is not a source pass: the manifest updater rejects observed Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` against lock source `ab1e4f6141987706132916e2da16477f5a019464`, and vendor verification reports mismatches for `am-footage/component.tsx` and `rendering/elements/catalog.ts`. These require qualified producer inputs and existing generation tools; no pins were invented.
