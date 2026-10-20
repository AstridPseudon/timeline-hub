# Mounted test handoff

The test patch adds two focused cases to the existing App suites:

- `canonicalRenderBounds.test.ts` proves `storedOccurrenceDurationMs` is used only by the private stored-cap copy, while the source editor clip remains at effective 5000ms.
- `useVideoEditorPreviewSurface.lifecycle.test.tsx` mounts the actual preview hooks and Player boundary. It proves 4000ms gives hold 4, fade opacity 0.5 at frame 105, and end frame 120; 4500ms gives hold 4.5, fade opacity 1 at frame 105, and end frame 135. It also observes the compiled transition vector, Player extent, private config identity, original editor values, local/saving/accepted labels, and the late-A acknowledgement race.

Existing command projection, mailbox, and render-state tests are included in the command and were rerun unchanged.

This is candidate evidence only. The App producer that supplies the approved scalar is still pending; these tests do not certify that producer or a production merge.
