# P1 encoder current review handoff

## Verdict

**FAIL for current combined feasibility + encoder evidence.** The new encoder tests pass 2/2, but the mandated combined run fails 8 provenance tests in `p1FeasibilityCorpus.test.ts` because Node child-process calls report `spawnSync git EPERM` in this worker runtime. Shell-level `git show`/SHA-256 verification independently matches all eight recorded source hashes, so this is an execution-environment failure rather than a source-hash mismatch; it nevertheless blocks a green review result.

Source under review: `fc714799b019387435009a59e62b309b4c9f1919`, tree `3ee79e814560c1e5cb324000dc8d9b6b65de279e`. The sanctioned merge-forward is still in progress with `MERGE_HEAD=794d365ae03725453c3359d21c791b1ffe7ccee9`, which contains required ancestor `78e7eafa3974718b673f9bf3b08cc95a26654676`. No merge or commit was run by this reviewer.

## Evidence

- Vitest combined command: **FAIL**, 1 failed file / 14 tests; `p1FeasibilityCorpus`: 8 failed, 4 passed; `p1EncoderCorpus`: 2 passed.
- `node node_modules/typescript/bin/tsc --noEmit`: **PASS**.
- `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/p1EncoderCorpus.test.ts --max-warnings 0`: **PASS**.
- `git diff --check`: **PASS**; supplemental `git diff --cached --check`: **PASS**.
- The split fixture is genuine, not a fabricated row: its pinned Agent fixture is covered by the existing golden test that executes split and compares records/output/command exactly.
- No split→trim success or mounted transport success is claimed; corpus status remains `authored-not-go`.

## Qualification gaps

The App trim encoder test has a complete exact delta and checks null/absence, clears, mirrors, roots, and created IDs. The split encoder test is only partial: it checks insertion/order metadata and created ID but not the full generated delta, split target changes, complete inserted payload, roots, mirrors, or preserved fields.

`documentPatchIntent` has no production caller; repository search finds only its implementation and tests. Thus the new file proves the encoder in isolation, not the acceptance phrase “the production caller uses it.” The v2 request/reply fields and H3 mixed-command/restart chain remain unverified.

## Required follow-up

Rerun the exact combined command in a child-process-capable test environment without weakening provenance checks. Then add complete split-delta assertions and qualify a real production caller and the mounted split → trim-new-clip → intervening Agent edit → lost ACK → restart chain. Keep this as FAIL until those results are green and the full v2 contract boundary is separately evidenced.
