# d00 source-manifest mismatch handoff

Diagnosis: algorithm/fixture mismatch, not source drift.

- Frozen App: `d00a66134f330672ea7471dc69db38c1566d94cf`, tree
  `a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba`, 5,902 members.
- 0417 `prepare.mjs` / frozen d00 `harness.ts` algorithm: per-member hashes
  include `sha256:`; result `sha256:76694aa3...`.
- Historical 0417 literal `sha256:a2478c3c...`: identical paths, modes, bytes,
  and member content digests, but bare per-member hex (no prefix).
- First serialized difference: `!prev`, mode class `file`, 0 bytes,
  `e3b0c442...` versus `sha256:e3b0c442...`; no divergent source member.
- Frozen git tree has 5,902 paths; worktree is clean and `git diff --quiet`
  against d00 passes. `dist/` is ignored and not in the manifest.

Minimal supported correction for the owner: regenerate only the stale wrapper
expected literal to the existing prefixed algorithm's `76694aa3...` value.
Keep every source guard and d00 source identity unchanged. No correction was
applied here; see the worker REPORT for exact commands/results.

