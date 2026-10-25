# R2 D110 independent protected/core review

## Verdict

**PASS.** Candidate `ccf831df632c0821fea0dec102b6fbd6a30439ad` is accepted for the normal release/merge queue, subject to the orchestrator's existing integration gates. No product or test files were changed by this reviewer.

## Scope and source custody

- Reviewed exact candidate `ccf831df632c0821fea0dec102b6fbd6a30439ad`, parent `b27ff3449ec4d9b5e14ac25b8f5a18c1999c21f6`, candidate tree `6056414359ae9fce08d999d54cbecf719fda33c3`.
- Exact diff is limited to `astrid/sdk/timeline/inverse.py` and new `tests/sdk/test_inverse_removed_shot_owners_runtime.py` (98 insertions, 1 deletion).
- Immutable Runtime producer is clean `/home/user/work/wt/rt-pin-1daca2a3` at `1daca2a33f6d7b10053e07c539a54843e3984e19`, tree `a522511414947e48e317a5e5c2103483b121a750`; lock source matches. No ambient Runtime was used.
- Author durable evidence was read without rerunning RED: `D110-red.xml` is 2 tests / 2 failures / 0 errors / 0 skips; `D110-green.xml` is 2 / 0 / 0 / 0; `D110-neighbors.xml` is 42 / 0 / 0 / 0. RED is the genuine registered-provider path ending in `KeyError: 'local-shot'` at `_doc_patch_materialize.remember`, surfaced by Runtime as catchall/503, not setup failure or swallowed substitute behavior.
- Author and candidate test bytes match SHA-256 `a325f2706e3d5c8c8b5b34e4fec6975206d7217a55e04dd4454a8cd39166ecdb`; candidate inverse bytes match author SHA-256 `6c794734cb763c21cec386f764bc63b94f3a74b4dd9f8464136a285c628d0423`.

## Decision and code audit

The one-line semantic addition at `inverse.py:1176-1177` is canonical under C0: after authenticated `restore_root_baselines`, it retains the existing live-owner filter and additionally excludes only `(owner, local)` pairs whose `local` shot is absent from the restored `bundle['shots']`. It does not broaden authority, catch exceptions, bypass materialization, alter guards, or change schema/client/Runtime/auth/store/pin behavior.

The production path remains `commit.commit -> commands.execute -> inverse.apply_inverse -> restore_root_baselines -> remember`; `commit.py`, `commands.py`, and `_doc_patch_materialize.py` are byte-identical to the parent. The full C0 request/reply contract was read through §§1–5: base pair, command envelopes, label/steps/patches, fields/atomic/read semantics, accepted/merged/conflict/invalid/preview replies, durable receipt/idempotency, and guarded whole/per-step inverse/history behavior remain outside this two-file diff. Historical rebased retries remain untouched.

The new real-provider ADD+Undo and SWAP+Undo cases assert the retained sibling row is unchanged, its source shot remains materialized in the accepted closure, and whole-commit inverse restores the exact pre-edit canonical document including occurrence rows, shot/internal revisions, dependency manifest, media/source/placement/timing and opaque values. A live `remember` audit of both cases observed no `_doc_patch_images` residue. Existing retained-sibling, shared-root, binding, missing-authority, forged/malformed binding, ambiguous/ref/owner/edge, ABA and later-write guards remain unchanged and pass.

## Independent commands and results

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1daca2a3 \
PYTHONPATH=/home/user/work/wt/agt-R2-D110-core-review-0658:/home/user/work/wt/rt-pin-1daca2a3 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 \
  --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-D110-core-review-0658/evidence/D110-reviewed44.xml \
  tests/sdk/test_inverse_removed_shot_owners_runtime.py
```

Result: **2 passed**, 0 skips, 5.549s. The durable XML is retained in `evidence/D110-reviewed44.xml`.

```text
ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-1daca2a3 \
PYTHONPATH=/home/user/work/wt/agt-R2-D110-core-review-0658:/home/user/work/wt/rt-pin-1daca2a3 \
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 \
  --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-D110-core-review-0658/evidence/D110-neighbors-reviewed44.xml \
  tests/sdk/test_inverse_removed_shot_owners_runtime.py \
  tests/sdk/test_timeline_inverse_shared_root_baseline.py \
  tests/sdk/test_timeline_inverse_fork_guard.py \
  tests/sdk/test_timeline_inverse_binding.py
```

Result: **44 passed**, 0 skips, 15.556s. Durable XML is retained in `evidence/D110-neighbors-reviewed44.xml`.

Additional review commands: Ruff passed for the changed product/new test; mypy passed with “Success: no issues found in 2 source files”; in-memory compile passed for both files; `git diff --check` passed; unchanged-tree conservation compared 3,561 base paths and found 0 unexpected blob mismatches; AST conservation compared 26 top-level definitions and found 0 mismatches outside `apply_inverse`; protected Runtime lock/schema/client/store/auth/fixture and original neighbor-test paths were unchanged. Candidate source/runtime/XML hashes and raw command logs are in the evidence directory.

## Blockers and next steps

No review blocker. This is an independent targeted/core PASS only; no full suite, App/P2/P4/D108, or release-wide acceptance claim is made. Keep the candidate unmerged until the normal merge worker and existing MAIN integration/final gates run.
