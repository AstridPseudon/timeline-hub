# rt-m2-render-fixture-preserve

## Result

No product or test-source edits were necessary. The current tree already contains the required accepted sole-writer fixture migrations:

- `tests/test_canonical_render_admission.py` uses `TimelineCommitStore` acceptance for canonical render-positive setup.
- `tests/test_direct_render_admission.py` uses constrained host acceptance for direct render-positive setup. Its two legacy-shot cases restore authenticated historical M1 archives only to preserve intentional negative admission behavior; they do not save retired shapes.
- `tests/test_idempotency_compaction.py` inserts historical command-kind rows only to exercise compaction policy; it does not invoke a retired publisher.

All existing idempotency, custody, snapshot, claim/retry, restart/reopen, compaction, refusal, and positive assertions remain unchanged.

## Evidence

- Local targeted run: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -B -m pytest -q tests/test_canonical_render_admission.py tests/test_direct_render_admission.py tests/test_idempotency_compaction.py` — **87 passed in 35.32s**.
- Central bounded whole-file run: request `rt-m2-render-fixture-preserve-targeted-1020005042-15909`, command `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_canonical_render_admission.py tests/test_direct_render_admission.py tests/test_idempotency_compaction.py` — **87 passed in 35.04s**, exit 0.
- `git diff --check` — clean; worktree has no product/test-source diff.

## Decisions and limits

No new decisions were needed. The requested `tests/test_direct_render_journeys.py` does not exist in this checkout; the actual file is `tests/test_direct_render_admission.py`. No full suite, browser, live-socket, or cross-repository suite was run. M2 integration remains held per the orchestrator instruction.

## Recommended next step

Orchestrator review can treat this worker as a no-op qualification and proceed with the existing accepted fixture commits; no merge is needed from this worktree.
