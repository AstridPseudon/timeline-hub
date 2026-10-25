# Report — P2/A2 whole-path investigation

## Outcome

No product or test files changed. The retained D97 SWAP run proves:

- Initial SWAP request was sent and accepted: HTTP 200, history/reload checks passed.
- Intended native Undo request was sent with the correct `timeline.inverse` envelope.
- Undo failed at the Runtime unknown-outcome boundary with HTTP 503 `not_ready/runtime_unavailable`.
- No inverse acceptance, receipt, terminal history, or eventual outcome was retained.
- Exact failing owner and missing input are UNKNOWN; no product fix is justified.

## Action correlation

| Action | Retained evidence |
|---|---|
| Initial SWAP | POST present; ordinals `[0, 1]` (`occurrence.fork`, `occurrence.swap-media`); provider `astrid-v1`; accepted result/history/reload passed; HTTP 200. Exact mapping to private phase ordinal is unavailable. |
| Native Undo | POST present; ordinal `[0]`, `timeline.inverse`, targeting the accepted SWAP publication; `merge: fields`, `reads: []`, correct label/step/source envelope. HTTP 503 after ~3.157 s; test failed at `accepted(inverse)` before receipt/history assertions. |

The App outbox retains and retries 5xx unknown outcomes using the exact request. App source construction is therefore not the proven failure owner.

## Runtime phase boundary

`p2-commit-phase.jsonl` retained 128 events, reaching the capture cap.

- Two requests have complete provider → accept → receipt → HTTP 200 phase coverage.
- The only incomplete phase request reaches provider start and six authorization events, then ends without provider completion, accept, receipt, coordinator completion, or HTTP phase.
- The phase capture has no safe request-body/hash correlation, so assigning that private ordinal to Undo is UNKNOWN.
- No correlated phase watchdog `.stacks.txt` or 0600 observer dump exists.
- The 158 terminal metadata files are not phase watchdog dumps; 157 report `response`, one reports `failed`, with no safe correlation to the Undo POST.

Runtime source has two generic 503 unknown-outcome routes: coordinator lookup failures and service-level unexpected commit failures. The retained evidence cannot distinguish them. Agent inverse code requires authenticated accepted history/closure inputs, but no structured refusal or missing-input detail was retained.

## Comparator limits

Passing native Undo evidence exists for:

- `single5678`: App `24865fa…`, Agent `6386c700…`, Runtime `6634a17…`, Composition `635f4de0…`
- `asset27438`: App `5337b439…`, Agent `6386c700…`, Runtime `6634a17…`, Composition `635f4de0…`

Both validate the native request/reply shape, but they are different tuples and inputs. They do not establish a common authentication, cost, or provider cause for current SWAP tuple App `3199118d…`, Agent `5faeec5b…`, Runtime `0c62dfa6…`, Composition `635f4de0…`.

## Evidence validation

- Retained preflight: PASS.
- Retained readiness: 1 PASS, 24.956538 s.
- Retained original: 1 FAIL, 76.766014 s, inverse HTTP 503.
- Manifest/source test hashes: PASS.
- JUnit XML parsing: PASS.
- Phase JSONL parsing: PASS, 128 events.
- Trace JSON parsing: PASS, 62 JSON entries.
- Sensitive-pattern scan of retained stderr: 0 matches.
- Pinned commit/tree identity checks: PASS.
- Assigned worktree: clean.

No browser, full suite, build, install, new collector, replay, or timing/security probe was run. Required commit message and empty `DONE` marker were created.