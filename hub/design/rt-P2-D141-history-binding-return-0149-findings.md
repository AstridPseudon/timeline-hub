# D141 P2 history-binding return

## Verdict

`UNKNOWN_CAUSAL_ATTRIBUTION`, with source intent `INTENDED_CONTRACT`.

The D118 placement receipt is now present and supplies the immutable passing tuple: App `96d4754b4eef0591a208d6b51b60c30fc44b6915` / tree `3f9da34c4f116026ec21022421850e0608ba653b`, Agent `070dfc5ef4f3dc35062fcb36a50cb571cd77fbd2` / tree `6056414359ae9fce08d999d54cbecf719fda33c3`, Runtime `d23a8e0d24bf2aeaf984072eaca0d3dcf8873c2e` / tree `6283b5fbb128447f1b333e0e6af334d35637cf69`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` / tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`. Its automatic child placement case is recorded as PASS 88.780s with strict history and guarded-Undo predicates.

The cut is App `867cb2737af1b46dc608c7cd37c349e920fe9422`, Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70`, Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`, Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`; the retained App note reports one failure at `assertNativeHistoryEntry` line 757 from guarded Undo line 1284, with additional history binding fields versus `expected.records`. No safe actual field names/indices were published for this pass.

## Static causal delta

The strongest source-proved activation is Agent D124 commit `16bbd56dbf016bcddeafa891291129efcfa87196`, which is between the passing Agent pin and the cut Agent pin. In `astrid/sdk/timeline/_commit_patch.py`, the passing source had:

```text
if not self.v2 or not segments:
    materializations(...)
```

The cut source retains that branch and adds:

```text
complete_stage = (len(segments) == 1 and segments[0][0].document == before.document
                  and segments[0][1].document == after.document)
...
elif complete_stage:
    proposed = {'bindings': []}
    self.materializations(proposed, before, after, ...)
    if all(exclusive single-owner turnover predicates):
        record['bindings'].extend(proposed['bindings'])
```

This is a real new predicate activation for v2 inverse records. The older `8a66b1…` R1 writer and `61ceeb…` R2 integration explain why the binding family exists, but their presence alone cannot explain a new binding in this pass/final comparison. The D124 branch can.

The D100a commit `bbeea9ddf750b1d67d08e848c20262d748e6ff03` also changes `_command_state.py`: shared placement may reopen the exact physical image, accepts physical item membership without extending an alias map, and changes the projected expected item set. This changes physical input/image state, not serialization. Without the actual 3118 image/binding packet, it is not possible to prove that D100a made the D124 `complete_stage` predicate true for this particular run.

Runtime `d23a8e… → 6a011d…` changes authentication/projection/history verification and adds bounded diagnostics, but the inspected Runtime delta contains no new history-binding writer. Current Runtime validates `commit.materialization` edges against complete-step input/output images and persists `canonical_json(records)`; it does not invent the provider binding.

## Attribution limit

The source supports `INTENDED_CONTRACT`: C0 requires authenticated physical refs, revision/content identity, evaluation boundaries, and materialization/edge provenance for inverse history. It does not support run-level attribution to D124, D100a, Runtime, or an expectation solely from source-derived field names. The required safe App packet—actual-versus-expected binding family/index/keys—was not available in the normal paths during this finite pass. Therefore causal attribution remains `UNKNOWN` and Main retains the gate decision.

No source, test, fixture, guard, expectation, import, provider, browser, network, or production caller was changed.
