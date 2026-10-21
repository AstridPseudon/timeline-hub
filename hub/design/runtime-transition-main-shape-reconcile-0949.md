# Runtime transition Main-shape reconciliation — 2026-10-21 09:49Z

Status: **UNAPPLIED source/contract correction.** No Runtime, Agent, App,
schema, generated artifact, pin, release, caller, or test was changed.

## Source identities

- Main/App witness: commit `860d43b331fb4422b16bc0dbd7b08666a0c766a0`,
  tree `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`,
  `src/tools/video-editor/runtime/element-adapter.ts`.
- Agent semantic/schema source: clean ca9 commit
  `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`, tree
  `87b432d48b0e1a5e0410c630ca76150095075eff`; canonical schema
  `astrid/core/timeline/schema/edit-command.schema.json`, SHA-256
  `a70f0e8898c6acccb34062e73733c93dd4e7bc22c34ef012431e1791907e1f4a`.
- Current App source inspected read-only: commit
  `4db86a76acd505dd1c7dc798695e2b7a9c932170`, tree
  `461fa0cddd67f4eb574563b38407733bd50afa7c`.
- Runtime base/public floor: `b92d3e7a05eec65c142294ef4873edd059e9b31d`,
  tree `6abc2f117391de8e7e35c0283f575a002199894d`.

## Verdicts for the five App findings

### #1 paired transition/reference clear — App adapter prerequisite

The canonical rule is sound: `clear:["transition"]` remains the existing
RESET and preserves unrelated `elementRef`/`element_ref`; only the explicit
pair `clear:["transition","elementRef"]` removes the transition and matching
references atomically. App’s current `clipScalarCapture.ts:202-204` and
`clipScalarGesture.ts:7-15` cannot express the pair. This is an App adapter
prerequisite, not a reason to alter the carrier or RESET semantics.

### #2 existing transition with no `elementRef` — **canonical mismatch; correct**

Main has two distinct callers in `element-adapter.ts`:

- `timeline.apply_transition` at `:345-367` is a new selection. It resolves
  the requested element and always writes `elementRef` on the destination clip
  (`:358-365`).
- `timeline.update_transition` at `:369-405` is the preservation path.
  `operation.transition` is optional (`:372-374`); when omitted it uses the
  existing `clip.transition`/catalog fallback (`:383-392`), spreads the
  existing raw transition (`:399-403`), and writes `elementRef` only when a
  new `operation.transition` was supplied (`:396-401`). This is the positive
  Main case for duration/parameter updates on a legacy incoming transition
  that has no reference.

Ca9’s schema already makes `values.elementRef` optional at
`edit-command.schema.json:1761-1763`, but the handler makes it mandatory at
`_clip_scalar_commands.py:98-104`. The minimum correction is:

1. With `values.elementRef`, retain the existing exact `kind/id/revision`
   match and selected-pack/P1 authority checks.
2. Without it, permit a SET **only** when the target already has a transition,
   has no canonical or legacy `elementRef`, and the requested transition has
   exactly the same `(type, revision presence/value)` tuple. Read/record that
   existing transition and references as the authentication; write no ref.
3. If an existing canonical/legacy ref is present but omitted from the SET,
   refuse rather than silently selecting or fabricating it. If the target is
   absent, has a different type/revision, or supplies a new selected tuple
   without a ref, refuse. A selected new tuple still requires its matching ref
   and the existing retained source authority; no project-pack authority is
   inferred for a no-ref legacy row.

This distinguishes authenticated existing no-ref preservation from genuine
selection. The existing guards remain: `_clip_scalar_commands.py:52-65`
reads both reference spellings and source identity; `:243-287` records the
predecessor/target transition and adjacency/frame-fit reads; and
`_selected_param_authority.py:9-49,52-170` plus `commit.py:503-590` retain
accepted P1 source/snapshot proof for selected project-pack transitions.

### #3 selected `schema_source` / P1 handoff — App adapter prerequisite

The canonical requirement is correct and remains unchanged. Current App
scalar capture requires exactly `args:{values,clear}` at
`clipScalarCapture.ts:189-212`, while selected authority is implemented for
other carriers in `elementCapture.ts:69-75`. App must later carry the exact
existing `DocumentPin` and retained P1 association for selected project-pack
SET. No pin, owner, revision, or authority is to be invented here.

### #4 type-selector callback loses opaque data/ref — App adapter prerequisite

Main’s preservation rule is correct. Current App type selection constructs only
`type`, `duration`, and optional defaults at
`ClipTransitionSection.tsx:145-163`; duration and parameter callbacks spread
the raw transition at `:258-275` and `:300-315`. The type-selection callback
must later become a complete raw-envelope producer with the selected ref. This
is a caller/adapter repair, not a canonical relaxation.

### #5 `params:null` versus absent — **canonical mismatch; correct**

Main’s `timeline.update_transition` at `element-adapter.ts:369-405` spreads
the existing transition and only replaces `params` when `operation.params` is
truthy (`:399-404`). Therefore an existing `params:null` or absent `params`
survives a duration-only update. App’s existing preservation controls exercise
both cases at `TransitionPreservation.test.tsx:273-307`; its duration callback
also spreads the raw envelope at `ClipTransitionSection.tsx:267-275`.

Ca9’s schema currently admits only an object at
`edit-command.schema.json:1746-1750`, and `_clip_scalar_commands.py:109-110`
assumes `.items()`. The minimum correction is to admit literal `null` as well
as an object and to iterate changed parameter keys only when the supplied
`params` is an object. The transition write must retain the supplied field
exactly: absent stays absent, `null` stays `null`; no normalization to `{}` is
allowed. A parameter edit that intentionally adds a named parameter may
materialize an object from null/absence, and Reset defaults remains an explicit
SET; those are distinct user intents.

## UNAPPLIED minimal diff (Agent source only)

This is a source proposal, not an applied patch. The surrounding current
schema/handler and all current operations must be preserved.

```diff
diff --git a/astrid/core/timeline/schema/edit-command.schema.json b/astrid/core/timeline/schema/edit-command.schema.json
@@ ClipSetArgs.values.transition.params
-                "type": "object",
+                "type": ["object", "null"],
                 "additionalProperties": {
                   "$ref": "#/$defs/JSON"
                 }
diff --git a/astrid/sdk/timeline/_clip_scalar_commands.py b/astrid/sdk/timeline/_clip_scalar_commands.py
@@ _transition_set
-    selected = values.get('elementRef')
-    if not isinstance(selected, dict) or selected.get('kind') != 'transition':
-        raise CommandError('transition SET requires its matching elementRef', ref=ref)
-    if selected.get('id') != transition['type'] or selected.get('revision') != transition.get('revision'):
-        raise CommandError('transition requires its matching selected reference', ref=ref)
     before = ctx.read(ref, ['transition'])
     previous = identity['elementRef'] or identity['element_ref']
+    selected = values.get('elementRef')
+    same_legacy = (isinstance(before, dict)
+                   and before.get('type') == transition.get('type')
+                   and before.get('revision') == transition.get('revision'))
+    if selected is None:
+        if previous is not None or not same_legacy:
+            raise CommandError('transition SET requires a matching selected reference '
+                               'for a new or referenced transition', ref=ref)
+    else:
+        if not isinstance(selected, dict) or selected.get('kind') != 'transition':
+            raise CommandError('transition SET requires its matching elementRef', ref=ref)
+        if selected.get('id') != transition['type'] or selected.get('revision') != transition.get('revision'):
+            raise CommandError('transition requires its matching selected reference', ref=ref)
     same = isinstance(before, dict) and before.get('type') == transition['type']
-    same = same and equal(selected, previous)
-    changed = {key: value for key, value in transition.get('params', {}).items()
+    same = same and ((selected is None and previous is None) or equal(selected, previous))
+    params = transition.get('params')
+    changed = {key: value for key, value in (params.items() if isinstance(params, dict) else ())
                if not same or not equal(present(value), ctx.state.get(ref, ['transition', 'params', key]))}
```

The exact error text is not normative; the guards and refusal boundary are.
The `selected`-dependent catalog/authority branches below this hunk must keep
their current behavior: built-ins remain pinless, selected project packs still
require the exact `schema_source`, and a no-ref legacy update cannot bypass
that authority.

## Canonical-source and floor rule

Agent owns the semantic correction and the current complete canonical schema
source. `ca9` is feature provenance, not a license to regenerate its old
union blindly. The future complete source must retain published ordinary6ba
exactly, and may retain the ordered017 floor only when that floor is explicitly
included. Immutable 014/95 and 017 remain unchanged. Runtime remains limited
to the normal generator/transport; no new operation, DTO, endpoint, store,
authority, allocation, generation, pin, activation, or live caller change is
authorized by this report.

## Requested ACKs / next action

- **Agent:** ACK or correct the #2/#5 semantic rules above; keep generation
  HOLD; name the current full source that incorporates the correction while
  retaining ordinary6ba and any explicitly included ordered017 floor.
- **App/App2:** ACK that #2/#5 are the canonical correction and keep #1
  paired-clear, #3 selected-source handoff, and #4 complete type-selection
  envelope as separate adapter prerequisites. Confirm that new selection emits
  its ref, no-ref legacy updates preserve the tuple without fabricating a ref,
  and duration-only edits preserve params absence/null.

## Evidence

Read-only source probes only: `git show` of the frozen Main/Agent identities,
line-numbered inspection of current App sources, and current App HEAD/tree
identity checks. No tests, generation, pinning, release, native/HTTP/browser,
render, or live-caller run was performed.
