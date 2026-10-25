# Validation

All checks were read-only except creation of this evidence packet.

## Exact source and custody checks

- `git rev-parse HEAD^`: `9521bed8e3174d5fe257d3b8d75828121bec4150`.
- Own name-status: exactly `M astrid/sdk/timeline/_command_state.py` and `A tests/sdk/test_d100_item_birth_boundary.py`.
- Donor range name-status: the same exact two paths.
- Product base blob equals donor parent blob `4bbb4615d276ecae57965993e38080c77a93f757`.
- Test path is absent at the requested base.
- Product final blob `09cbeeddefdc6375ba7d026406c95fb35bafda40`, SHA-256
  `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.
- Test final blob `39ed571d5f3e49d2545fc31e1f868ee7c58dbc8a`, SHA-256
  `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37`.
- Both final modes are `100644`.
- `git diff --binary` own delta equals donor delta byte-for-byte.
- AST comparison: all module nodes outside `State` and all `State` methods
  outside the three approved methods are exact.
- Protected identity16, typed-FPS, U2, U4a, and canonical15 source ancestry or
  bytes remain preserved by the exact two-path delta.

## Static call-chain and contract checks

Read-only source inspection verified Runtime registration and `commitTimeline`,
the coordinator’s registered `provider.commit` call, Agent provider execution,
`commands.execute`, the `doc.patch` operation, and State dispatch to the three
approved methods. The C0 contract still contains the specified request fields,
accepted/merged/conflict/invalid replies, preview `would_status`, and history,
binding, effect, dependency, and undo fields. No contract or caller file is in
the own delta.

## Permitted static checks

- `RUFF_CACHE_DIR=/tmp/w-beb19d12f6/agt-R1-D100a-receiving-review-2341/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_command_state.py tests/sdk/test_d100_item_birth_boundary.py` — PASS (`All checks passed!`).
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-R1-D100a-receiving-review-2341 /usr/bin/python3.11 -c '...'` compiling the two touched files — PASS.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-R1-D100a-receiving-review-2341 /home/user/work/venv-agent/bin/mypy --config-file pyproject.toml --no-incremental --cache-dir=/tmp/w-beb19d12f6/agt-R1-D100a-receiving-review-2341/mypy-cache astrid/sdk/timeline/_command_state.py tests/sdk/test_d100_item_birth_boundary.py` — PASS (`no issues in 2 source files`).
- `git diff --check` — PASS.

Pytest, provider imports/execution, Runtime services, browser/live sockets,
original9 reruns, managed cohorts, and full suites were not run by this
receiving review.
