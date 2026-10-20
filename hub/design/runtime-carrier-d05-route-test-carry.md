# Runtime D05 route-test carry

## Result

Carried the exact `tests/test_timeline_clip_replacement.py` blob from
`d05e6383f4ccaf7541698a65b2737fbc5f3f0fbb` onto the private carrier worker
tree. The current-schema parent-ownership marker now sends the request through
`RuntimeService.commit_timeline` via `_native_commit`, rather than calling
`validate_request` directly. The complete positive parent-swap body and
assertions remain unchanged under the strict `ValidationError` xfail.

The resulting test blob is `150a7abb340040e45c34742bc871ef83caab0575`, equal
to the D05 source blob and the `e2db1e8` integration blob. No Runtime product,
carrier implementation, ownership/source-authority logic, private contract,
or generated artifact was changed.

## Tests

- `PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-next-ordinary-official-prep/agent-final-source PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider -m integration -k 'test_native_parent_clip_swap_route_refuses_parent_ownership_on_current_schema or test_native_parent_clip_swap_route_replaces_parent_media' tests/test_timeline_clip_replacement.py`
  - PASS: `1 passed, 23 deselected, 1 xfailed` in 4.84s. The refusal reached the actual `RuntimeService.commit_timeline` route; the positive remains the authorized strict schema-0.2.14/D04 marker.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -B - <<'PY'
  from pathlib import Path
  path = Path('tests/test_timeline_clip_replacement.py')
  compile(path.read_text(), str(path), 'exec')
  print(f'compiled {path}')
  PY`
  - PASS: `tests/test_timeline_clip_replacement.py` compiled.
- `git diff --check`
  - PASS.

No full suite, broad targeted suite, fake provider, SDK change, version/pin
change, or coordinated native 3730 pair was run.

## Compatibility handoff and limitation

The worker base is `0b8f7f2a61c20eb876aec367526358412161bb46`; the harness will
create the successor commit SHA and tree after exit. The orchestrator should
record that successor SHA/tree in the Agent INBOX as a test-only compatibility
carry. This is not public adoption. The current public schema still rejects
`parent` ownership, so the positive acceptance case must remain strict xfail
until the approved schema-0.2.14 pair is adopted.
