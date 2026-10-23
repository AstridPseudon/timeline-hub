# Handoff: ap2-P2-popup-cases-0959

The requested popup P2 coverage is blocked on an authentic mounted seam, not on test assertion design.

Current production facts:

1. `shotTimelineDataProvider.ts` is the real popup save caller. Its shared-media branch requires an exact selected occurrence, a second parent occurrence sharing the same shot/revision/internal revision, and Runtime `getProjectMediaSelection` identity for every media row. It emits `occurrence.fork` first, then `occurrence.add-media` or `occurrence.swap-media`.
2. The reusable `seedThreeProducts` fixture has one `f2-occurrence` and no `generationId`/`variantId` in its registry entries. It cannot exercise the shared branch or authenticated physical source mapping.
3. The mounted popup has no production `parentClipSwapMediaPort` caller. External file/asset drops insert media; replacement is only exposed through the generation-backed “Update to current variant” action, which the seed cannot use.

The 0956 branch was inspected and has no usable popup-spec WIP. No donor ancestry, duplicate-as-fork substitute, mocked provider/executor, private authority, or legacy setup write was introduced. The original P2 tour remains unchanged.

Next owner action: supply a real shared-occurrence/generation-backed fixture and mounted replacement action (or explicitly scope P2 to the currently reachable unique popup add), then implement the named spec with commit POST and Runtime `/commits` evidence, full v2 wire-shape assertions, exact child/parent canonical preservation, reload, and guarded Runtime Undo.
