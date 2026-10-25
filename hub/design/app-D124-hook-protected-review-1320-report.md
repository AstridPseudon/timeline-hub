# D124 protected App hook review

**Verdict:** SOURCE PASS  
**Attachment:** Pending next sole tour

Reviewed immutable candidate:

- Head: `4c56a6282e25c0c4dbb4355164d27d28fdbe1757`
- Base: `fe3309dba4520835a685f925468bff1acdc0506f`
- Tree: `2afa38ba9e8ebfcefb23c81dbc1af3b1b9eabe0c`
- Only authorized D66/harness files changed.
- Production Runtime remains `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`.

The explicit helper path/hash is validated before startup, propagated through generated preflight/normal recipes and `runtimeEnv`, and recorded separately from Runtime identity. Missing path, missing/wrong hash, and missing file fail closed. Default pinned-helper behavior remains intact.

Correct helper for the next tour:

```sh
D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D124-helper-first-return-1312/evidence/p2_commit_phase_capture.py
D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760
```

Run the existing generated `p2 --preflight` recipe, then the same normal recipe with all four exact source tuples unchanged. The manifest must contain a distinct `diagnostic_helper` object with `source: "explicit"`.

The author’s printed recipe incorrectly references the superseded 1304 helper (`13883f…`); do not use it.

Tests:

- Node 20 focused D66 file: **29 passed**
- Node 20 D124 pattern: **2 passed**
- App and Node TypeScript checks: **passed**
- Changed-file ESLint: **passed**
- Node syntax checks and `git diff --check`: **passed**
- Existing central harness: **44 passed, 3 failed** before Runtime startup because `ASTRID_RUNTIME_PYTHON` was absent.

No browser/native HTTP probe, body capture, full suite, or P2 qualification was run. Evidence and corrected recipe are under the assigned worker directory.