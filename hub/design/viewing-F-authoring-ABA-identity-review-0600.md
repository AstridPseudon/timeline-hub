## Verdict

- Controls: PASS — `2 passed, 7 deselected`.
- Source proposal: FAIL/unqualified. No product repair applied.

## Findings

- `_shot_item_path()` does not enforce a complete bijection: missing mappings fall back via `mapping.get(identity, identity)`, and extra/unbound mappings are accepted.
- It does not authenticate source owner, shot revision, internal revision, or digest against the current published occurrence. Changed-revision and foreign-owner cases remain unsafe.
- `authored=True` only translates leaf paths. Whole `payload.items` aggregate writes remain published-ID values in placement-local storage.
- The inverse hunk only adds `item_id:` lookup; it does not establish exact aggregate folding, stage-boundary order guards, or root/leaf ordering preservation.
- `assets` and `audio_bindings` still emit numeric paths. Declaring them out of scope means the native media caller is not fully repaired.
- The new controls do not exercise State storage, inverse folding, mapping corruption, owner/revision changes, ABA, or media scope.

Original `tests/timeline/test_authoring_media.py` remains byte-identical to `9cd3dbe86`; the 59 original assertions are preserved.

## Evidence

- Targeted controls: PASS.
- Ruff on changed test: PASS.
- Mypy on changed test: PASS.
- `git diff --check`: PASS.
- Recorded prior evidence reused as instructed: author0554 `2 failed, 78 passed`; media `113 passed`.
- No full/live/browser/HTTP/install runs performed.

Required next work: Agent R1/R2 must implement authenticated bijective mapping validation, owner/revision/digest/order guards, aggregate projection, complete inverse stage folding, and explicitly scoped assets/audio handling before re-review.