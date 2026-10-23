# R2 parent-media diagnosis (READONLY)

Date: 2026-10-23  
Worker: `agt-R2-parent-media-diagnosis-1740`  
Agent base: `079580ca46af77e0292d49dc34386b25c8391f99`  
Runtime reference inspected: `d9e2a71e87c827290a3ff58a94f6fb8b4bc11e0b`  
Scope: PLAN §3 R2/G4/G5/C0; diagnosis only.

## Flat verdict

The 14 failures are two distinct Agent-owned inverse problems exposed by the existing source-backed parent-media recipe. They are not evidence of one shared Runtime cause, and they do not justify a product patch, a contract change, a fixture-body change, or a guard waiver.

* Six `missing_registry_containers_are_guarded_writes_with_exact_inverse_redo` nodes fail in Agent inverse landing-guard/coalescing after the document round trip. The forward record contains the registry-container write and the child asset/clip writes, but the inverse guard compares the container's authored empty `after` image with a reloaded state in which the child asset is present. The failure is `original authored guard changed` before the inverse mutation. This is a genuine Agent inverse/materialized-registry defect in the existing source, not proof of an old mixed-envelope fixture.
* Eight exact/ordered provider nodes fail in Agent nested inverse-stage selection before the detached provider can return a Runtime acceptance. The failing check is `nested inverse ranges differ from accepted history`; current `_step_undo.py` rejects the nested inverse shape when `derived_writes` is present. The parent mirror write must not be dropped or flattened. The repair seam is Agent record/stage materialization and effect-range attribution, not Runtime authority.

The disjoint legacy restoration baseline `d1d41c4056f509ce24af916ee20b7b683ac8f8f1` does not make these failures an old missing-v2 envelope: the parent-media recipe, `_step_undo.py`, and `_recording.py` are byte-identical to the current source, and the relevant inverse difference is occurrence aggregate physical mapping rather than parent-media registry handling. This comparison shows a real pre-existing Agent source defect that the current existing fixture exposes; it does not establish that `d1d` ever passed these cases. No current-source change was made.

## Exact failure nodes and ownership

| Node family | Exact nodes | Observed boundary | Exact failure | Owner / fix seam |
|---|---|---|---|---|
| Registry-container reload | `absent-image`, `absent-video`, `direct-image`, `direct-video`, `mirrored-image`, `mirrored-video` | Pure Agent `execute` through `test_recipe_m1_commands.inverse`; no Runtime/public API | `_recording.py:286`: `original authored guard changed`; current `inverse.py:736` rejects the guard for the materialized registry path | Agent R2 inverse coalescing/ancestor landing guard (`inverse.py:202-282, 724-737`), preserving child/ancestor write order and exact guards |
| Exact provider reload | `test_provider_exact_reload_inverse_redo_and_retired_ids[False]`, `[True]` | Detached `MediaRealm` provider path; failure occurs in Agent before detached port acceptance | `_step_undo.py:169`: `nested inverse ranges differ from accepted history` | Agent R2 nested inverse stage/history-record materialization (`_step_undo.py:129-181`, with effect attribution in `_commit_patch.py:470-588`) |
| Ordered provider reload | `A-image`, `A-video`, `target-image`, `target-video`, `C-image`, `C-video` | Same detached `MediaRealm` path; failure occurs in Agent before Runtime | `_step_undo.py:169`: `nested inverse ranges differ from accepted history` | Same Agent nested inverse stage/effect-range seam; ordered target identity must remain authenticated |

The first family is six nodes. The latter two rows are eight nodes total. No node was rerun through the known failing live body.

## Retained original trace and loss boundary

The retained A4 worker log contains the complete pytest node IDs, traceback locations, parameter values, and failure messages. It is at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-A4-provider-map-1732/log.txt`

The retained A4 report and source map are at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-A4-provider-map-1732.md`

The exact original request body, Runtime/public request receipt, generated publication/head IDs, private accepted-history proof, and a serialized full prepared v2 packet were not retained in the worker log. They are **LOST**, not reconstructed below. The fixture helper and direct engine output provide source facts, but are not substituted for a Runtime receipt or accepted-history record.

The six registry failures are source-backed direct Agent execution. The eight provider failures use `MediaRealm` in `tests/editing_conformance/test_recipe_occurrence_media.py:250-266`, an in-memory detached realm that calls `create_runtime_commit_service().commit(context, MediaPort(...))`. This is a detached fixture/provider boundary, not proof that a mounted public Runtime API accepted the failing redo. The A4 source map separately identifies the mounted parent-media caller: App `commitSession` reaches registered Agent `clip.add-media`, whose native handler is `native_parent_media_commands.py:25-52,87-94`.

## Bounded reconstructed packet

Label: `RECONSTRUCTED-OFFLINE`; source: existing test fixtures and deterministic Agent command engine; authority: Agent source only; Runtime/public body: not used.

This packet is intentionally bounded. Fields marked `unknown/lost` are not recoverable from the retained trace and are not invented.

### Request and command facts

* Project/timeline/base revision/base publication: fixture context supplies the project/timeline and the direct engine's source document; exact original C0 values and generated base IDs are not retained.
* Commands for the add path: registered `clip.add-media`, with image/video parameterization. The source fixture uses the `parent` clip, `asset:reserved-new`, `clip:born`, and the media selection pin; the video case has the captured/replaced media variants described by the parameter. Exact original serialized request body is lost.
* Replacement path command order is source-observed as `timeline.assembled-target`, `clip.add-media`, then `clip.delete`, with target parameterization `A` or `C`; exact accepted command tuple and generated IDs are not retained.
* Label, merge mode, declared reads, idempotency key, `dry_run`, source, rationale, and `group_id`: not retained in the original packet. No values are inferred from defaults.
* The direct deterministic engine produced the following source facts for the add path: two primary forward writes (asset and clip) plus one `derived_writes` parent/config/clips mirror. The replacement path produced command ordinals 0/1/2; the add and delete records each carried their own primary/derived write shapes. The direct legacy helper has no serialized accepted v2 step list, so it cannot establish the missing Runtime `steps[].patch`, `steps[].reads`, or effect ranges.

### History, prepared, native, effect, and physical facts

* Source history for the detached path is the `MediaRealm` in-memory history and its accepted command records. Exact history/publication IDs, ordinals after service hydration, receipt IDs, and private proof fields are not retained; no compact history is invented.
* Forward writes include the parent registry/container creation and the child asset/clip writes. On reload, the container's physical/canonical image contains the child asset. The inverse record still carries the authored empty-container `after` image, which is why the landing guard rejects it. The test's empty-container guard expectation is preserved; it must not be weakened.
* The inverse record for the provider shape carries `derived_writes` for the parent mirror. Current `_step_undo.py:168-169` treats that shape as incompatible with the nested range path. This is an observed source condition, not permission to omit the derived write.
* Native/effect ranges, private inverse-stage proof, physical revision/digest pins, and complete owner/boundary bindings are unavailable in the retained original packet. The only source-observed owner/path facts are the parent registry/asset/clip identities and the parent/config/clips mirror. No occurrence root, successor, revision, or digest is fabricated.
* Failure occurs before the inverse mutation in both families: the registry path raises during guard validation; the provider path raises during Agent inverse-stage validation before detached provider acceptance. This supports a no-write boundary classification, but is not a substitute for a serialized no-write receipt. The provider redo's original no-write/identity-collision assertions are not treated as passed after this earlier failure.

### C0 field audit

| C0 area | Status in this diagnosis |
|---|---|
| `api_version`, project, timeline, base pair | Shape known from Runtime d9e contract; exact original values lost |
| commands, label, full steps, patch, reads, merge, declared reads, key, `dry_run`, source, rationale, `group_id` | Command identities/ordering are source-observed; full serialized values are lost or only fixture-derived; no values invented |
| accepted/merged status, canonical, receipt, full records, bindings, effects, deps, history, `undo_steps` | Not an accepted Runtime packet for these failures; direct Agent records and detached fixture history are partial source evidence only |
| preview `would_status` | Not run/recovered |
| structured failure code/path/head/hint/suggested command | Agent codes/paths observed: `original authored guard changed` and `nested inverse ranges differ from accepted history`; Runtime structured reply fields are not recovered |

Runtime d9e2's nested authority remains strict: one outward actual immediate identity with inherited partitions, authenticated source publication/step IDs, contiguous native/effect ranges, and physical bindings. Nothing in this diagnosis waives, flattens, drops, or reassigns those requirements. If Agent later produces a candidate, Runtime must independently validate it.

## Deterministic offline evidence

Only reconstruction was run after the retained failure. It used the existing fixture source and direct Agent command engine, not a live provider/public body. The eight source shapes were exercised for forward serialization/document round trip and record inspection; the known failing provider body was not rerun.

For the six registry shapes, forward records consistently contained the expected container write followed by `asset:reserved-new` and `clip:born` writes. After document round trip, the reloaded parent registry path contained the child asset, while the authored container write still had the empty-container after-image. That is the concrete state mismatch behind the guard failure.

For the provider shapes, the direct pure engine confirmed the relevant record shape: add has two primary writes plus one parent/config/clips `derived_writes`; replacement has the ordered assembled-target/add/delete records and derived parent mirror writes. A second direct pure inverse is not an accepted-history replay and fails with `inverse insertion order needs an accepted boundary`; this is not substituted for the retained provider error. The retained provider traceback remains the authority for the eight-node classification.

## Legacy comparison and source hashes

The following blob identities were checked against current `079580...` and the A4 `6531622c8f198c3efb509217e303fcad0126c47b` source:

```text
astrid/sdk/timeline/inverse.py                         5567e57d3b60e8002faa4e261b5a23407206a5f0
astrid/sdk/timeline/_step_undo.py                      505fe243fc2188b702245f037dfdabcd3d88ad1a
astrid/sdk/timeline/_recording.py                      10b17db43964ed0016e3d0527910bc9e56ccaf4f
tests/editing_conformance/test_recipe_m2_parent_media.py
                                                         6052a414c1c09d819e27de8d65d493ca9d1ba060
astrid/sdk/timeline/_commit_patch.py                   b91222b9c933b7107a334d153b68ca2f44d2b944
astrid/sdk/timeline/commit.py                          86be6ff6e7c79621335f880fa22587820cf09672
astrid/sdk/timeline/native_parent_media_commands.py    433f94a1b3a4f1a5f9bd2aa5c4fa5d344231a557
tests/editing_conformance/test_recipe_occurrence_media.py
                                                         072b777aa723d73527ac56e9a4877553ca9f3615
```

The d1d inverse blob is `c649182d0e45630ffd3c329a9547bd3cf97068db`; its `_step_undo.py`, `_recording.py`, and parent-media recipe blobs match current. Therefore the legacy comparison does not support “old fixture mixed envelope missing full v2” as the cause. It supports “existing Agent inverse source defect exposed by current source-backed test.”

Retained artifact hashes:

```text
8bd1bdb6b084ebe8aaf2e2cdded016edff9657ed7198c6dc9a46fd186d2ccddb  A4 worker log
53ab09d48ad91ef32fa4d3b00ac350fc59ac1688a110faf466930713cb023d58  A4 provider-map report
```

Credential scan of this report and the retained A4 report/log found no matches for common AWS access keys, private-key blocks, Slack tokens, GitHub tokens, or OpenAI-style secret prefixes. No credentials were copied into the packet.

## Exact next meaningful regression

1. Agent R2 owner should repair the six-node registry landing/coalescing seam so the authenticated ancestor/container and child writes have a valid sequential inverse guard after reload. Keep the existing empty-container negative guard and exact behavior test unchanged. The first regression is the six parameterizations in `test_recipe_m2_parent_media.py` only.
2. Agent R2 owner should repair the eight-node nested inverse stage/effect-range materialization seam so `derived_writes` remain represented and authenticated ranges cover the actual native/effect images. Do not delete the parent mirror, flatten nested history, or manufacture ordinals. The first regression is the exact/ordered provider parameterizations, followed by the relevant `_step_undo`/provider targeted neighbors.
3. Only after Agent emits a complete authenticated candidate should Runtime d9e2 be exercised. Runtime is not the current failure boundary. R1 remains the owner of `commit.py` hydration/`_commit_patch`; this diagnosis makes no overlapping code change.

Strict controls for the next run: preserve all guards and expected behavior; no `xfail`, skip, or assertion change; no new schema/client tuple/pin/fixture body; no history compaction; no dropped bindings/native writes; no public API conclusion from detached fixtures; and no full suite until the targeted Agent evidence is green.

## Commands and results

The retained A4 worker ran:

```text
PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest --collect-only -q tests/editing_conformance/test_doc_patch_v2.py tests/editing_conformance/test_recipe_m2_parent_media.py
187 collected in 1.55s

PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_doc_patch_v2.py
102 passed in 11.81s

PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_parent_media.py --maxfail=20
71 passed, 14 failed in 26.64s

PYTHONPATH=/home/user/work/wt/agt-A4-provider-map-1732:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_commit_provider.py -k 'retained_input_closure_survives_document_overwrite_and_new_provider or missing_or_malformed_transcript_source_is_refused'
9 passed, 105 deselected in 2.17s
```

I did not rerun the 14 known failing live nodes, request a full/original suite, run browser/live-socket coverage, modify source/tests, or perform Runtime/public acceptance. This report and its bounded reconstruction are the only task outputs.

