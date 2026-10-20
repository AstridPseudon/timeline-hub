# Selected PARAM original-pin review

## Verdict: REQUESTCHANGES

The `89bb04462` read bridge is independently sound as an authenticated transport seam, and the current Agent `30fc8dd1`/WC4 native authority path is compatible with it. The App row is not qualified for production activation because the current App still has no authoritative way to discover the original pin for the selected raw clip and does not wire the existing selected-parameter props into the mounted `PropertiesPanel` path.

This is a source qualification finding only. No App, Agent, Runtime, ledger, branch, or integration files were changed.

## Reviewed source and rules

- App read bridge `89bb04462` over production-binding source `64d7e19b3`.
- Current Agent `30fc8dd154015a7c58cf4ce7b065ccc46f470ee8`, including WC4 native publisher `47c1ee60a023c77deb7f3a9f6b5a32e6f3653211`.
- `selected-param-original-pin-rule.md`, `agent-review-selected-param-authority.md`, `handoff-app-to-app2-selected-param.md`, and App status/plan documents.
- No old cohort or pin was used as an implementation source.

## Findings

### App read bridge

`89bb04462` adds only the two existing authenticated verified reads through `paramReadClient`, forwards that capability through the runtime data provider, and gives `useTimelineSave` the same provider capability. It does not create a local authority source, endpoint, or DTO. This is the correct bounded transport seam and can be retained.

The bridge cannot qualify the original pin by itself. `64d7e19b3`'s retained-input reader validates the exact supplied DocumentPin, admission, snapshot, and object; it does not determine which historical pin originally established the raw target.

### Current App production path

`ClipPanelBody`/`AstridElementParams`/`SelectedElementParamFields` already accept `retainedDocumentPin`, `timelineOps`, and `commandState`, and the focused component tests exercise the fail-closed pending/refusal behavior. However, the actual `PropertiesPanel.tsx` `ClipPanel` invocation supplies none of those three props. Thus the mounted production path cannot capture or submit the selected PARAM command with an original pin, even though the leaf components can do so when tests inject one.

The current `RuntimeDataProvider.loadTimelineCommandBasis` also loads one default `listTimelineCommits` page. The rule requires the complete relevant history through the captured head, with predecessor/order integrity. A one-page basis cannot safely resolve a pin across an older selection, inverse, removal, restart, or pagination boundary.

### Current Agent compatibility

The current native resolver requires the exact direct triple in the accepted command record: `command.args.schema_source == P`, the `params.schema` dependency, the exact `params.snapshot` source/element/object descriptor, and the fixed `params.element` binding. It rejects missing, ambiguous, incomplete, or forged history rather than scanning manifests/catalog state or inventing a pin. Native capture preserves the caller's exact `schema_source`; dependency and binding records are authored by native commit recording.

The current native path therefore satisfies the authority side of the contract observed here:

- no relabel from original pin B to a newer pin HA;
- PENDING/raw 16 is refused visibly while retaining the draft;
- a V1 original schema remains authoritative through V2/removal/restart and refuses value 16;
- accepted records retain exact source, dependency, snapshot, and binding evidence.

The App cannot claim those guarantees in production until it supplies the original pin from this native-compatible authority source. In particular, it must not select `dependency_manifest.documents[0]`, the latest catalog/admission, a display descriptor, an element revision, or a locally cached/synthesized pin.

## Exact bounded App additions required

1. Extend the existing authenticated command-session/basis path to page the existing timeline history through the captured head, preserving page predecessor/order checks. Do not add an endpoint or DTO.
2. Add one command-session authority accessor for the selected raw parent/occurrence clip. It must resolve the unique exact `P` only from the accepted history direct triple and freeze it for capture, async read, retry, recovery, and restart. Missing or ambiguous authority must return a visible refusal and preserve the draft.
3. Wire `PropertiesPanel` to the existing `ClipPanel` props: the accessor's `retainedDocumentPin`, `useTimelineOpsFromStore()`'s `timelineOps`, and the current command-session state. Keep the command payload limited to the exact `schema_source`; do not synthesize native dependencies or bindings in App.
4. Add a mounted panel-to-command control covering B versus HA, pending/raw16 refusal, V1 through V2/removal/restart, and exact source preservation in the native accepted record. Include a pagination/incomplete-history refusal control.

## One concrete next implementation task

Implement the bounded App selected-PARAM authority accessor and wire it through `PropertiesPanel.tsx` into the already-existing `ClipPanel` selected-parameter props, using fully paginated authenticated history through the captured head and fail-closing on missing/ambiguous authority. Add the mounted controls above; leave the `89bb04462` read bridge unchanged.

## Evidence

- App focused Vitest: 3 files, 82 tests passed.
- Current Agent selected-authority suite: 27 passed.
- Current Agent native retained-schema lifecycle probe: 3 passed, 29 deselected.
- No full, browser, socket, or live-service suite was run.
