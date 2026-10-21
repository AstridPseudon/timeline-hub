# Runtime transition frame/ID source clarification — 2026-10-21

## Disposition

This is a bounded correction of only the three new clarifications in
`agent-transition-existing-clipset-next-public-0934-REPORT.md`. It does not
ACK a complete generated Agent source, change Runtime, allocate a version, or
qualify an App consumer. The owner-selected carrier remains the existing
`clip.set` operation on the incoming/TO clip.

## Evidence traced

- Main/App witness: commit
  `860d43b331fb4422b16bc0dbd7b08666a0c766a0`, tree
  `ea4eabb8eb469df63fd1d515f84982d85b2f14cc`.
- Agent ca9 witness: commit
  `ca9f5f8eeba96bb9cb8f9d700c2714c2ed9f9a20`, tree
  `87b432d48b0e1a5e0410c630ca76150095075eff`.
- Runtime base: `b92d3e7a05eec65c142294ef4873edd059e9b31d`.

Main's real normal path is:

1. `src/tools/video-editor/components/ElementsLibraryPanel.tsx:46-84`
   calls `elementOperationAdapter.execute` with
   `timeline.apply_transition`, passing the selected catalog `id`, `kind`,
   `revision`, and optional `packId`.
2. `src/tools/video-editor/runtime/element-adapter.ts:445-483` validates and
   dispatches the operation; `:487-507` reads the current timeline and calls
   `applyTimelineOperation`; `:508-523` performs the one expected-version
   save. The frozen witness has no separate production UI call to
   `timeline.update_transition`; that operation is nevertheless the normal
   adapter operation at `:369-405` (tests and agent operation dispatch invoke
   the same `execute` path).
3. `element-adapter.ts:175-189` resolves the adjacent destination for apply
   and update. `:211-215` returns the supplied element ID unchanged; it does
   not alias-normalize it.
4. `element-adapter.ts:218-228` is the duration source. The requested value,
   or an integer catalog default (otherwise `8`), must be a positive integer
   frame count. `element-contract.ts:327-335` independently rejects a
   supplied non-integer `duration_frames` before the adapter runs.
5. Apply calls that helper at `element-adapter.ts:345-367`, checks fit, and
   writes `transition.duration = durationFrames / fps` at `:361-364`.
   Update calls it at `:369-405`, including the no-new-reference preservation
   path, and overwrites the duration with the same division at `:399-403`.
   Existing raw transition duration is not parsed or rounded into frames.

Therefore Main's real path admits integer frames, then stores seconds by exact
division. For example, its default `8` at 30 fps is stored as `8 / 30`; this
is fractional seconds, but it came from an integral frame count. Main does not
admit an authored `0.75`-second input at this boundary because its operation
contract has no seconds input and rejects `22.5` as `duration_frames`.

Agent ca9 is different: `_clip_scalar_commands.py:98-104` validates a
positive duration in authored seconds, and `:135-138` checks only that
`duration * fps` is finite and in the safe positive range (`0.75 * 30 ==
22.5` is accepted). It neither requires an integer product nor converts the
seconds to a saved frame count. Its `number()` helper in `capture.py:24-35`
rejects non-finite/non-positive values but does not enforce integrality.

## Finding 1 — exact descriptor ID, not an alias

**Agreement/correction:** `cross-fade` is the canonical Agent built-in
descriptor ID. `crossfade` is only an alias/renderer-facing spelling and must
remain illustrative, not a second carrier identity.

Evidence: Agent's registry declares
`ElementKindDescriptor(catalog="transition", id="cross-fade", aliases=("crossfade",))`
at `astrid/core/pack/registry.py:237-241`, and the descriptor manifest is
`.../transitions/cross-fade/element.yaml:10-18`. Main's
`transitionType()` preserves the supplied ID at
`element-adapter.ts:211-215`, while `ElementsLibraryPanel.tsx:70-83` passes
the selected descriptor's exact `element.id`. The Agent handler also matches
the selected descriptor identity literally at `_clip_scalar_commands.py:111-126`.

The next carrier must therefore use the selected descriptor's exact `id` in
both `values.transition.type` and `values.elementRef.id`, with no Runtime
alias normalization. A sample showing `crossfade` does not confer alias
authority and cannot justify changing the canonical ID.

Ownership/prerequisites:

- Agent: preserve the existing catalog ID and exact descriptor matching in the
  complete future source; no new alias authority is needed.
- App: emit the selected catalog `id` verbatim for both fields. If its browser
  renderer accepts `crossfade`, that resolution behavior stays downstream of
  the authored carrier.
- Runtime: carry the literal JSON unchanged; no semantic change or new
  operation is authorized.

## Finding 2 — authored seconds and Main integer-frame admission are distinct

**Correction:** the proposal's statement that no Main/Agent semantic
inconsistency remains is too strong. The `clip.set` carrier may remain
authored seconds, but Main compatibility is only exact for Main-originated
whole-frame values mapped as `duration = duration_frames / fps`.

The current ca9 Agent source accepts positive fractional frame products, while
Main's real apply/update path accepts only positive integer `duration_frames`.
There is no fractional-seconds validation or conversion on Main's operation
path: Main receives frames, validates integrality, and divides by FPS when
writing. Conversely, Agent receives seconds and does not round or convert
them. This is a real source-level disagreement, not a Runtime transport
detail.

Smallest semantic correction: remove the claim of unconditional Main parity
and state the boundary explicitly. App adapters translating Main's existing
operation must convert integer frames to authored seconds exactly. Agent owns
the remaining policy decision: either narrow `clip.set` transition admission
to integral `duration * retained_fps` when Main-equivalent behavior is required,
or explicitly document that arbitrary safe authored seconds are an Agent-only
authoring capability. This report does not make that policy exception or
pretend that ca9 already supplies a Main-compatible complete source.

Ownership/prerequisites:

- Agent: source owner for the admission rule and its documentation/tests; a
  future complete source must state whether integral frame equivalence is a
  requirement. No Runtime-side rounding or hidden frame alias is acceptable.
- App: when adapting Main's `duration_frames`, calculate the authored seconds
  from the retained FPS and preserve that literal value in the raw transition;
  do not round authored seconds in the adapter.
- Runtime: no new DTO or conversion; it must preserve the selected carrier's
  literal authored value and must not claim integer-frame admission for
  `clip.set` unless Agent source actually enforces it.

## Finding 3 — selected revision is required; legacy no-ref revision state is
authenticated separately

**Agreement/correction:** a selected transition SET and an authenticated
legacy no-reference update are different cases.

For a selected SET, `ElementRef.revision` is schema-required at
`astrid/core/timeline/schema/edit-command.schema.json:595-617`, and the
transition body must carry the same non-empty revision: `ClipSetArgs` admits
the body field at `:1727-1745`, and the handler currently compares
`selected.revision` with `transition.revision` at
`_clip_scalar_commands.py:98-104`. Thus a valid selected pair is:

```json
{
  "transition": {"type": "cross-fade", "duration": 0.75, "revision": "r1"},
  "elementRef": {"id": "cross-fade", "kind": "transition", "revision": "r1"}
}
```

Omission, `null`, or an invented revision is not a valid selected reference.
For a project-pack selection, the exact selected revision/owner and existing
`schema_source`/retained authority remain required; no type-only or latest
fallback is allowed.

Main's positive preservation path is different. In
`element-adapter.ts:369-405`, `operation.transition` is optional; when it is
omitted Main spreads the existing raw transition and writes no `elementRef`
(`:372-401`). The corrected native `clip.set` contract must preserve that
case without treating it as an incomplete selection:

- With a requested `elementRef`, require the exact selected `id`,
  `kind`, `packId` (when present), and non-empty `revision`, and require the
  transition's revision key/value to match it.
- Without a requested `elementRef`, permit SET only for an already-present
  transition on a target with neither canonical `elementRef` nor legacy
  `element_ref`. Authenticate the update by exact transition `type` and by
  the revision's tagged presence/value state: absent is different from
  present `null`, empty, or any other present value. Record those reads and
  write no reference. Do not infer selected-pack authority from this path.
- If either reference spelling is present, even with `null`, empty, or
  malformed data, omission is not a no-reference legacy state and must refuse.
  A new selected tuple without its reference must also refuse.

This explicit key-presence comparison is required; `.get()` and truthiness
cannot decide whether a revision or reference exists. The current ca9 handler
still requires a matching reference at `:100-104`, so the no-ref legacy case
is an Agent-owned source correction before a complete ACK. The schema's
optional transition revision is live for this authenticated legacy path; it is
not merely an unusable raw shape. A selected pair still requires the revision
because its `ElementRef` is selected authority.

Ownership/prerequisites:

- Agent: implement/document the two-path guard with an explicit missing
  sentinel and independent `elementRef`/`element_ref` presence; retain exact
  selected revision and project-pack authority checks.
- App: selected/new transition producers must carry the exact ref and
  retained `schema_source`; duration/parameter updates on a legacy no-ref row
  must copy the existing raw transition and omit `elementRef`, preserving the
  revision key's presence/value exactly.
- Runtime/App2: preserve literal presence/null states and do not alias,
  fabricate, or select a revision on behalf of either path.

## Scope/evidence boundary

Read-only `git show` probes were used against the frozen Main/App and Agent
identities and the current Runtime worktree. No product files, schema,
generated artifact, pin, registry, ledger, branch, or version were changed.
No full, HTTP, browser, renderer, live-socket, or passing-suite replay was
run. No new matrix or golden was made. This is a clarification report, not a
source-generation or consumer-qualification ACK.
