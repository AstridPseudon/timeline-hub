# D100/R1 source-only validation

Result: source checks PASS; behavioral tests NOTRUN.

The only worktree change is the additive test `tests/sdk/test_d100_item_birth_boundary.py`. The protected product file `astrid/sdk/timeline/_command_state.py` remains byte-exact at SHA-256 `018f174004bf9b9c275aa23ef6ceb432ce9d7294d71e3024f96353c25fa808a`. The source-manifest records all referenced read-only source/fixture hashes.

## Changes

- Split both broad source-mapping equality expectations into exact authoritative comparisons of `source_mapping.shots`, `source_mapping.placements`, and `source_mapping._runtime_document`.
- Assert that `_doc_patch_images` is the only additional top-level source-mapping key, then compare its exact owner/source physical IDs and revisions, authored payload, and internal timeline projection.
- Set the direct shared-owner fixture's source offset to admitted default `0` before command setup and recompute its authored parent digest with the existing `_digest` helper.
- Preserved the item correspondence, canonical document, internal revision, original-bundle immutability, wrong-pair, digest, unique-ID, and no-write predicates.

## Commands and exits

- `/home/user/work/venv-agent/bin/ruff check tests/sdk/test_d100_item_birth_boundary.py` — exit 0 (`All checks passed!`).
- `/home/user/work/venv-agent/bin/mypy --config-file pyproject.toml --cache-dir=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-Agent-D100-test-return-1914/tmpdir/mypy-cache tests/sdk/test_d100_item_birth_boundary.py` — exit 0 (`Success: no issues found in 1 source file`).
- `/usr/bin/python3.11 -c 'from pathlib import Path; p=Path("tests/sdk/test_d100_item_birth_boundary.py"); compile(p.read_text(), str(p), "exec")'` — exit 0; Python 3.11.17 compile passed without writing a pyc.
- `git diff --check` — exit 0.
- Read-only AST/source/hash check — exit 0; required custody/cache/default-offset fragments present, only assigned test path in `git diff --name-only`, product and referenced read-only hashes exact.

## Behavioral admission

Free space measured at `4,632,576,000` bytes at admission and `4,587,384,832` bytes after source checks, below the required `5,000,000,000`-byte ordinary/light behavioral floor (the final value is also below the `4,600,000,000` source floor). The targeted pytest command was not started:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d100_item_birth_boundary.py
```

No full suite, old TEN/P4, browser, socket, provider-body, collector, acquisition, Store/install, alternate environment, or App test was run/requested. Prior source-author/security PASS evidence for the unchanged product remains retained; this worker makes no new behavioral claim. Source `9486cbb…` remains HELD.

## Handoff state

Harness commit SHA/tree are pending because this worker does not commit or write Git refs. Before App's meaningful corrected-27 proof, obtain one independent protected review of this exact test delta. After the bounded Agent result is GREEN, App remains the sole owner of its exact `f53b` original-9 receiver proof. The receiving recipe contains the required order and hold conditions.
