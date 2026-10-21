# RT07/D13 original-six current mapping

## Current disposition

No complete exact-current equivalence map exists to reuse. The reviewed Agent
source is `5be2918c45909abcf0c91b79b53a2ce73eed83b1`, tree
`218da96139901ced0a059cdce37146cb7fc314db`; its D13 source/custody review is
approved, but its installed profile preflight is not a native workflow proof.
The staged Runtime cut is `16c32fe7398bcac1e80620451e6d762a95069b90`, tree
`303b4ad095b97aa605d0d80aad27b3c3e9015936`; its `24+13` refusal/retry/
authority controls qualify the cut boundary only. They do not replace native
behavior. All six original positives remain strict RED and unchanged.

The older `runtime-native-render-recovery-original-map.md` is not current
(Agent `3c4f6de4`, Runtime `7d1cfa6b`) and is not reused as qualification.
The only active current-source native workflow IDs are:

- `tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_authoring_proposal_publishes_one_canonical_render_task`
- `tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render`

The latter is the only current test with requester outbox lost-ACK/reopen,
accepted-revision render authority, real render output, and undo assertions.
Neither has passed with the trusted installed Agent source above.

## Six-positive mapping and uncovered equivalence

| Original strict positive | Existing current native mapping | Still uncovered before replacement can pass |
| --- | --- | --- |
| `test_publication_is_fenced_atomic_and_exactly_replayable` | The first native ID covers settled child ordering, native proposal/requester commit, version 2, one ordinary render task, and the committed snapshot. The second covers lost acknowledgement, outbox reopen/exact retry, accepted revision/publication, one render admission, revision-pinned render, decoded output, and undo. | No explicit stale-fence refusal; no changed-payload conflict/no-write assertion; no replay of the same accepted result after author cancellation; no old publication-checkpoint/task identity. Native success is also unqualified on `5be2918c`. |
| `test_prepared_checkpoint_cannot_publish_after_cancel_or_stale_fence` | `test_legacy_assembler_admission_refuses_before_execution_and_keeps_artifacts` proves only the retired-hook refusal and artifact preservation. The two native IDs prove only the successful settle-first path. | No active current native positive proves the old stale-fence and cancel-at-prepare assertions: unchanged film/head, zero render tasks, zero publication checkpoint writes, and the original task's prepared state. The strict-xfail legacy hook is not equivalence. |
| `test_prepared_checkpoint_resumes_on_retried_attempt_after_runtime_restart` | The second native ID partially maps lost ACK, persisted flight, session reopen, exact requester retry, and one render task; the first maps the resulting native render admission. | No Runtime close/reopen after a persisted prepared checkpoint, producer-attempt reclaim, exact resumed publication receipt, or explicit exactly-one checkpoint/render assertion. The current path is accepted native commit recovery, not old prepared-checkpoint recovery. |
| `test_exact_published_checkpoint_replays_before_live_target_changes` | The second native ID pins a new render to the accepted revision. | No retained legacy checkpoint replay after target/head/task/spec cancellation or archival changes; no exact original result/receipt replay, changed-payload refusal, or SQL/CAS/task/history no-write assertion. The staged Runtime read-only replay control is boundary evidence, not native replacement evidence. |
| `test_tracking_is_scoped_to_the_publication_target` | The second native ID records and reuses one `admitted_target` for `main`; the first confirms the native request creates the render task for that target. | No same-project A/B target isolation, no proof that A's head/history remain byte-identical while B succeeds, and no wrong-target substitution refusal/no-write assertion. |
| `test_legacy_head_without_canonical_publication_remains_publishable` | Neither native ID uses a legacy parent head; both bootstrap a fresh canonical timeline and commit through the native producer/requester path. | No equivalent original-film/legacy-head fixture preserving authored content, opaque/media facts, target scope, and retained render behavior. No proof that the original task/checkpoint identity is replaced by a legitimate canonical commit rather than merely using a fresh toy film. |

Consequently, the current map identifies intended native owners but closes none
of the six positives. The missing evidence is an installed, trusted
`5be2918c` native run that supplies the listed target, cancel, fence, exact
retry, original-task/checkpoint, restart, and retained-render assertions; no
Runtime source cut, route/schema change, xfail, refusal-only result, or old
`7012`/ambient run can supply it.
