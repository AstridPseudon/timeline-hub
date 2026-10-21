# VW-D09b/c retained32349 default-crop equivalence map

## Result

The retained physical run proves only the complete explicit anchor
`mouth={x:151,y:104,w:19}`. Its private crop and public component inspection
crop are the same 640x360 rectangle `(298,202,345,219)` (799 pixels), and the
four retained PNGs reproduce the recorded natural, threshold, padding, and
planted-mismatch controls. This is a valid KNOWN positive for the explicit
anchor, not default coverage.

Default remains UNKNOWN for private equivalence: `model.mouth_box()` returns
`None` when `mouth` is absent, while the public component's normalized frame-0
diagnostic is known at `(894,606,1032,654)`, the same 799-pixel 640x360
coordinates. No retained default PNG exists, and public `mouthInspectionRect`
for absent input is `null`; no private/public pixel equality can be claimed.

## Exact source and retained evidence

- Physical test: `vw-m3-mouth-corrected-wrapper-one-run-0244-e2e-viewing-mouth-browser-guard-correction-0238-1021024258-32349`, exit 0, one test passed in 13.74s.
- Agent source: commit `ac4e004a664b96d58a00b66c7a2fa702a191f5bd`, tree `a36a38e234813638530d03a6916dc84768caa9dd`; graph label `d0a5072b`.
- Composition public13: 0.0.13, 77 members, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Node20.19.4: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`, SHA-256 `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- PNG directory: `/tmp/vw-m3-mouth-public13-0223-WpDP5W/pytest/test_actual_registered_present0/capture`.
- PNG hashes: frame-0 `fa68d076a79c9c553fc79fc83128c55da7ed542aed47640f6e571598b2e3b2f6`; frame-3 `ddea7b2cb0e89d3cca6df0bd7b70e160338122d5a72d4ad12bed1ebf14e08886`; frame-4 equals frame-0; frame-5 `79ef9e2d8d7c5456f463bd32e9432c0f9a47a60ccbc7601638f63822f1b425e7`.

## Geometry and controls

| Input | Private frame-0 geometry | Public behavior | 640x360 map / disposition |
|---|---|---|---|
| explicit `{151,104,19}` | `(894,606,1032,654)` | same compatibility region | `(298,202,345,219)`, 799 px; KNOWN positive |
| default absent | `None` | normalized diagnostic `(894,606,1032,654)`; `mouthInspectionRect` `null` | same public coordinates, but private equality UNKNOWN |
| partial `{x:151,y:104}` | `(894,606,1014,654)` | normalized diagnostic is full 19-wide region; legacy query `{x:149,y:101,w:20,h:8}` maps to `(894,606,1014,654)` | `(298,202,339,219)`, 697 px; geometry-known, no physical partial capture |
| raw-invalid `{x:'bad',y:null,w:900}` | `(-12,-18,5412,30)` | normalized diagnostic `(894,606,1158,654)`; legacy query `null` | private out-of-bounds; no equivalence claim |

Retained-PNG measurements use unchanged `CHANGE_LEVEL=18` and strict `>2%`:
natural old/public `0.42052565707133915` each and erase `0.8682170542635659`; planted 8 = old/public `0.010012515644555695`, erase `0.020671834625323`; planted 15 = `0.01877346683354193` vs erase `0.03875968992248062`; planted 16 = `0.02002503128911139` vs `0.041343669250646`; planted 20 = `0.025031289111389236` vs `0.05167958656330749`; padding16 = old/public `0.02002503128911139`, erase `0.0`. Hashes were unchanged after the in-memory controls.

## Limits

No browser, renderer/helper, Runtime, socket, central, full, new render, or
CPU-heavy qualification was run. The controls are analytical mutations of the
retained explicit-anchor PNGs, not default/boundary captures. Keep default
private equivalence UNKNOWN and retain the private fallback/statistics path;
no code, tests, caller, threshold, or production behavior changed.
