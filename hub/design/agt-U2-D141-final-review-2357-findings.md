# U2 / D141 independent final cut findings

## FAIL — source qualification is not ready

The exact candidate is `aa5a91a618f4d28308772169bc08e8e79274cd6a`, tree
`c3ad6cca753bf1bfd033bf016c1d93e4b9f07127`, with parents
`c585cb2aa73c5298d474e614cb2144f58f27e605` and
`8b6ed2116fd1803d24b2be5bc08bd9490407fe4a`.

The automatic merge reconstruction found exactly the two author-reported
conflicts. All 19 upstream-only paths and all 922 current-only/later paths
match their respective parent blobs; the automatic non-conflict result has zero
mismatches. D100a approved blobs are exact. The committed index is clean, both
parents are ancestors, and no conflict markers remain. No semantic conflict
was found.

The normal producer-aware lock check is a hard failure:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-fa9cd546
```

Exit 1. The Runtime checkout is clean and exactly `fa9cd5464a8b37b02f971de375e56be846cd69e2`, but the candidate lock differs from its committed producer manifest for the timeline schema and three client artifacts, and names two producer artifacts absent from that manifest (`timeline_commit_types.py` and `commit_conflict_409.json`). The no-producer check passes, which is insufficient provenance evidence.

The normal artifact check also fails:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check
```

Exit 1: `astrid/packs/astrid_motion/rendering/elements/effects/am-footage/component.tsx`
is changed relative to the committed `artifacts.json` digest. This stale manifest
is inherited from the frozen upstream source; no regeneration was performed.

## Validation outcomes

- `node --test remotion/tests/am-footage-cover.test.cjs` — PASS, 1 test.
- Required Python targeted command against the exact Agent + Runtime tuple —
  incomplete at the 30-second tool boundary after reaching 11% collection,
  with actual `E` and `F` output and no final exit/summary captured. It was not
  rerun or reduced to manufacture a result.
- `bun run check:chat-bundle` — exit 1, environment missing `zod` in the
  immutable shared dependency tree; no acquisition or overlay was attempted.
- `bun test ./astrid/chat` — exit 1: 29 passed, 18 failed, 18 errors across
  47 tests/24 files, with the unhandled missing-`zod` import as the boundary.
- Ruff over the 19 changed Python files — exit 1, 574 findings. Per-file
  findings are inherited from the current parent; the candidate finding
  signatures are also present in the frozen upstream comparison.
- Scoped Mypy over 10 changed source files — exit 1, 168 errors in 6 files.
  Current-parent shadow comparison is exactly 168 with identical per-file
  counts; frozen upstream comparison is 175. No suppressions or fixes were
  made.

No full suite, provider cohort, child suite, ship/final-core/REG0 credit, or
product investigation was run. This is a source qualification FAIL, not a
claim that all product behavior is broken; the lock/artifact gates and the
incomplete/environmental test gates prevent PASS.
