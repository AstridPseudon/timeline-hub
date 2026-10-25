# D108/D69 Runtime assertion JOIN review

Verdict: **FAIL_WITH_EXPLICIT_RT07_SOURCE_GAP**

- Both partitions pass source audit: even 57, odd 56; disjoint and exhaustive over 113 functions.
- Assertion totals verified: 72 removed, 205 added; equality drops 5, membership increases 3.
- All 72 removed assertions and 8 removed `pytest.raises` entries have exact source/citation maps. Raise serializer limitation is recorded; no counts-only pass was used.
- Source receipts: 311/311 pass. Tree, manifest, patch size/hash, and source hashes pass.
- JOIN fails because author hashes use different algorithms:
  - Even: `7fbf7c79…9fcf7` — selector/index/body hashes.
  - Odd: `cd09ec32…f44c` — selector-only.
  Canonical function/body identity still matches.

RT07 review:

- Source-mapped current commit-path proof covers old lines 96, 97, 99, 106, 107, 108, and 115.
- Remaining source gap: old lines 102, 104, 105 lack direct proof that accepted `config` and `registry` snapshot content—and its digest—match the current render task input. Exact unapplied scope is recorded in the evidence JSON.
- Retired-route strict xfails were not treated as positive proof.

Evidence:

[d108_assertions_review_join.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-assertions-review-0813/evidence/d108_assertions_review_join.json)

[d108_assertions_review_join.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-assertions-review-0813/evidence/d108_assertions_review_join.md)

Checks run:

- `python -m py_compile`: PASS
- Independent read-only review script: PASS with recorded FAIL verdict
- `git diff --check`: PASS
- Worktree clean
- No pytest, lint, typecheck, browser, provider, or full suite runs

The applied commit object itself was unavailable locally, but captured commit/tree `1daca…`/`a522…` and all source receipts were verified. Commit message and `DONE` marker were created.