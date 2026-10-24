## Verdict: FAIL

- Test ID: `agent-authoring-current8ea-nodes-1024050427-11466`
- Agent head/tree: `9cd3dbe865a941c052bda04ae0d61306d18f8f26` / `57f0231da0d7904ecd8778169973d6384e0ae141`
- Test: `tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba`
- Result: 1 collected, 1 failed, 29.28s.

Exact managed command:

```bash
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-8ea0766f" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_RUNTIME_SOURCE_ROOT=/home/user/work/wt/rt-pin-8ea0766f ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-v3-819acf-1110 ASTRID_TEST_NODE_MODULES=/home/user/work/runtimes/agent-remotion-v3-819acf-1110/node_modules ASTRID_NODE_EXECUTABLE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.13/site-packages /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 -m integration tests/timeline/test_authoring_media.py::test_real_runtime_document_script_same_alias_rebind_reload_undo_retry_and_aba
```

The first meaningful boundary is the undo call at line 1088. Runtime returned:

```text
validation_error: provider observation has an ambiguous item path
details.status=refused
details.reason=invalid_records
receipt=None
idempotency_key=wc6-undo
```

This occurred before the lost-ACK trap. The path/source investigation remains owned by `agt-F-ABA-11466-path-0507`; no cause was inferred here.

Source/assertion custody:

- Function lines 700–1173, 24,123 bytes.
- 59 assertions retained; 40 executed before failure, 19 remained unrun.
- Current function AST exactly matches the retained original source at commit `4e1004511`.
- Direct body SHA-256: `d0633f31274765d8bb08148db2a841e59b85e72a7d6b4768cd6430a215b1d321`.
- Packet index verification passed: 6 packet files matched recorded sizes and SHA-256 values.
- Reviewed Agent provider origins are the assigned worktree’s `commands.py`, `commit.py`, and `_commit_patch.py`; the packet records Runtime `8ea0766f`, Node `20.19.4`, and Remotion `819acf`. Those managed paths are no longer present locally, so I did not reconstruct or rerun them.

Unrun predicates include lost-ACK persistence/retry, restart idempotency, undo history, disjoint rebase, bad-write refusal, redo, and final ABA undo conflict.

Historical results remain unchanged:

- `Original13559`: FAIL at undo with “landing execution output differs from the prepared document.”
- `old26248`: stale-oracle failure.
- Neither is relabeled.

Checks:

```text
git diff --check: PASS
```

No product, test, generated, pin, or dependency changes were made. `DONE` and the commit message were written.