# Agent D13 Main custody patch review

Verdict: **APPROVE**, bounded to the committed three-file custody patch. This is an independent source/security review, not owner permission to land it in another worktree.

## Source identity

- Final harness commit: `46f2b9e2ff5d74f03249b0f90bc9b00910b23856`, parent `65c87dd5d5310bc028acafaf1cab31196a03a86d`.
- Commit subject: `tl/agt-m2-d13-custody-cleanup-finish: Finish ONLY D13 exact014 custody/lifetime failure after functionalrend`.
- Exact diff: `astrid/core/execution/custody_broker.py`, `astrid/core/execution/process_group.py`, and `tests/core/execution/test_process_group.py`; `+67/-2`, no other paths.
- The central rerun snapshot was tree `46e4327f1691f2a0142bc899b39cd194120c9343`. Its three allowed-file blobs match the committed WIP; the review did not use the original branch HEAD as the WIP source.
- Allowed-file SHA-256 fingerprints at the final commit:
  - `custody_broker.py` `e66ccfcd6ff812d9038ba546ea9e855e462be22c8aaffd672a3214b029eaa1e8`
  - `process_group.py` `df8d111c415b2700d1421a1a592bce38267b939395945adbf7600412db8d1cb1`
  - `test_process_group.py` `410d4dce998de3eeb9a7f19d3318631e64ca5a50c3790cf76d064ef5798856f3`

## Safety review

`ProcessCustody.retained_incarnation_exited()` requires the exact `(pid, birth)` entry in the custody handle ledger. A live integer pidfd is accepted only when its poll state is readable, which is positive exit evidence for that retained Linux incarnation; a missing entry, birth mismatch, non-pidfd handle, closed/invalid raw descriptor, or poll error does not produce proof. `_PIDFD_RELEASED` is only installed by the existing release path after exact absence/exit has already been verified, so it is a proof-carrying terminal state rather than an arbitrary closed-descriptor fallback.

In `process_group.py`, a reused root PID is ignored only after `Popen.returncode` proves the original direct child was reaped. A reused descendant is ignored only with matching retained-custody exit proof. Neither path admits replacement processes: the reused root is removed from ancestry traversal, and a reused descendant is absent from the returned live set. Signal paths still operate on the birth-fenced live set, never on a numeric PID or process group alone. Existing session/process-group ownership checks, custody ledger checks, uncertainty latching, cleanup refusals, and final absence verification remain in place. There is no teardown ignore, cleanup-success fallback, skip, xfail, or weakened assertion in the patch.

The new regression proves all three relevant outcomes: reaped/reused root does not poison a known child, a changed descendant is accepted only when the fake retained proof says that exact old birth exited, and the same changed descendant still raises `owned process identity was reused` without proof. Existing refusal tests remain present, including the process-group uncertainty/reuse tests and custody tests for PID reuse/absence, unknown or reused targets, and positive retained direct-child exit.

## Test evidence

- Central exact named run, not duplicated:
  `registered014-render-integration` request `agt-m2-d13-custody-cleanup-finish-registered014-render-integration-1020161250-30005`; exact command was `python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/packs/video_editing/test_runtime_publication_chain.py`; result **2 passed, 1 deselected** in 304.33s. Both functional positives and teardown completed.
- Local focused process suite on the committed tree: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<private git-archive checkout> /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/core/execution/test_process_group.py` -> **61 passed, 5 deselected**.
- Local focused custody/pidfd selection: same command with `tests/core/execution/test_custody_broker.py -k 'positive_owned_child_exit or pid_reuse_or_absence or unknown_or_reused_target or only_positive_retained_direct_child_exit or observed_census_does_not_change_linux_pidfd_admission or linux_descendant'` -> **12 passed, 564 deselected**.
- A broader local run of both process/custody files reached **602 passed, 24 failed, 16 deselected**; all 24 failures were sandbox `PermissionError: [Errno 1] Operation not permitted` on socket/network capability tests in `test_custody_broker.py`, not failures in the changed paths. No test was modified or weakened.
- No full suite was requested. The prior central run on the pre-commit WIP failed in teardown; the exact post-commit-tree rerun above passed.

## Clean landing plan and risks

Do not merge the D13 + Composition 0.14-pinned tree wholesale to land this Main infrastructure fix. Start from the current clean `current013` integration/main target, verify the two custody-file preimages, and port only the committed `46f2b9e2` three-file delta (including its direct regression test). Preserve the current013 Runtime/App/Composition pins and unrelated timeline changes. Then run the focused process/custody commands above and request one central `registered014-render-integration`/equivalent real-two-render qualification for that clean current013-based tree. If a preimage differs, re-apply the same narrow logic manually and re-review the resulting source; do not resolve by taking the D13/014 branch wholesale.

Residual risk is operational: the new regression uses a mocked retained-proof callback, while direct invalid-pidfd polling is guarded by the production exception/fail-closed path rather than a new raw-descriptor test. The central real-render qualification passed teardown, so this is a follow-up test-hardening opportunity, not a basis to hold this bounded patch.
