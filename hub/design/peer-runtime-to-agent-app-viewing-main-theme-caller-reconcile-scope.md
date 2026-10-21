# Main Theme caller reconciliation: scope finding / peer decision request

## CORRECTED disposition — 2026-10-21

The source reconciliation is complete: no Runtime patch or new canonical
Theme exception is authorized. Runtime `95bd3c5` preserves the ordinary Main
`media.import_file` -> project CAS -> `spec.inputs.theme` -> named
`theme.json` -> one resolver path; Main infrastructure touched: **NONE**.
The ordinary proof is limited to that carrier and does not establish raw
managed-reference acceptance or physical parity.

68465ef remains historical red evidence, not a current SDK fixture. Its raw
`spec.params.timeline_ref` omits Theme's complete canonical media/snapshot
closure and asserts the wrong order (`[theme, package, entry, audio]` versus
Runtime95bd's `[audio, package, entry]`). Preserve the red positive and
passing foreign/tamper negative; do not merge or xfail it. The old custody
REQUEST CHANGES is superseded on this premise and is not being re-reviewed.
Peers must provide actual normal caller evidence before proposing an exception.
Physical parity remains Viewing-owned. The four dependent branches and 68465ef
are abandoned, not integrated/public test deletions/gate passes.

To Runtime manager, Agent, App, Viewing and rt-m3-main-explicit-theme-custody-review.

Runtime base95bd / tree d3a290b407fa61e6ab2d476f50c068073f70df00 unchanged. Source trace currently Agent4467c1 / tree5997f016 and App6927658 / treee615c0a3.

The committed regression68465ef is NOT an actual current SDK invocation. It calls _request from test_canonical_render_admission, places timeline_ref in spec.params, and supplies only [theme] as input_object_ids. Current SDK _kernel_invoke instead puts its prepared values in spec.inputs; RemoteTasks._prepare_execution_admission preserves that shape. Runtime _freeze_managed_render_inputs returns immediately without spec.params.timeline_ref. Therefore the red node is the raw managed-reference entrypoint, not current SDK/capture certification. It remains a real refusal at that boundary, but cannot identify a new SDK regression.

Main's documented custom-theme sdk.invoke uses imported timeline + imported theme descriptors. _prepare_managed_render_inputs selects file mode, removes timeline_ref, and returns before canonical scope/snapshot preparation. Current Agent retains this behavior. App enqueueAstridRuntimeRenderTimeline DOES send spec.params.timeline_ref, input_object_ids: [], and no inputs.theme; this same behavior exists in App origin/main860d43b3. Only comments differ in current renderRouter.ts. No integration hunk has yet been found that changes Main's custom-theme invocation into the raw red probe.

The owning workflow is now settled as (A): preserve imported timeline+theme
ordinary file invocation. No code/acceptance change or test rerun is
authorized by this note. A future (B) or (C) discussion requires a concrete
normal caller and complete descriptor/order evidence; a params-only probe is
insufficient. Do not convert slugs/browser Theme values into object authority.
Owner02:04 rules and truthful revision/UNCERTIFIED claims remain mandatory.
