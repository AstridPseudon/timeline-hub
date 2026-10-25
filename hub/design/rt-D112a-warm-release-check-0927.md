# D112a warm forward/read acceptance

Result: PASS. The existing D94 warm forward/read flat-N controls pass on frozen candidate `be828d92cba9200a6ae0ded3a2e968dc3f6ac383`; the source/evidence packet is release-ready for this gate.

## Source and ancestry

- Candidate branch: `tl/rt-D112a-warm-release-check-0927`, exact commit `be828d92cba9200a6ae0ded3a2e968dc3f6ac383`.
- Source SHA256: `runtime_protocol/timeline_commit_store.py` = `34d0f401236c957cb126713c0f1319affadf65e08cbe727223d97ad0de775e56`; `tests/test_timeline_history_state.py` = `788e1280c61cbee6817595544495ba462365d956d0cd85499923328dedba838b`.
- Deterministic source pair hash (filename + SHA256 lines, sorted): `0fa2ad93606210d29538b6be4265e0175dc994f23919325dd496b21b5aa897d4`.
- Candidate is based on `c91626f5e905f9336b51aae0486a071d83f0bac7`. `tl/integration` is `e6b669b98d8eeb349c311741cdfd8cfbfe5e5486`, also based on `c91626f5e905f9336b51aae0486a071d83f0bac7`, and carries the disjoint snapshot test merge `1eceb7ff7dcf4272afe7f2d15daf1727fa40fed4`.
- `git merge-tree` reports no textual conflicts when combining the candidate with `tl/integration`; the D112 pair and the integration snapshot test are disjoint.

## Acceptance

Exact command:

`/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_history_state.py`

Result: **53 passed in 24.95s**, exit 0. This includes `test_warm_entries_and_closures_are_detached_and_only_new_entry_is_verified`, existing flat verification/count controls, replacement recovery, tamper refusal/no-write, and protection fallback controls. The current D108 snapshot test added after the candidate parent remains preserved on `tl/integration` in `tests/test_timeline_render_publication.py`.

The settled D112a criterion is baseline-equivalent behavior under the identical lifecycle, not constant wall time through externally invalidated, growing-history responses. Retained Sol 0907 evidence records identical verification counters/payloads and candidate timings within noise at N=4/5/6 (baseline 2634/939/1028 ms; candidate 1947/664/1197 ms). No repeated native curve/body was run.

## Scoped checks and retained limits

- `/root/.local/bin/ruff check --no-cache --select E9,F runtime_protocol/timeline_commit_store.py tests/test_timeline_history_state.py`: PASS; parent-normalized and candidate checks both pass.
- `PYTHONPYCACHEPREFIX=/tmp/w-565ff267cc/pycache /home/user/work/venv-runtime/bin/python -m py_compile runtime_protocol/timeline_commit_store.py tests/test_timeline_history_state.py`: PASS.
- `git diff --check`: PASS.
- Fresh scoped Pyright invocation reports 61 inherited diagnostics for the two files; no source changed. The exact prior D112 security review remains applicable to this identical source pair and records 59 existing diagnostics with zero-new comparison. No repair or weakening was introduced.
- Full Ruff currently reports inherited I001/SIM102/BLE001 findings in the unchanged source; no source change was authorized for this read-only acceptance.
- The two SQLite authorizer failures (`PRAGMA data_version`) were independently reproduced on the parent and remain explicitly retained; they were not skipped or xfailed.
- Prior PASS0827 344-control security review, native0850/0907 recovery positives, tamper controls, and real-provider seed/SWAP positives remain retained evidence. No new semantic review stage was added.

Safe evidence (20 KiB) is under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D112a-warm-release-check-0927/evidence/`; it contains counts/hashes only and no auth, payload, private URL, or stack data.
