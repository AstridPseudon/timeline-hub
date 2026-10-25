# D127 command results

- Baseline: git rev-parse HEAD -> ab1e4f6141987706132916e2da16477f5a019464.
- Import: exact donor blobs from 231ddb5a6605b535d26172d34439ebe7b90804de.
- Blob proof: git hash-object matches donor for both target files; helper SHA-256 4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e; test SHA-256 d6b5703492b4b4d399ee1d5d7350faae615a01448df70229efc3cc03a1ecff18.
- Scope proof: git diff --name-status HEAD reports only the two authorized target paths.
- Donor scope: git diff-tree --no-commit-id --name-status -r 231ddb5a6605b535d26172d34439ebe7b90804de reports only tests/test_p2_commit_phase_capture.py.
- RUFF_CACHE_DIR=/tmp/w-993b1dd8ec/ruff-cache ruff check tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py — PASS.
- MYPY_CACHE_DIR=/tmp/w-993b1dd8ec/mypy-scoped mypy --follow-imports=skip --ignore-missing-imports tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py — PASS.
- PYTHONPYCACHEPREFIX=/tmp/w-993b1dd8ec/pycache-py311 /usr/bin/python3.11 -m py_compile tests/helpers/p2_commit_phase_capture.py tests/test_p2_commit_phase_capture.py — PASS.
- git diff --check — PASS.
- An initial unscoped mypy invocation was not used as acceptance evidence: it followed repository imports and reported 271 pre-existing/environment errors. No source changed.
- No pytest, localhost/service, full, browser, tour, recovery, profile, native, family, or SWAP run was performed per brief.

Reused evidence: independent D127 source reviews, original 160 Runtime predicates, four schema lifecycle migrations, and central 28551 PASS23.
