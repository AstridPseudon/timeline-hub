# G5 guidance authority review — PASS / DRAFT ONLY / P1 NO-GO

## Result

**PASS for the scoped source/read-authority review of `tests/v10/test_domain_cli_projects_timelines.py`.** This is not whole-G5 qualification: the three parameterized JSON workflow bodies were intentionally not run, pending the reviewed R1 atomic-scope join. Keep G5 **DRAFT ONLY** and P1 **NO-GO**.

Reviewed `tl/agt-G5-guidance-one-owner-1234` (`71d1602dc`) against original three-workflow source `206d0f8b037d49305f84621d8b7b1dbff36c5582`, with the prior source review and one-owner design report as context.

## Authority/source findings

- The fixture constructs exactly one `RuntimeService` (test line 1200), wraps all setup/yield work in `try/finally`, and closes that service at line 1278. It depends only on `tmp_path`.
- It uses production `RemoteTimelines.open_bundle` without assigning/replacing `open_bundle`. `document()` obtains the public history head's exact `(revision_id, publication_id)` pair and reopens through that reader.
- The generated seam contains public Runtime operations only: `list_timeline_commits`, parent/shot/internal revision reads, and `commit_timeline`. The commit provider is `load_timeline_commit_provider("astrid")`; there is no fake provider, closure-cell extraction, private revision cache, or `revision_closure` use in the fixture.
- The nine authority cases mutate public read responses/pairs, then call `client.timelines.open_bundle` and assert `protocol_error`, zero captured commits, identical SQL dump, unchanged public history, and an unchanged fresh public document read. They therefore reach the reader's exact-pair, receipt, digest, canonical-closure, media/dependency-manifest checks; no expected exception is injected into `open_bundle`.
- The prior two-owner `OwnerBusyError` setup problem is absent. No owner guard, product code, provider code, Runtime, CLI, schema, contract, pin, generated file, dependency, or production caller was changed. The cumulative diff from `206d0f8b` names only this test file.

## Original workflow fidelity

The original `test_timeline_editing_guidance_consumes_its_json` remains one parameterized test covering `checkout`, `file`, and `draft`. AST mapping shows all 21 behavioral assertions retained exactly, including JSON validation, CLI module/path/quoted-target checks, request base pair, atomic merge, label, command ordinals, per-step patch, `doc.patch`, edited values, accepted receipt, idempotent retry, history, and canonical readback.

The only removed original assertion is the seam-only assertion inside the deleted fake `pinned_bundle` reader (`(revision_id, publication_id) == ...`). It did not test production behavior; retaining it would reintroduce the authority counterfeit identified by the 1216 review. Actual CLI guide strings and target assertions are unchanged. The production caller and full-v2 forwarding/result paths are unchanged because no production file changed; the unrun accepted/retry behavior remains pending the R1 join.

## Exact authorized tests

Runtime checkout: `/home/user/work/wt/rt-pin-3b926efa`, HEAD `3b926efab2eed122d374540baee297d4cdcec62a`, clean.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=25 --basetemp=/tmp/w-1e3ffb52e6/authority-review-1239/authority tests/v10/test_domain_cli_projects_timelines.py -k guidance_reader_rejects_wrong_authority_without_writes
# 9 passed, 100 deselected; exit 0

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=25 --basetemp=/tmp/w-1e3ffb52e6/authority-review-1239/safe27 tests/sdk/test_scene_save_core.py tests/v10/test_domain_cli_projects_timelines.py -k 'scene_save_core or navigation_preserves_resolved_scope_and_editing_resources or timelines_help_is_executable or render_help_includes_copyable_flat_profile or visualize_help_describes_filmstrip_navigation or show_defaults_to_readable_authored_rows or visualization_human_navigation_footer_is_compact'
# 27 passed, 98 deselected; exit 0
```

The first attempts with a mistyped Runtime path and the harness `tmpdir` file were collection/basetemp setup failures, not test-body results. The corrected commands above are the authoritative runs. No full suite, daemon, browser/socket suite, or the three known-failure workflow cases was run.

## Quality and durable checks

- Scoped Ruff on base `e0c64da34` and current source: 3 inherited diagnostics on each, exact identity, zero added/removed; both exit 1 because the inherited findings remain.
- Private scoped mypy with a base shadow file and isolated caches: 15 inherited diagnostics on each, exact path/message/code identity, zero added/removed; both exit 1 because the inherited findings remain.
- `git diff --check`: exit 0.
- AST checks: retained top-level source equal after excluding the intentional fixture/import changes; one RuntimeService constructor; `tmp_path` only; close in `finally`; no private closure/revision-cache reader; no `open_bundle` override. Current test file SHA256: `e7a4efce1169eb52d7df4592eaa38eb023707c9429e098e334960d97e37187ab`.
- Worktree status is clean after the review; no repository file was edited.

## Next step

Independently review/join the R1 atomic dependency-union repair, then run the three unchanged workflow modes on that joined source. Do not promote this scoped PASS to whole-G5 or P1 GO until those behavioral results and the orchestrator's integrated gate are satisfied.
