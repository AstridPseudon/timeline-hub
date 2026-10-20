# RT07 read-only replay 969 draft review

## Verdict

**APPROVE DRAFT QUALITY ONLY. Do not land or merge this candidate yet.**

Reviewed `969bcdbe4bff19debd015908c8ae5af97f07e7f5` against parent
`5410256fc5fa3b934001cd7752138d989f124d4e` and base/current `6ab3243972f8dc49105819e6d7ba7aef1a2888b8`, using
`design/runtime-rt07-readonly-replay-fix.md` as the controlling design.

## Findings

No blocking RT07 draft-quality finding.

- The published-checkpoint branch authenticates through the attempt and task,
  requires the task's project to remain present, compares the request hash to
  the stored checkpoint hash, compares the supplied timeline to the stored
  checkpoint custody, and returns only the stored published result. It does
  not consult live target/spec/head state or perform document, CAS, task,
  history, or checkpoint writes.
- A changed payload is rejected before any write. A prepared checkpoint and a
  fresh request both retain the existing lease, continuation, same-project
  timeline, admitted-target, immutable-spec, and tracked-head checks as
  applicable, then receive the retired-route refusal without creating or
  resuming a legacy publication.
- The diff adds no table, compatibility writer/provider, credential scope,
  route, or relaxed lease authority. The actual stored checkpoint's
  `timeline_id` is used for custody comparison, with the prepared payload only
  as the existing-row fallback when that stored field is absent.

## Evidence

- Focused local command reviewed:
  `/home/user/work/venv-runtime/bin/python -m pytest -q tests/test_timeline_render_publication_authority.py -k 'retired_writer_refuses_before_lookup_without_writes or retired_writer_refuses_without_prepare_or_publication_writes or published_checkpoint_replays_read_only_after_live_authority_changes or prepared_checkpoint_remains_retired_without_recovery_write or tracked_target_refuses or same_project_unadmitted_target or malformed_admitted_target or inconsistent_native_target or corrupt_immutable_spec'`
  — **17 passed, 3 deselected**.
- Central authority/door command reviewed:
  `python -m pytest -q tests/test_timeline_render_publication_authority.py tests/test_timeline_authority_door.py`
  — **29 passed, 3 failed**. The failures are the unchanged fresh legacy
  positives `test_exact_published_checkpoint_replays_before_live_target_changes`,
  `test_tracking_is_scoped_to_the_publication_target`, and
  `test_legacy_head_without_canonical_publication_remains_publishable`.
  They are intentional strict draft-red cases, not xfails, and must remain
  mapped to the Agent current-014 actual native proposal-completion positive
  before landing.
- `git diff-tree --check 969bcdbe4bff19debd015908c8ae5af97f07e7f5^ 969bcdbe4bff19debd015908c8ae5af97f07e7f5` — passed.
- Candidate `python -m compileall -q runtime_protocol/service.py` — passed.

No full suite, browser/live-socket, render/duplicate, or native Agent
qualification was run or requested. The review worktree was left unchanged at
base `6ab3243`.

## Before landing

Keep the three strict draft-red positives unchanged. Do not claim that either
the route or its old consumers are retired in integration. Land only after
the Agent current-014 native replacement supplies the actual proposal-
completion positive and the paired qualification passes.
