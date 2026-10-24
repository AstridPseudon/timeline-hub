Implemented the D42 complete-input memo in [timeline_commit_store.py](/home/user/work/wt/rt-R-D42-complete-input-memo-sol-0330/runtime_protocol/timeline_commit_store.py), with separate [memo tests](/home/user/work/wt/rt-R-D42-complete-input-memo-sol-0330/tests/test_timeline_history_replay_memo.py).

The 256-entry process-local LRU caches successful deterministic replay/schema validation only. Its key includes exact accepted row bytes, every captured replay input, realm, and schema/validator version. Fresh envelope, event-prefix, sequence, closure, continuation, inverse-history, and sequential identity checks remain outside the memo. No results or caller-owned objects are retained.

Verification stays under the existing mutex: the fresh checks use the shared SQLite connection, and no immutable snapshot was established.

Validation used Runtime parent `42080f33d778fcb979f0c437f2198370e3202898`, tree `89727e1a35c88b71a47816b08f02b3d4822b331d`, and an exact Agent `415181d983d6d1d56a912da16ad4c5690e663187` archive, tree `f49cae445194350ed6def2aed65abbf4d870f639`.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
ASTRID_CHECKOUT=/tmp/w-7dfe8f3514/agent4151 \
/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= \
-p no:cacheprovider --basetemp=/tmp/w-7dfe8f3514/lane145-final \
tests/test_timeline_history_boundaries.py \
tests/test_timeline_commit_authentication.py \
tests/test_timeline_commit_read_basis.py \
tests/test_timeline_history_authenticated_read.py
```

**145 passed in 46.51s.**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python \
ASTRID_CHECKOUT=/tmp/w-7dfe8f3514/agent4151 \
/home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= \
-p no:cacheprovider --basetemp=/tmp/w-7dfe8f3514/inverse-final \
tests/test_timeline_inverse_stage_authentication.py \
tests/test_timeline_history_memo_inputs.py \
tests/test_timeline_history_replay_memo.py
```

**159 passed in 39.68s**, with all seven witnesses and existing refusal assertions unchanged.

The independent replay-counter test is **parent RED / candidate GREEN**: parent replay calls rise from 2 to 4 on the second read; candidate adds no replay or schema work.

Uninstrumented accepted-entry timings used retained native21/P1 state, reconstructed with authenticated parent joins:

| Fixture | Parent cold / repeated | Candidate cold / warm |
|---|---:|---:|
| native21 | 2.590 / 2.258, 2.002s | 2.081 / 0.164, 0.160s |
| P1 | 0.383 / 0.380, 0.404s | 0.303 / 0.023, 0.025s |

Replies matched across parent/candidate and cold/warm reads. These measure `history_entry`, not HTTP or browser readiness.

Additional checks:

- `pyright --outputjson --pythonpath /home/user/work/venv-runtime/bin/python runtime_protocol`: parent/final **1,449 diagnostics**, zero new or removed normalized identities/multiplicities.
- `ruff check runtime_protocol/timeline_commit_store.py tests/test_timeline_history_replay_memo.py`: **11 unchanged existing findings**; new test file passes.
- `python scripts/artifact_manifest.py --check`, `git diff --check`, and new-file diff check: passed.
- All 64 protected contract/schema/client files remain identical. Manifest SHA-256: `a0211ffaa76476c668385c739e0862279817c0e20cae32d9c847214a53ca0923`.
- Runtime imports resolved here; Agent imports resolved from the exact archive; generated client resolved from this worktree’s `packages/python`.

Prospective final tree: `a51d298e6b5d5ab4edfbaa4bb1f42f31bf367719`. Only the store and new test file changed. C0 wire shapes, server guards, old assertions, and historical `079` transcript-failure evidence remain unchanged.

No blockers. No full suite, browser, HTTP, or Git writes performed. Commit message and `DONE` are written. Next: independent security review, normal merge, then the separate D41 backport.