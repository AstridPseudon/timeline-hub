# Trim source precision

`clip.trim` v1 and `Clip.trim` share `units.trim_source_interval`. New trims
author six-decimal **source seconds** and keep the existing speed rule:
playback duration is `hold / speed`. Registry duration remains authoritative
and unrounded. Reading, compiling, restoring or undoing existing films does
not normalize their authored windows or holds.

Resolve null endpoints from the current source window, defaulting missing
`from` to zero and missing `to` to the raw file duration `D`. Before rounding
or writing anything, require finite endpoints and `0 <= in < out <= D`.
A genuinely overrange raw request is refused even if rounding would fit.
Existing native source identity, unsupported source-map/window, provenance,
capture, replay and inverse guards remain in force.

The exact policy (all binary64 conversions use nearest, ties to even):

```text
Q = 1_000_000
E(x) = the exact rational value of the input binary64 number x
N(x) = binary64(nearest_even_integer(Q * E(x)) / Q)
I = N(in)
O = N(out)
if O > D:
    O = binary64(floor(Q * E(D)) / Q)
H = N(binary64(O - I))
refuse if O <= I or H <= 0
write from=I, to=O, hold=H
```

`N` is the existing Python `round(float(x), 6)`; unrelated `_r` calls are
unchanged. The interior floor uses exact multiplication, with no epsilon.
In particular, `D=1.0485929999999999` has an interior endpoint `1.048592`;
binary64 `D * Q` rounds up to `1048593.0`, so `Math.floor(D * Q) / Q` is
incorrect. Decimal-string ties and `Math.round(x * Q)` also do not reproduce
Python's binary64 nearest rule; the vectors include both tie directions.

The policy refuses a positive raw interval if its applied endpoints coincide,
including after moving the out point inward. It never stretches a collapsed
interval to manufacture a minimum duration. A file shorter than one
microsecond has no positive six-decimal source window. This is source
precision only: rational fps and half-open playback boundaries are unchanged.

Portable vectors are in
`tests/editing_conformance/fixtures/recipe_m2_clip_trim_boundaries.json`.
Start each case with the unchanged sibling `recipe_m2_clip_trim.json`'s
`input`; replace only `parent_revision.payload.registry.assets.picture.duration`
and recompute that payload's required content digest. Apply the case's `args`.
`applied` gives exact authored numeric values; `error` requires refusal before
writes. The original golden's commands, records and compiled output still
match exactly. Native tests exercise model parity, publication mirrors,
opaque data, child pins, exact replay/retry and guarded undo/redo.

| Raw duration | Requested out (`in=0`) | Authored out / hold |
| --- | --- | --- |
| 9.9999999 | 9.99999989 | 9.999999 |
| 9.9999999 | 9.9999999 | 9.999999 |
| 9.9999999 | 9.999999900000002 or 10 | Refused before writes |
| 0.0000009 | 0.0000009 | Refused: no positive authored window |

Source identity for the App handoff: integration base commit
`df2739f903edac02bd36b4446deeea847524c040`; the commit containing this fix is
assigned by the worker harness. Exact changed source **Git blob SHAs**:

| File | Blob SHA |
| --- | --- |
| `astrid/sdk/timeline/units.py` | `f30260efaef8f0d9d6735d4d13a042a8eadf4bee` |
| `astrid/sdk/timeline/_trim_commands.py` | `c5dd666a676d09c2a232e3f81031b736feb50916` |
| `astrid/sdk/timeline/model.py` | `2101f1e6611518b43a1c4f5bf57060df1ac6dbc5` |

The original golden's SHA-256 is
`4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152`.
The escalation's pinned native source commit
`76737ca2f9c86a075e7e03dfc8990e3090acc234` reproduces `to=hold=10` for
both below-end and exact-end requests; the corrected source and model both
produce `to=hold=9.999999`, preserving raw duration `9.9999999`.

Mirror this policy in App, then qualify its native capture parity against
these vectors and the untouched original golden. Runtime receipt retry,
browser preview and rendering require their own qualification; these native
domain tests make no claim about those paths.
