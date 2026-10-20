# Runtime a6a corrected consumer-probe evidence

Date: 2026-10-20 UTC

Candidate: `a6a11a806a51262192447fdeccc726b01ffd78fb`.

## Contract corrections

The scratch package is now in the worker worktree at
`workers/rt-m2-private613-client-probes/probes/`.

- Python resolves generated `ForwardRef` union leaves with the generated
  module's namespace before calling `get_type_hints`; the prior probe's
  `get_type_hints(ForwardRef(...))` crash was a probe defect.
- Python compares the generated `MutationReceipt` annotations with Main's
  `runtime_protocol/timeline_commit_types.py` and expects Main's actual
  `project_seq: list[int]`. It does not impose the TypeScript tuple shape on
  Python.
- The five intentionally open authored payload aliases
  (`ParentComposition`, `ShotPayload`, `TimelineConfig`, `RawTimelinePayload`,
  and `Document`) are allowed to retain `Any`. Representative closed fields
  (`ClipMoveArgs.on`, `WordAnchor.source`, `AgentRead.path`, and the producer
  pin) remain checked.
- TypeScript imports all source-bound definitions from the actual internal
  `timeline-commit-types` module. It checks the documented package-barrel
  surface for the seven new Args/`WordAnchor` exports and checks the direct
  `MutationReceipt` type is assignable both ways to Main's barrel receipt.

Compact fixture excerpts establishing those assumptions:

```python
return typing._eval_type(annotation, vars(module), vars(module), set())
assert candidate.MutationReceipt.__annotations__ == main.MutationReceipt.__annotations__
assert get_origin(project_seq) is list and get_args(project_seq) == (int,)
```

```typescript
import type { WordAnchor, TimelineInitArgs } from "__CANDIDATE_INDEX__";
import type { AgentRead, MutationReceipt } from "__CANDIDATE_TYPES__";
// @ts-expect-error Empty operation intents are closed objects.
const openEmptyIntent: EditCommand = { /* clip.delete v1 with an extra key */ };
```

The last expectation is intentionally the separate known
`rt-m2-closed-empty-intent-generator` red: a6a emits an open map for an
operation intent whose schema has `additionalProperties: false` and no
properties. No generator or generated artifact was changed here.

## Source and candidate identity

- Frozen Agent source commit: `357230816c86da65d5f8cc92b10a3a90d29874e0`
- Frozen schema SHA-256:
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`
- Schema inventory: 55 `$defs`, 29 operation clauses, 12 v2-capable
  operations (`track.set`, `shot.set`, `clip.set-params`, `clip.set-element`,
  `clip.move`, `occurrence.add-media`, `occurrence.swap-media`,
  `placement.move`, `placement.create`, `placement.unplace`, `shot.pool`,
  `clip.set`).
- Candidate digests are unchanged from the a6a run:
  - Python package init:
    `5e0b9adee1649d89d5447b5affb888b680943e992be6ef639cbf794acc68195d`
  - Python timeline DTO:
    `ad8deaf65feafb88158d2747d1df2751cde3a0f06d5f122e0d2827c91a846e9c`
  - TypeScript package index:
    `2d23f8ee1cb38e6b1d3366663887b88a4981ec298d8c8d5a758a62a7ad8cc0e4`
  - TypeScript timeline DTO:
    `970d306de53e35bb7cd8c599f84f1f5ae62ad23a425987c48048f962afe78828`

## Corrected probe results

Python command (private schema materialized from the frozen Agent commit):

```text
python workers/rt-m2-private613-client-probes/probes/python_reflection_probe.py <candidate> <private edit-command-357.json>
```

Results:

```text
PASS [closed command discriminants]
PASS [55 source definitions and closed fields]
PASS [public Args and WordAnchor exports]
PASS [Main MutationReceipt alias and list sequence]
FAIL [closed empty operation intents]: ... clip.delete v1, track.set v1, track.set v2, clip.set-params v1, clip.set-params v2, clip.set-element v1, clip.set-element v2, clip.add v1, clip.set v1, clip.set v2, clip.trim v1, clip.split v1, producer.guard v1, timeline.assembled-target v1, clip.add-media v1, timeline.init v1
PASS [old public provenance]
```

The Python process exited 1 solely for that known generator failure.

TypeScript command (placeholders replaced with absolute candidate `.js`
source paths):

```text
tsc --noEmit --strict --module NodeNext --moduleResolution NodeNext --target ES2022 <private typescript_consumer_probe.mts>
```

The compiler exited 2 with exactly one diagnostic:

```text
error TS2578: Unused '@ts-expect-error' directive.
```

That is the expected diagnostic for the same open `clip.delete` intent map.
There were no package-barrel `TS2305` errors; the previous 19 missing-export
diagnostics were probe imports of intentionally internal aliases. The public
Args/`WordAnchor`, closed discriminant, typed-field, and Main receipt checks
all compile as intended.

Legacy public schema/OpenAPI provenance passed. No full, native, HTTP,
provider, health, install, or shared-dependency suite was run.
