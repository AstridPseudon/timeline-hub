# F-D108 swap24 protected source rereview

Verdict: **PASS_SOURCE** for first-return author commit `3e31a0bc58314a457d228eb1c065d8ed2b6de083` (parent `f764ad5fd80bcf919f2214d532df00690a465c98`). This is source qualification only, not behavior qualification or an independent product NO-GO.

## Exact custody and cumulative diff

- Repo: Agent/Astrid immutable Git object store; original baseline `d0ecf1d69a7b37f86034bc52004f73f6c6231603`.
- Reviewed file only: `tests/editing_conformance/test_commit_runtime_parent_media_swap.py`.
- Original blob SHA-1: `ff5493dc43b563832f4ea2a15e544e3b3d080afe`; SHA-256: `685f6168fa378b9269a2e605e5bec4643a413b856e2782a786bbe4e7dfbd9fcf`.
- First-return blob SHA-1: `76f584b0b323f47a564f0763f0ae670ac759443a`; SHA-256: `e733226964bb5df253d3a3b4bb887e6fe573eda9090623c91725aa3f2c6f1ec9`.
- Author commit tree: `e74f2f64d69cda3caf4ea0a56d59aed2708fcdea`.
- Cumulative `git diff --binary d0ec..3e31` SHA-256: `5354fe88b48ff3628b707956268c38f64351b5fcf0cc8af210712ccc545b8b93`.
- Own-only return diff `git diff --binary f764..3e31` SHA-256: `d9eca0af22954852f3d76e1fad92868f28e339c11ec10a1357357d91e4feaa1e`.
- One path, exactly three changed lines: line 78 passes `source_bytes`; line 105 adds `source_bytes` to `http_editing`; line 113 passes it to `occurrence_editing`.

## Source conservation and defect clearance

The retained collector evidence contains all 25 original node IDs (`nodeids_sha256=6503d1b5c0b5aca70466598645d0b1812d1b9571908c26e7a3e3c840961becc4`; collector SHA-256 `b418d2e70dd35b3678cc1a9fa17183d94e28afc880614e6c2a31e41d26af1834`). I did not rerun the 24 behavior cases.

Independent AST conservation against the exact original blob passed after normalizing only the two callable replacements and removing the added fixture parameter from the comparison: normalized AST SHA-256 `be462fccace6309092cc864debe0754244f0719ddf152f6cd62ef8d7775c2de9`; normalized counts are 62 asserts, 67 comparisons, 6 boolean operators, 180 calls, 21 functions, 1 `for`, 5 `with`, 2 `try`, 1 `raise`, and 6 `if`. The predicate count is `62 + 67 + 6 = 135`; all six test function names and bodies are unchanged after normalization. Raw call count changes only as expected from removing two nested `source_bytes.__wrapped__(tmp_path)` calls (182 → 180). No assertion contains `source_bytes`.

The previous materialized-callable defect is cleared in source: `http_editing(request, tmp_path, monkeypatch, source_bytes)` now receives the genuine fixture result, and its occurrence setup passes the `source_bytes` name directly. The candidate contains zero `source_bytes.__wrapped__` occurrences; the HTTP fixture has one direct materialized-source call, and the existing `editing` fixture has the other.

D104 remains conserved: clip spans `[1,3)` and `[5,7)`; video source window `[2,6)` and authored output `[1,5)`; occurrence ends `8000+10000=18000ms` and `10000+10000=20000ms`. Shared seed callers remain image/video `editing` and parent/occurrence `http_editing`. No authored timing, input, opaque graph, assertion, negative guard, or callable-representation assertion changed.

## Static checks and retained behavior boundary

Checks ran on a private immutable-blob scratch copy `/tmp/agt-F-D108-swap24-rereview-0914-source-review/candidate.py`:

- `/home/user/work/venv-agent/bin/ruff check /tmp/agt-F-D108-swap24-rereview-0914-source-review/candidate.py`: exit 1 only for retained baseline `F811` at line 226; the exact original blob reports the same diagnostic.
- `(cd /home/user/peteromallet/astrid-agent && /home/user/work/venv-agent-typecheck-v2/bin/mypy /tmp/agt-F-D108-swap24-rereview-0914-source-review/candidate.py)`: PASS.
- `/home/user/work/venv-agent/bin/python -m py_compile /tmp/agt-F-D108-swap24-rereview-0914-source-review/candidate.py`: PASS.
- `git -C /home/user/peteromallet/astrid-agent diff --check d0ecf1d69a7b37f86034bc52004f73f6c6231603 3e31a0bc58314a457d228eb1c065d8ed2b6de083 -- tests/editing_conformance/test_commit_runtime_parent_media_swap.py`: PASS.

The retained author execution remains `1 passed, 24 errors`; its errors are the separate Runtime `popup-birth` intermediate-parent/effect-image rejection under Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`. The return author log records 25 tests collected and source conservation; no unchanged behavior body was rerun by this review. No behavior PASS is inferred.

The read-only production trace is intact: `remote.py:1338-1375` routes `replace_parent_media` to `timeline_media_replacement.py:156-255`, which captures `capture_parent_swap_media`/`capture_occurrence_swap_media` and calls `TimelineSession.commit`; the fixture registers `load_timeline_commit_provider('astrid')` and submits through `service.commit_timeline`.

Proposed existing D72 disposition: Agent `WC3` may move to **SOURCE-QUALIFIED / BEHAVIOR-PENDING**, while retaining the existing `explicit branch lifecycle and caller cuts pending` behavior entry. Do not claim BEHAVIOR-PASS or append/update the ledger from this source review. No product, test, generated, pin, registry, ledger, or author-source files were modified by this rereview.
