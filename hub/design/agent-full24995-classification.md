# Agent full24995 classification

Date: 2026-10-20

## Exact historical result

The requested run was agent-full-remotion12-s2-integration-1020143255-24995,
completed against Agent commit 8130a401bf44a518d5a40ae274d398b8c560be55
and source tree 236c3e57e0265c52b81ba8085de3193026176bff. It was not rerun or
relabeled against the later current tree.

Recorded command:

    env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/nix/var/nix/profiles/default/bin:/root/.local/bin:/root/.cargo/bin:/usr/local/go/bin:/opt/node22/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-current ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent-child-s2/lib/python3.13/site-packages ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-0012/node_modules ASTRID_VIBECOMFY_CHECKOUT=/home/user/work/fixtures/vibecomfy PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent-child-s2/bin/python -m pytest -q -n 3

Result: **14,696 passed, 3 failed, 452 skipped, 4 xfailed, 83 warnings, 565
subtests passed** in 3,879.09 seconds. The exact three failed nodes were:

- tests/packs/timeline/test_cli_assets.py::test_edit_replace_asset_and_swap_asset_forward_to_the_sdk
- tests/packs/timeline/test_cli_voice_bindings.py::test_replace_insert_and_from_script_forward_existing_sdk_arguments
- tests/packs/timeline/test_cli_voice_bindings.py::test_repeated_gap_flags_and_script_gap_override_preserve_sdk_rules

## Classification

All three failures are one test-fixture compatibility issue, not product
behavior failures. Each traceback reaches
astrid/packs/timeline/cli.py:3298, where _cmd_edit calls
tl._check_core(), and stops with:

    AttributeError: 'FakeCheckout' object has no attribute '_check_core'

The fixtures already provided check() returning the intended "valid" report.
The current CLI change f5d0b4e0 intentionally switched this implicit preflight
from check() to _check_core() as part of separating scene checks from save
validation. The fixtures were not updated with the equivalent test seam. No
forwarding, default, repeated-gap, script-gap-override, or argument assertion
was reached or contradicted by the historical tracebacks.

## Bounded repair

The current worker tree adds _check_core = check to the fake checkout in each
of the two affected test files. This preserves the existing fake result and
all original assertions. No product source, skip, xfail, expected value, or
CLI behavior was changed.

Current-fix identity:

- base worker commit: 30fc8dd154015a7c58cf4ce7b065ccc46f470ee8
- base worker tree: 50925d6df67ce717653e3ce7ac12803f8865da93
- changed-files binary patch SHA-256:
  415744518d1223940e6e1588ebe9c6eee0a26250b7696063f36771ad387bd45b
- final edited-file SHA-256 values:
  - tests/packs/timeline/test_cli_assets.py:
    deb336a4e5e265b516d93c3cafe89bc3cc6460ccf95f0ff137be6037ca69cb1a
  - tests/packs/timeline/test_cli_voice_bindings.py:
    88d282086e79a22d92a6b581bad86798d07b503f71623e6825d4433d7d4e2e94

## Targeted proof

The exact historical full suite was not rerun.

    PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/timeline/test_cli_assets.py tests/packs/timeline/test_cli_voice_bindings.py
    4 passed in 0.88s

    PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q tests/packs/timeline/test_cli_*.py tests/packs/timeline/test_verbs_working_copy.py
    254 passed in 20.99s

    PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check --select E4,E7,E9,F tests/packs/timeline/test_cli_assets.py tests/packs/timeline/test_cli_voice_bindings.py
    All checks passed!

    git diff --check
    clean

Unscoped Ruff also reports one pre-existing I001 import-order finding in
test_cli_assets.py; no import formatting was changed for this bounded fix.

Recommended disposition: accept the three historical failures as repaired
test-environment/fixture failures, retain the full-run count as historical
evidence, and let the harness commit this two-file test-only fix. A future full
qualification may be requested by the orchestrator when appropriate; this
worker did not request or run one.
