## G3/G5 cumulative frontdoor review

**PASS for the source and targeted P1 gate; live Runtime HTTP qualification remains unverified.**

Reviewed the settled plan, the 1602 failure report, the 1606 author report/evidence, and the current return commit.

### Source and diff

- Original frontdoor commit: `23cac8b72b29188b3a42cd63aa7a8821fa51abce`, parent `cc8be25d4ad46fae3f7d0889aaee88f85ab6a9c6`; exactly four files changed in that first attempt.
- Reviewed return commit: `4b248adc5c22e05b6168284aa8ceace8afe61752`, parent `23cac8b72`; exactly two files changed: `astrid/packs/timeline/cli_native.py` and `tests/packs/timeline/test_cli_document_commit.py`.
- `git diff --check 23cac8b72 4b248adc5`: PASS.

The production route is `cli._cmd_commit` → `commit_document` → authenticated `TimelineSession.open` with the detached document's exact base revision/publication pair → G2 `Timeline.commit` → G3 emitter. Runtime remains authoritative for retry, body hash, auth, scope and base-pair validation. The 1602 local one-page/200-entry receipt replay and any second executor are gone; blank keys are refused before outbox creation. Existing persisted outbox sidecars are supported G2 behavior.

The official Runtime producer `34eac0041b0891e9011966b39bcbd26053fde5bc` source-checks exact scoped key/hash lookup after authorization. The 200+ history attack is no longer a client history scan. The regression tests simulate a 201-row fake history shape, but are not claimed as HTTP evidence. Normalization tidies only generated empty film app containers; direct probing preserved unknown data containing `None`, explicit `null`, and absence. Human output and canonical Runtime receipt/result fields remain present.

The 1606 joined G5 blobs were **74 passed / 2 failed** because their separately owned fake fixture lacks Runtime key semantics; absent causal proof, these are not product defects and no assertions were changed.

### Evidence

- `PYTHONPATH="/home/user/work/wt/agt-G3-frontdoor-final-review-1612:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/timeline/test_cli_document_commit.py`: **12 passed in 2.64s**.
- Five-neighbor command: `PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 tests/packs/timeline/test_cli_parity.py::test_normal_commit_undo_preserves_full_v2_request_reply_and_history tests/packs/timeline/test_cli_parity.py::test_normal_commit_preview_preserves_full_v2_without_acceptance[undo] 'tests/packs/timeline/test_cli_parity.py::test_normal_commit_parser_has_no_retired_or_overwrite_options[--force]' tests/sdk/test_timeline_public_command.py::test_public_command_stays_private_and_commits_through_history tests/sdk/test_timeline_public_command.py::test_public_patch_preview_keeps_original_pair_and_reports_would_status`: **5 passed in 2.04s**.
- Ruff current/parent comparison (`ruff check` on `cli_native.py` and `test_cli_document_commit.py`, parent versions streamed with `git show`): **PASS**, zero added findings.
- Private mypy: `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy --follow-imports=silent astrid/packs/timeline/cli_native.py`: **PASS**, no issues; unchanged shared files retain the author's 87/87 zero-added-identity comparison.
- Artifact: `/home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`: **PASS**.
- Vendor: `/home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`: **PASS**, manifest matches.
- `git diff --check 23cac8b72 4b248adc5`: **PASS**.

### Limits

No product/shared dependency/branch/ref changes were made. No full/P1/live HTTP suite was run. The targeted tests use fake/in-memory transport, so central live qualification remains required for lost-ACK/restart, >200 history, changed-body/same-key refusal, and complete authenticated Runtime request/reply behavior.
