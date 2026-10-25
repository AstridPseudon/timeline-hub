# D127c report

Verdict: **PASS — review2013 F002 closed**

- Verified App `fd586440…`, tree `6d2744e…`, source SHA `59a4d116…`; worktree clean.
- Reused Sol 2033’s genuine Node20.19.4 execution via TSX 4.21.0 `tsx/cjs/api`: **3 intended passes, 0 failures, 0 intended skips/missing**, 1.38s.
- Whole-file result preserved: **4 ordinary nonmatching skips**; none counted as passes.
- Verified original source loading, native assertions, real Node/npm origins, event hashes, and no predicate/assertion monkeypatching.
- Outside service `13179` hit its 5GB guard before execution; no credit or retry.
- Runtime helper `095c252b…` and prior Runtime result `30318` verified read-only.

Evidence written to the assigned worker directory:

`evidence/{verdict.json,findings.md,source-manifest.json,validation.md,event-check.json}`

Validation:

- JSON parsing: PASS
- Permanent `check-events.py`: PASS
- App `git status`, `git diff --check`, `git diff --quiet`: PASS

No product changes or prohibited suites were run. D130 SWAP, WAL/recovery, full-tour, and original profile/element/latency/core/ZIP holds remain separate.