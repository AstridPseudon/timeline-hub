# R2r native store return — PASS

Base `1365e4b17b31c4a7093d5943674637067fd2bab4`, tree `6c69c3dc47822fffbaf27cd63815d2895155ffaa`. Only auth/store/new-stage-test changed; cumulative file-only recovery from `21b329935`, with no git mutations or borrowed ancestry. Harness creates the single own commit.

The real store split+note inverse now accepts. Direct forward and inverse authentication both pass using only the exact accepted forward history returned by `TimelineCommitStore.history_entry`. Native physical root paths retain their distinct mirror observations until both separately recorded writes finish. Logical clip/asset captures retain their corresponding mirror projection. Exact ordered native membership, ranges, complete physical payload coverage, sequential values, physical bindings/digests, and all prior source/forgery/history guards remain active. Extra non-source history publications are now explicitly refused by authentication.

Added eight cases: the exact mounted music-documents store/provider split+note witness, four forged mirror before/after values with complete database dump equality on refusal, and missing/forged-step/future-history controls against the validator itself. The positive checks accepted replies, direct auth, exact source history, both physical native mirrors, full restored closure, persisted readback, and exact retry. All previous 33 new-stage cases, including the reviewer forged native path and six actual-Agent native membership mutations, remain unchanged.

## Final commands and results

The first requested lane is split because read-basis contains a localhost HTTP fixture; only that file uses the central service. All commands run from this worktree, unless stated otherwise.

```sh
PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-bed45687cb PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_inverse_stage_authentication.py tests/test_timeline_commit_authentication.py
# 114 passed in 40.35s (auth-stage-complete.log)

/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-R2r-native-store-return-sol-1008 targeted --files tests/test_timeline_commit_read_basis.py
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-R2r-native-store-return-sol-1008-targeted-1023101343-31189
# 12 passed in 3.65s; service exit 0; snapshot 48ca2b77d81e578ed2cfd4dd013f78aba32c6d99

CORRECTASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-bed45687cb PYTHONPATH=.:packages/python:/home/user/work/agent ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_acceptance.py tests/test_timeline_commit_integration.py -k 'inverse or history'
# 10 passed, 68 deselected in 10.93s (inverse-history-final.log)

PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-bed45687cb PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_source_duplicate_authority.py tests/test_timeline_commit_inputs.py tests/test_timeline_source_document_boundary.py tests/test_timeline_raw_capture.py tests/test_timeline_commit_port.py
# 101 passed in 14.10s (d17-final.log)

TMPDIR=/tmp/w-bed45687cb PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python:/home/user/work/agent /home/user/work/venv-agent/bin/python /tmp/w-bed45687cb/verify_store_probe.py
# PASS: production forward/inverse accepted AND both direct auth checks pass; exact history map and actual source origins asserted.

PYTHONDONTWRITEBYTECODE=1 TMPDIR=/tmp/w-bed45687cb PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python /tmp/w-bed45687cb/baseline_probe.py
# Expected RED against candidate21b authentication: 1 failed, inverse stage write differs from its sequential input.

ruff check --no-cache runtime_protocol/timeline_commit_auth.py tests/test_timeline_inverse_stage_authentication.py
# clean
ruff check --no-cache --output-format=json runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py
pyright --outputjson runtime_protocol/timeline_commit_auth.py runtime_protocol/timeline_commit_store.py
# Each run in current and isolated HEAD snapshot: Ruff 11/11, Pyright 76/76 inherited diagnostics.
python /tmp/w-bed45687cb/compare_static.py
# All complete diagnostic identities, including source-line mapping: zero added/removed.
python /tmp/w-bed45687cb/final_preservation.py
# Compile/AST pass; all 277 existing test files byte/AST identical; all other tracked files identical except auth/store.
# Broader frozen directory set: 96 unchanged files; no schema/client/config/pin/artifact change.
# Entire 26,231-byte candidate test prefix unchanged, including original 367 lines / 20,020 bytes.
git diff --check
# pass
```

The retained corrected diagnostic is unmodified; the wrapper only asserts its JSON and records actual loaded origins. Actual Agent HEAD is `ef851b22c506245441b9a630c093b3460e39cbdc`. Runtime modules originate in this worktree; exact paths and SHA-256 values are in `store-witness-verified.json`. Historical commit labels embedded in the unchanged diagnostic are retained as data, and the wrapper separately records current identities. The original 0912 probe SHA-256 remains `47399344d70ecb35bca0f843aea5c7245cae35a623cdbbcfd777465d47810f8a`.

Original `/tmp/w-71481117c1/candidate.json` was absent in this environment; the retained diagnostic independently reproduced the same candidate refusal (`probe-before.err`, `failure.json`) before repair. Candidate21b regression sensitivity is also retained in `baseline-red.log`. This RED is against candidate21b, not original1365; the earlier original1365 real-store acceptance and separately retained detached0912 mismatch are not relabeled.

An intermediate run of the three newly added direct-history cases failed because their test imported the exception from the wrong module. That test import and failure-field assertion were corrected; the final 114-test run passes without skipped, weakened, or xfail cases.

## Evidence, limits, next step

Artifact directory: `/tmp/w-bed45687cb`. Manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R2r-native-store-return-sol-1008/evidence.json`. Full requests, replies, documents, native records, bindings, effects, and exact authenticated history map are in `store-witness-verified.json`; source and artifact hashes are in the manifest. Preservation verifies store changes are limited to `_verify_accepted`, `_validate`, and the new `_inverse_stage_history` handoff, preserving D17 interfaces.

No blocker. No full/broad58/native14/crash24/20/browser/P4 or HTTP mutation journey was run; no daemons started. The existing read-basis HTTP read ran only through the central service. H3 remains NO-GO and V4 remains cut. Next: harness commit, then immediate independent review of physical mirror sequencing, strict native membership/coverage and exact source history before integration.
