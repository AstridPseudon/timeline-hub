# D13/RT07 original-six lifecycle equivalence handoff

Status: **mapping and deferred-work handoff only**. This is not a native proof,
an RT07 readiness decision, a legacy-endpoint cut authorization, or a source-
origin result. The six original Runtime positives remain strict and open.

## Scope and evidence labels

The controlling Runtime map is
`runtime-rt07-original-six-current-map-0910.md`; the latest peer disposition
(`peer-runtime-to-agent-20261021T0916-current-proof-disposition.md`) keeps the
map report-only and requests no duplicate installed/native run. The ordinary
public/current Agent source identity named by that map is Agent
`5be2918c45909abcf0c91b79b53a2ce73eed83b1`, tree
`218da96139901ced0a059cdce37146cb7fc314db`; the held Runtime source is
`16c32fe7398bcac1e80620451e6d762a95069b90`, tree
`303b4ad095b97aa605d0d80aad27b3c3e9015936`. These are source-carrier labels,
not execution evidence. `private017` is a separate cohort and contributes no
mapping credit here.

The two Agent selectors named by the current map are:

- `tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task`
- `tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render`

Important source check: on the ordinary95/public/current Agent source, the
first selector calls `publish_authoring_proposal` at
`tests/packs/video_editing/test_runtime_publication_chain.py:918-922`, and
that carrier calls `tasks.publish_timeline_render` at
`astrid/packs/rendering/shared/runtime_stitch.py:143-170`. It therefore shows
proposal construction and a legacy publication-shaped result, but it is not
evidence of the replacement `/v1` requester path. This discrepancy is recorded
for the orchestrator; this handoff does not alter the settled plan or source.

The second selector is the relevant existing requester carrier:
`tests/packs/video_editing/test_runtime_publication_chain.py:1036-1270`.
Its useful current assertions are the captured target and exact children
(`:1160-1205`), the persisted `producer.guard` (`:1206-1208`), lost-ACK flight
and reopen (`:1209-1224`), accepted revision/publication identities
(`:1224-1228`), revision-pinned render authority and one render task
(`:1230-1266`), and guarded undo (`:1267-1268`). They are partial carriers,
not closure of the six original positives.

## Carrier inventory

| Carrier | Existing source and line range | What it can carry into a later normal installed proof |
| --- | --- | --- |
| proposal builder | `astrid/packs/rendering/actions/assemble_timeline/run.py:309-413` | deterministic two-child order, fenced dependency-edge membership, exact media identity, authored timeline/registry, Runtime-owned publication declaration |
| captured native proposal | `astrid/packs/rendering/actions/assemble_timeline/run.py:430-489`; `astrid/sdk/timeline/native_parent_media_commands.py:55-84` | admitted target, exact ordered association/media selections, producer identity, `producer.guard` plus the original proposal commands/digest |
| admission capture | `astrid/sdk/timeline/assembly.py:45-89`; `astrid/sdk/timeline/sync.py:211-254`; `astrid/core/contracts/runtime_orchestration.py:94-156` | one immutable base target, child association/version pins, ordered CAS inputs, dependency fences, proposal output declaration |
| settled-proposal requester | `astrid/sdk/timeline/assembly.py:92-167`; `astrid/sdk/timeline/sync.py:256-279`; `astrid/sdk/timeline/producer.py:47-62` | Runtime task/attempt/output provenance, exact proposal bytes, producer guard, original accepted base and rationale |
| commit/outbox handoff | `astrid/sdk/timeline/sync.py:375-389,417-491,493-513` | exact request flight, immutable retry key/body, `/v1` commit, accepted revision and receipt/publication identity, guarded inverse |
| Runtime producer capture | Runtime `16c` `runtime_protocol/timeline_commit_producer.py:224-284` | verifies project/target, task and current attempt fence, settled artifact, proposal digest, request guard, and capture identity |
| accepted-receipt/checkpoint handoff | Runtime `16c` `runtime_protocol/timeline_commit_producer_checkpoint.py:58-92,95-126,129-163` | binds accepted receipt to revision/content digest, prepares one producer checkpoint, validates immutable render intent, and links the task-admission receipt |
| retired-route boundary | Runtime `16c` `runtime_protocol/service.py:7534-7640` | refusal of fresh/prepared legacy writes and read-only exact replay of an already published checkpoint; it is not native-success evidence |

## Exact original-six mapping and remaining assertions

The “existing mapping” column names only the current carriers above. “Still
uncovered” is the assertion that must be visible in the same ordinary installed
fixture before the corresponding original positive can be considered
equivalent. No refusal-only control, fresh toy timeline, or historical replay
closes an item.

| Original Runtime test id | Existing current carrier | Still-uncovered success assertions |
| --- | --- | --- |
| `tests/test_timeline_render_publication.py::test_publication_is_fenced_atomic_and_exactly_replayable` (`103-131`) | Native installed host test captures a proposal/guard, sends one `/v1` commit, observes an accepted revision/publication, admits one revision-pinned render, and undoes it (`test_runtime_publication_chain.py:1197-1268`). Runtime’s accepted-receipt checkpoint helper is `timeline_commit_producer_checkpoint.py:58-92`. | In the native path, explicitly assert stale-fence refusal before any acceptance, changed-payload conflict with unchanged SQLite/CAS/task/history, exact replay of the accepted receipt after author cancellation, and one accepted publication/checkpoint plus one render admission. The first selector’s legacy carrier cannot supply these. |
| `tests/test_timeline_render_publication.py::test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence` (`134-157`) | Native capture stores `admitted_target` and fences (`assembly.py:45-89`; `sync.py:211-254`); the Runtime cut refuses fresh/prepared legacy publication (`service.py:7601-7640`). | A normal installed native run still needs the original cancellation-at-prepare and stale-fence assertions: unchanged authored head/content, no accepted revision, no render task, no new publication checkpoint, no CAS/history write, and the original prepared state left observable. Retired-route refusal is not the equivalent success assertion. |
| `tests/test_timeline_render_publication.py::test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart` (`160-194`) | Installed host test proves a lost commit acknowledgement, durable outbox flight, session reopen, exact commit retry, accepted identities, and cleared flight (`test_runtime_publication_chain.py:1209-1228`; `sync.py:417-491`). | It does not prove close/reopen with a persisted **prepared producer checkpoint**, producer-attempt reclaim under a new live fence, exact resumed publication receipt, and exactly one checkpoint/render admission. Add those observations around the existing installed fixture; do not substitute ordinary commit retry for prepared-checkpoint recovery. |
| `tests/test_timeline_render_publication_authority.py::test_exact_published_checkpoint_replays_before_live_target_changes` (`115-129`) | Runtime `service.py:7601-7618` retains read-only replay of an already published checkpoint; `timeline_commit_producer_checkpoint.py:95-126` validates accepted render identity. | The native installed path still lacks an accepted-receipt handoff followed by cancellation/head movement/spec removal/archival, exact result replay, changed-payload refusal, and byte-for-byte SQL/CAS/staging/task/history no-write checks. The staged read-only Runtime control is boundary evidence, not native replacement evidence. |
| `tests/test_timeline_render_publication_authority.py::test_tracking_is_scoped_to_the_publication_target` (`132-140`) | Capture and proposal preserve one `admitted_target` (`assembly.py:84-89`; `run.py:430-489`); the installed host test reuses one target and checks render authority (`test_runtime_publication_chain.py:1170-1178,1230-1266`). | Add same-project A/B target isolation: B succeeds, A’s head/history/content closure remains byte-identical, and a wrong-target substitution is refused before writes. The current single `main` target does not prove scope isolation. |
| `tests/test_timeline_render_publication_authority.py::test_legacy_head_without_canonical_publication_remains_publishable` (`142-150`) | Existing native fixture creates a fresh canonical timeline and captures its base pair (`test_runtime_publication_chain.py:1080-1082,1160-1175`; `assembly.py:84-89`). | Add the original-film/legacy-parent fixture while retaining authored config, registry, opaque/media facts, target identity, and the accepted native render/undo outcome. It must show a legitimate canonical commit replaces the legacy head; a fresh toy film does not establish that equivalence. |

## Smallest deferred additions after security approval

No product or test edit is made by this handoff. After the independent
source-origin/security approval for the ordinary public/current install, keep
the existing `installed_runtime` fixture and the second selector as the single
normal installed carrier. Add only the following assertion blocks (or
equivalent named subcases) around its existing captured project/target and
outbox state; preserve every original positive assertion and outcome:

1. **Cancel/fence:** capture pre-state, exercise cancellation and a stale
   attempt fence at the native admission/commit boundary, then assert visible
   refusal and zero accepted revision/checkpoint/render/CAS/history writes.
2. **Prepared restart:** force the existing Runtime producer checkpoint after
   acceptance has supplied its receipt, close/reopen Runtime, reclaim the
   author attempt, and retry the original handoff with the new live fence;
   assert the same receipt/result and exactly one checkpoint/render admission.
3. **Accepted handoff/replay:** retain the accepted revision/publication and
   render selector, mutate only live cancellation/head/spec/archive state,
   replay the exact handoff, then submit a changed payload; assert exact replay,
   conflict for changed payload, and unchanged SQLite/CAS/staging/task/history.
4. **Target scope:** create same-project timelines A and B using the existing
   service/client helpers, publish B through the native carrier, compare A’s
   head/history/closure before and after, and attempt one wrong-target capture;
   assert refusal and no writes.
5. **Legacy-head:** seed the original legacy-parent shape through the existing
   Runtime fixture seam, retain authored/opaque/media bytes, then run the same
   native proposal/requester path and assert accepted revision, render authority,
   and undo. Do not seed a fake accepted checkpoint or replace the original
   source/outcome with a refusal expectation.

The proposed future selectors are deferred and are not present today:

```text
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_native_cancel_and_stale_fence_are_no_write
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_native_prepared_checkpoint_restarts_and_resumes
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_native_accepted_receipt_replays_after_live_changes
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_native_target_scope_isolated
tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_native_legacy_head_preserves_original_film
```

These names are a selector/preflight plan, not claims that tests already exist.
The first existing selector remains useful only after its call is migrated to
the native requester; until then, do not count it as `/v1` lifecycle evidence.

## Deferred preflight and limits

Before any later named run, verify the existing offline selector
`test_d13_installed_native_preflight` (`test_runtime_publication_chain.py:663-668`)
against the normal public/current installed profile and the exact eight origin
keys. Then independently verify the security-approved source/profile tuple,
Runtime `16c` compatibility, ordinary public inputs, credentials, and the
existing native test collection. No private017 paths, ambient checkout/PYTHONPATH
authority, source-origin repair implementation, pin/schema/client change,
launcher/HTTP/pack-host/render/build work, or old7012 replay belongs in this
mapping.

The preflight is only a gate for a later run. It is not a lifecycle result. A
later successful run must report each of the six original selectors and the
assertions above separately; it must not collapse them into “native positive
passed,” and it must not claim RT07 readiness until Runtime’s own coordinated
cut review accepts the complete map.
