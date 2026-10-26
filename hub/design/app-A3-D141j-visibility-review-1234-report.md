# Report

Verdict: **FAIL**

The synthetic artifact and checker passed, but read-head continuity is invalid across repeat reads: the active observer reuses the collector’s first cached accepted head rather than correlating the active occurrences to the accepted read that produced them. The control exercises only one read/render.

Validation:

- Full touched test: **12/12 passed**
- Scoped ESLint: **PASS**
- App and Node typechecks: **PASS**
- `git diff --check`: **PASS**
- Malformed artifact correctly refused
- Focused filtered test selected case passed, process exited 1 due 11 undeclared filtered skips

No product files were edited; no diagnostic body or browser/native/full suite was run. Candidate remains private/unmerged and cause remains UNKNOWN.

Evidence: [review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A3-D141j-visibility-review-1234/evidence/review.json)

Next step: correlate each accepted read through `activeCanonicalOccurrences` and add repeat-read/render source control before re-review.