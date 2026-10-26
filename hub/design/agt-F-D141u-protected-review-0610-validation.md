# Validation

## Required two nodes

Ran exactly once from the protected review worktree, using Runtime `6a011d58`
and `/home/user/work/venv-agent/bin/python`:

```text
PYTHONPATH=/home/user/work/wt/agt-F-D141u-protected-review-0610:/home/user/work/wt/rt-pin-6a011d58 /home/user/work/venv-agent/bin/python -m pytest -q -n3 -o addopts= -p no:cacheprovider --timeout=45 --junitxml=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141u-protected-review-0610/evidence/private/targeted.xml tests/timeline/test_authoring_feedback.py::test_document_publish_stdout_and_durable_receipt_contain_shared_feedback tests/timeline/test_authoring_media.py::test_document_publish_forwards_new_stale_head_to_runtime
```

Result: **2 passed in 2.70s**, exit 0; zero failures, errors, or skips.
The two requested IDs both passed. Private XML/stdout/stderr remain mode 0600.

## Static and conservation checks

- `/home/user/work/venv-agent/bin/python -m ruff check tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py`: **PASS**.
- `git diff --check 8585ed9c0404d0187b2ce70242d25114a32747c2 2473301cc3513d045ea38b969b4750901b6c9c4c`: **PASS**.
- Exact diff audit: **PASS**, two method-name changes only; diff SHA-256 is `7cdf3f1bd17fe2fdb76687ed4da6f95af95a3317083423939e2b7868f21e4c76`.
- AST audit: **PASS** after normalizing only `_capture_bundle` to `_bundle`; assertion ASTs, exception predicates, authored input literals, function identity, purpose, and sequence bounds are conserved. Assertion counts are 16→16 and 23→23; raise counts are 0→0 and 1→1.
- Case-local double caller audit: **PASS**; the doubles are reached only through the patched `TimelineSession.open` seam in their own target cases.
- Product mypy: **N/A**; no product file changed.

No full suite, pristine repeat, other target, live service/body/row/kit/child/profile/Store/hub operation, or pin/source change was run.

## Custody limitation

The author's `evidence/disk-trace.txt` is explicitly historical reproduction0510
material (hash prefix `e83f4997`), not a trace of the author run. Manager actual
tracing began later. This review's persistent trace starts at the timestamp
recorded in its own `disk-trace.txt`; it is not backfilled and does not establish
continuous historic custody before that start.
