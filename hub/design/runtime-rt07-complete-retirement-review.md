# RT07 complete-retirement review — APPROVE (bounded)

Reviewed the immutable final port `tl/rt-m2-rt07-original-publication-suite-port`
at `1d8df1bb49a5df20b5529a389eb8820e0399eba7`, its compose parent
`9b0e540e0ccf4e422ad1d2edcc3565b7bec966da`, baseline `86ce14f`, and current
integration `5c32832`. This approves the narrow RT07 source/test candidate and
its evidence mappings. It is not an integration-adoption, release, pin, or
full-suite approval.

## Findings

The `publish_timeline_render` body cut is narrow and preserves the intended
boundary. The method now has only these paths:

- lookup of the attempt/task/project and wire validation;
- exact stored-request-hash and stored-timeline checks for an already published
  checkpoint, returning its durable result read-only;
- the existing lease, two-child admission, same-project timeline, immutable
  admitted-target, and tracked-head guards for fresh requests; and
- visible `RetiredRouteError` (`410`, `reason=command_required`) for fresh and
  prepared legacy requests.

The removed body no longer updates `project_documents`, appends legacy timeline
events, publishes an unpinned CAS snapshot, creates a render task, or creates/
completes a legacy checkpoint. The method contains no provider call or writer
after the guard path. `_assert_legacy_render_publication_target` is unchanged
against baseline/current and still fails closed on target mismatch, malformed or
inconsistent immutable admission, and tracked canonical history.

The accepted-checkpoint replay is the one retained legacy success path. It
compares the stored request hash and checkpoint target before returning the
stored result, without consulting live target/spec/head state or writing SQL,
CAS, staging, task, history, or checkpoint state. The preserved authority test
changes task cancellation/spec, target tracking, and archival state, then
asserts exact replay and unchanged SQLite/CAS state. A changed payload remains
a conflict. Prepared checkpoints remain durable but visibly refused; the old
writer is not resurrected.

## Original-success mapping

All three original publication positives are now strict real native tests, not
xfail-only replacements:

| Original behavior | Current proof |
| --- | --- |
| fenced atomic publication, exact retry, changed-payload refusal, cancel replay | `test_publication_is_fenced_atomic_and_exactly_replayable`: real Agent provider, settled proposal, requester `/v1` commit, accepted revision/head, revision-pinned render admission, exact commit/render idempotency replay, changed payload no-write, and replay after author cancellation |
| stale fence and cancellation at the old prepare seam | `test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence`: real producer guard refusal with unchanged state, then authentic proposal supersession after capture; no timeline revision, render task, or checkpoint is added |
| prepared checkpoint restart/recovery | `test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart`: accepted native checkpoint/pending render handoff, Runtime close/reopen, exact requester retry, one render admission, and exact render-admission retry |

The former same-project target-isolation positive is mapped to the real
provider/settled-proposal/requester/native commit plus historical render
admission in `test_tracking_is_scoped_to_the_publication_target`. Timeline B
succeeds while timeline A's head, history, and closure remain byte-identical;
wrong-target substitution is a separate no-write refusal. The former legacy
film positive is split correctly: the captured legacy head refuses the retired
writer without writes, then the equivalent canonical film is accepted through
the existing provider and admitted through the revision-pinned historical
render path. No fake accepted provider, forged history, compatibility writer,
or new artifact was introduced.

One existing strict xfail remains only for the deleted prepare/write race seam
(`test_canonical_tracking_after_prepare_refuses_before_publication_writes`). It
does not replace any of the three native positives and is correctly labeled as
the seam that no longer exists.

## Gate and marker accounting

The candidate adds `@pytest.mark.integration` to the three moved tests in each
of the two RT07 publication files. Repository default addopts exclude
integration tests. Therefore the recorded default targeted result:

```text
python -m pytest -q tests/test_timeline_render_publication.py tests/test_timeline_render_publication_authority.py
19 passed, 6 deselected, 1 existing xfail
```

has intentionally deselected those six moved tests. The separate recorded
integration lane ran the three ported publication tests (**3 passed**), and the
compose authority lane ran its four mandated authority nodes (**4 passed**);
the recorded bounded authority/publication selection was **19 passed, 6
deselected, 1 xfailed**. No RT07 credit is inferred from default deselection.

The named Gate2 proof also does not include either RT07 publication file. Its
exact file list is the commit execution/acceptance/integration/crash selection
in `ORCH/tests/suites.conf`, and its current result was **51 passed**. Thus the
moved RT07 markers are not hidden inside Gate2: the RT07 behavior is covered by
its separate named targeted/integration evidence, while Gate2 remains the
general atomic-commit proof.

## Tree, metadata, and staging checks

The candidate changes from baseline `86ce14f` are limited to
`runtime_protocol/service.py`, the two RT07 publication test files, and the
approved ordinary014 retry test delta in `tests/test_timeline_clip_replacement.py`.
There are no schema, OpenAPI, generated-artifact, lockfile, release, or pin
changes in the candidate diff. This is a code/test candidate using the
existing Agent provider import; it is not a newly generated normal014 artifact
and must not be advertised as one. Frozen R4 refs and artifacts were not
modified.

The candidate is not yet current-base: it descends from `86ce14f`, whereas
current integration is `5c32832`; current adds the boundary fixes in
`tests/test_runtime_boundary.py` and `tests/test_zero_shim_boundary.py`, which
are absent from the candidate branch. Before adoption, recompose the reviewed
RT07 changes onto current `5c32832` and rerun the required current-base
qualification. Do not replace or roll back those current fixes.

## Future contract cleanup

The retired operation remains advertised at the Runtime door
`/v1/attempts/{attempt_id}/publish-timeline-render`, in
`contract/openapi/workspace-v1.yaml`, and in the generated Python template and
client. The OpenAPI description still promises a durable `200` publication and
only lists `200`/`409`; it does not describe the intentional `410` retirement.
After all consumers migrate, this operation needs its own deprecation/removal
contract cleanup (including generated clients and route documentation). The
checkpoint store helpers and `timeline_commit_producer_checkpoint.py` are not
part of that cleanup: they are still used by the native producer handoff and
must remain.

## Evidence and limits

Recorded evidence, not rerun here per the brief:

- `ASTRID_CHECKOUT=/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/test_timeline_render_publication.py::test_publication_is_fenced_atomic_and_exactly_replayable tests/test_timeline_render_publication.py::test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence tests/test_timeline_render_publication.py::test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart`: **3 passed**;
- `ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-7b3e1205 PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-7b3e1205" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider -m 'not live and not darwin_native' tests/test_timeline_render_publication_authority.py::test_retired_writer_refuses_before_lookup_without_writes tests/test_timeline_render_publication_authority.py::test_exact_published_checkpoint_replays_before_live_target_changes tests/test_timeline_render_publication_authority.py::test_tracking_is_scoped_to_the_publication_target tests/test_timeline_render_publication_authority.py::test_canonical_equivalent_film_commit_remains_publishable`: **4 passed in 4.06s**;
- three ported tests plus two authority neighbors: **5 passed**;
- bounded publication/authority selection: **19 passed, 6 deselected, 1
  existing xfail**;
- four mandated authority nodes: **4 passed**;
- named Gate2 atomic proof: **51 passed**.

Static checks performed for this review:

```text
git diff --check 86ce14f tl/rt-m2-rt07-original-publication-suite-port  # passed
git show --check --oneline tl/rt-m2-rt07-original-publication-suite-port # passed
```

No full suite, renderer, MP4/ffprobe, browser, or live-socket run was made by
this review. Normal014 coordinated adoption, a qualifying full run on the
current-base composition, and current-base requalification remain explicit
holds. No product/test edit, pin, release, merge, or frozen-artifact mutation
was made.
