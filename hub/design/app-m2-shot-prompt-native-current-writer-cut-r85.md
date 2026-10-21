# App M2 embedded shot prompt native writer cut

## Bounded D01 subrow

| Subrow | Old path | Replacement | Result |
| --- | --- | --- | --- |
| D01-app-shot-graph-settings/prompt | Embedded canonical prompt changes could fall through the settings snapshot writer after the form changed. | The existing occurrence-owned `shot.set` capture/session path receives prompt intent before the local draft update; the canonical save consumes the captured edit, and native refusal keeps the draft dirty and refuses publication. | **DELETED (bounded embedded prompt path)**. The parent D01 row remains **OPEN** for unsupported fields, standalone/catalog/manual-position writers, and the remaining generic settings writer. |

Base current source: `5f513665a6961e3552cf47bf70303fe41f370ba3` (`tl/integration`), tree `1c28244f9de4399070bc31772aef2d1a6cfca128`.

The exact eight-file prompt delta from current-preserving donor `dfb96f10` was ported. The five disjoint nonprompt files from the donor's second parent were not changed. Existing popup props, credential metadata, seek pairing, trim, parent fixtures, and type fixes remain on the integration base.

## Live caller impact

- `ShotEditorView` passes `onSettingsIntent` only for editable embedded canonical shots.
- `VideoTravelSettingsProvider` forwards the optional callback to `useVideoTravelSettingsHandlers`.
- `usePromptSettings().setPrompt` reaches `handleBatchVideoPromptChange`, which captures prompt intent before updating the local form draft.
- Successful prompt saves use existing `captureShotSettingsEdit`/`submitShotSettingsEdit` and return before `updateCanonicalShotSettings`.
- Capture refusal records the prompt refusal latch, keeps the local draft, and prevents a snapshot publication; noncanonical consumers retain their existing optional-callback behavior.

Unsupported/compound settings and standalone/catalog/manual-position writers were not migrated or deleted. The generic settings writer remains intentionally bounded to those paths pending their native replacements.

