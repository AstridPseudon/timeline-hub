# VW-D09b/c retained32349 default-crop equivalence map

## Result

The retained physical run proves only the complete explicit anchor
`mouth={x:151,y:104,w:19}`.  Its private crop and public component inspection
crop are the same 640x360 rectangle `(298,202,345,219)` (799 pixels), and the
four retained PNGs reproduce the recorded natural, threshold, padding, and
planted-mismatch controls.  This is a valid KNOWN positive for the explicit
anchor, not default coverage.

Default remains UNKNOWN for private equivalence: `model.mouth_box()` returns
`None` when `mouth` is absent, while the public component's normalized
diagnostic is known at frame 0 as `(894,606,1032,654)`, i.e. the same 799-pixel
640x360 coordinates.  No retained default PNG exists, and the public
`mouthInspectionRect()` query for absent input is `null`; no private/public
pixel equality can therefore be claimed for default.

## Exact retained qualification tuple

- Physical test: `vw-m3-mouth-corrected-wrapper-one-run-0244-e2e-viewing-mouth-browser-guard-correction-0238-1021024258-32349`, central exit 0, one test passed in 13.74s.
- Agent source used by the central run: commit
  `ac4e004a664b96d58a00b66c7a2fa702a191f5bd`, tree
  `a36a38e234813638530d03a6916dc84768caa9dd`; the selected Remotion graph
  label/path was `agent-remotion-viewing13-d0a5072b`.  The report names the
  production presenter source parent as `4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a`.
- Composition public13: version `0.0.13`, 77 regular members, artifact
  SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Node: `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`,
  v20.19.4, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.

## Retained bytes

Source directory:
`/tmp/vw-m3-mouth-public13-0223-WpDP5W/pytest/test_actual_registered_present0/capture`

| PNG | SHA-256 |
|---|---|
| `frame-0.png` | `fa68d076a79c9c553fc79fc83128c55da7ed542aed47640f6e571598b2e3b2f6` |
| `frame-3.png` | `ddea7b2cb0e89d3cca6df0bd7b70e160338122d5a72d4ad12bed1ebf14e08886` |
| `frame-4.png` | `fa68d076a79c9c553fc79fc83128c55da7ed542aed47640f6e571598b2e3b2f6` |
| `frame-5.png` | `79ef9e2d8d7c5456f463bd32e9432c0f9a47a60ccbc7601638f63822f1b425e7` |

The retained `inspection.json` records one component-zero query for
`presenter` at the public mouth ROI `(894,606,138,48)`, basis 1920x1080 at
30fps, output PNG size 640x360.  No PNG was written or changed here.

## Geometry map

The private values below are the existing Agent `model.mouth_box()` frame-0
calculation.  The public diagnostic is the normalized component region; the
public legacy inspection query is `mouthInspectionRect()` projected through
the same frame-0 view.

| Input | Private `mouth_box` | Public normalized diagnostic | Public legacy inspection query | Disposition |
|---|---|---|---|---|
| explicit `{151,104,19}` | `(894,606,1032,654)`; crop `(298,202,345,219)`, 799 px | same | known explicit compatibility crop `(298,202,345,219)` | KNOWN physical positive |
| default / absent | `None` | `(894,606,1032,654)`; crop `(298,202,345,219)`, 799 px | `null` | UNKNOWN private equivalence |
| partial `{x:151,y:104}` | `(894,606,1014,654)`; crop `(298,202,339,219)`, 697 px | `(894,606,1032,654)`; crop 799 px | `{x:149,y:101,w:20,h:8}` -> `(894,606,1014,654)`; crop 697 px | geometry-known legacy match; no physical partial capture |
| raw-invalid `{x:'bad',y:null,w:900}` | `(-12,-18,5412,30)`; out-of-bounds crop `(0,0,1805,11)` | `(894,606,1158,654)`; crop `(298,202,387,219)`, 1513 px | `null` | UNKNOWN/refused legacy equivalence |

The public query also reports `mouthAnchor(raw-invalid)` as the normalized
fallback `{x:151,y:104,w:40}`, but its inspection query refuses the malformed
raw input.  These are distinct facts and are not a private crop replacement.

## Retained-PNG controls

All measurements below used only the four retained PNGs, the existing crop
coordinates, and the existing comparator semantics (`CHANGE_LEVEL=18`, strict
`fraction > 0.02`).  Natural pairs are 0→3, 3→4, and 4→5.

| Control | old/private crop | public compatibility crop | erase crop | Result |
|---|---:|---:|---:|---|
| natural pairs | `0.42052565707133915` each | `0.42052565707133915` each | `0.8682170542635659` each | old/public equal; KNOWN explicit positive |
| planted 8 | `0.010012515644555695` | `0.010012515644555695` | `0.020671834625323` | old/public below threshold; erase above |
| planted 15 | `0.01877346683354193` | `0.01877346683354193` | `0.03875968992248062` | old/public below threshold |
| planted 16 | `0.02002503128911139` | `0.02002503128911139` | `0.041343669250646` | old/public above threshold |
| planted 20 | `0.025031289111389236` | `0.025031289111389236` | `0.05167958656330749` | all above threshold |
| padding 16 | `0.02002503128911139` | `0.02002503128911139` | `0.0` | old/public detect padding; erase does not |

The analytical probe re-hashed all four source PNGs after measurement and
matched the hashes above.  The controls are mutations of in-memory copies;
they are not new captures or physical default/boundary inputs.

## Tests, limits, and next step

Passed:

- Inline retained-PNG probe using PIL and the existing comparator algorithm:
  source hash verification, 640x360 metadata, natural pairs, 8/15/16/20
  planted controls, padding16, and post-probe hash stability — PASS.
- `git status --short --untracked-files=all` — PASS, clean Agent worktree.
- `git diff --check` — PASS (no repo diff).

Not run by instruction: browser, renderer/helper, Runtime, socket, central,
full, new render, or CPU-heavy qualification. Existing geometry/helper tests
were read for the source map but not executed. The one bounded remaining gap
is a real default (and, separately, partial/raw-invalid) retained PNG pair;
until such bytes exist, keep the default private/public equivalence UNKNOWN and
keep the private fallback/statistics path live. No caller, test, threshold, or
production source was changed.
