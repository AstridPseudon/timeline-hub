# agt-m3-capture-source-recover: blocked before any test ran

## Done
- Worktree is on base 62e6d2c2. Copied `tests/sdk/test_capture_source_runtime.py` byte for byte from `agt-m3-capture-source-proof`. It is the only change.
- Checked statically that its helper imports resolve (`_closure`, `_digest`, `_replace_values`, `OLD`, `AUDIO` in `tests/timeline/test_authoring_bundle.py`, `prepare_filmstrip`, `use_runtime` and `unavailable` in `tests/lanes.py`).
- Read `runtime_protocol/snapshot_refs.py::publish_snapshot` at /home/user/work/runtime. It checks the project, that the parent revision row exists with a matching digest, and for working copies that the marker equals the supplied binding and the base parent digest matches. It does not compare `snapshot.config` or `snapshot.registry` against the parent, shot or internal closure. The `revision_digest` it checks comes from the snapshot's own `capture_authority` claim. This agrees with the source worker's finding, but it is a code reading only, not a demonstrated forgery.

## Blocked
Every invocation of `/home/user/work/venv-agent/bin/python` returned "requires approval", even `--version`, so I ran no test. I did not work around it (for example by putting the venv's site-packages on system python3's path). Nothing is verified:
- whether the file collects;
- whether the saved and unsaved positives pass;
- whether the forged config, registry and shot-digest cases are really admitted;
- the duplicate-ref and native-compiled cases;
- the `True == 1` and `2 == 2.0` check in `VerifiedTimelineSource.validate_snapshot`;
- the Agent caller-boundary review.

## Known problems in the staged test
- The forgery test calls `pytest.xfail(...)` after the fact. That is neither strict nor limited to a known failing case. Once it has run, replace it with `@pytest.mark.xfail(strict=True)` on exactly the cases that are admitted, keeping the positive `values.timeline_source is None` expectation unchanged.
- No Runtime or product edits, no escalation note in the coordination files, no HEADs or hashes recorded.

## Next
Approve the venv interpreter, or run on a worker where it is allowed:
`ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=<worktree> /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_capture_source_runtime.py`
