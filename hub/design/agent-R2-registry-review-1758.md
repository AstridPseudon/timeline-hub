# R2 registry inverse review

## Verdict

**PASS for the isolated registry delta only.** Review target: `22f1cb169bfd0f2aed79910c047581cd970c9541` (`tl/agt-R2-registry-sol-1750`), based on `079580ca46af77e0292d49dc34386b25c8391f99`. The delta is limited to the 16-line `coalesce` change in `astrid/sdk/timeline/inverse.py` and the 124-line focused test file `tests/editing_conformance/test_inverse_registry_containers.py`.

The change projects a sequential `parent/asset:<id>` write into the directly authored physical `parent.registry.assets.<id>` landing image only while the direct registry container is present. It preserves the original native asset writes and exact before/after states for sequential reversal, history scans, source-order checks, collection-order checks, and ABA checks. It does not add a public API, schema, client, operation, guard waiver, or C0 field.

## Findings against the settled criteria

- PLAN §3 R2: the registry-container reload/undo/redo boundary is corrected without weakening the existing inverse guards. The original authored six-node behavior remains green on the final source.
- C0 §§2/3/5: no request/reply shape, addressing contract, dependency, history, or undo protocol was changed. The implementation is internal coalescing of already-authenticated provider records; physical source writes remain intact.
- New strict controls cover changed ancestor, changed child asset, changed child clip, foreign asset identity, out-of-order source writes, asset ABA, ancestor ABA, occupied ID, and no-write immutability assertions. They also cover direct/mirrored/absent storage, image/video round trips, disjoint registry sibling preservation, and the “asset before direct registry creation” boundary.
- No blocking finding was identified within the assigned registry delta. No source edit was made by this review.

## Independent evidence

All logs are retained under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-review-1758/evidence/`.

| Check | Exact command/result |
|---|---|
| Original six | `TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-review-1758/evidence/tmp-test-original PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py -k "missing_registry_containers_are_guarded_writes_with_exact_inverse_redo and not config"` → **6 passed, 79 deselected**; `review-original-six.log`. |
| New controls | `TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-review-1758/evidence/tmp-test-new PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_inverse_registry_containers.py` → **41 passed**; `review-new-41.log`. |
| Ruff | `TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-review-1758/evidence/tmp-ruff PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e RUFF_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-review-1758/evidence/tmp-ruff-cache /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline && /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/inverse.py tests/editing_conformance/test_inverse_registry_containers.py --output-format concise` → **current 2149 = baseline 2149; all checks passed**; `review-ruff.log`. |
| Private Mypy | `TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-review-1758/evidence/tmp-mypy PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-d9e2a71e MYPY_CACHE_DIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-review-1758/evidence/tmp-mypy-cache /home/user/work/venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline` → **current 1912 = baseline 1912**; `review-mypy.log`. |
| Integrity | `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json && PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check && git diff --check` → **pass**; `review-integrity.log`. |

The author’s bounded neighbor evidence remains accepted as disclosed context: **10 passed, 6 failed**, with the same six failures reproduced against the original inverse in the baseline comparison at `_step_undo.py:169` (`nested inverse ranges differ from accepted history`). Per task instructions, I did not rerun those six and do not treat them as a registry-delta blocker or assume a whole-suite pass. The author’s logs are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-registry-sol-1750/evidence/`.

## Source and field audit

`review-source-audit.log` records exact SHA-256 values. HEAD is `22f1cb169bfd0f2aed79910c047581cd970c9541`; base is `079580ca46af77e0292d49dc34386b25c8391f99`.

- Changed source: `inverse.py` current `00c19d53ecc7d5b3940906ad16cabf9cb1d07335feda0012d5faf038dd87b01f`; base `626f26805c406081ad034af73459c85e350cbaeeba3bddc2021f1eb5f97a72ab`.
- Changed field: `coalesce` current `be7007637b85c59555e4fa01ed103869503f5cc7b079b296a8c5d74656053ae0`; base `5a49ef8a17c031a0c28a9c466dd442a3280b3cb480a8e3e2bf18bfc37cdc7c2a`.
- New focused test SHA-256: `353f59f08e63c00ae4a9e8e6aa55ed1234e0c751a16b8ca99c17832b755d5d78`; absent at base.
- Exact protected-file equality passed for `test_recipe_m2_parent_media.py`, `_recording.py`, `_step_undo.py`, `_commit_patch.py`, `commit.py`, `runtime.lock.json`, and `artifacts.json`.
- `git diff --name-status` reports only the two intended files; the review worktree is clean after removing its temporary audit script.

## Scope limits and next steps

No full suite, live socket/browser journey, mounted/public Runtime acceptance, C0 receipt, dependency install, daemon, merge, or Git ref mutation was run. The review qualifies only the registry delta. The separate nested inverse-stage/effect-range repair remains with its owner; merge this narrow change through the Agent queue without requiring that outside repair first.
