# G5 guidance source/behavior-fidelity review

## Result

**SOURCE FAIL — behavioral evidence remains PENDING; do not integrate or claim whole-G5/P1 GO.**

Reviewed cumulative `206d0f8b0` (`tl/agt-G5-guidance-sol-1158`) against
`086db31e4`, using PLAN §3 G3/G5 and C0 §§1–5 plus the settled Sol guidance
report at `design/agent-G5-guidance-sol-1158.md`.

The production diff is bounded to the requested guidance seams:

- `astrid/packs/timeline/cli.py`
- `astrid/packs/rendering/docs/scripts/timeline_document.py`
- `tests/v10/test_domain_cli_projects_timelines.py`

There are no schema, contract, generated-client, lock/pin, Runtime, provider,
writer, or unrelated file changes. No product files were edited by this
review.

## Finding

### F1 — the new three-case harness does not use the actual public exact-pair read

The new test replaces `client.timelines.open_bundle` with `pinned_bundle`
(`tests/v10/test_domain_cli_projects_timelines.py:1209–1218`). The wrapper calls
the imported fixture's already-replaced lambda and, when given a
`publication_id`, only asserts the expected tuple and injects that publication
ID into `base_parent`; it does not perform or verify the public exact
revision/publication-pair read.

The imported `saved_source` fixture itself replaces `open_bundle` with a lambda
that directly calls the Runtime service's private
`revision_closure(...)` (`tests/editing_conformance/test_commit_runtime_source_copy.py:254–256`)
and ignores the publication argument. Production `RemoteTimelines.open_bundle`
must instead scan history for the exact publication, verify its revision and
receipt pair, hydrate the canonical document, and compare it with the closure
read (`astrid/sdk/_remote_timeline.py:169–206`).

Therefore the three new tests do exercise the real Runtime commit path and
real generated request capture, but they cannot certify the requested
read-authority/complete-closure/base-pair behavior. The harness has a
counterfeit read seam for precisely the authority context under review.

Recommended repair is test-only: drive the real `RemoteTimelines.open_bundle`
through a generated/public read implementation, or make the fixture's seam
faithfully implement the exact pair/history/canonical-document checks. Keep the
accepted/retry/history assertions intact; do not replace the current Runtime
failure with an expected refusal.

## Source checks that passed

- The cumulative diff is only the three paths above; `git diff --check` passes.
- JSON navigation now uses `checkout → edit → check → commit`; no cut-sheet
  `timelines apply`, guessed flags, or draft-path-as-ref substitution remains.
- `_cmd_edit` exports local draft JSON with the existing
  `Checkout.load(source).document()` API to a separate `.commit.json` path,
  then emits quoted helper `check` and `commit` commands. The source path is
  not written by this export expression.
- Project, timeline, source, and candidate paths are shell-quoted with
  `shlex.join`; the source contains spaces/apostrophes coverage.
- The helper's `commit` parser is the same existing normal `TimelineSession.commit_many`
  implementation (`timeline_document.py:327–333`) with the exact base pair,
  atomic merge, label, source, key, and existing result handling. The
  compatibility `publish` spelling is an argparse alias to this same command
  branch; it does not retain a separate writer body and is not itself a G5
  separate-publish violation.
- The legacy `timelines publish` CLI route is not registered in the current
  draft. Existing prose/compatibility strings containing “publish” are not a
  new writer route.
- Existing navigation/resource/scope assertions remain present; only the
  intentional workflow literal changed from `publish` to `commit`. The three
  new accepted/retry/history assertions remain in the test and are not
  weakened or skipped.
- No changes touch request base pairs, commands, labels, per-step patches and
  reads, command ordinals, merge/read/key/dry-run/source/rationale/group ID,
  receipts, canonical documents, records/dependencies/effects, history,
  undo steps, preview/would-status, or conflict/invalid envelopes.

## Behavioral status and evidence

The exact permitted safe selector was run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTEST_ADDOPTS= /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/w-125cb2f4b9/protected-final tests/sdk/test_scene_save_core.py tests/v10/test_domain_cli_projects_timelines.py -k 'scene_save_core or navigation_preserves_resolved_scope_and_editing_resources or timelines_help_is_executable or render_help_includes_copyable_flat_profile or visualize_help_describes_filmstrip_navigation or show_defaults_to_readable_authored_rows or visualization_human_navigation_footer_is_compact'
```

Result: **27 passed, 89 deselected**. This includes all 16 scene-save cases
and the retained navigation/resource/help assertions.

I did not rerun the three continuation cases, per the brief. Durable prior
evidence in `design/agent-G5-guidance-sol-1158.md` records **3 failed** at the
paired Runtime's `provider atomic dependency union omits a touched scope`
records-authentication refusal. All three modes reach that unchanged Runtime
failure after JSON loading, validation, command emission, and
`session.commit_many`; the accepted, canonical-data, retry, and unchanged
history assertions remain in place but are not reached. This is behavioral
PENDING and owned by the dedicated Sol R1 atomic-scope task, not a reason to
weaken the guidance tests.

Prior durable gate evidence records normal mypy **1911/1911** and normal Ruff
**2149/2149**, with raw diagnostic identities unchanged (inherited findings
only), plus artifact/diff/vendor checks passing. No full, browser, HTTP/socket,
P1/P4, native14/58, D17, daemon, shared-dependency, or Git mutation was run.

## Next steps

1. Repair the new test's read seam so it exercises the actual exact
   revision/publication pair authority, while retaining the current behavior
   assertions.
2. After the Runtime atomic-scope repair, rerun the three continuation cases
   and then let the orchestrator decide integration/P1 status.

