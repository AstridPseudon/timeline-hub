# Findings

## F1 — ordinary recovery

**NONE.** The finite records inspected contain no ordinary guarded release that is simultaneously supported, owned, unreferenced, non-KEEP, and free of dirty-worktree disqualifiers.

The protected byte totals were independently reproduced with targeted `du -x -s -B1` checks. The two F-final records have actual `KEEP` markers. The P2 records have no local marker but remain referenced proof fixtures; that reference is sufficient to keep them protected for this review.

## F2 — small metadata candidates

Targeted totals were reproduced as follows:

| Record | Bytes | Review result |
| --- | ---: | --- |
| `archive-v1-20261022` | 2,097,152 | Not actionable; control archive custody and no authorized route |
| `tests/cache` | 6,881,280 | Not actionable; central test-service ownership and no release row/command |
| unowned `.test-agt-…` path | 15,032,320 | Not actionable; unknown ownership and no permission |
| `/home/user/work/wt/nesttest` | 8,192 | Not actionable; unknown/unmarked and negligible |

The first three total `24,010,752` bytes, less than the census's `60,479,488`-byte gap. They cannot independently clear the gap, and the records do not authorize mutation.

## F3 — five Runtime guard refusals

The owning Runtime manager's 14:42 log records the supported `bin/recycle` command refusing each of these five names with `DIRTY, refused`:

- `rt-m3-legacy-capture-replay-proof`
- `rt-m3-capture-candidate-actual-pair`
- `rt-m2-parent-media-door-proof`
- `rt-m2-public018-generation-gate-preflight-1134`
- `rt-m2-rt03-peer-agreed-raw-capture-impl`

This is a manager guard-refusal fact, not a new review-side dirty-tree inspection or sandbox host audit. No force path is available or inferred.

## F4 — owner decision and lifecycle

The existing Main 14:50 escalation remains the sole owner decision: an owner may use the already recorded guarded `hub-repack runtime` path, or leave the F-final positive-control gate held. The census author did not approve or execute it; this review does not repeat the ask.

The author reused historical sampler metadata. The prior sampler's positive controls were not run, and no new sampler was started here. Historical values cannot be credited to this worker's continuous coverage or current stop condition.

## Scope limit

These findings cover inspected records and targeted metadata only. They do not claim that no other path exists. No cleanup or action recommendation has automatic permission.

