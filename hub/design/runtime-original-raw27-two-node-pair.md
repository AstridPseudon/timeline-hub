# Runtime raw27 two-node pair

Status: blocked on the historical-audio fixture setup under the exact Runtime
7d source. The requested two-node central run was executed once after fixing a
suite-command quoting error that had prevented the first queued attempt from
starting pytest.

## Scope and exact sources

- Runtime worktree/base: `/home/user/work/wt/rt-m2-original-raw27-two-node-pair`,
  HEAD `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`.
- Agent checkout: `/home/user/work/wt/agt-pin-27e823a5`, HEAD
  `27e823a5ddeb4f8995c436b44c8d42f728350919`, tree
  `7f43878c1f37abf1a8bef6d79b44df51d1ced50a`.
- Normal producer/artifact source: `/home/user/work/wt/rt-pin-a0dca169`,
  HEAD `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Normal metadata preflight passed: client `0.2.14`, schema
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`,
  producer source `a0dca169…`, artifact
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- Only these test sources were changed, copied byte-for-byte from Runtime
  `7e160c5d`: `tests/test_timeline_public_s2_mixed_cli_journey.py` and
  `tests/historical_audio_fixture.py`.

The central request, snapshot, external-source manifest, and actual imports
were kept distinct:

- request: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-original-raw27-two-node-pair-original-raw27-two-node-pair-integration-1020182542-6174/request`
- snapshot: same result directory `snap`, tree `ee9ff255d6fd04523c54dc2656710e2523599a2c`
- external source manifest: same result directory `ext`
- actual Runtime import: central snapshot's `runtime_protocol/__init__.py`
- actual Agent import: `/home/user/work/wt/agt-pin-27e823a5/astrid_runtime_client/__init__.py`
- normal artifact source: `/home/user/work/wt/rt-pin-a0dca169/contract/artifacts.json`

## Tests

Local source preflight and collection:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/home/user/work/wt/agt-pin-27e823a5 /home/user/work/venv-agent/bin/python -P -c '<Runtime/Agent import and 0.2.14/a0/f021 metadata assertions>'
source preflight OK
/home/user/work/venv-agent/bin/python -m pytest --collect-only -q -p no:cacheprovider -m integration --runxfail tests/test_timeline_public_s2_mixed_cli_journey.py
2 tests collected
git diff --check
```

The named central suite is `original-raw27-two-node-pair-integration`; it
guards the exact Runtime and Agent identities, uses the actual Runtime and
Agent paths through `ASTRID_RUNTIME_CHECKOUT`/`ASTRID_CHECKOUT` and `PYTHONPATH`,
uses `--runxfail`, and runs only the two parameter nodes.

Central result (exit 1, 9.13s): **1 passed, 1 failed**.

- `literal-media`: passed.
- `historical-audio`: failed before the real CLI POST during sibling-fixture
  setup/use. The first semantic failure is:

  ```text
  could not open 'historical-audio-pcm' in '7b6f2bae8ffe42bf925216c38249ed79':
  ErrorObject(code='not_found', message='internal timeline revision not found',
  details={'revision': 'film-internal-1', 'timeline_id': 'historical-audio-pcm'})
  ```

  The unchanged test then reports at
  `tests/test_timeline_public_s2_mixed_cli_journey.py:308` that the CLI exited
  without submitting native trim. Full log:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/rt-m2-original-raw27-two-node-pair-original-raw27-two-node-pair-integration-1020182542-6174/log.txt`.

The merged fixture clones the captured child revision records while publishing
the sibling as `historical-audio-pcm`; exact Runtime 7d then looks up
`film-internal-1` under the sibling timeline and refuses it. This indicates an
incompatibility between the authorized merged test source and the exact 7d
product source. I did not rewrite the fixture or alter Runtime behavior because
the task explicitly forbids deviating from the settled source-only request.

No full, browser, exhaustive matrix, or unchanged retry was run. The original
19-byte malformed control remains local-only; the genuine WAV setup leaves the
authored duration absent. Runtime product files, generated artifacts, Agent
files, normal producer files, and shared dependencies were not changed.
