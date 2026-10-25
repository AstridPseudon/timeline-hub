# F-D86 source review — ordinarysheet11

Verdict: `PASS_SOURCE`

## Exact source

- Repository: Agent (`/home/user/peteromallet/astrid-agent`), read-only.
- Captured base: `tl/integration` = `657bc2e8dba066df1c7d21851315bdb6b0f16a3a`.
- Parent: `657bc2e8dba066df1c7d21851315bdb6b0f16a3a`.
- Candidate: `tl/agt-F-sheet11-source-0325` = `8aa201a76cf3ceca2b67d54a871b2ec0c057d4d6`.
- Candidate parent is exactly the captured base; the candidate has one file and one line changed.
- File: `tests/editing_conformance/test_native_sheet_ordinary_runtime.py`.
- Parent blob SHA-256: `9f80d4ee3c1e5d76781ac32a5c4e330f8c3ba76ef733a94d88515ca13d50f7ed`.
- Candidate blob SHA-256: `a4183c3e875f4a0c2337c44aa8de07fe0d1abd717d6df9ba122285a0a04045af`.

Exact diff at candidate line 274:

```diff
-'source': {'via': 'test-bootstrap'},
+'source': {'via': 'python'},
```

## Static conservation

- The seven `test_*` function ASTs are identical parent/candidate.
- All 152 `assert`/`raise` AST nodes are identical parent/candidate.
- The original ordinarysheet11 family remains the same source file and its 11 parameterized original IDs are retained; this source edit changes no selector, parameter, decorator, body, input, command, base pair, step, merge, read, dry-run, rationale, group, idempotency, accepted/refused/conflict, retry, inverse, ABA, or no-write predicate.
- The complete bootstrap request remains C0-shaped: `api_version`, scope IDs, exact base revision/publication pair, commands, label, steps with patches/reads, `merge: atomic`, `reads: []`, `dry_run: false`, source, rationale, and group ID. Only the source annotation's producer value changes.

## Mounted production trace

The source is a real registered-provider bootstrap, not a synthetic history shortcut:

1. `historical_sheet_film` registers `commit.create_runtime_commit_service()` with `RuntimeService`.
2. It calls `service.commit_timeline(...)` with the complete request and idempotency key.
3. The existing Python provider's `TimelineSession.commit_many`/`_flush` path emits `source: {"via": via}`; its default producer value is `via="python"`.
4. The actual `NativeSheet.apply` path remains unchanged and calls `session.commit_many(..., via="sheet", ...)`, which goes through the same `_flush` and `client.timelines.commit` route. This review does not relabel the sheet caller.

Therefore `python` is the truthful producer annotation for the setup's direct Python commit request. No authority, route, schema, registry, custody, or behavior policy changed.

## Checks run

Source-only checks, with no pytest collection, fixture/helper/function execution, probe, service, render, browser, or package install:

- In-memory `ast.parse` + `compile(..., "exec")` for parent and candidate: PASS.
- `/home/user/work/venv-agent/bin/python -m ruff check` on parent and candidate extracted source: PASS for both.
- `/home/user/work/venv-agent/bin/python -m mypy` on parent and candidate extracted source: PASS for both (`Success: no issues found in 1 source file`).
- `git diff --check 657bc2e8dba066df1c7d21851315bdb6b0f16a3a..tl/agt-F-sheet11-source-0325 -- tests/editing_conformance/test_native_sheet_ordinary_runtime.py`: PASS.

Behavioral qualification is intentionally unverified here; MAIN11 remains required after merge.
