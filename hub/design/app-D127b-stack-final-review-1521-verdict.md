# D127b corrected1518 bounded review

## Verdict

- Packet privacy: **PASS** for the durable corrected Git packet. The checked JSON and safe-frame outputs contain only relative frame fields, counts, shares, artifact hashes, and the retained key hash; no raw payload, key preimage, auth, private URL, absolute path, local, or raw stack text is present.
- Packet content custody: **PASS**. The corrected Composition commit SHA is `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` in both corrected custody bindings; the full four-repo commit/tree manifest and helper hash match the exact manifest; the only tracked 1518 delta is metadata/binding.
- Required absolute-input persistence: **FAIL**. The advertised parent path `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127b-stacks-binding-return-1518/evidence` is absent after worktree recycling, and its ignored `handoff.md` is not in the durable corrected Git ref. The corrected four-file packet is available from `tl/app-D127b-stacks-binding-return-1518` at `b48fa11ab5`.
- Overall packet custody: **FAIL** solely because the brief makes missing absolute evidence a failure.
- Request binding: **UNKNOWN overall**. The retained element trace has an exact key-hash join to Runtime launch d22 request 3. SWAP remains UNKNOWN. Runtime outcome, handler end, response, and request-wall denominator remain UNKNOWN. No request-2 timing or ordering attribution is made.

## Byte and delta checks

The three safe frame outputs are byte-identical to original1503 commit `48464827`: hashes `7d5d143c…`, `5f07fda1…`, and `e8e0824d…` match exactly. The 1518 corrected ref changes only `facts.json`, `privacy-check.json`, `request-binding.json`, and `stack-index.json`; no source, test, generated, or pin files changed.

## Tests

N/A by brief: read-only JSON/schema/hash/count/privacy/custody review. JSON parsing and the bounded invariants passed. The exact commands and results are recorded in the final report.

## Next step

Republish the corrected packet, including `handoff.md`, under the required permanent worker-root absolute path, then rerun this bounded review. The content-level corrected verdict should remain privacy PASS, custody-content PASS, element EXACT_JOIN, SWAP UNKNOWN, and outcome UNKNOWN.
