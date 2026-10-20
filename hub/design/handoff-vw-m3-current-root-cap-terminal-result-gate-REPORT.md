# Current-root three-still terminal result audit

## Verdict

PASS for the requested terminal-result gate. The one existing central request terminated `pass`, exit `0`, in `25s`; no retry, new grant, or new run was made.

Result: `vw-m3-current-root-cap-three-stills-prep-e2e-viewing-current-root-cap-three-stills-1020140356-7643`  
Snapshot: Composition tree `13e375534fffd704305eced5686699d2c8c9c948`  
Frozen controller SHA: `079fa981108214b0dac2d7f1453ae95fc716e2444ae4d6457d3cec538178dc97`  
Frozen manifest SHA: `4127d7e25aba66d57862af09a46368004fcda0a95c5c531ae80c0b0ae490dff9`

## Actual output

The captured metadata is `1920x1080`, `30 fps`, `durationInFrames=120`. Exactly three PNGs were emitted: frames `90`, `105`, and `119`.

| Frame | PNG bytes | PNG SHA-256 | RGB SHA-256 | Full histogram | Sample RGB (corner/center/corner) | Max RGB delta | Pixels >2/255 |
|---:|---:|---|---|---|---|---:|---:|
| 90 | 34422 | `7640face...a88444a` | `2677c0b2...70d9bd3` | 2,073,600 × `(240,240,240)` | `(240,240,240)` | 0 | 0 |
| 105 | 34427 | `c0b0adc7...d14431b` | `9b6f5046...5e3d69f` | 2,073,600 × `(122,124,130)` | `(122,124,130)` | 0 | 0 |
| 119 | 34429 | `12801737...a63be` | `3aeb1695...04a1cb` | 2,073,600 × `(13,16,28)` | `(13,16,28)` | 0 | 0 |

The independent native-RGB comparison against the exact frozen MAIN PNGs found zero differing pixels and zero channel delta for all three files. The controller's `comparison.json` agrees. PNGs are RGB (not an alpha-opacity channel), with no resize, padding, realignment, or tolerance waiver. Frame 105 RGB inference is `0.5`.

## Source and environment proof

- Frozen Agent revision `4ef1391c2c104d5d11b3a27265035c51be296045`, tree `afb2ed8506a99a088d7be3dbadaf593338d2fb5a`.
- Source manifest: 1,427 members / 76,351,190 bytes; immutable public12 package: 77 members, tar SHA `0a7b6152...77f0f1a3`.
- Dependency proof: `PASS`, 98 resolved source files, 367 edges, zero nonliteral imports and zero failures.
- Full f816 graph: 21,488 entries, SHA `9e556a87...acc425`; six peer hashes, admitted Node SHA `43d6cf63...bb99490`, and Chrome155 255-file tree SHA `5b9b48fa...de0e` match preflight and postflight.
- Postflight: `valid=true`, no errors, source outputs unchanged. Owned temp `/tmp/vw-cap-tyoz9eis` was removed. The central `CAPTURE-STARTED` marker records the result directory and remains as run provenance; the one-shot test marker was removed on completion.

Existing offline comparator controls passed unchanged: missing grant refused; exact three-PNG positive passed; one channel delta `+2` accepted; `+3` rejected; wrong dimensions rejected. The preparation log also retains an initial missing-fixture collection error followed by correction with the exact Git fixture and `5 passed`; this does not affect the central terminal result or pixel comparison.

## Scope and decisions

The only claim supported is **UNCERTIFIED static compiled currentRoot reference**. This is not evidence for normal Runtime admission, normal MP4/capture authority, Player/export parity, Gate 6, or audio. No intended pixel differences were approved; none were needed. Existing source proof was sufficient, so no additional TGZ or raw RGB copy was created.

No browser/render/network/install/service/full-suite action was initiated by this audit, and no worktree or shared dependency was modified. No blocker or failed comparison remains. Recommended next step is for the orchestrator to consume this bounded reference result while keeping the stated uncertified scope.
