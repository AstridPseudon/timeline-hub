# F-D108 swap24 protected source review

Verdict: **FAIL_SOURCE** for author commit `f764ad5fd80bcf919f2214d532df00690a465c98`. This is a source-only qualification finding, not an independent product NO-GO and not a behavior result.

## Exact custody

- Repo: Agent/Astrid immutable Git object store.
- Parent: `d0ecf1d69a7b37f86034bc52004f73f6c6231603`.
- Reviewed file only: `tests/editing_conformance/test_commit_runtime_parent_media_swap.py`.
- Parent blob SHA-256: `685f6168fa378b9269a2e605e5bec4643a413b856e2782a786bbe4e7dfbd9fcf`.
- Author blob SHA-256: `22f5dca98934ded620b219d6c19af4439bd2bfc9a664ce3feea120145644ae86`.
- Diff SHA-256: `c04e6add4df14dae618fa0b146abcc6b8ddf8264abc7e211fcd71dad6ffc047f`.
- Only one path changed; exactly two substitutions occur at source lines 78 and 113.

## Conservation result

The 25 collected node IDs are retained byte-for-byte by the collector evidence (`nodeids_sha256=6503d1b5c0b5aca70466598645d0b1812d1b9571908c26e7a3e3c840961becc4`, collector file SHA-256 `b418d2e70dd35b3678cc1a9fa17183d94e28afc880614e6c2a31e41d26af1834`). Parent and candidate both have 62 `assert`, 135 predicates, 67 comparisons, 6 `if`, 6 boolean operators, 180 calls, 21 functions, 1 `for`, 5 `with`, 2 `try`, and 1 `raise` AST nodes. After normalizing only the two intended callable arguments, the module AST is identical (`be462fccace6309090...5c2de9`); literal inventory and all six test function names are unchanged. No assertion contains `source_bytes`.

D104 arithmetic is retained: clip spans `[1,3)` and `[5,7)`; video source window `[2,6)` and output `[1,5)`; occurrence ends `8000+10000=18000ms` and `10000+10000=20000ms`. The shared seed callers are the image/video `editing` fixture and the parent/occurrence `http_editing` fixture.

## Blocking source finding

Line 78 is valid: `editing(..., source_bytes)` receives the materialized callable through the fixture parameter.

Line 113 is not equivalent: `http_editing(request, tmp_path, monkeypatch)` does not request `source_bytes`, so the bare name resolves to the module-level pytest fixture wrapper. The occurrence fixture subsequently calls the passed value as `source_bytes(kind, name)`. Under the repository's pytest 9.0.2, calling a `FixtureFunctionDefinition` directly raises `Failed: Fixture "source_bytes" called directly`; only `source_bytes.__wrapped__(tmp_path)` creates the callable. Therefore the author commit does not establish a valid HTTP fixture source binding.

The retained author run is recorded without reinterpretation: exact command used Runtime `1daca2a33f6d7b10053e07c539a54843e3984e19`, result `1 passed, 24 errors in 36.76s`, with the remaining errors reported at shared `popup-birth` Runtime validation (`provider intermediate parent lacks an effect image`). This does not clear the independently visible line-113 binding defect, and no behavior PASS is inferred.

Static checks on a private immutable-blob copy:

- `/home/user/work/venv-agent/bin/ruff check /tmp/w-aa875387c0/source-review/test_commit_runtime_parent_media_swap.py`: exit 1, retained baseline `F811` at line 226; parent blob reports the same diagnostic.
- `(cd /home/user/peteromallet/astrid-agent && /home/user/work/venv-agent-typecheck-v2/bin/mypy /tmp/w-aa875387c0/source-review/test_commit_runtime_parent_media_swap.py)`: PASS.
- `/home/user/work/venv-agent/bin/python -m py_compile /tmp/w-aa875387c0/source-review/test_commit_runtime_parent_media_swap.py`: PASS.
- `git -C /home/user/peteromallet/astrid-agent diff --check f764ad5fd8^ f764ad5fd8 -- tests/editing_conformance/test_commit_runtime_parent_media_swap.py`: PASS.

Production-caller read-only trace remains unchanged: `RemoteTimelines.replace_parent_media` routes exact selected media to `timeline_media_replacement.replace_selected_media`; that captures `capture_parent_swap_media`/`capture_occurrence_swap_media` and calls `TimelineSession.commit`; the fixture registers `load_timeline_commit_provider('astrid')` and submits through `service.commit_timeline`.

Proposed existing D72 disposition: keep Agent `WC3` at its existing `OPEN — explicit branch lifecycle and caller cuts pending` entry. Do not mark `SOURCE-QUALIFIED`, do not claim behavior qualification, and do not append/update the ledger. No author code, product code, tests, pins, generated files, or ledger entries were changed by this review.
