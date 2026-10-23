# G5 guidance authority return — BLOCKED / DRAFT ONLY

Do not integrate this draft. P1 remains gated; the three accepted/retry workflow bodies have not been rerun. The independent review's SOURCE FAIL is not cleared.

## Source

- Agent base: `206d0f8b037d49305f84621d8b7b1dbff36c5582` (`tl/agt-G5-guidance-auth-return-1225`).
- Prospective source tree (computed from Git tree bytes without writing Git objects): `1841585731d7e41b44f19b318f475071e7cce614`.
- Changed test file SHA-256: `4ee43b493e831ced785c1322c507fbb63a3ba11b64760fbb45b87399750d7f52`.
- Patch SHA-256: `dd5d90c0449adf1005363b33dd0b8b85a996e6d6109053962d0e4b156dac783a`; patch: `/tmp/w-017fa3be65/final.patch`.
- Paired Runtime inspected: `/home/user/work/runtime`, `3b926efab2eed122d374540baee297d4cdcec62a`.
- No commit was created; the harness assigns the final commit SHA.

## Draft changes

Only `tests/v10/test_domain_cli_projects_timelines.py` is changed. The proposed scoped `guidance_source` fixture reuses trusted setup, replaces the imported fixture's counterfeit `open_bundle` with the bound production `RemoteTimelines.open_bundle`, and binds public revision reads on the WorkspaceClient generated-method seam. The three workflow cases use this fixture and the same WorkspaceClient transport for helper checkout. Their accepted, canonical-data, exact-retry and unchanged-history assertions remain unchanged. Nine new authority-negative cases cover absent publication, wrong revision/publication pair, wrong receipt pair, parent/shot/internal digest damage, a validly rehashed but divergent canonical document, missing media pins and incomplete dependency manifest, with no-commit/history/database checks.

**This implementation is unfinished:** it attempts to construct a second `RuntimeService` for the realm already owned by the reused seed fixture. Runtime correctly denies owner admission. None of the authority-negative cases reached the production reader or their refusal/no-write assertions. No read-authority or complete-closure proof is claimed.

## Commands and results

Safe selector (after the test seam edit):

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-017fa3be65/safe tests/sdk/test_scene_save_core.py tests/v10/test_domain_cli_projects_timelines.py -k 'scene_save_core or navigation_preserves_resolved_scope_and_editing_resources or timelines_help_is_executable or render_help_includes_copyable_flat_profile or visualize_help_describes_filmstrip_navigation or show_defaults_to_readable_authored_rows or visualization_human_navigation_footer_is_compact'
```

**27 passed, 98 deselected (4.47s).** All 16 scene-save cases and the safe help/navigation/resource assertions remain green.

Authority negatives:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-017fa3be65/authority tests/v10/test_domain_cli_projects_timelines.py -k guidance_reader_rejects_wrong_authority_without_writes
```

**9 setup errors, 100 deselected (9.57s).** Every setup failed at `RuntimeService(tmp_path / "saved-source")` with `OwnerBusyError: another runtime daemon owns this realm`. The existing seed service owns this test-local realm; no daemon was started. Per the brief's actual-safety-denial stop/report requirement, I stopped this test work without weakening, bypassing or retrying the owner lock.

An earlier invocation used the literal worker `tmpdir` pathname as `--basetemp` and produced 9 `NotADirectoryError` setup errors. The harness stores the actual scratch directory as text in that file (`/tmp/w-017fa3be65`); the command above used the resolved scratch directory. No safety denial occurred in that first invocation.

Scoped quality:

```bash
PYTHONDONTWRITEBYTECODE=1 RUFF_CACHE_DIR=/tmp/w-017fa3be65/ruff-cache /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/v10/test_domain_cli_projects_timelines.py
git diff --check
```

Initial explicit Ruff check exposed three inherited I001 diagnostics and one new fixture F811. The F811 was corrected using the existing imported-fixture convention. A subsequent programmatic base/current comparison using `/home/user/work/venv-agent/bin/python -m ruff check --no-cache --output-format json --stdin-filename tests/v10/test_domain_cli_projects_timelines.py -` found the exact same three inherited `(code, message)` identities in base and final source, with no new finding. AST parse passed, and an AST comparison verified retained workflow assertions (excluding only the removed counterfeit nested seam's tuple assertion). `git diff --check` passed.

No full suite, HTTP/socket/browser fixture, native14/58, D17, P1/P4, shared install mutation, daemon, Git mutation or provider/core edit was run. No known-failing three-case body replay was run. Normal repository-wide mypy/Ruff gates were not run for this test-only blocked draft.

## Decisions, blocker and next steps

The production reader was chosen rather than reproducing its checks. Reusing trusted seed setup was intended to minimize the fixture diff, but opening a second service violates Runtime's owner admission; this is a fixture design error. The owner-lock rejection was respected, with no bypass.

A follow-up should replace this fixture with a scoped local fixture that owns exactly one RuntimeService from initialization through trusted seeding, generated/public read binding, real commit and teardown. Do not open a second owner or inspect closure cells/private revision caches. Then rerun authority negatives and the safe27 selector. Only after the manager joins the reviewed R1 atomic dependency-union fix should the three original workflow bodies run. This draft is not ready to merge and provides no whole-G5/P1 GO evidence.
