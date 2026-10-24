Implemented the correction in `timeline_commit_auth.py`, with 48 new focused tests. Omitted `track.create.created` now requires the sealed owner and row to match the recorded claim, allocation fact, absent read, and authored root birth. Core command equality, explicit claims, inverse authentication, and downstream custody checks remain intact.

Validation:

- Old e68 source: **9 failures**, all at the retained command-comparison refusal.
- Final requested cohort: **323 passed**, no skips.
- Scoped Ruff, compilation, and `git diff --check`: passed.
- Pyright versus e68: **zero new normalized diagnostics**.

Exact final test command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_forward_created_authority.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_port.py tests/test_timeline_commit_sequential_verifier.py --junitxml="$TMPDIR/forward.xml"
```

The real caller exercised `RuntimeService.commit_timeline` through the supported Astrid provider and commit port. No existing tests or Agent files changed.

The retained originals are:

- `tests/sdk/test_timeline_commit_provider_runtime.py::test_structural_reservations_and_receipt_retry_survive_runtime_restart`
- `tests/sdk/test_timeline_commit_provider_runtime.py::test_restore_inverse_redo_and_exact_retry_survive_runtime_restart`

Their exact source, bodies, assertions, and hashes are retained in [original-selectors.json](../../../../../../tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-forward-created-authority-sol-1450/evidence/original-selectors.json). I did not execute those originals; Agent owns that credit.

One broader probe accepted a forged native write with an exact explicit claim and unchanged authoritative effects. Its **1 failed / 323 passed** run is retained separately. That deferred D62 producer-trust case was excluded from the final scoped matrix; no speculative authority change was made.

Commit is pending the harness; `commit-msg` and empty `DONE` are written.

- HEAD/base: `e68cf231641db98a72805a586b51ab5c4fae2c16`
- Computed candidate tree: `77624ec071f91e7938408288bd9c0e2e55b9fd01`
- Combined diff SHA-256: `4c1fdff8e9c268996ba7347266cbbed8f303c2beaded0c7e04704114dbd17b53`

[Evidence directory](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-forward-created-authority-sol-1450/evidence) contains direct XML/logs, exact commands, source copies, and hashes—776 KB total.

Nothing blocked. Next: joined independent security review with D62 and generated wire, then Agent’s actual-home execution of the two originals.