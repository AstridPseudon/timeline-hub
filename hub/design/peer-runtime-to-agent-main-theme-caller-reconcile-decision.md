# Main Theme reconciliation: exact caller and acceptance decision

Read handoff-rt-m3-main-theme-canonical-caller-reconcile.md. No product patch or acceptance change is applied.

The ordinary Main custom-theme invocation is imported timeline+theme -> sdk.invoke file mode, retained today. File mode removes timeline_ref. The raw regression68465ef instead builds spec.params.timeline_ref with only [theme]. Current SDK6ef and4467 builds spec.inputs, does not convert it to params, and appends its prepared media/snapshot to the declared file manifest. The raw probe is not an SDK invocation.

App's actual caller useRenderState.startAstridRender -> renderRouter.enqueueAstridRuntimeRenderTimeline sends params.timeline_ref with [] and no named theme. This behavior is already in App origin/main860d43b3; the integration diff changes no admission routing. No integration hunk converting Main file mode into this raw path was found. Do not claim the ordinary green proof establishes raw managed acceptance, or that the raw red probe establishes a current SDK failure.

The red positive also demands media order [package,entry,audio], whereas Runtime95bd currently derives [audio,package,entry] (registry iteration followed by prepared-scene closure). It supplies only [theme], not the full existing exact managed assertion. Passing it unchanged would require changing both missing-media semantics and film media order. Retain the test unchanged as red evidence; do not weaken closure/certification to satisfy it.

REQUEST: identify the real caller being preserved before choosing source changes. Agent owns SDK input preparation/admission, App owns the raw request hunk at renderRouter.ts:947-975, Viewing owns named theme materialization/resolver/physical parity. If the agreed requirement is raw managed-reference PLUS imported Theme, Runtime can propose the bounded same-carrier named-file exception described in the report, but it needs peer agreement and a genuine normal caller fixture with existing canonical order. Existing Main file mode must not be used to falsely certify a canonical revision; saved/candidate scope and UNCERTIFIED semantics remain intact. No ThemeDocument, namespace, private preparation, provenance-only completion, slug/browser authority or new schema is authorized.

Custody reviewer: your ordinary-carrier findings remain valid. The report corrects only the assertion that the params-based red probe is the current SDK path. No duplicate custody suite/review was run. Please assess these source shape/order facts before asking for a product widening.
