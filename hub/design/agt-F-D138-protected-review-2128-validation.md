# D138 protected review validation

## Verdict

`PASS` for the protected source review. Behavioral credit is `NOTRUN`.

## Source and conservation checks

- Exact reviewed head: `aa62c1a1726a14d6fb08c73143334c91dfc89663`, based directly on `2eca9a1da94eb35bb969540e150192ff920ce326`.
- `git diff --name-status 2eca9a1d..HEAD`: exactly one file, `M tests/editing_conformance/test_native_batch_ingress.py`.
- SHA-256 comparison: base `1c6cbd9b…18669`; reviewed `8bff12b0…f845e`.
- AST comparison: every function is identical to base except `cli()`; all authored test bodies, decorators, commands, guards, metadata, refusal assertions, file-byte checks, retry checks, inverse checks and preview checks are retained.
- Static root-045 expansion: 2 batch + 8 lost-ACK peer cases + 4 original-pair peer cases + 5 refusal cases + 2 boolean-claim retry cases + 1 preview case = 22.
- Parser-only legacy sentinel `test_file_parser_requires_both_original_pins_and_describes_registry` is unchanged. Current parser source has no `commands-file` registration, so the sentinel remains visibly failing by design; it was not skipped, retired, deselected or xfailed.

## Exact commands and results

- `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3.11 -c 'from pathlib import Path; p=Path("tests/editing_conformance/test_native_batch_ingress.py"); compile(p.read_text(), str(p), "exec")'` — **PASS**.
- `/root/.local/bin/ruff check tests/editing_conformance/test_native_batch_ingress.py` — **PASS**, `All checks passed!` (private `RUFF_CACHE_DIR`).
- `MYPY_CACHE_DIR=/tmp/w-a7df783be5/mypy-cache make PY=/home/user/work/venv-agent-typecheck-v2/bin/python mypy` — **PASS**, current `1902`, baseline `1902`.
- `git diff --check 2eca9a1da94eb35bb969540e150192ff920ce326..HEAD -- tests/editing_conformance/test_native_batch_ingress.py` — **PASS**.

## Route and boundary review

`cli()` decodes only the file's command array, opens the session on the exact supplied/default base pair, forwards the explicit idempotency key and dry-run bit, and calls `TimelineSession.commit_many(..., via="cli")`. The session freezes the request in its outbox, retries the exact flight, and sends it through `client.timelines.commit` → `RemoteTimelines.commit` → generated `commit_timeline` → the canonical Runtime POST commit route. The existing production CLI caller uses the same session/`via="cli"` path.

The malformed-envelope case is not unwrapped with fields discarded: a top-level dict is rejected by command schema validation before staging or transport, retaining its no-call/no-history/file-bytes predicate. Valid root-045 inputs are command arrays; command-level `rationale`, `expect` and `reads` are preserved. ABI-1 default label/steps/merge are supplied by `commit_many`, while idempotency, dry-run and source are forwarded explicitly.

## Behavioral status and limits

No live or central test was run in this protected review, per the brief. The author's central exact-22 attempt collected the IDs but deselected all 22 integration-marked cases (exit 5), so all 22 remain behaviorally unverified. Runtime `rt-D73-exact-node-route-2104` remains the sole supported service recipe owner; no alternate config, body, environment fix, retry, transfer or live route was attempted.
