# Runtime seven-baseline fixture-fidelity review

## Verdict

**APPROVE.** No correction is required for `d6ae19b54151aa4938c6d0fce462b2615c300c78` (`test(runtime): restore boundary fixture fidelity`) against its parent `86ce14f144a740d9002d8758f952bdb4324847d8` and current integration.

The patch is test-only: it changes only `tests/test_runtime_boundary.py` and
`tests/test_zero_shim_boundary.py`. No Runtime product path changes.

## Assertion inventory

- `_CustodyChild` now follows the relevant `Popen` protocol: it starts with
  `returncode is None`, `poll()` returns `None` while live and updates the
  returncode after the explicit exit transition, and `wait(timeout=...)`
  records and returns the positive exit. It does not manufacture a positive
  exit during setup or polling.
- `_stub_owner_broker` explicitly selects the retained Darwin broker branch.
  The fake broker checks the exact child PID, raises `CustodyError` for the
  identity-unavailable cases, and makes numeric PID/PGID fallback fail the
  test. This preserves the custody-only signal requirement.
- `test_token_signal_exit_race_uses_only_retained_child_exit` still proves that
  an exit observed through the retained direct-child handle wins the signal
  race. `test_unverifiable_live_owner_retains_cleanup_uncertainty` still proves
  a live child plus failed identity observation raises cleanup uncertainty,
  leaves the child live, and records `_runtime_cleanup_error`.
- `test_primary_start_error_retains_cleanup_uncertainty_as_cause` still keeps
  the original `OSError` object and requires the cleanup uncertainty as its
  cause; it also requires the child to remain live. No broad exception or
  setup-error absorption was added.
- `test_unowned_handle_does_not_infer_termination_from_poll` still rejects the
  handle before any positive poll result can be treated as authoritative; the
  `sole-reaper` refusal remains intact.
- The former launch-uncertainty case remains positive in the right sense:
  `_spawn_runtime` is forced through Darwin, fake `Popen` returns the child,
  ownership/broker attributes are asserted before `wait_until_sealed`, and a
  seal `CustodyError` must produce `RuntimeCustodyLaunchUncertain` containing
  the exact process and broker while leaving `boundary._process` retained.
  The setup assertions for the role, scoped authority directory, journal
  parent, wrapper argv, and `start_new_session=True` remain active.
- The retained stop-owner fixture now has a `returncode` property and a
  truthful wait protocol. It explicitly models release generation 2, reclaim
  to generation 3, TERM timeout, KILL changing the child to exit 0, and the
  final successful wait. The required event sequence remains exactly
  `TERM -> timeout wait -> KILL -> positive wait`; there is no hidden early
  exit or fake retained-child ownership.
- The zero-shim launch fixture now explicitly selects the broker-backed branch
  before substituting `RoleBoundCustodyBroker` and `Popen`; Linux native
  custody therefore cannot silently bypass the assertions. Its fake process
  remains live (`returncode=None`, `poll() is None`) and its identity provider
  returns the queried PID, current UID, and birth marker. Thus parent/child
  identity queries cannot be conflated by a constant PID; the substituted
  broker intentionally owns the broker-specific lineage checks.
- The zero-shim source-isolation assertions remain intact: no `cwd`, no source
  checkout in the wrapper argv or environment, the host `PYTHONPATH` is
  preserved in the child environment, and `PYTHONPATH` is not injected as a
  `Popen` keyword. The installed-client `sys.path` non-mutation assertion is
  unchanged.

## Review checks

- `git diff --check d6ae19b^ d6ae19b` — passed.
- `git show --check --oneline d6ae19b` — passed.
- `git diff --name-only d6ae19b^ d6ae19b -- ':!tests'` — empty; no product
  files are in the patch.
- Existing tests were **not rerun**, as required. No full suite, pin, install,
  or Git mutation was performed. This is a static custody/interface review;
  runtime execution remains covered by the existing seven-pass and boundary
  neighbor evidence supplied by the worker/orchestrator.

## Follow-up

Merge the test-only candidate as-is. If the zero-shim test is later expanded
to exercise the real broker rather than source-isolation wiring, give that
separate fixture a real `parent_pid` relationship and test it independently;
the current substituted-broker test does not claim to prove the Darwin broker's
full lineage handshake.
