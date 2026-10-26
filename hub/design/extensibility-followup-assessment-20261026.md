# Extensibility follow-up: assessment (26 Oct)

Sources:
- PLAN-v1.md §4.2–4.3, the five extension types and the shared primitives;
- five read-only audits of the final heads (Agent ec0a9f5b, App 82e9e13d, Runtime 95d98f03, Composition 635f4de0).

Estimates are in senior-engineer days.

| Type | Exists today (main precursor) | Main gaps | Estimate |
|---|---|---|---|
| Commands | Hard-coded op table `astrid/sdk/timeline/commands.py:75`; its docstring defers the registry to M2. Recording API, `commit(fn)` retry, undo, selectors | Registry and decorator, pack discovery, a published op contract, rationale/group not exposed by `commit_many`, markers refused by the compiler, the `doc.patch` escape hatch, two commit paths | 21 (+6–8 markers) |
| Views | `timelines show --as cuts/script/code/sheet`, the editable cut sheet (`timeline_sheet.py`), `diff --as`, `visualize_layers` discovery, Runtime `create_timeline_view` | Registry, generic parse-to-commands (only the opt-in NativeSheet path does it), pin contract, App panel host (only `asset-panel` placement) | 31 |
| Elements (+ signals) | `element.yaml` ×45, registry, generated composition registry, modifiers and transitions, keyframes | One kind vocabulary, an animatable flag, a signal contract, a preview/export parity harness; the App Elements panel was removed upstream | 38 (+10 parity risk) |
| Checks | Publish refusals (core), lint, visualize checks with a `fix` field, Runtime seam reports, App export guard | Registry, one finding shape with stable refs and a revision, fix as proposal, policies. The App blocks on seam "blocked" while Runtime says advisory: a conflict | 23 |
| Producers (+ markers, signals, proposals) | Pack actions (`music/beats`), `import_authoring_media`, managed outputs and CAS, client-side proposals, commit rationale and group_id, namespaced `meta` | Producer kind, markers (none anywhere; beats copied into clips and addressed by ordinal), signals (none), Runtime proposals (client-side only; AUTO_FIX bypasses review), meta merge policy | 27 (+4 signals) |

Naive sum is about 140 days. Removing the shared work (one registry and manifest pattern, one conformance harness and scaffold, markers counted twice) brings it to **about 110–120 days**.

## Recommended shape

**Phase 0: foundation (4 weeks)**
- unify the two commit paths;
- one extension registry and manifest, with pack discovery;
- stable refs and one finding shape;
- rationale and group plumbing;
- the conformance harness and the `astrid ext new/test` scaffold.

**Phase 1: Commands + Markers + Producers + Proposals (5 weeks)**
- The beat litmus works end to end: the detector publishes markers, beat-snap proposes anchors, and the anchors follow when the beats are re-detected.

**Phase 2: Checks + Views (4 weeks)**
- an off-beat check whose fix is beat-snap;
- a beat-grid view;
- an editable shot-list view that edits through commands;
- a read-only App view panel;
- the App/Runtime seam blocking conflict resolved.

**Phase 3: Elements + Signals (6–8 weeks)**
- the parity harness comes first;
- start after the shot-layering release, which reworks rendering.

**Time:** one engineer, about 6 months. Two to three engineers in parallel after Phase 0, about 2½–3 months.

**Cross-cutting risks**
- Third-party code runs in-process, in a trusted provider, with no sandbox.
- SCHEMA_DIGEST couples command extensions to releases.
- Python and TypeScript resolvers must agree on anchors and markers.
- Transcript authority is deferred, which blocks word-anchored producers.
