# Agent Main custody security review

**HOLD** on `f511038ded7a0ae49e2935efc37800b63038d0b3`. The owner’s 16:16 exact retained-pidfd exit-proof condition is not satisfied under descriptor invalidation/reuse. Existing Linux tests pass; their green result does not cover this counterexample. No product or test changes were made by this review.

## Exact source and scope

- Reviewed branch: `tl/agt-m2-main-custody-current-port`; harness commit `f511038ded7a0ae49e2935efc37800b63038d0b3`, parent `2f8b9cc53648a392da8684016c6ee15e589ea060`, tree `b5cd1a3123c3bddb1f0482c5687cadd00fd88bb6`.
- The committed delta is exactly three paths, **+67/-2**, with no D13/014 pin changes. Its patch SHA-256 is `95af79fba0e178d09e7589ae9f6b5dc0cf1a662a85bcb23dc47bd43304d8c7c1`, identical to the allowed three-file delta from `46f2b9e2^..46f2b9e2`.
- The initial source worktree had been recycled. Source inspection and the local probe used an unmodified `git archive` of the committed ref in this reviewer’s private directory. The central service recreated the source worker and tested the same committed tree; its `snap` records the tree above. Recreated source HEAD was `f511038d`, clean. The reviewer’s own worktree remains unchanged at `2f8b9cc5`.
- SHA-256: `custody_broker.py` = `e66ccfcd6ff812d9038ba546ea9e855e462be22c8aaffd672a3214b029eaa1e8`; `process_group.py` = `df8d111c415b2700d1421a1a592bce38267b939395945adbf7600412db8d1cb1`; `test_process_group.py` = `410d4dce998de3eeb9a7f19d3318631e64ca5a50c3790cf76d064ef5798856f3`. Archive bytes matched those blobs.
- Read PLAN, the owner grant at `managers/agent/INBOX.md:1761`, and `design/agent-review-d13-main-custody-patch.md`. This report supersedes that earlier review’s claim that invalid/closed descriptors cannot produce exit proof.

## Blocking counterexample: descriptor events are not necessarily pidfd exit events

At `astrid/core/execution/custody_broker.py:3878`, `retained_incarnation_exited()` checks the `(pid, birth)` ledger key, but accepts an integer descriptor using `bool(poller.poll(0))`. Registering `POLLIN` does not restrict returned events to `POLLIN`: a closed descriptor returns `POLLNVAL` without throwing. The helper therefore returns `True` on invalidity. If the descriptor number is reused for `/dev/null`, its ordinary read readiness also returns `True`, without that file being a pidfd at all.

The private, reproducible probe is `workers/agt-review-main-custody-security-final/probe_pidfd.py`. It binds a real live child through the committed `ProcessCustody.bind_launch()`, retaining the real pidfd and birth. Results:

| Probe | Observed result |
| --- | --- |
| Live child, original retained pidfd | `False`, correct |
| Wrong birth or missing ledger entry | `False`, correct |
| Synthetic replacement-incarnation census with original live pidfd | `CleanupUncertainError: owned process identity was reused`, correct |
| Close that retained descriptor while child remains alive | poll `[(3, 32)]` (`POLLNVAL`), **exit proof `True`** |
| Same synthetic replacement census after close | **accepted, empty live set**, instead of reuse refusal |
| Reuse descriptor 3 for `/dev/null`, child remains alive | poll `[(3, 1)]` (`POLLIN`), **exit proof `True`** |
| Call existing `release_pidfds(only_exited=True)` after descriptor reuse | installs `_PIDFD_RELEASED`; helper still reports **exit proof `True`** for the live child |
| Restore a genuine pidfd, terminate child, wait via `waitid(P_PIDFD, WEXITED | WNOWAIT)` | exit proof `True`, correct |
| Reap and release that genuinely exited incarnation | exit proof `True`, correct |

The close/reuse steps intentionally inject descriptor-lifetime faults inside the probe’s own process. The changed-incarnation census is synthetic; no real PID recycling was forced. I found no normal internal close race: admission, proof and release use the same lock; successful admission stores a real `os.pidfd_open()` result after birth revalidation, and normal production unconditional release follows final absence verification. This finding does **not** establish an external exploit, spontaneous handle substitution, or unowned signaling. It establishes that lost/reused descriptor authority can be interpreted as positive exit evidence, contrary to the explicit review requirement. The earlier claim that invalid-descriptor polling necessarily takes a fail-closed exception path is concretely false.

`_PIDFD_RELEASED` is also not intrinsically an exit certificate: the pre-existing release method supports unconditional release, and its conditional mode shares the nonempty-poll-result test. Normal unconditional callers have an absence-check precondition, but the new helper cannot infer proof from the sentinel without preserving that precondition and ruling out erroneous conditional release.

The Linux kernel’s [v6.12 `pidfd_poll()` implementation](https://raw.githubusercontent.com/torvalds/linux/v6.12/fs/pidfs.c) returns `EPOLLIN` for an exited retained task and adds `EPOLLHUP` after it is gone. Thus `POLLIN` on the **actual retained pidfd** is valid positive exit evidence; `waitid()` is not mandatory for non-child descendants. The [pidfd_open manual](https://man7.org/linux/man-pages/man2/pidfd_open.2.html) documents those process-exit semantics and child-only waiting. The [poll manual](https://man7.org/linux/man-pages/man2/poll.2.html) separately documents unconditional error events and ordinary-file readiness. Inferring pidfd exit from an arbitrary event tuple loses that distinction.

Required correction before approval: explicitly accept positive exit events from the same retained kernel process capability; invalid/error descriptors and substituted ordinary descriptors must refuse. Preserve trustworthy terminal-release provenance. Merely masking `POLLIN` fixes the closed-descriptor case but leaves the `/dev/null` substitution case. Keep this correction minimal and add direct live/invalid/reused-descriptor negatives without altering existing expectations. A successor needs a fresh bounded review and focused qualification; this review does not authorize product edits.

## Guards that remain intact

The reaped-root exception uses the original Popen’s non-None return code. Replacement roots are excluded from ancestry traversal; changed descendants are also excluded by birth matching and never become traversal anchors. Without proof the changed-incarnation census still raises, including the final negative in the added regression. Existing uncertainty latches remain sticky. The patch does not alter signal authority, signal implementation, session/process-group checks, admission ledgers, final group absence checks, or Darwin role custody. There is no numeric-PID or process-group kill fallback, new adoption path, ignored teardown error, skip, xfail, or weakened assertion in the patch. The demonstrated fault bypasses observation refusal; it does not demonstrate signaling a replacement.

All original test source remains intact relative to both parent and `origin/main` (`96b283d5d6fd8031538f881e486bb2ebf45dce75`). `test_custody_broker.py` is byte-identical (SHA-256 `ea6b9b779d6c4f857e55da4138cda267d1afdb00f1a7cf989b0149023a753c91`). The process test diff only inserts the 31-line regression. Source-segment comparison also found zero changed/removed original top-level definitions: 50 process definitions and 213 custody definitions. The original negative `test_observation_uncertainty_persists_without_adopting_unknown_children[pid-reuse]` and the added regression’s proof-false negative remain passing. These cover unproven reuse under intact authority; they do not cover a false positive from the real proof helper.

## Exact commands and results

Here `O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`, `W=$O/workers/agt-review-main-custody-security-final`, and `S=$W/source`. To reproduce the private source, create `$S` and extract `git archive f511038ded7a0ae49e2935efc37800b63038d0b3` there from the Agent repository. The temporary archive is removed after this review; the probe remains.

1. **Required central unfiltered strict files:**

   ```sh
   "$O/bin/request-test" agt-m2-main-custody-current-port root-prep-current-integration --files "tests/core/execution/test_process_group.py tests/core/execution/test_custody_broker.py"
   "$O/bin/wait-test" agt-m2-main-custody-current-port-root-prep-current-integration-1020162947-27808 0
   ```

   **PASS, exit 0: 627 passed, 16 skipped in 21.66s** (service elapsed 23s), **0 deselected, 0 failed**. Result: `tests/agt-m2-main-custody-current-port-root-prep-current-integration-1020162947-27808/{summary,log.txt,snap}`. This was not a cache hit. Named suite’s exact pytest invocation was `/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/execution/test_process_group.py tests/core/execution/test_custody_broker.py`, under the existing `root-prep-current-integration` clean environment with `PYTHONPATH=$PWD` and `PYTHONDONTWRITEBYTECODE=1`; the summary records the complete environment. No full or unrelated suite was requested.

2. **Local original refusal and added regression, from `$S`:**

   ```sh
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/core/execution/test_process_group.py -k 'observation_uncertainty_persists or reaped_root_pid_reuse'
   ```

   **5 passed, 62 deselected in 0.22s**, exit 0.

3. **Local descriptor probe:**

   ```sh
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python "$W/probe_pidfd.py"
   ```

   Exit 0, all listed controls and counterexample assertions reproduced. This is a diagnostic reproduction, **not** an added passing behavior test or a claim that the security invariant passes. The probe prints the imported committed-source location, and leaves no child alive.

4. **Identify the previously deselected lane, collection only, from `$S`:**

   ```sh
   PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$S" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only -m darwin_native tests/core/execution/test_process_group.py tests/core/execution/test_custody_broker.py
   ```

   **16/643 collected, 627 deselected in 1.53s**, exit 0. The 16 are precisely the Darwin-native lane (5 process, 11 parameterized custody cases). The unfiltered central run selected all 643, but `tests/lanes.py:125` adds `skip(reason="darwin_native: needs macOS")` off Darwin, with some tests also having their own platform skips. **These 16 were not executed successfully on Linux.** No marker or test was overridden or weakened. Consequently “all original strict tests executed and passing” cannot be claimed from this host; their macOS execution remains unverified.

5. `git diff f511038d^ f511038d --check`: exit 0. Exact patch hashes, unchanged-original-test source checks and archive-to-blob comparisons: all matched as detailed above.

## Delivery and next step

The requested one-line Main-infrastructure note already exists in `design/agent-main-infrastructure-touched.md`; it is not public-release clearance. No shared dependency, product source, original test, branch or ref was changed. No commit, merge, checkout, push, broad rerun, or public release was performed by this reviewer.

Return the concrete descriptor-proof gap to the source owner. Re-review a committed minimal successor with direct negative coverage and the same strict files; retain the explicit Linux/macOS caveat. This review task is complete with a **HOLD** verdict, not blocked awaiting an uncommitted source.
