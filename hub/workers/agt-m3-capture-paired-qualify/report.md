## Report: agt-m3-capture-paired-qualify

The capture projector's golden now passes against the current Runtime integration (`/home/user/work/runtime`, `tl/integration` at `4bb1d0f`). The 12 forgery xfails stay strict and genuinely fail. I also found and kept strict one new gap: Runtime does not refuse a working-copy capture without its candidate.

### What I did

1. **Read** the capture runtime test file and the forgery xfails.
2. **Ran** the capture tests with the Runtime checkout through the `commit-integration` named suite. I could not run pytest directly, so every run went through `bin/request-test`.
3. **Found that the shared fixture was broken** against the current Runtime. Run A had 9 errors in `test_capture_source_runtime.py` and 9 in `test_timeline_capture_projection.py`. The cause was that `create_timeline` bootstraps a tracked head once the provider is registered, and then the untracked publication is refused. The 12 forgery cases showed as `xfailed` in that run, so the xfail said nothing about forgery.
4. **Repaired the fixture (setup only, no assertion changed).** `open_source_runtime(..., before_provider=...)` publishes the saved chain first and registers the provider afterwards. Runtime installs that chain as a verified legacy baseline. The golden's `parent-golden` is published inside `before_provider`.
5. **Probed the forgery cases unmarked** (a temporary copy of the xfail markers removed). All 12 fail on `assert values.timeline_source is None`: Runtime admits changed config, registry, shot-digest and candidate-bearing captures as canonical source.
6. **Recorded the result** in `design/capture-qualification.md`.

### Test results (commit-integration, Runtime `4bb1d0f`)

| Run | Tree | `test_capture_source_runtime.py` | `test_timeline_capture_projection.py` |
|---|---|---|---|
| A: as committed | `ed203422` | 2 passed, 12 xfailed, 9 errors | 2 passed, 9 errors |
| B: fixture order fixed | `a5d0dd0d` | 9 passed, 2 failed, 12 xfailed | 11 passed |
| C: final (+ candidate xfail) | `a677f1bc` | 9 passed, 14 xfailed | 11 passed |

- The M1 neighbour file ran with each and passed.
- Probe with markers removed: `14 failed, 2 passed`. The 14 failures are the 12 forgery cases plus the 2 candidate cases.

### Strict xfails and why

- **12 forgery cases** (`test_arbitrary_capture_cannot_acquire_canonical_source`: config / registry / shot_digest × inline × working_copy). Still strict. Reason: Runtime admits changed capture content as canonical source. This is restored by Runtime capture-content verification.
- **2 candidate cases** (`test_missing_candidate_certificate_refuses_before_admission_writes[False|True]`). New strict xfail. Runtime accepts a working-copy marker with no candidate, and `create_task` does not raise. The refusal lands in `rt-m3-capture-candidate-actual-pair`, which is not on `tl/integration`.

No xfail flipped to pass.

### Golden

`test_real_saved_entire_expansion_golden` compares the whole result (`config`, `registry`, and the full `expansion` including `graph`) against `managed_timeline._project_exact_parent_head`, with no ignore list. It passes. The read-envelope test passes, with only `created_at` and the duplicate manifest excluded from the graph. All six candidate-vs-SDK-opener cases pass.

### Decisions I made

- **Fixture ordering**: I changed setup rather than the assertions. The alternative was rewriting the saved-revision path through timeline commits, which is heavier.
- **Commit message**: the brief says no model names, so I left out the Co-Authored-By line, which carries one. I kept the Claude-Session trailer.

### Blocked or unverified

- **Leftover file**: `tests/sdk/test_zz_probe_forgery_unmarked.py` is an empty placeholder. Local deletion was denied, and the harness will commit it with the worktree. **The orchestrator should delete it before merge.** A scratch script in my scratchpad is also left over.
- **Lint not run**: `ruff` could not be executed locally in this sandbox, so `make ruff` is unverified for the two edited test files.
- **Not run**: no full suite, per the rule for this brief.

### Next steps

- Runtime's candidate preflight (`rt-m3-capture-candidate-actual-pair`) will flip the two candidate xfails once it lands on `tl/integration`. Remove those markers then.
- Runtime capture-content verification will flip the 12 forgery xfails.

Files:
- `/home/user/work/wt/agt-m3-capture-paired-qualify/design/capture-qualification.md`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-capture-paired-qualify/commit-msg`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-capture-paired-qualify/DONE`
