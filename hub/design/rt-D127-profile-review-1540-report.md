## Report

Completed read-only D127 review. Safe derivative: [d127-profile-review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D127-profile-review-1540/evidence/d127-profile-review.json).

- Corrected Composition SHA in the derivative to `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`; preserved original typo.
- Verified: 20 summaries, 6,089 samples, 109 lost, 7,598 seen, 2,489 retained, 5,109 dropped, 19 truncated, 21,000.903 ms capture-wide observer CPU.
- Request 2 remains distinct: 19,603.087 ms wall / 11,840.358 ms provider, 60.4004767%.
- Request 3 is exactly joined to element (`69c6463f…`), but has only 352 samples/3 lost, ends at authorization, and has no handler/provider/response denominator.
- No retained d22 full stack or provider leaf exists. Other launch leaves cannot be assigned to d22; request-3 operation attribution is blocked.
- Existing helper can expose counters only when its safe sink bytes are retained; current publication has only bounded counts/top-10 summaries. No new collector/body is justified.
- Production path verified through `door.py → server.py → service.py → coordinator → provider.commit`.
- Full v2 request/reply contract fields were reviewed against C0/`commit-v2.md`.

Validation:

```text
DERIVATIVE_JSON_PASS
INDEX_COUNTS {"sources":9,"missing":3,"safe_stack_artifacts":3}
FACTS_TOTALS ... verified expected totals
COMPOSITION_OBJECT commit
WORKTREE clean
```

No product tests were run because this was a read-only evidence review. Commit message and `DONE` marker were written.