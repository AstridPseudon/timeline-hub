# D127b independent safe-stack packet review

## Verdict

- Packet privacy: **PASS**.
- Packet custody: **FAIL** because `evidence/facts.json:2752` retains the stale Composition commit SHA `635f4de06da22a85fc2e4cfc764d0153a4c9f40`; the exact manifest requires `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`. `stack-index.json` and `handoff.md` are corrected, and all three safe frame byte hashes are unchanged from original1503 commit `48464827`.
- Request binding: **UNKNOWN overall**. The retained element Playwright network trace contains a header whose local hash matches retained Runtime launch-d22 request 3, with the Runtime namespace/PID-birth/request/UTC evidence; the Runtime outcome remains UNKNOWN. Retained SWAP trace header hashes do not match any Runtime key, so SWAP remains UNKNOWN. No operation success, timing, dominant-cost, or order inference is made.

## Coverage and privacy

The three present stack artifacts reconcile to the exact 10721 source hashes, sizes, line counts, and frame counts: root 62/50, launch-1b97 72/60, and launch-d15d 74/62. The three absent launch stack paths are verified absent; all six retained JSONL source hashes and sizes match. Safe output contains only relative frame labels, lines, functions, counts, shares, and hashes; no raw stack text, payload, key preimage, auth, private URL, absolute path, or local is published.

## Tests

N/A by brief: this was a read-only JSON/schema/hash/count/privacy/custody review. No source, test, generated, pin, product, or branch state was changed.

## Next step

Correct the one stale Composition SHA in `facts.json` and reconcile `request-binding.json` with the retained element-trace key match, then rerun this independent custody check. Keep SWAP request binding UNKNOWN unless a retained exact key-hash join is available.
