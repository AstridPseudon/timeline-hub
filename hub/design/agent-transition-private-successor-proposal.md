# Agent private incoming transition SET successor proposal

Status: **PROPOSED FOR App2 and Runtime AGREEMENT; no generation or activation**.
This is a source-only handoff for the current Agent ordinary root. It does not
change public 0.0.13, ordinary 0.2.14/6ba, or private 357/613 artifacts and
does not authorize an App cast, Runtime DTO, endpoint, or consumer pin.

Date: 2026-10-20

## Exact source and frozen inputs

| item | identity |
| --- | --- |
| Agent source root | `tl/agt-m2-transition-current-native-contract`, HEAD `490c10ac12d55f75d698213487353a7912d33067` |
| Agent source tree | obtained with `git rev-parse HEAD^{tree}` before the candidate edit |
| current ordinary schema | `astrid/core/timeline/schema/edit-command.schema.json`, SHA-256 `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef` |
| App prerequisite | public Composition 0.0.13, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` |
| App observed source | `ElementsLibraryPanel.tsx` -> `runtime/element-adapter.ts`, as named by `ap2-m2-element-remaining-literal-ingresses-REPORT.md` |
| Runtime prerequisite | Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` are the current App report tuple; neither is changed by this proposal |

The source candidate must be compared to the exact current tree after the
harness finishes. No generated schema, Runtime client, artifact, release, or
pin is produced by this worker.

## Closed carrier contract (additive private proposal)

The existing ordinary operation remains the carrier: `clip.set`, version `1`,
one command selected on the incoming/TO clip. No alias operation is proposed.

```json
{
  "values": {
    "transition": {
      "type": "<element id>",
      "duration": "<positive authored seconds>",
      "revision": "<exact descriptor revision>",
      "params": "<complete literal params when present>",
      "<other own keys>": "<opaque literal values>"
    },
    "elementRef": {
      "id": "<same element id>",
      "kind": "transition",
      "revision": "<same exact revision>",
      "packId": "<exact selected pack owner when present>"
    }
  },
  "clear": []
}
```

For apply and update, `transition` and its matching `elementRef` are required
as one SET pair. This records both destination fields atomically. `duration`
is authored seconds, not compiled frames; `type`, `revision`, and pack identity
are literal retained declarations. Compiled-only `id`, `durationFrames`,
`align`, and `incomingPolicy` are refused in the transition body. Known selected
properties are validated only through the exact retained declaration selected
by `schema_source`; unknown properties and nested JSON remain opaque.

Remove uses the existing ordinary clear body and no null sentinel:

```json
{"values": {}, "clear": ["transition"]}
```

The handler atomically records and clears the destination clip's `transition`
and both stored element-reference spellings (`elementRef` and legacy
`element_ref` when present). Inverse restores their exact prior presence,
including absent/null/opaque distinctions. No other clip fields are touched.

## Capture and guards

- App `timeline.apply_transition` captures the TO clip's stable native select,
  complete raw transition, and exact catalog `elementRef` through the existing
  scalar carrier. Update recaptures the current target and carries all
  unmentioned transition keys forward; it does not select by type only.
- Parent and occurrence-owned clips use the current `_target`/owner binding and
  existing scalar image dependency. The handler records target identity, owner,
  source asset identity/digest, owning track, retained rational FPS, and the
  `transition.predecessor` selection (same-lane immediate predecessor, stable
  order with collection-order ties, and track boundary). Other lanes remain
  independent. No adjacency, successor-fit, renderer, or shortest-clip write is
  invented; incoming compilation owns its window policy.
- Apply/update require the exact destination descriptor and matching id/kind/
  revision/pack owner. Selected project-pack inputs require the existing exact
  `schema_source` DocumentPin and verified immutable snapshot resolver; a latest
  or type-only declaration is refused.
- Replay uses the original captured body and guards. Inverse uses the existing
  guarded write/read/selection machinery and refuses later same-lane transition
  writes, including A→B→A. A newly introduced DocumentPin is not removed by
  this candidate unless the existing retention seam can prove that no later
  record depends on it; the first-selected-transition exact-document inverse
  assertion remains strict until that primitive exists.

## Golden source and peer gate

The golden source is the existing App three-products raw fixture:
`tests/editing_conformance/test_recipe_clip_scalar_fields.py::app_closure`
and `tests/editing_conformance/fixtures/recipe_m2_app_clip_scalar_fields.json`.
It is reused; no transition matrix or copied schema fixture is proposed. The
representative target is `parent/clip:f2-transition-clip`, predecessor
`parent/clip:f2-app-clip`, FPS 30. The candidate record must show one paired
SET write for apply/update and two clear writes for remove, with exact inverse
and replay.

App2 and Runtime must ACK this closed body, version, capture/record shape, and
golden source before normal schema generation, client generation, or activation.
Until both ACKs and a matching native pair exist, this remains an Agent source
candidate only; no App writer deletion or D01 closure is claimed.
