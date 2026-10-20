# Agent outer voiceover native handoff

2026-10-20. Bounded result: **BLOCKED by missing authored command carriers and an actual Runtime admission restriction**.
No Runtime contract decision is reopened. No product code, pack declaration,
schema, permission, generation intent, pin, endpoint or requester implementation
was changed. The original outer authoring test double remains, explicitly
unqualified. No outer settlement/requester success or WC5 retirement is claimed.

## Source

Worker: `agt-m2-voiceover-outer-native-producer`.
Base commit `9c8a38e067ce5ba14612c2179abc89fb5487ddb3`, base tree
`83f16e907286f0a33b92a15a9df42277b4188264`, inherited from
`tl/agt-m2-speech-claim-fixture-repair`.
Only added source file:
`tests/packs/video_editing/test_outer_voiceover_native.py`.

Required tuple retained without overrides:

- Normal generated client contract `0.2.14`, schema
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- `runtime.lock.json` source `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  producer `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- Integration daemon explicitly uses `ad97e16effc53fa13f91c43f076f6edb3c38985f`
  through the existing Runtime archive locator.
- Shared environments were read-only. No dependency installs or cache writes
  into shared environments. No full suite and no duplicate inner WAV cases.

## Actual fixture counterexample

The new bounded probe imports the existing `fixture` and `synthesis` from
`tests/packs/video_editing/test_draft_voiceover.py`; it does not replace their
expectations or add a snapshot writer. With changed first script text
`Long new narration`, `prepare_draft_voiceover(..., timing_policy='ripple',
padding_seconds=.15)` produces the original successful intent:

| Existing original assertion | Exact required outcome |
| --- | --- |
| First placement duration | 3000 -> 4150 ms |
| Second placement start | 3000 -> 4150 ms |
| First still hold | 3 -> 4.15 seconds |
| Narration source end | 2 -> 4 seconds |
| Spanning parent hold | 6 -> 7.15 seconds |
| Parent config duration | 6 -> 7.15 seconds |
| Shot draft provenance | text/digest/settings/new audio/run/task/base-head record at `payload.metadata.draft_voiceover` |
| Detached safety | Original first placement remains 3000 ms |

The strict positive xfail attempts `capture_shot_set` using the exact prepared
provenance. Existing `ShotSetArgs.values` accepts only `name` and bounded
`settings`, with `additionalProperties:false`; it rejects `metadata` before
execution. The test retains the intended successful capture and resulting
metadata assertion, with `xfail(strict=True, raises=CommandError)` naming WC5.
No original passing behavior test was changed, skipped, weakened or removed.

This is a decisive missing carrier even for preserve timing. Further existing
source limits prevent a complete lowering:

- `astrid/sdk/timeline/_media_inputs.py:_verified` accepts only image/video;
  exact Runtime-verified `audio/wav` is rejected. A readable WAV and five-field
  media selection do not themselves authorize an edit.
- `native_occurrence_media_commands.py:_clip` requires a visual child track;
  the fixture's narration is on an audio track. `clip.add` only admits parent,
  non-media clips. Neither is an audio insertion workaround.
- `clip.set` exposes only hold set and bounded clears; it cannot replace the
  existing direct-media selector or set the source window.
- `shot.set` cannot write the required draft provenance, payload asset/item
  mirrors, or an internal registry binding. `clip.set-params` targets clip
  params and cannot serve as shot metadata.
- No installed command writes the existing occurrence's duration or the parent
  config duration. `placement.move` moves a raw clip inside its owner, not the
  occurrence's parent placement. Duplicate/delete cannot preserve the exact
  existing occurrence identities while changing those fields.
- `timeline.inverse`/`timeline.restore` consume accepted history/revisions;
  they cannot import a newly synthesized candidate. `producer.guard` records
  verified authority and has no authored writes.

Changing the five-field pin, using a bare digest/latest lookup, dropping
provenance, moving metadata to params, relabelling audio as visual, inventing
accepted history, or comparing snapshots to emit arbitrary writes would not
preserve this authored result. All are excluded by the settled brief.

## Identities, custody and authority

Outer: registered executor **`video_editing.sync_draft_voiceover`** from the
actual video_editing pack and GenericPackHost discovery/preflight/registration.
Inner: **`generation.generate_speech`** remains a separate executor identity.
There is no declared child_delegation/local_orchestrator relation on the outer
action; call nesting does not establish a Runtime parent-child relation.

The existing outer action returns only report/receipt and currently calls the
legacy bound authoring interface. It has no declared file output
`authoring_proposal` and does not settle the closed six-field D13 artifact.
Adding that declaration alone cannot produce missing command meaning.

The admission test records ordinary SDK `invoke(..., kind='executor',wait=False)`
and its actual retained spec. That normal submit has no original admitted target
and an empty input manifest. The current action has no file port. Adding a script
execution_request descriptor to that ordinary invocation fails before dispatch:
SDK invocation constructs `input_manifest=[]` and exact manifest merge refuses
the descriptor as missing from input_object_ids. No port/manifest override is made.

The probe then separately submits through normal `client.tasks.create`, with
exactly `runtime_dependencies.publication.admitted_target` containing project,
timeline, original revision and original publication, and exactly ordered
`execution_request.inputs` / `input_object_ids`. This request reaches the actual
Runtime and refuses: **runtime continuation requires exactly two ordered
dependency edges**. There is NO admitted spec/task for this pinned request.
Its ingested script.txt bytes prove managed object custody only, not authoritative
timeline script selection. No new `script_pins` field or child relation is added.

**Evidence contradicting the carrier audit:** ad97 `runtime_protocol/store.py`,
`_continuation_predecessors` (2823-2857), inspects any public
`spec.runtime_dependencies` object. It requires two edges plus ordered_cas_inputs
aggregation and also refuses nonempty top-level input_object_ids. Thus the
publication-only target + ordered script-input shape described in
`runtime-voiceover-native-admission.md` is not actually admissible in this flow.
The source-only audit's claim of an existing usable generic admission seam is
incomplete. This is reported to the orchestrator, not fixed or bypassed here.
The generic D13 settled-artifact checks themselves are not disproven.

The ordinary diagnostic task is not executed, claimed or settled and is cancelled
through the normal owner API before the pinned admission probe. The refused
request creates no task. There is no outer attempt pin or settled proposal,
and no inner task is started by this investigation. The previously qualified
inner managed WAV/selection/provenance tests are unchanged and are not rerun.
Their success cannot stand in for an outer producer pin.

The admission fixture uses an empty canonical bootstrap, not a seeded voiceover
timeline. The ripple counterexample uses the original detached unit fixture.
No end-to-end authored voiceover materialization is claimed.

The integration negative submits to the existing commit door with the real
worker credential and asserts exact HTTP 401 / unauthorized / credential lacks required scope, plus unchanged
accepted bootstrap history and head. No
requester credential is lent to a worker. The request's empty command suffix is
intentional: authorization must refuse before edit validation, and it cannot
masquerade as a substitute voiceover proposal.

Once a carrier is authorized and implemented, use only the existing D13 codec:
`commit._digest` over the full proposal minus its own digest, declared durable
`authoring_proposal` artifact, exact outer five-field attempt identity and
original four-field target. Requester `TimelineSession.queue_proposal` owns the
outbox and commit. Producer output never gains commit authority. This worker
adds none of those product steps because the mandatory command lowering is not
available within its allowed scope.

## Validation

Local bounded command (no sockets):

```sh
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_fixture_still_requires_audio_provenance_and_ripple tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_fixture_provenance_can_be_captured_without_a_snapshot_writer tests/packs/video_editing/test_draft_voiceover.py tests/sdk/test_timeline_producer_guard.py
```

Final-tree result: **41 passed, 1 xfailed**, 2.50 seconds (earlier bounded run: 4.85 seconds). The entire existing voiceover
unit file is unchanged, including all original22 readable-audio/RIPPLE positives
and the inherited speech-admission addition. Existing producer guard/outbox
neighbors pass. A focused `-rx` rerun confirms the strict xfail reason above.

```sh
env PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/packs/video_editing/test_outer_voiceover_native.py
git diff --check
```

Result: PASS.

Central final result `1020203011-12468`: **1 xfailed in 13.67 seconds**;
service exit 0. This is the missing target admission requirement, NOT a passing
outer settlement. Final source tree **3f9514685990cd261c54ecbfd28580e2df014b90**;
source bytes were compared with the central snapshot tree.

- Actual outer queued task: `7dcf6d2ad4204beda5612b9922900a5e`.
- Registered capability digest:
  `sha256:952b6df12941758550b696a06f980580fead2f40381fe5954eaddbc0fb3a08c5`.
- Project `4399b84a8caf4bf6bfa1d261c786185e`, timeline `film`.
- Actual original base revision `bootstrap-cb774932ae3441fbb975e60242d287a1`,
  publication `txn-8c90769ad56c4dc0aec194764f7836f0`.
- Script object/digest
  `sha256:6264b5eac37a1c42bd1f653665504601a4a45bba89b48cdb40ba55f953bd2bbd`.
- Worker negative completed before pinned submit: exact 401/unauthorized/missing
  required scope; accepted history and real bootstrap head unchanged.
- Pinned request was refused before task creation: no pinned admitted spec,
  attempt, settled proposal or producer digest exists.

Exact captured normal request, normal admitted spec and refused pinned request:
`workers/agt-m2-voiceover-outer-native-producer/outer-admission.json`.
Central complete command/result:
`tests/agt-m2-voiceover-outer-native-producer-native014-sockets-integration-1020203011-12468/{summary,log.txt}`.

Exact service invocation:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
$ORCH/bin/request-test agt-m2-voiceover-outer-native-producer native014-sockets-integration --files tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_admission_records_exact_spec_and_worker_has_no_commit_authority
$ORCH/bin/wait-test agt-m2-voiceover-outer-native-producer-native014-sockets-integration-1020203011-12468
```

The named suite's actual pytest suffix is:

```sh
/home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/packs/video_editing/test_outer_voiceover_native.py::test_outer_admission_records_exact_spec_and_worker_has_no_commit_authority
```
Only the one explicit admission/authority node is selected; no outer settlement
or inner generation case is run. Trace output uses the test capture fixture.

Diagnostic history (all the same bounded node, no product changes):

- `1020202335-31688`: service rejected `-s` in --files before pytest; zero tests.
- `1020202406-19667`: failed before admission because test executor identity
  differed from the fixture's credential binding; use actual astrid-pack-host.
- `1020202605-21464`: normal SDK refuses added undeclared file descriptor
  because its explicit [] input_object_ids does not mirror the script input.
- `1020202707-8097`: normal outer submit succeeded; the pinned RemoteTasks
  request reached Runtime and failed the two-edge continuation requirement.
- `1020202818-26978`: public commit-history read on a provider-less empty
  timeline failed history_unavailable before the authority negative. Fixed
  fixture to install the normal provider, bootstrap an actual base pair,
  and compare read-only history plus public head.
- `1020202917-5715`: superseded run cancelled (not qualification evidence).
  Its partial log also showed the real missing-scope response is HTTP 401,
  rather than the probe's guessed 403; final assertion requires exact 401,
  unauthorized, and credential lacks required scope.

A strict expected failure preserves the successful target/script admission
requirement and matches only this precise Runtime continuation rejection via a
test-private exception. Other integration assertion failures remain failures.
The registry metadata requirement is a separate strict positive xfail.

## Next bounded decision for the orchestrator

Resolve the existing Runtime continuation-only admission restriction with its
owner, and authorize the existing command-registry owner to supply the missing
lossless audio/provenance/ripple carrier, or explicitly keep WC5 blocked.
The actual generic task-admission restriction above needs Runtime-owner review;
the settled D13 artifact/authority design is unchanged.
Do not restore a legacy writer or broaden this worker into a new framework.
After a real exact lowering exists, declare the proposal output, implement the
owned producer/session adapter, place the worker authority negative first,
freeze source, then run one real outer settlement -> requester/outbox case on
the exact tuple above. Keep original22 expectations and verified WAV selection.
