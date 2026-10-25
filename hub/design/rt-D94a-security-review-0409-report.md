# D94a independent security review

Verdict: **source security PASS conditional on deployment data-root ownership/mode; no global release approval.**

- Candidate verified: commit `09a27efc6cac5a25fbcc63cffa7ca4e221336ee8`, tree `6a0db1ec092cf1631761fd4bbc8a0ae33eebeec8`.
- Store/test blobs match: `dc7035cd…41236` / `7c764726…40da`.
- Only authorized files differ; no product edits made.
- Source satisfies the approved custody trade conditionally: pinned SQLite connection, transaction-before-cache checks, `BEGIN IMMEDIATE`, DB/WAL device/inode/size/mtime/ctime fingerprints, post-commit sampling, rollback/refusal/restart/connection replacement handling, detached cache values, and lifecycle isolation.
- Existing defensive coverage passed for external writes, WAL/file changes, rewind/replacement, ABA-like races, concurrent reads, partial rollback, and retained warm-cache forgery.
- Forward/warm curve remains qualified; inverse ancestry growth remains disclosed with no P4 credit.

Tests:

```text
/home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
tests/test_timeline_history_state.py \
tests/test_timeline_history_authenticated_read.py \
tests/test_timeline_history_boundaries.py \
tests/test_timeline_commit_authentication.py \
tests/test_timeline_inverse_stage_authentication.py \
tests/test_timeline_request_verification.py \
--timeout=45 \
--junitxml=<worker evidence>/security.xml
```

Result: **246 passed, 74 deselected, 40.01s**. Local JUnit XML is present at [security.xml](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D94a-security-review-0409/evidence/security.xml). Prior central run truthfully supplied no XML.

Scoped Ruff/Pyright matched the author comparison: Ruff **11→10**, Pyright **74→54**, with no added diagnostic identities. Compile and `git diff --check` passed.

Finding/blocker: production data root remains **unknown**. Observed code paths are UID/GID `0:0`, mode `0755`; module mode `0644`. No declared or conventional production data root exists in this environment. Owner disposition is required before release/global GO.

Commit message and `DONE` marker were written.