# P2 normalized inverse correction handoff

Source-only correction completed against App base `7ada5a22afaf032cc3698b3e2c5c1a71560967c3`. The only worktree change is `tests/e2e/local/three-products.p2-tour.spec.ts` (67 additions, 8 removals).

## Contract correspondence

`assertNormalizedCommands` checks every submitted field with exact equality, including full operation/version/select/args/publications and optional submitted guards. It permits only the known fields added by `commands.execute` / `Recording.finish`; intent and resolved defaults remain exact. Authoritative commands are never reduced to a metadata-free projection: the complete reply array equals the complete recorder command array. Command counts and ordinals remain exact.

For mounted modern `doc.patch`, ordered submitted changes equal the recorder's operand bindings, while physical refs and normalized paths equal the exact authoritative step patches. The original root-addressed request and normalized `config.clips` effects remain distinct. Submitted step metadata is checked exactly and reply/history/recorder steps retain complete patch/dependency equality.

The ABI-1 Undo request stays minimal, with exact `timeline.inverse` envelope and publications. Synthesized default label, step identity/metadata, nonempty patch/dependencies, effective fields mode and exact source stay asserted. Full history equality after reload, preservation of every prior entry after Undo, and a repeated full history read retain all records, captures, bindings, steps, dependencies and receipts.

Two additional concrete false claims were corrected without weakening behavior:

- Native external dependency pins are exactly empty for this unanchored doc.patch/inverse tour. These differ from nonempty field/scope `steps[].dependencies`, which remain required. Source: `_recording.py`, `_doc_patch.py`, `inverse.py`, `_commit_patch.py`, `native_word_anchor.py`.
- Clearing a transition legitimately updates the mirrored `config.clips`. Every other config field remains exact; existing raw order/absence/opaque preservation and intended-field allowlist continue to cover both mirrors.

Read PLAN and C0 §§1/3/4/5/7, ef6c/7ada and independent 0436 FAIL; consulted the independently reviewed P3 `expectV2History` distinction between submitted claims and normalized authoritative recorder commands, without copying its large helper. Read actual App A2 handoff/outbox/provider, Agent `commands.py`, `capture.py`, `_recording.py`, `_doc_patch.py`, `_commit_patch.py`, `inverse.py`, `commit.py`, `_commit_preview.py`, and Runtime normalization/history/auth/schema sources read-only. Inspected Agent head `9729c07b764ba6cce1bb31686cb93d29fc72b14d` and Runtime head `62c454ac07fb46a1a67847d933f1ed5f53043e30`.

## Exact final checks

From `/home/user/work/wt/ap2-P2-normalized-inverse-sol-0440`:

```bash
scratch_dir=$(cat /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-normalized-inverse-sol-0440/tmpdir)
TMPDIR="$scratch_dir" PLAYWRIGHT_OUTPUT_DIR="$scratch_dir/playwright-output" npm exec playwright -- test --config playwright.three-products.config.ts tests/e2e/local/three-products.p2-tour.spec.ts --list
npm exec tsc -- --noEmit
npm exec eslint -- tests/e2e/local/three-products.p2-tour.spec.ts --max-warnings 0
git diff --check
```

All exited 0; exactly 3 tests in 1 file listed; ESLint had no warnings. Root project TypeScript excludes e2e and does not establish test-file typechecking. Initial list invocation used the `tmpdir` pointer file itself and failed ENOTDIR; resolving its private `/tmp/w-9c1e4329ef` path fixed listing without cleanup or shared dependency writes.

## Production caller gap / later execution

Evidence contradicts the prior handoff's claim that mounted Undo already calls `RuntimeDataProvider.undoTimeline` on this base. `useTimelineState.ts:641` installs `useTimelineHistory`. That hook initializes its Undo stack as an empty in-memory ref at line 212; toolbar Undo at line 424 requires that stack and restores a snapshot through `commitData` at line 314. There is no production call to `undoTimeline` beyond exposing its provider forwarder. A page reload recreates the local stack. The test still requires the real mounted Undo to submit the minimal guarded inverse; no snapshot workaround, direct test submission, refusal, skip or weakened outcome was introduced.

The source correction is complete; behavioral execution remains unqualified. The orchestrator should resolve or verify that product caller on the current joined cohort before accepting execution proof. Then run the original three cases through the central service, with resolver merge `616ee85b86db6c1d8506a5b74ba13e62b91f0061` included. Future D13 reads are not forced into this 66b-based request; omitted reads/atomic is preserved. Merged/conflict/invalid/preview obligations are separate.

No browser/socket/service/body/build/full run, product/config/schema/generated/pin/lock/launcher/suite changes, fixtures, TypeScript executor, test deletion, commit/merge/checkout/push/ref mutation or shared dependency mutation occurred.

Worker report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P2-normalized-inverse-sol-0440/report.md`.
