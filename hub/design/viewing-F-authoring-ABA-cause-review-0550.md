## Verdict

- **Causal finding: PASS.** `_replace_payload_media()` emits numeric paths such as `payload/items/0/media_id`, while Runtime requires identity-qualified list paths.
- **Test validity: PASS for offline controls.** Accept and preview both correctly remain red; strict numeric/missing/duplicate negatives pass.
- **Product behavior: FAIL/unverified.** No repair is approved or claimed.

## Evidence

Focused command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider \
--timeout=45 --tb=short \
tests/editing_conformance/test_authoring_item_observation_boundary.py
```

Result: **2 failed, 5 passed**. The two failures are the expected accept/preview controls, both reporting `invalid_records: provider observation has an ambiguous item path`.

Retained 0544 evidence: **2 failed, 76 passed** in neighboring controls. The attempted collection-write candidate caused **6 existing media regressions** and was withdrawn.

Also passed:

- Ruff: all checks passed.
- Mypy: no issues in 6 inspected source files.
- `git diff --check`.
- Original `tests/timeline/test_authoring_media.py` byte-identical to `9cd3dbe865`.
- Original ABA function contains all **59 assertions**.

## Source cause and minimum seam

- [`native_occurrence_media_commands.py:69`](/home/user/work/wt/vw-F-authoring-ABA-cause-review-0550/astrid/sdk/timeline/native_occurrence_media_commands.py:69) writes numeric item paths.
- Runtime’s strict resolver accepts only tokens such as `item_id:<id>`.
- [`State.get()`](/home/user/work/wt/vw-F-authoring-ABA-cause-review-0550/astrid/sdk/timeline/_command_state.py:290) exposes published item identities through `item_id_map`.
- [`State.set()`](/home/user/work/wt/vw-F-authoring-ABA-cause-review-0550/astrid/sdk/timeline/_command_state.py:369) stores collection values literally, without projecting published IDs back to placement-local authored IDs.
- Inverse storage/application delegates through the same unprojected path.

The minimum seam is the Agent-side published-to-authored identity projection shared by native capture, `State.set()`, and inverse normalization. It must use identity-qualified paths or a complete collection capture, while preserving the authenticated mapping.

Required guards remain: unique item identity, owner/revision/digest/order, exact before/after states, evaluation boundaries, native ranges, history/dependency/ABA checks, and no byte-equality retargeting or Runtime path relaxation.

The original private `11466` packet and withdrawn `collection-candidate.patch` were unavailable after worker cleanup; the preserved log contains the synthetic packet projection. No original/live/full/browser run was performed.