D101’s finite paired candidate is complete and **unmerged**. Commit message and `DONE` are written; the Runtime commit awaits the harness.

Runtime `validate_step()` now requires two lossless physical field guards: raw `registry`, and config `registry` (or config itself when absent/malformed). Agent `CommitPatch.finish()` emits the same union. Existing rebase and guarded-undo consumers use that index. Native captures, declared scopes, selection/binding guards and atomic fallback remain intact; Store/D97/history memo are untouched.

Validation:

- **RED:** exact baseline Agent file — two expected disjoint-edit failures; 88 protection cases passed.
- **GREEN:** 99 focused cases passed, including 92 genuine service/provider cases.
- Mutation outcomes: 20 history conflicts and 58 refusals, with no-write assertions.
- Retained auth/sequential controls: **23 passed**; inverse/recorder controls: **14 passed**.
- Scoped Ruff and `git diff --check`: passed.
- Scoped Pyright: nine baseline and nine candidate diagnostics; **zero new**.

[Exact commands and results](./../../../../../../tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D101-asset-union-sol-0450/evidence/verification-commands.json) are preserved alongside durable XML.

Exact identities:

- Runtime base: `0c62dfa63db9ff608ac9338388431e31a814e080`
- Computed candidate tree: `e69e0265e2653f74c1f7486f0fed394ca5a1c67f`
- Agent baseline: `786385631b8096e50e66b8ecff1e7034c5bc1da9`
- Agent candidate SHA256: `76224a62434ade240e298bf6a1d14b64bdc2ed650923c2160cf22bdbb23a4a50`

The exact [Agent file](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D101-asset-union-sol-0450/evidence/agent-candidate.py), [patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D101-asset-union-sol-0450/evidence/agent-candidate.patch), [Runtime blob hashes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D101-asset-union-sol-0450/evidence/runtime-identities.json), and [baseline/patch hashes](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D101-asset-union-sol-0450/evidence/source-identities.json) are preserved privately. Only `_commit_patch.py` differs across the 1,514 verified archived Agent files.

Limits: config-only populated setup encounters existing validation refusal; some dual-mirror replacements encounter existing history-replay limitations. No fixes outside the allowlist were applied. No full suite, browser, protected-six body, merge or release ran.

Next: independent **SECURITY review of this exact pair**, then protected review, then MAIN six-case proof.