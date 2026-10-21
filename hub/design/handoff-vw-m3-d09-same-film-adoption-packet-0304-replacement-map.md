# D09 same-film public replacement map (dormant; one-to-one)

| Retained legacy assertion | Dormant public14 replacement | Retirement condition |
|---|---|---|
| `tests/core/timeline/test_onscreen_more.py::test_a_cross_fade_of_two_full_plates_is_covered_not_dip` | `tests/packs/rendering/test_d09_same_film_public.py::test_same_film_independent_fades_are_public_dip` — exact same `out` AM snap-plate + `in` AM-footage film, per-frame public evaluator answers: `COVERED/CONTENT` [0,16), `DIP/None` [16,30), `COVERED/CONTENT` [30,45), then GAP. | Retire only after the public14 packed/qualified artifact and the reviewed Agent AM-footage source/resources are both adopted on the active tuple, followed by independent Agent owner review. |
| Same-film incoming control required by the source report | `tests/packs/rendering/test_d09_same_film_public.py::test_same_film_incoming_transition_remains_covered` — same AM family through canonical incoming transition; all [0,60) `COVERED/CONTENT`, frame 22 incoming opacity 0.4666666666666667, frame 60 GAP. | Retain as a separate control; it does not justify retiring or rewriting the independent-fade assertion by itself. |

The original legacy assertion remains byte-identical (source-report digest
`80c31db3d2c74fecb5453abcf01f53ce3e4ee43c0d4b4d8b8f0a3634fa7ab0fa05`).
The settled MAIN6 pixel8195 proof is the authority for the explicit intended
difference: independent element fades DIP in frames 16..29, while the
canonical incoming transition remains COVERED. No public13 capability,
different film, fake row, pin change, package/release edit, or live retirement
is included.

