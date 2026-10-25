# D100a clean intake validation

## Result

Source intake PASS for the approved two-file delta. The current integration
preimage was checked before application. The product file matched the approved
donor parent byte-for-byte; the test file was absent as expected. After
application, both files match the approved final blobs and modes exactly.

This is source custody and static validation only. No new behavioral PASS,
count deduction, provider execution, or release-gate result is claimed here.

## Exact source checks

- Current head/tree before edits: `9521bed8e3174d5fe257d3b8d75828121bec4150` /
  `2e44289552b3cd52152e80f22f21d5e12d1bf52c`.
- Approved donor range: `d4ba991638f7d94e6b9f91f5a463cd3587af00eb..42040a9c05ae7105cf88459cad5f0b8b9bf56fd1`.
- Approved range path census: exactly `astrid/sdk/timeline/_command_state.py` and
  `tests/sdk/test_d100_item_birth_boundary.py`.
- Product current preimage blob `4bbb4615d276ecae57965993e38080c77a93f757`
  equals donor parent; post-apply blob is `09cbeeddefdc6375ba7d026406c95fb35bafda40`
  with SHA-256 `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a3`.
- Test post-apply blob is `39ed571d5f3e49d2545fc31e1f868ee7c58dbc8a` with
  SHA-256 `fcd5f187e185faa2222fb23c69827bd6d8bcbb710fdad131f649973f95e6de37`.
- Both modes are `100644`; no outside-scope worktree path changed.
- `git diff --check` — exit 0.

## Static commands

- `RUFF_CACHE_DIR=/tmp/w-97b59b89ac/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_command_state.py tests/sdk/test_d100_item_birth_boundary.py` — exit 0, all checks passed.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/mypy --config-file pyproject.toml --no-incremental --cache-dir=/tmp/w-97b59b89ac/mypy-cache astrid/sdk/timeline/_command_state.py tests/sdk/test_d100_item_birth_boundary.py` — exit 0, no issues in 2 source files.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /usr/bin/python3.11 -c 'from pathlib import Path; paths=(Path("astrid/sdk/timeline/_command_state.py"), Path("tests/sdk/test_d100_item_birth_boundary.py")); [compile(p.read_text(), str(p), "exec") for p in paths]'` — exit 0.
- `git diff --check` — exit 0.

## Prior proof scope and limits

The owner release filing records authentic 27/27 on Runtime
`ab1e4f6141987706132916e2da16477f5a019464`, independent security review 1803
as `PASS_SOURCE_SECURITY`, and zero B022 function/path intersection. Those
existing results are reused as prior proof scope only. The original 9 gate is
separate and remains open; managed105/media48 and Farm full-core work remain
downstream. No repeat of those bodies was run.

The named peer filing and standalone release-assessment packet were not present
as files in this sandbox; the complete manager inbox filing and retained review
artifacts were available. No fetch, reconstruction, checkout, or ancestry
import was used.

Per the brief, pytest, provider import/execution, Runtime service/request-test,
full/family/cohort runs, and behavioral qualification were not run.
