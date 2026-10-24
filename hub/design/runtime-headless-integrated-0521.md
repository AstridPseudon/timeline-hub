## R5/D43 integrated proof — PASS

- Runtime before: `faf6a5477f9f6e4d96829046957518fef7a0dbed`, tree `5e909a876c780025c4b8aca10e42ff57cac092fd`
- Integrated HEAD after: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`, tree `f56c396c4495547680b46e832565278d2c375e69`
- Reviewed commits: `66657fda...` and `778878be...`
- Agent archive: `9cd3dbe865a941c052bda04ae0d61306d18f8f26`, tree `57f0231da0d7904ecd8778169973d6384e0ae141`, archived under `/tmp/w-16bda8f014/...`

Fixture identity:

- Current fixture blob: `1182259ea4bbb8f62ef3443f7db3f6a5e3bb50c4`
- Independent review 0518 / `778878be` fixture blob: identical.
- All non-fixture bytes match prior `faf6`; all non-headless/occupancy bytes match prior `2b49`. No product, auth, schema, client, pin, or caller changes.

Test command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/tmp/w-16bda8f014/agent-9cd3dbe865a941c052bda04ae0d61306d18f8f26 /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_headless_overwrite_refused.py
```

Result: `13 passed in 3.44s`, exit 0.

Origins verified:

- `astrid` and Agent-vendored `astrid_runtime_client`: exact Agent archive.
- `runtime_protocol`: this Runtime worktree.
- Production caller remains `runtime_protocol/server.py:302` → `commit_timeline`.

Checks:

- Ruff target: PASS
- `git diff --check`: PASS
- Worktree clean
- No full suite or supplementary pytest run.

Original 10 failures now tested and passing:

- `test_empty_default_over_authored_headless_shell_is_refused_untouched`
- `test_empty_default_over_empty_headless_shell_is_refused_untouched`
- `test_empty_default_on_a_fresh_timeline_is_accepted_and_replays`
- `test_empty_parent_over_hidden_nonempty_content_of_a_headless_timeline_is_refused_untouched`
- `test_genuinely_empty_headless_timeline_still_accepts_expected_head_null`
- `test_cas_correct_republish_after_reading_the_head_is_accepted`
- `test_headless_timeline_with_scoped_rows_refuses_empty_publish_untouched[timeline_references]`
- `...[timeline_shots]`
- `...[snapshot]`
- `...[dependency]`

The other three passing nodes—trackless invalid input, fresh second-timeline creation, and retired-route 410—are additional cases and were not credited as original closures.

D43 accounting: **36 closed / 0 open / 0 unaccounted**:

- 10 current integrated headless nodes.
- Prior 15 occupancy closures from `faf6` + Agent `9f2da582...` evidence.
- Prior 11 manifest, response, receipt/auth-key, and speed closures from the retained D43 reports.

The original baseline remains disclosed: full run `runtime-full-1024005856-29085` had `6479 passed, 36 failed`; this is not a new full-suite result, and no claim is made that all Agent heads were tested. Earlier failed qualification runs remain superseded and disclosed.

Commit message and `DONE` marker were written.