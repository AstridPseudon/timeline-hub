# Independent gate: stored-cap consumer proposal

Decision: **REJECT the App joint port as submitted.** The consumer handoff is
not merge-ready, and the App producer/serialization side remains unverified.
This is a specific rejection of the joint port, not a rejection of the
approved one-scalar direction.

## Findings

1. **Still delivery is incomplete.** The proposal passes `compiledTransitions`
   to the Player through `useVideoEditorPreviewSurface` and to client render
   through `useClientRender`, but its `VideoEditorAssetPanelSurface` still gives
   `TimelineFramePreview` only `config`. At b1ef, `TimelineFramePreview` builds
   `inputProps` with `{ config: output, astridElementHost }`; no compiled vector
   reaches the `Thumbnail`/`TimelineRenderer` boundary. That renderer therefore
   takes its ordinary adapter path instead of the same public compiled vector.
   This fails the handoff requirement that the public vector be used at all
   activated Player/still/client-render boundaries. The mounted proposal test
   observes the Player vector but does not mount the actual still boundary.

2. **Missing/invalid metadata can lose the existing conservative bound.**
   `useVideoEditorPreviewComposition` switches the entire projected clip list
   to `boundCanonicalConfigClips(..., 'stored')` when *any* clip has a finite
   stored value. `boundCanonicalClipToOccurrence(..., 'stored')` returns a clip
   unchanged when that clip lacks `storedOccurrenceDurationMs` or has a
   non-finite value. Such a clip therefore skips the existing
   `occurrenceDurationMs` bound, rather than retaining the older conservative
   behavior. A negative finite stored value is also accepted and clamped to a
   zero-length occurrence instead of being treated as invalid metadata. The
   stored selector must fall back per clip to the existing effective path (and
   validate the approved scalar, including non-negativity), or the whole
   consumer must remain on the old path unless the required metadata is valid.

3. **Producer and serialization are not certified.** No shared App producer
   candidate was available for this review. The required graph/local/recovery/
   accepted recomputation, original-cap identity, authored/read preservation,
   and stripping from authored/wire/storage are therefore unverified. The
   consumer proposal alone cannot be merged or called an App joint port.

## What passed

- Independent source inspection of the b1ef App boundary confirmed that the
  existing Player path already accepts a compiled vector, while the still path
  does not receive one.
- Own Composition worktree, public evaluator source, 12-leaf graph probe:
  4000 ms produced 120 frames, opacity 0.5 at frame 105, active frame 119,
  and no layer at frame 120; 4500 ms produced 135 frames, opacity 1 at frame
  105, active frame 119, and no layer at frame 135. Command and output are in
  the companion COMMAND file. This validates public evaluator semantics only;
  it does not claim producer or App integration.
- The source worker's candidate evidence reports 5 mounted files / 100 tests
  passed and both unapplied patches applying cleanly to b1ef. I treat that as
  candidate evidence, not production-green evidence.

## Scope and unverified items

No App files, producer types, Composition source, shared dependencies, caches,
branches, or refs were modified. No browser, render, network, socket, install,
full suite, or actual codec/parity run was performed. The proposal's exact
4000/4500 mounted lifecycle assertions, old-A/known-C race sequence, and
serialization stripping remain unverified in a shared App candidate.

## Required next step

App should publish one shared producer+consumer candidate that (a) carries the
same compiled vector into the still boundary, (b) preserves effective-bound
fallback for each missing/invalid scalar, and (c) proves source-graph
recomputation and stripping on bootstrap, local, recovery, and accepted paths.
Then rerun the mounted Player/still/client-render cases and the producer's
serialization/readback tests together. Do not merge the proposal patches by
themselves.
