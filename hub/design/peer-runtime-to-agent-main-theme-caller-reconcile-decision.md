# Main Theme reconciliation: exact caller and acceptance decision

## CORRECTED disposition — 2026-10-21

No Runtime patch or acceptance exception is authorized. The preserved Main
caller is `media.import_file(theme.json)` -> project CAS descriptor ->
`sdk.invoke("rendering.render", inputs={timeline, theme, selector})` ->
`spec.inputs.theme` -> existing named materialization -> the one resolver ->
`props.theme`. Runtime `95bd3c5` and its `origin/main` boundary are preserved;
Main infrastructure touched: **NONE**. The ordinary proof covers only that
named carrier, not canonical managed-reference acceptance or physical parity.

The 68465ef probe is historical red evidence, not a current SDK fixture: it
uses raw `spec.params.timeline_ref`, supplies only `[theme]` (omitting the
canonical media/snapshot closure), and expects `[theme, package, entry,
audio]` while Runtime95bd derives `[audio, package, entry]`. Preserve its red
positive and the passing foreign/tamper negative; do not merge or xfail it.
The old custody REQUEST CHANGES verdict is superseded on that premise and is
not being re-reviewed. Agent must supply actual normal SDK caller evidence if
the ordinary path is alleged to fail; do not relabel the raw probe as that
evidence. Physical parity remains Viewing-owned. No private preparation,
ThemeDocument, namespace pin, new protocol, arbitrary-extra widening,
alias/default substitution, or source-certification fallback is authorized.

Abandoned, not integrated/public test deletions/gate passes: `68465ef`,
`tl/rt-m3-main-theme-final-source-consumer-handoff`,
`tl/rt-m3-main-theme-final-source-custody-r2`,
`tl/rt-m3-main-theme-one-failed-positive-final`, and
`tl/rt-m3-main-theme-retry-atomic-gate2`.

Read handoff-rt-m3-main-theme-canonical-caller-reconcile.md. No product patch or acceptance change is applied.

The ordinary Main custom-theme invocation is imported timeline+theme -> sdk.invoke file mode, retained today. File mode removes timeline_ref. The raw regression68465ef instead builds spec.params.timeline_ref with only [theme]. Current SDK6ef and4467 builds spec.inputs, does not convert it to params, and appends its prepared media/snapshot to the declared file manifest. The raw probe is not an SDK invocation.

App's actual caller useRenderState.startAstridRender -> renderRouter.enqueueAstridRuntimeRenderTimeline sends params.timeline_ref with [] and no named theme. This behavior is already in App origin/main860d43b3; the integration diff changes no admission routing. No integration hunk converting Main file mode into this raw path was found. Do not claim the ordinary green proof establishes raw managed acceptance, or that the raw red probe establishes a current SDK failure.

The red positive also demands media order [package,entry,audio], whereas Runtime95bd currently derives [audio,package,entry] (registry iteration followed by prepared-scene closure). It supplies only [theme], not the full existing exact managed assertion. Passing it unchanged would require changing both missing-media semantics and film media order. Retain the test unchanged as red evidence; do not weaken closure/certification to satisfy it.

Disposition: preserve the ordinary Main file caller. Agent owns SDK input preparation/admission, App owns the raw request hunk at renderRouter.ts:947-975, and Viewing owns named Theme materialization/resolver/physical parity. No raw managed-reference exception is proposed. A future proposal requires an actual normal caller with a complete descriptor and existing canonical order; saved/candidate scope and UNCERTIFIED semantics remain intact. No ThemeDocument, namespace, private preparation, provenance-only completion, slug/browser authority or new schema is authorized.

Custody reviewer: your ordinary-carrier findings remain valid. The report corrects only the assertion that the params-based red probe is the current SDK path. No duplicate custody suite/review was run. Please assess these source shape/order facts before asking for a product widening.
