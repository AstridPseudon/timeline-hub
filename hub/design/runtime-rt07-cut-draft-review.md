# RT07 Runtime render-writer cut draft review

## Verdict

**BLOCKED for landing; DRAFT is acceptable.** Reviewed immutable candidate
`5410256fc5fa3b934001cd7752138d989f124d4e` (parent/base
`6ab3243972f8dc49105819e6d7ba7aef1a2888b8`). This review does not authorize
merge.

The candidate removes only the intended legacy canonical writer body: 172
product lines from `runtime_protocol/service.py`. Its two-file diff does not
touch Runtime execution, catalog, normal commit/history, receipt, or ordinary
render admission writers. The route and generated/OpenAPI surface remain, and
the door-level authentication controls passed. The deletion boundary is
therefore directionally correct, but the current replacement is too early and
too unconditional for RT07.

## Findings

### 1. Blocking: accepted publication replay and checkpoint recovery are lost

At candidate `runtime_protocol/service.py:7172-7181`, the method raises
`RetiredRouteError` before parsing the request, finding the attempt, or reading
`timeline_render_publications`. The old accepted result was intentionally
replayable without depending on live task/spec/timeline state:

- `tests/test_timeline_render_publication.py:103-129` checks exact replay,
  changed-payload refusal, and replay after author cancellation.
- `tests/test_timeline_render_publication_authority.py:116-129` checks replay
  after the live target/spec has been removed or archived.
- `tests/test_timeline_render_publication.py:160-192` checks the durable
  prepared-checkpoint restart path.

The candidate therefore loses the required accepted-retry seam, not merely the
unsafe writer. Keep a minimal read-only ledger/checkpoint lookup for an already
durably accepted publication, keyed by the stored request hash, and return the
stored result without invoking a provider, re-executing render, publishing CAS,
creating a task, or writing a document. The prepared-checkpoint restart case
must also be explicitly accounted for before landing; it cannot silently become
an unrecoverable row. Do not restore the compatibility writer to solve this.

The unchanged positive tests must remain strict and must not be converted to
xfail, skipped, weakened, or have assertions removed. The candidate's central
lane reports 17 failures, including these replay/recovery cases; that is not
all legacy-positive failure as claimed in the candidate handoff.

### 2. Blocking: project/target authority guards are dead code

The candidate leaves `_assert_legacy_render_publication_target` at
`runtime_protocol/service.py:7144-7169`, but the unconditional raise means it is
never called. Consequently the unchanged authority tests at
`tests/test_timeline_render_publication_authority.py:56-113` no longer verify
tracked-head refusal, same-project target matching, malformed/admitted target
validation, or immutable-spec authority. These are safety refusals, not
legacy-positive behavior that may be allowed to fail. Preserve the existing
route authentication plus project/target scope checks and zero-write refusal
semantics while cutting every canonical document/render side effect.

The candidate's new test at `tests/test_timeline_render_publication_authority.py:44-53`
proves only a direct service call with a missing attempt returns 410 without a
write. It does not protect the dead project/target guard seam. The central door
controls passed, so HTTP credential rejection remains present; that does not
substitute for the service-level project/target authority checks.

### 3. Blocking gate: native consumer replacement is not qualified

The current Agent still calls the retired route from:

- `astrid/core/execution/generic_host.py:8419-8450` and
  `:9648-9657` (`_publish_assembled_timeline` from `run_task`);
- `astrid/packs/rendering/shared/runtime_stitch.py:143-156`;
- `astrid/sdk/remote.py:2124-2150` and
  `astrid/sdk/workspace_client.py:1198-1259`.

The required equivalence map is the current-014 registered two-positive real
host cohort in
`tests/packs/rendering/test_registered_assembler_producer.py`: settled
proposal, requester/outbox handoff, commit retry, lost acknowledgement,
restart, historical revision-pinned render, real MP4 output, and guarded undo.
That peer-owned gate is pending. Until those consumers migrate to
settled-proposal -> requester/outbox -> `/v1` commit and the paired gate is
green, this route retirement cannot land.

## Evidence and test mapping

Candidate diff evidence:

- `git diff-tree --check 5410256fc5fa3b934001cd7752138d989f124d4e^ 5410256fc5fa3b934001cd7752138d989f124d4e`: pass.
- Changed files are only `runtime_protocol/service.py` and
  `tests/test_timeline_render_publication_authority.py`.
- Candidate targeted refusal: `python -m pytest -q tests/test_timeline_render_publication_authority.py -k retired_writer_refuses_before_lookup_without_writes` — **1 passed, 17 deselected**.
- Candidate legacy publication lane: `python -m pytest -q tests/test_timeline_render_publication.py` — **3 failed** at the deliberate retired-route refusal; original assertions remain unchanged.
- Central lane `rt-m2-render-writer-cut-prepare-targeted-1020161414-17036`, command
  `python -m pytest -q tests/test_timeline_render_publication_authority.py tests/test_timeline_authority_door.py` — **17 failed, 13 passed in 50.24s**. The 13 door/refusal controls passed; the 17 failures include the service authority negatives and old replay/positive cases, so they are not all acceptable legacy-positive failures.
- No full suite, browser, renderer, or duplicate live-socket run was requested
  by this review. The candidate handoff records its local door attempt was
  blocked by sandbox bind permission; the central door lane supplied the
  available evidence.

## Blockers and required next steps

1. Repair the cut with a read-only accepted-checkpoint replay seam and an
   explicit disposition for prepared checkpoint recovery. No compatibility
   document writer, provider re-execution, render dependency, new route, DTO,
   or scope widening.
2. Keep route authentication and project/target authority tests green while
   retaining the visible zero-write retired refusal.
3. Complete Agent consumer migration and the current-014 registered two-positive
   real-host/requester/outbox/lost-ACK/restart/historical-MP4/undo gate.
4. Then run the required paired Runtime/Agent qualification and green full
   suite through the central test service. Do not merge or request merge before
   those results are recorded.

