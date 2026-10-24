Implemented the narrow forward fix; **integration remains blocked**.

- Changed only `_doc_patch.py` and new occurrence-reorder tests.
- Allows guarded occurrence `list.move`, preserving complete rows, membership, native owners and pins.
- Added native row reads to detect same-row writes and ABA.
- Preserved the six root-assignment source lines and its test file exactly.

Causal parent run: **2 failed** at the managed-edge refusal. Both acceptance cases now pass.

Final targeted command, using the prescribed pinned Runtime environment:

```bash
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= \
  -p no:cacheprovider --timeout=45 --tb=short \
  tests/editing_conformance/test_doc_patch_occurrence_reorder.py \
  tests/editing_conformance/test_doc_patch_v2.py \
  tests/editing_conformance/test_doc_patch_mirrors.py
```

**142 passed, 3 failed.** All existing guards pass. The three new failures expose `_commit_patch.py:743–753`: it cannot replay occurrence `list.move` effects through history. Consequently, order/ABA conflicts return `history_unavailable`, and a permitted disjoint merge fails. Expectations remain intact. I left that file untouched because ownership is restricted.

Validation:

- `ruff check . --no-cache --output-format=json`: parent/current **2,145**, identical diagnostic identities and multiplicities.
- Private `mypy astrid scripts/reshape` with parent shadow source: parent/current **1,909**, identical diagnostic identities and multiplicities.
- Ruff on changed files, `scripts/artifact_manifest.py --check`, and `git diff --check`: **passed**.
- `scripts/vendor_lock.py check runtime.lock.json`: **passed**. Producer-qualified check reports the existing `34eac004` versus execution-fixture `8ea0766f` mismatch; no pins changed.

Next: assign the history-scanner correction, then combine with publisher source **`5b5eab591a65774e248386fa2cb87c0b1a980a90`** and run `test_reorder_emits_source_bound_list_move_and_keyed_timing_changes`. That combined witness remains unverified here.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. No full suite ran.