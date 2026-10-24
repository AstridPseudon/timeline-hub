## Result: PASS

Reviewed cumulative `458595850c...` → `d12e5143f...` (tree `703b1aac...` → `d2f3ea43...`).

- Diff: exactly one file, `tests/test_timeline_null_speed_retained.py`; `7 additions, 2 deletions`.
- Targeted test: mandated pytest command — **14 passed**.
- Six cases preserved: `None`, `[3, 2]`, `"3/2"` × child/parent.
- SQL `iterdump()` and CAS no-write assertions: unchanged, 2 occurrences each.
- Non-target ASTs: **9/9 exact**; only the intended refusal test function changed.
- Ruff: passed.
- In-memory compile: passed.
- `git diff --check`: passed.
- Private baseline/candidate Pyright (`--outputjson`): **7 vs 7 diagnostics**, zero new normalized identities/multiplicities.
- No skip, xfail, deselection, broad exception tuple, assertion loss, or status allowlist.

The real `RuntimeService.publish_parent_composition()` contains only the retirement guard, which raises status `410`, code `retired_route`, reason `timeline_commit_required`, before any speed inspection. The six tests exercise this production boundary and preserve the same no-write property.

The intentional behavior change is from prior `ValidationError`/`ConflictError` speed refusal to the earlier R5 retired-route refusal. This matches the settled plan: legacy publisher cannot seed those values.

No reviewer edits were made; worktree is clean. No full suite was rerun. The prior 0134 socket-bind failure is classified as ordinary sandbox networking, not a product or safety failure.