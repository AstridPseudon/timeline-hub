# G5 publish/idempotency independent final review

Disposition: PASS for the bounded source/behavior review; DRAFT/P1 gate remains; no merge.

## Scope and source

Reviewed target d0fc9848a0a7acfd0548cf60b9777634b4a1e98a (test: model Runtime idempotency in G5 fixture) against parent/join 4b248adc5c22e05b6168284aa8ceace8afe61752, with earlier G5 join 246c3b0642df5513f9e30c92b35881cd0f62a835 and pre-retirement publish tests inspected.

Only these two test files differ:

- tests/packs/timeline/test_cli_parity.py
- tests/packs/timeline/test_cli_status_publish.py

No product source, Runtime source, schemas, clients, pins, dependencies, or shared environments changed.

Current file SHA-256:

- tests/packs/timeline/test_cli_parity.py: c0748f89014ca8a6def028c5f0e3d7779ab8ebe251b414c3de3cf2b22837b17e
- tests/packs/timeline/test_cli_status_publish.py: c413da73cdfdc136b4d9b1f6740e1d6ebf8258d261099819f3073c3b61b632b1

## Fixture review

The added normal_commit wrapper is Runtime-shaped and does not intercept legitimate first-seen requests:

- It wraps only commit_timeline; all other operations delegate to the original public fixture transport.
- It hashes the complete canonical invocation, including operation, route, publisher, and request body.
- Its replay identity is scoped to (project_id, timeline_id, idempotency_key).
- First-seen requests delegate to the real public-session commit service; only successful results with receipts are stored.
- Identical replays return a deep-copied stored result without another write.
- Same-scope changed bodies return conflict/idempotency_mismatch before delegation.

The isolated changed-body attack check independently passed: after an accepted request, changing both document body and message under the same key returned the mismatch refusal and left head, entries, and documents unchanged.

## Preservation review

The retained ports preserve the requested semantic coverage:

- accepted receipt/idempotency and project/message forwarding;
- full-v2 durable CLI request/reply, history, undo/redo, preview, structured refusal, and no-write assertions;
- retry with no second history write;
- CAS refusal preserving the file and avoiding retry;
- clean no-op with no receipt/history write;
- human output bounded without leaking canonical document data;
- old publish/overwrite options and old publish hints remain rejected/absent.

All 10 durable CLI test function bodies are AST-identical to the 246c3b064 join. Their parametrization covers 22 durable CLI cases; none changed.

The pre-retirement fake-Checkout.publish tests were not resurrected, and this review makes no fake HTTP/body evidence claim.

## Exact evidence

1. Joined retained parity/publish tests, with the shared Runtime checkout required by this repository:

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=35 tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py

Result: 76 passed in 8.06s.

2. Isolated changed-body attack check (temporary file outside the worktree):

    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=35 /tmp/g5_changed_body_attack_agt_G5_publish_final_review_1617.py

Result: 1 passed in 1.45s.

3. Scoped Ruff:

    RUFF_CACHE_DIR=/tmp/agt-G5-publish-final-review-1617-ruff-cache /home/user/work/venv-agent/bin/python -m ruff check tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py

Result: All checks passed.

4. Private repository mypy baseline:

    make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python

Result: repository gate exits 2 because current=1911 baseline=1912; this is one fewer diagnostic (an improvement), not a regression. The baseline was not rewritten.

5. Compile and whitespace/diff checks:

    PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m py_compile tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py
    git diff --check d0fc9848a^ d0fc9848a

Result: PASS.

## Limits and follow-up

- The 76-test joined suite does not itself invoke the changed-body branch; the branch is independently exercised by the one-off attack check above. If the gate requires that control to be a committed regression test rather than review evidence, add one dedicated same-key changed-body test in a follow-up.
- The fixture is in-memory and process-scoped; this review does not claim restart persistence or a live HTTP/Runtime journey.
- No full, browser, socket, daemon, native, P1, P4, or integration suite was run.
- Official vendor-lock checking was not rerun because the target tree has no vendor/source/pin changes; prior source-identical quality evidence remains applicable.

