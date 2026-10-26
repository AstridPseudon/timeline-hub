# D141c validation record

## Commands run

- `sed`/`rg` read-only inspection of `PLAN.md`, `AGENTS.md`, the Agent manager `INBOX.md` 00:52:33 ruling, and the seven retained originals.
- `cmp -s <worker-original> <published-design-original>` and `sha256sum` for all seven packet files.
- One `python3 - <<'PY'` stdlib-only validation using `json`, `hashlib`, `pathlib`, and `xml.etree.ElementTree`; it did not import Astrid or product modules.
- `git rev-parse HEAD` and `git status --short --untracked-files=all` in the assigned worktree.

## Results

- All seven `cmp` checks returned 0. Published/worker hashes are recorded in `review.json`; no original was rewritten.
- XML bytes: 4,690,547; SHA-256 `ceeb66095a1e00929da0007639dd3d7c8267126b4541c0da2c86011dab63009a`.
- XML testcase elements: 3,082. Derived XML statuses: 3,077 PASS, 4 FAIL, 1 ERROR, 0 SKIP.
- Published inventory: 3,255 records, exactly 3,082 concrete records plus 173 explicit null-ID aggregate PASS records. Concrete ID uniqueness: 3,082/3,082. XML/inventory ID set equality: PASS.
- Field-by-field concrete correspondence: 0 mismatches across node ID, class, name, time, original attributes, status, and serialized testcase SHA-256. All 3,082 serialized-node hashes matched.
- Bad-node membership and status correspondence: 5/5 PASS. Sanitized bad records preserve the observed XML result type; raw messages/traces are not published.
- Every file hash referenced by the retained source manifest that was locally available was recomputed and matched, including XML, stdout/stderr, pytest log, disk/status/exit files, source witnesses, controller result, and central wrapper log.
- Retained stdout and pytest log summary parsing independently found 3,077 passed, 4 failed, and 1 error; the 173 aggregate count is provenance from the retained summary plus XML suite accounting, not invented selector data.
- Worktree HEAD: `28e56cacb42d3da85b02e5b3543895b44f3d0f70`; source status was clean before review artifacts (the evidence artifacts are outside the product worktree).

## Test applicability

Tests, typecheck, and lint are not applicable to this documentary read-only review. No pytest or product import was run. The retained comparator's terminal body status is `FAIL` with body exit 1 and monitor exit 0; this review reports evidence custody only and does not convert that terminal result into a behavior, REG, or ship verdict.
