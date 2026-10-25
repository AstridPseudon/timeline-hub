# Validation

## Source custody

- Current Agent: 5b11a383247c7877b85ec6ae7c08f5cd43d790e7, tree 71f45785a19ca3213eb50ac47ab0b9359c0119ca; worktree clean.
- git diff --check: PASS.
- Exact root-019 source scope: all nine target files have identical current,
  shared-author-96a6, and prior-base-a30a blobs; target diff exit 0.
- Imported common fixture and five recipe JSON inputs are unchanged from a30a.
- git diff 96a6..HEAD --name-status: only the unrelated
  tests/editing_conformance/test_occurrence_fork_source_baseline.py.
- AST parse/hash, byte hashes, test-function names, and assertion counts for all
  nine files are in source-manifest.json.

## Allowed static checks

- PYTHONDONTWRITEBYTECODE=1 PYTHONPYCACHEPREFIX=/tmp/w-605f94dc53/d134-compile /home/user/work/venv-agent/bin/python -m py_compile tests/editing_conformance/test_commit_runtime_occurrence_media.py tests/editing_conformance/test_commit_runtime_parent_media_swap.py tests/editing_conformance/test_commit_runtime_video_unplace.py — PASS.
- PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_commit_runtime_occurrence_media.py tests/editing_conformance/test_commit_runtime_video_unplace.py — PASS, all checks passed.
- Scoped parent fixture Ruff is the known pre-existing F811 baseline reported by author2055; no unrelated fix was applied.
- Mypy: not run; known baseline is the author packet's missing YAML stubs / Python-version NumPy stubs.
- No pytest, collection, Runtime/provider body, service, browser, socket, full/E2E, seed, SQL, pin, generated, schema, or product/test edit was made.

## D100/current caller checks

Static source comparison of current 689c and held 9486 product blobs:
PASS for the exact three changed methods and guard conservation. Held 9486 is
source-purpose/security reviewed, but behavioral qualification and the D134
representative remain unverified.

