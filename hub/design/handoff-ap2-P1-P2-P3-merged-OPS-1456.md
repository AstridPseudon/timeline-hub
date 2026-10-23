# Handoff: ap2 P1/P2/P3 merged/current583 D21 binding

The three approved App suite rows are statically ready on the exact owner-merged tuple:

- App `6294895141ffe0e92a83c61ba0541249a41243eb` / tree `03714e15af54da54865c1d732b2ea03900731fe1`
- Agent `58316fd6e0ce8a1fb3b2b3826ec71906d29080de` / tree `00c04a48841d95f5bf95dc604758767d2b065227`
- Runtime `cfa0af0d476e6954df041c08d7ef378fd6782932` / tree `3675f446c82c455ef5635ae725409eb6076a4f83`

Rows changed: `full-e2e-three-products`, `ap2-P3-gate5-h6-0348`, and `ap2-P1-chain-h6) only. Fresh benches are `venv-agent-child-ap2-current-583-cfa-1451` and `agent-remotion-ap2-current-583-cfa-1451), with matching 14:51/14:52 custody receipts.

Static extraction/syntax/execution passed for all three rows. Wrong source/tree/body probes refused. P1 now uses blob `daa50e369e46c859831e5a753013924aef179c31` and SHA `098d631e6536752963a5065b706bade4d1bedca89ee6d25b734a0f7686d17ca1`; current common harness is `3455a5ebcff5666081745ba90723465d6b656e9f`. Gate-5 and all P2 selector/body guards remain unchanged.

This handoff intentionally does not claim actual body qualification or common durability. The manager owns the one serialized P1 → P3 → P2 run and must stop before or report any failed real preflight.

