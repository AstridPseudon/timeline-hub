# actual19078 retained wire disposition

## Answer

Placement had a **pending intended commit**, not an absent commit. Both the original and retry1 retained traces contain one intended Runtime `/commit` POST with the safely derived operation `occurrence.add-media`; both completed with HTTP 200. The prior 0810 packet's `UNKNOWN` placement response is superseded only for this finite wire fact. No Runtime ordinal was correlated.

The complete machine-readable packet is `notes/19078-wire-disposition.json`. It contains the four trace ZIP hashes, endpoint counts, network/event member hashes, body-resource hashes, and parser limits. Request bodies were read privately and are not exported.

## Four retained traces

| case | intended `/v1/projects/.../timelines/.../commit` | commit POST | safe command ops | status | monotonic start → end | duration |
| --- | --- | ---: | --- | ---: | --- | ---: |
| element singletrace | PRESENT | 1 | `doc.patch` | `-1` / incomplete | `39700.067 → unavailable` | `-1 ms` |
| placement original | PRESENT | 1 | `occurrence.add-media` | `200` | `85990.415 → 97371.430` | `11381.015 ms` |
| placement retry1 | PRESENT | 1 | `occurrence.add-media` | `200` | `229954.714 → 241179.691` | `11224.977 ms` |
| SWAP | PRESENT | 1 | `occurrence.fork`, `occurrence.swap-media` | `409` / completed refusal | `431133.077 → 451301.598` | `20168.521 ms` |

Endpoint counts are respectively:

- element: handshake 6, inspect 2, import 0, commit 1; `0-trace.network` has 108 records.
- placement original: handshake 13, inspect 68, import 1, commit 1; `0-trace.network` has 495 records.
- placement retry1: handshake 13, inspect 68, import 1, commit 1; `0-trace.network` has 495 records.
- SWAP: handshake 6, inspect 9, import 1, commit 1; `0-trace.network` has 165 records.

All four network JSONL streams parsed through EOF with zero parse errors. The element `-1` is an actual incomplete network response record; its `response_resource` is absent. The other three commit records have retained response resources. Every commit `postData._sha1` resolved to a `resources/<sha>.json` member and was parsed privately for operation names.

## Source boundary retained

The SWAP source/trace boundary remains `runPopupCase933 -> accepted495`, before reload/Undo. Historical inverse `503` was not borrowed. The source operation is `occurrence.swap-media`; the retained body also contains the paired `occurrence.fork` command.

No new body, browser, HTTP, collector, Runtime replay, source repair, cache investigation, test, TypeScript check, lint, or full-suite rerun was performed. Existing Runtime catchall `ProtocolError` was not re-investigated.

## Verification

- Manifest, XML, and all four ZIPs parsed in place.
- ZIP SHA-256 values and the four source tuple hashes match the 0810 packet.
- `git diff --check`: PASS.
- App source worktree: clean; no product source changed.
- Full v2 request/reply guard fields are preserved in the JSON packet; no C0 guard was changed.
