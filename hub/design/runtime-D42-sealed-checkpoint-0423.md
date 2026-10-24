**BLOCKED — checkpoint only; the D42 implementation is incomplete. Do not release this as the fix.**

The unsafe early return remains at [timeline_commit_store.py:419](/home/user/work/wt/rt-R-D42-sealed-validation-sol-0423/runtime_protocol/timeline_commit_store.py:419). Its dependency comparison misses mutable state that changes cold validation.

Added three regressions in [test_timeline_history_memo_state.py](/home/user/work/wt/rt-R-D42-sealed-validation-sol-0423/tests/test_timeline_history_memo_state.py:20): active resolver replacement and direct-global class/callable mutations. All confirm cold refusal and unchanged database rows. The six prior regressions remain intact.

I discarded the snapshot prototype: it passed seven demonstrated attacks but failed three existing cache controls and still accepted both direct-global attacks. **Production source is unchanged.**

Final required test command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
ASTRID_CHECKOUT="$TMPDIR/agent4151" \
/home/user/work/venv-runtime/bin/python -m pytest -q \
-o addopts= -p no:cacheprovider --tb=line \
--basetemp="$TMPDIR/required-final" \
tests/test_timeline_inverse_stage_authentication.py \
tests/test_timeline_history_memo_inputs.py \
tests/test_timeline_history_replay_memo.py \
tests/test_timeline_history_memo_dependencies.py \
tests/test_timeline_history_memo_state.py
```

Result: **184 passed, 9 failed**, two existing warnings. A final isolated state-file run reproduced all nine failures. No corrected-source GREEN proof or 145-case qualification was obtained.

Other verification:

- Exact read-only Agent `415181d983d6d1d56a912da16ad4c5690e663187`: **3,453 blobs verified**, import origins confirmed.
- `ruff check --no-cache`: parent/final **11 findings**, zero normalized additions/removals; changed test file clean.
- `pyright --outputjson --pythonpath /home/user/work/venv-runtime/bin/python runtime_protocol`: parent/final **1,449 diagnostics**, zero normalized identity or multiplicity changes.
- `python scripts/artifact_manifest.py --check` and `git diff --check`: passed.
- All **64 protected hashes unchanged**; aggregate `a0211ffaa76476c668385c739e0862279817c0e20cae32d9c847214a53ca0923`.

`commit-msg` and `BLOCKED` are written; no `DONE` or Git mutations. Next: complete the sealed boundary while retaining all nine RED cases, then run the full requested targeted qualification and independent review.