# G5 guidance single-owner fixture return — DRAFT ONLY / P1 NO-GO

Read-authority qualification passes: **9 authority negatives and safe27 pass**. The fixture source now uses one Runtime owner. The original three accepted/edit/retry workflow bodies remain unchanged and **unrun**, pending the manager joining independently reviewed R1 atomic-scope1216. This is not whole-G5, P1, or integration approval.

## Source and scope

- Agent base: `e0c64da34132143632132ef147e588d086cd7639`, continuing the saved1225 draft.
- Only changed repository file: `tests/v10/test_domain_cli_projects_timelines.py` (85 insertions, 28 deletions).
- Test file SHA256: `e7a4efce1169eb52d7df4592eaa38eb023707c9429e098e334960d97e37187ab`.
- Patch SHA256: `9a35eb3680464d44c555c738b085be0339041dc95e91e2187e18f10d0209720a`.
- Actual Runtime module: `/home/user/work/wt/rt-pin-3b926efa/runtime_protocol/service.py`; HEAD `3b926efab2eed122d374540baee297d4cdcec62a`; `git status --short` empty.
- No product/core/CLI/reader/provider/Runtime/dependency/pin/generated/schema/contract changes. No Git writes or integration merge.

The earlier `OwnerBusyError` was Runtime correctly refusing a defective second-owner fixture, not a safety/tool-classifier denial. D18 authorizes the harness correction; the owner guard is unchanged. No safety/tool/automatic-review denial occurred in this return.

## Fixture correction and sole-owner evidence

`guidance_source` now depends only on `tmp_path`, rather than the imported `saved_source` fixture. It initializes the realm with `RealmStore.initialize(...).close()`, constructs **one** `RuntimeService`, and owns it through all project/timeline creation, real media ingestion, trusted film seeding, provider registration, generated/public reads, captured commit calls, and final `service.close()` in `finally`. The `try` includes setup as well as yield, so setup failures also close the owner. The unused imported fixture is removed.

The local seed preparation retains the existing saved-film fixture's shape, `flat_film()` input and real media ingestion. It calls the existing `tests.helpers.trusted_seed.seed_trusted_parent` acceptance helper unchanged. That helper is trusted test setup, not positive evidence that Agent commands authored the seed. This fixture adds no fabricated prepared acceptance or synthesized authority. It neither opens a second service nor extracts closure cells/private revision caches as a public read.

`WorkspaceClient._generated` binds the actual service's public exact parent, shot and internal revision methods, and public commit-history method. `RemoteTimelines.open_bundle` is its default production method, with no override. The existing identity/inspection seam resolves the test's quoted aliases to canonical IDs; it supplies no revision closure or receipt. `document()` reads the current history's exact revision/publication pair through that production reader. Each negative case successfully opens that authentic closure both before and after the damaged read. This exercises actual supported in-process public service reads, not HTTP/daemon transport.

The captured send forwards the complete body and key unchanged to `RuntimeService.commit_timeline`, and returns its complete reply unchanged. This is the seam used by the retained workflow cases, but those commit bodies were deliberately not executed here. Static AST checks establish one service constructor, only `tmp_path` fixture dependency, close in finally, no `open_bundle` override, and no closure-cell/private-revision reader in the fixture. Executing all nine cases without owner admission errors supports that source finding; no second-owner admission probe or guard bypass was attempted.

## Tests: exact commands and results

Working directory: `/home/user/work/wt/agt-G5-guidance-one-owner-1234`. Each command ran once after the final fixture edit; there were no failed or intermediate test runs in this return.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=/tmp/w-4ca763e37a/authority tests/v10/test_domain_cli_projects_timelines.py -k guidance_reader_rejects_wrong_authority_without_writes
# 9 passed, 100 deselected in 3.24s; exit 0.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=30 --basetemp=/tmp/w-4ca763e37a/safe tests/sdk/test_scene_save_core.py tests/v10/test_domain_cli_projects_timelines.py -k 'scene_save_core or navigation_preserves_resolved_scope_and_editing_resources or timelines_help_is_executable or render_help_includes_copyable_flat_profile or visualize_help_describes_filmstrip_navigation or show_defaults_to_readable_authored_rows or visualization_human_navigation_footer_is_compact'
# 27 passed, 98 deselected in 4.41s; exit 0.
```

No full suite, socket/browser/live service/daemon, original three workflow replay, native14/58, D17, or P1/P4 suite was requested or run. No shared install or shared cache was modified.

## Quality and assertion mapping

```bash
git show HEAD:tests/v10/test_domain_cli_projects_timelines.py > /tmp/w-4ca763e37a/test-before.py
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/w-4ca763e37a/quality.py
git diff --check
```

The private script (durably copied into evidence) runs these exact scoped commands on base and final source, with `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=.:/home/user/work/wt/rt-pin-3b926efa`, and `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-3b926efa`:

```bash
/home/user/work/venv-agent/bin/python -m ruff check --no-cache --output-format json --stdin-filename tests/v10/test_domain_cli_projects_timelines.py -
# stdin = base, then final; each exit 1 with the same 3 inherited I001 findings.
/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-4ca763e37a/mypy-base --hide-error-context --no-color-output --no-pretty --show-error-codes --shadow-file tests/v10/test_domain_cli_projects_timelines.py /tmp/w-4ca763e37a/test-before.py tests/v10/test_domain_cli_projects_timelines.py
/home/user/work/venv-agent/bin/python -m mypy --cache-dir=/tmp/w-4ca763e37a/mypy-current --hide-error-context --no-color-output --no-pretty --show-error-codes tests/v10/test_domain_cli_projects_timelines.py
# Each exit 1: 15 inherited errors in 1 file; exact path/message/code multisets identical.
```

Quality script exits 0: Ruff identities (code/message within the same single path) **3 → 3**, mypy path/message/code identities **15 → 15**, zero additions or removals including multiplicity. AST parse and diff whitespace checks pass. These are baseline-parity results, not zero-diagnostic claims or a repository-wide make-check qualification.

AST comparison excludes only `guidance_source` and its now-unused fixture import and proves **every remaining top-level node, test body, decorator, parameter list and assertion unchanged** from e0c64da341. Full assertion text and final line mapping are in `quality.json`:

| Requirement | Retained assertions / source | Qualification |
|---|---|---|
| Nine strict authority controls | Lines 1281–1344: absent publication, wrong revision/publication, receipt pair, parent/shot/internal digests, rehashed divergent canonical payload, missing media, incomplete internal manifest | All 9 pass |
| Refusal/no writes | Lines 1339–1344: refusal + protocol_error, no captured commits, identical SQL dump, unchanged history and publicly reopened document | All 9 pass |
| Three quoted JSON workflows | Lines 1347–1405: checkout/file/draft parameters, quoted project/timeline/path, correct helper invocation, export to separate `.commit.json` | Source unchanged; bodies pending |
| Accepted + full canonical readback | Lines 1408–1425: valid check, accepted data + receipt, exact base pair, atomic mode, label, ordinal/patch/doc.patch, edited internal parameter and parent/shot opaque content | Source unchanged; bodies pending |
| Exact retry + unchanged landed state | Lines 1426–1428: identical publication reply, unchanged history and canonical document | Source unchanged; bodies pending |
| Original editable-file handling | Workflow export/path assertions unchanged; production helper preserves the source by writing a separate prepared file at `timeline_document.py:286` | Source preserved; no new behavioral claim |

The unchanged production caller is `timeline_document.py:265–333` → `TimelineSession.open/_bundle/commit_many` → `RemoteTimelines.open_bundle/commit` → WorkspaceClient generated seam. The replacement fixture does not filter or rebuild requests/replies: base pair, commands, label, steps/patch/reads/ordinals, merge, reads, idempotency key, dry_run, source, rationale, group_id; data+receipt accepted/merged, full canonical document, records/dependencies/effects, history/undo_steps; preview/would_status, conflict head/reason and invalid code/path/hint/command remain on the unchanged production paths. This task does not newly qualify all those fields or outcomes. No contract or production behavior was edited to obtain green tests.

## Durable evidence and handoff

Evidence directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-G5-guidance-one-owner-1234/evidence`.

Contains `fixture.patch`, `identity.txt`, `authority.log`, `safe27.log`, `quality.py`, `quality.json`, base/final Ruff JSON, and base/final mypy logs. Worker report is also saved beside that directory. Scratch caches need not be retained for this result.

No fixture/read-authority blocker remains. The R1 atomic dependency-union source is not joined into this worker tree; the known failing three workflow bodies were not repeated. Manager should independently review this fixture diff, join reviewed R1 atomic-scope1216, then dispatch the three unchanged workflow bodies on that joined source. Keep G5 DRAFT ONLY and P1 NO-GO until the applicable reviews and integrated proof permit otherwise.
