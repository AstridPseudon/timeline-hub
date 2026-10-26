# Popup read review: UNKNOWN

## Identity and result

Actual retained run: `app-pin-867cb273-d141-p2-popup-add-867cb273-submit-1026014140-1368`. Exact tuple: App `867cb2737af1b46dc608c7cd37c349e920fe9422` / `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`; Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70` / `2ebe2ddf5a61f013953ab1e21d51ebaab746e58a`; Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d` / `ac5b862744bece65b2e30565db1777bacd60da28`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / `5ab5191a296980a0a6bcd1178ab6902d6478a148`. Readiness passed; the unchanged popup ADD failed at `three-products.p2-popup.spec.ts:356` before double-click.

Authentic last selector PASS: `app-pin-96d4754b-d73-p2-96d4754b-submit-1025100712-15203`, popup ADD 36.819s. Its overall eight-case suite was NO-GO (exit 1), so only this selector receives PASS credit. Tuple: App `96d4754b4eef0591a208d6b51b60c30fc44b6915` / `3f9da34c4f116026ec21022421850e0608ba653b`; Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd3` / `6056414359ae9fce08d999d54cbecf719fda33c3`; Runtime `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e` / `6283b5fbb128447f1b333e0e6af334d35637cf69`; Composition is the same `635f4de0` / `5ab5191a`. Existing source author App04beedcd18b8abb49502f65cd3facaafbe93db4e has the same popup/readiness blobs.

Both selector sources are Git blob `d7da4c234fb921c448bc18e9ac174b1a11dbc4a6` and SHA-256 `09f5e2c2ea2a207575534a88adf2847d68cdd389caa5d145580100f21302b2b9`. The actual packet records readiness PASS, setup lifecycle phases with HTTP 200 responses, and DOM `No shots yet`, but no canonical read/projection record.

## Exact change since selector PASS

- `2f36246a32f17fa63c97d399360079a004b1dfac` (`tl/app-U3-D135-model-menu-return-2033`) changes Runtime connection activation fields and `EditorConnectionPanel`, adds metadata polling, and adds delayed project selection.
- `263b728f014040afc9c6b3fdfb54963b93b757eb` (`tl/app-U3-D141-tour-gate-return-0014`) changes shell rendering/layout fields: `renderTimeline`, `toggleFullscreen`, `hostPanelInset`, `mainPadding`, and `gridTemplateColumns`.

The five canonical caller/renderer objects (`useAstridShotsHost`, `AstridTimelineEditor`, `useShotGroups`, `TimelineCanvas`, `ShotGroupOverlay`) and the popup/readiness specs are byte-identical between compared App sources. No canonical occurrence read/projection field or popup expectation changed. Later App commit `5fe3e4debec5fb030f772ca41f16c86cc80e6150` is not retargeted because it post-dates run 1368.

## Causal finding

0226's `PROVED_PRODUCT_GAP` is challenged. The exact missing record is accepted setup-head continuity plus canonical occurrence presence at `shotComposition.load`, then `activeCanonicalOccurrences` and `useShotGroups` immediately before `ShotGroupOverlay`. Without it, accepted setup semantics and the pre-popup DOM failure cannot distinguish producer persistence/read omission from App projection omission. Verdict: `UNKNOWN`, not `PROVED_PRODUCT_GAP` and not `REG`.

The missing record is not authority for a new capture. Preserve the original test and all request/reply/undo assertions. No new reader, author, body, retry, browser run, or test expectation is requested.
