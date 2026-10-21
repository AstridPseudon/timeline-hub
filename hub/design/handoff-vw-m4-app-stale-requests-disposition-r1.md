# Viewing stale App request disposition

Reviewed 2026-10-21 against App `tl/integration` at
`e1e153091b23aeafd09a15c500616384fba4330a` (tree
`aa20a99731b91c2fa5e36b258c131147f3d7d651`), the successor table, current
reports/merge records, and the App 04:17 opaque-root safety directive.

## Twelve stale `vw-m3` records

All twelve are **SUPERSEDED**. The cited successor is an actual ancestor of
the current App integration; no unchanged test was rerun.

| Request | Current successor and retained assertions |
| --- | --- |
| `vw-m3-app35-pcm-preserve-progress` (`30b8df289`) | App `ea38656fe62950440b36cafee780698cff2c3f9c`; `AudioTrack.tsx`, `AudioTrack.test.tsx`, and `continuousPCM.lifetime.test.tsx` retain progress renewal, readiness/stall, retry/abort/close/URL, envelope, boundary, occurrence, and export assertions. |
| `vw-m3-cap-es2020-last-own-call` (`4256efc2e`) | App `a8283307a7a5537a95988031b385ef28df7524ea`; `shotTimelineDataProvider.ts` retains the safe own-property call and `ShotTimelinePreview.test.ts` retains raw-key, collision, publication, and popup-recovery assertions. |
| `vw-m3-cap3a-corrected-consumer-port` (`8488f9c1c`) | App `a8283307a7a5537a95988031b385ef28df7524ea`; stored-cap, render-bound, and command-session projection assertions are retained. |
| `vw-m1-projection-labels` (`5c7ff0a8b`) | Current carriers `af218d0260d81a602f5b34bc8fafc0b7e63987df` plus lifecycle successors `8a79a7bb9` and `5404ca470`; paired geometry, original-base/B-local behavior, refusal, and remount/recovery assertions are retained. |
| `vw-m3-app-pure-opacity` (`df6ba7120`) | App `927545cf52fdfbb273afbe7f190e00e11e5e2d70`; public `clipOpacity` evaluation and fps/speed/boundary assertions are retained. |
| `vw-m3-flat-compiled-source` (`b23108926`) | Current carriers `af218d0260d81a602f5b34bc8fafc0b7e63987df` and `927545cf52fdfbb273afbe7f190e00e11e5e2d70`; flat-local/accepted projection, late graph, clear, and native omission assertions are retained. |
| `vw-m3-initial-projection-mounted` (`910773b31`) | App `927545cf52fdfbb273afbe7f190e00e11e5e2d70`; graph-free initial projection, frame cases, revision/config pairing, delayed generation, and lifecycle assertions are retained. |
| `vw-m3-d08-public-trim-delete` (`3812ff4c8`) | App `9d518546df880ec515f2f424c55073193f2a2e64`; public `computeMediaTrim` re-export and visible-time/boundary/malformed-fps assertions are retained. |
| `vw-m3-app-pcm13-preserve-audible-cases` (`70e378e3f`) | App `ea38656fe62950440b36cafee780698cff2c3f9c`; public envelope, speed/fade/boundary/overlap/curve, occurrence/mute/boost, PCM source-clock, retry/abort/close/URL, and stalled-preparation assertions are retained. |
| `vw-m3-native-frame-fixture-frozen-pair-proof` (`e4c7a3792`) | App merge `4553d4b8c7a7fdf226b25634660c63da9f0c947a`, followed by current canvas successor `0f62205256a816a0d46f3f5b2c1ef9e1670564ed`; Runtime/producer/Agent identity, archive/tree, module-origin, ordered `PYTHONPATH`, manifest, restore, forged-task, and zero-write assertions are retained. |
| `vw-m3-audio-join-existing-contract-fix` | Actual App integration merge `480db7febe624fe4658a75cbdb66ed5de84c2c61`; full audio-join assertions and negatives from `a4b1a30d1` are retained. Hub status record updated without deleting its original text. |
| `vw-m3-owner-five-current-base-port` | Actual App integration merge `5af486a0fa99ff0c3092f75026cea0e9e055f909`; owner-five source guards/assertions are retained. Hub status record updated without deleting its original text. |

No concrete conflict remains among these twelve. Controller `e9d04f4bf`,
physical PCM `a6fa6ff8c`, native canvas `0f6220525`, and the bounded D08 cuts
(`bdeb5e97e`, `a12b19be5`, `dce7eea63`) are existing current proofs/context,
not additional stale requests and were not replayed.

## Separate manager action: safe-error request

`vw-m3-payload-latest-home-final-forward-0404` at
`822bafd4531b4dbdc2e694801ece0a69dae6beae` remains **MERGE** (manager action
required). It is not an ancestor of current integration and is not superseded
by an equivalent current assertion set. Its exact delta is limited to:

- `tests/e2e/timeline/viewing-parity/bootstrap.ts`: retain validated
  `error_type`/`error_location` in the helper failure message while redacting
  unknown fields;
- `tests/e2e/timeline/viewing-parity/harness.test.ts`: preserve that safe
  failure cause when startup cleanup also fails, while asserting credential
  redaction.

The 04:17 directive remains binding: preserve opaque roots, refuse unsafe
headless overwrite visibly, and do not broaden routes, DTOs, pins, or source
authority. No merge was requested by this worker.

## Limits

Read-only classification only. No product/source/pin/authority change, test,
browser, build, install, full suite, census, or Git mutation was performed.
