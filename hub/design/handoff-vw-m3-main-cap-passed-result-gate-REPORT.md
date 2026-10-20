# Independent actual-result gate: PASS

The central test-service run `vw-m3-main-cap-locked-theme-stage-e2e-viewing-main6-locked-theme-image-cap-three-stills-1020115023-5447` passed with exit 0 in 38 seconds and produced exactly three stills: frames 90, 105, and 119. This worker consumed that result and did not recapture or rerun the browser, renderer, service, or product tests.

## Captured artifact identity

- Root metadata: `TimelineComposition`, 1920x1080, 30 fps, 120 frames.
- Binding: static-public executable analog using the original MAIN Root; explicitly not a live Runtime or App path.
- Original MAIN source: commit `a411628f8fd6129f9c58c332019b56769d997384` (the frozen `a411` source).
- Locked Composition 0.0.6: 29 regular members.
- Historical theme: version 0.1.1, 20 members; source tag commit `1db8440aabf0769b01453831a06f3c609bbc90c9`.
- Full physical dependency graph: checkout `f8164bef73215272562c4d6974acadbd82c2898a`, 21,488 entries, SHA-256 `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425`.
- The six peer postflight hashes are unchanged and postflight is valid (`source_byte_equal`, `graph_unchanged`, and `valid` are all true).
- The raw closure replay held `raw_hold=5` and projected/serialized hold at 4; all seven consumer outputs are byte-equal.

PNG bytes were preserved. The three exact files are:

| frame | bytes | SHA-256 |
|---:|---:|---|
| 90 | 34,422 | `7640face10c33eb4c8682b890ddcc6faacaf0e57c0810e9438e4b2df8a88444a` |
| 105 | 34,427 | `c0b0adc7856e2750137315451a9657661925436746d0da1e9cd6a2527d14431b` |
| 119 | 34,429 | `128017371420be346796916879dc2e5faac0f2761d5025018e392913abea63be` |

## Independent RGB measurement

The instrument ran against the original 16x16 RGB240 source, explicit RGB background `(5, 8, 20)`, frame 90 as the opaque control, and ROI `(192, 108, 1536, 864)`. It used RGB only: no resize, realignment, frame-membership rounding, or PNG alpha as layer opacity. Control confidence was 1.0: source match 1.0, background informative fraction 1.0, control RMSE 0.

| frame | RGB-derived observed fraction | channel fractions (R/G/B) | conservative bounds | source prediction fit |
|---:|---:|---|---|---|
| 90 | `1.000000000` | `1.000000000 / 1.000000000 / 1.000000000` | `[0.995454545, 1.000000000]` | `1` fits |
| 105 | `0.500000000` | `0.497872340 / 0.500000000 / 0.500000000` | `[0.493617021, 0.504545455]` | `0.5` fits |
| 119 | `0.034482759` | `0.034042553 / 0.034482759 / 0.036363636` | `[0.029787234, 0.040909091]` | `1/30 = 0.033333333` fits |

The median quantization intervals are, respectively, `[0.995689655, 1.000000000]`, `[0.495454545, 0.504310345]`, and `[0.030172414, 0.038793103]`; the source predictions remain inside those intervals. These are RGB measurement results and quantization diagnostics, not an actual-opacity assertion.

## Scope and limits

- No new domain policy or threshold was introduced.
- No visual golden was selected.
- No App/Runtime live-path or unified viewer parity claim is made.
- The earlier `1020113140-6461` attempt remains failed before frame capture and is not combined with this PASS.
- No repository source files were changed. No full suite, product test, network, socket, install, or shared dependency write was run by this worker.

## Recommended next step

Keep the central PASS and this independent measurement as evidence for the orchestrator’s review. Any later parity or live-path claim requires its own explicitly authorized evidence.
