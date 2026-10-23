# PASS — R1 inherited read-capture correction review

Reviewed HEAD `169293c92` (`fix(timeline): separate R1 inherited reads from native claims`) against parent `fa2cf5b66`, per PLAN §3 R1 / contract §§1 and 3.

## Review result

PASS. The product delta is the requested five lines in `astrid/sdk/timeline/commands.py`; the added 111 test lines cover the mixed native `move` + `doc.patch`/meta case, both `fields` and `atomic`, forged native claims, landing-head replay, and request/step dependency conflicts including A→B→A. The only other commit content was the inherited design report.

The boundary is correct: `CommitPatch.before` evaluates request reads once at batch entry and step reads at each step input; the change temporarily removes only those inherited observations before `_verify_claims` and native execution, so submitted native `command.reads` remain exact authored captures. After capture verification, it restores inherited plus native reads with equality deduplication. `record.reads`, step dependencies, bindings, history, and undo therefore retain the complete original-boundary union. There is no refresh after execution, discarded read/history path, or blanket exemption: missing/extra/forged native claims still take `capture_mismatch`.

The original v2 scope remains present: base/publication, commands, label, steps with patch and reads, merge, optional request reads, dry-run, accepted/merged data and receipt/effects/dependencies, conflict/invalid/preview behavior, and the production caller. No plan decision changed.

## Evidence

All commands ran from this worktree with `PYTHONPATH=$PWD:/home/user/work/runtime`, private caches under `/tmp/agt-R1-inherited-review-0145`, and `/home/user/work/venv-agent/bin/python` unless noted.

- `.../python -m pytest -q ... tests/editing_conformance/test_doc_patch_v2.py tests/sdk/test_p1_doc_patch_provider.py` — **119 passed**.
- `.../python -m pytest -q ... tests/editing_conformance/test_doc_patch_v2.py -k 'mixed_native_capture or inherited_reads_do_not_authorize or mixed_native_inherited_reads or inherited_native_read_conflicts'` — **16 passed, 86 deselected**.
- `.../python -m pytest -q ... tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py -k 'paths_json_equality_claims_and_frozen_schema or original_capture_claims_are_verified_before_refresh or dependent_unsent_original_guards_allow_equal_state_aba_at_fresh_base'` — **3 passed, 234 deselected**.
- `.../python -m ruff check --no-cache astrid/sdk/timeline/commands.py tests/editing_conformance/test_doc_patch_v2.py` — **passed**.
- `/tmp/astrid-u2-typecheck/bin/python -m mypy astrid/sdk/timeline/commands.py --hide-error-context --no-color-output --no-pretty --show-error-codes` — **passed; no issues**.
- `.../python -m scripts.reshape.compare_ruff_baseline` — **current=2151, baseline=2151**.
- `/tmp/astrid-u2-typecheck/bin/python -m scripts.reshape.compare_mypy_baseline` — **current=1915, baseline=1915**.
- `git diff --check HEAD` — **passed**.

No product or test files were edited by this review. No full, browser, live Runtime, schema, generated-file, pin, shared-dependency, or git mutation was performed. The inherited report was copied to the flat ORCH design path and deleted only from this worker worktree as authorized.

## Remaining qualification boundary

True wire/provenance qualification remains Runtime-owned and unqualified. The detached provider tests do not qualify real HTTP `merged` envelopes, Runtime persisted history/idempotency, authorization, generated schema/client validation, or Runtime binding provenance. The parallel R3 invalid-envelope repair and Runtime provenance work remain prerequisites for joined native service qualification.
