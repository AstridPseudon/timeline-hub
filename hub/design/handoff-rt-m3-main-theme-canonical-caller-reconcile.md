# Main Theme caller reconciliation

## CORRECTED disposition — 2026-10-21

**No Runtime product change or new acceptance exception is authorized.** The
ordinary Main caller is the imported-file path, not the raw probe used by
68465ef:

`media.import_file(theme.json)` -> project CAS descriptor -> `sdk.invoke("rendering.render", inputs={timeline, theme, selector})` -> `spec.inputs.theme` -> existing named-input admission -> `theme.json` -> the one Theme resolver -> `props.theme`.

Runtime source `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` (tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`) preserves that ordinary carrier;
Runtime `origin/main` preserves the same boundary. Main infrastructure
touched for this investigation: **NONE**.

The exact source names are `astrid/sdk/remote.py` (`import_file`),
`astrid/sdk/invocation.py` (`_validate_render_input_mode`,
`_prepare_managed_render_inputs`, `_kernel_invoke`),
`astrid/core/execution/generic_host.py` (`_materialize_inputs`),
`astrid/packs/rendering/shared/rendering_backend/__init__.py`
(`_resolved_theme_for_render`), Runtime
`runtime_protocol/store.py` (`_freeze_managed_render_inputs`), and App
`src/tools/video-editor/hooks/useRenderState.ts` /
`src/tools/video-editor/lib/renderRouter.ts`. Current SDK `6efc8150` builds
`spec.inputs`; App `860d43b3` Main and integration both use the raw
`params.timeline_ref` caller and omit Theme.

The ordinary proof is limited to named project-CAS input retention,
materialization, and existing resolver input shape. It is not canonical
managed-reference acceptance or physical frame/render parity. Physical Theme
parity remains Viewing-owned and open.

The raw 68465ef fixture is historical red evidence only: it constructs
`spec.params.timeline_ref`, supplies `input_object_ids=[theme]` while omitting
the canonical media/snapshot closure, and expects `[theme, package, entry,
audio]` even though Runtime95bd derives `[audio, package, entry]`. It is not a
current SDK fixture. Preserve its red positive and the passing foreign/tamper
negative; do not merge or xfail that invalid new fixture.

Peers must provide an actual normal caller, with its complete descriptor and
existing canonical order, before proposing any new canonical Theme exception.
No private preparation, ThemeDocument, namespace pin, new protocol,
arbitrary-extra widening, alias/default substitution, or source-certification
fallback is in scope.

Branch `68465ef` and these four stopped dependent branches are **ABANDONED**:
`tl/rt-m3-main-theme-final-source-consumer-handoff`,
`tl/rt-m3-main-theme-final-source-custody-r2`,
`tl/rt-m3-main-theme-one-failed-positive-final`, and
`tl/rt-m3-main-theme-retry-atomic-gate2`. They are not integrated branches,
public test deletions, or gate passes.

Result: **bounded caller/acceptance handoff; no Runtime product change**. The two results exercise different entrypoints. The committed red node is a real raw-reference refusal, but its description as an actual current canonical SDK positive is incorrect. No Runtime gap is dismissed on the strength of the unrelated ordinary green proof. No physical parity or canonical explicit-Theme qualification is claimed.

## Exact sources

| Source | Commit | Tree |
| --- | --- | --- |
| Runtime worktree/base | 95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c | d3a290b407fa61e6ab2d476f50c068073f70df00 |
| Runtime upstream Main | b535646faaad2f8ae7968dfe0f4fa3057f960264 | read through origin/main |
| Agent normal client | 6efc81500a0e0688c2bb41e736503f0fc3e04abb | 2ed2b8a12b5b3391ca221ba6ff05390f71a73556 |
| Agent current integration | 4467c1c1a9ed81fa7cd1b2d7687b8ada54dc216a | 5997f0162374dcfb56597b636caaad597c951b68 |
| Agent upstream Main | 497714c73531f164082555ec81b61ca5bc8b6554 | read through origin/main |
| App current integration | 692765846fef511047445fecef3e55ec8bb6a5bf | e615c0a3aafca34504ba3544560de3887e4de38d |
| App upstream Main | 860d43b3 (origin/main) | read through origin/main |
| Red regression branch | 68465ef2499f6803c0f9e856480616361d746d46 | test-only successor of Runtime95bd |

Runtime worktree remains clean and byte-identical to95bd. All76/generated/schema/client bytes are untouched;95bd remains immutable. Reports and peer notes are outside the repo under this absolute shared ORCH/design directory.

## One real Main invocation and today's same route

The Main user example is Agent rendering/actions/render/STAGE.md's “With a custom theme and strict qualified renderer” example: import authored timeline JSON and authored theme.json with client.media.import_file, then sdk.invoke("rendering.render", project="demo", inputs={"timeline": timeline_descriptor, "theme": theme_descriptor, "selector": "rendering.remotion"}, client=client). This is ordinary FILE mode, not the CLI's separately documented managed timeline-ref mode.

Current Agent and normal6ef retain that path:

1. sdk/remote.py:1543 import_file submits the authored bytes to project CAS and returns the managed identity (upstream line1615).
2. sdk/invocation.py:982 _validate_render_input_mode chooses file mode when timeline is present. It rejects simultaneous timeline_ref, rather than silently migrating file input.
3. _prepare_managed_render_inputs:1221-1240 validates the existing descriptors, removes timeline_ref, and returns (values, None) BEFORE scope resolution or canonical snapshot preparation.
4. _kernel_invoke:2539-2544 stores prepared request values in spec.inputs. Lines2633-2659 authorize declared file ports in sorted order (theme then timeline) and record input_digests.
5. RemoteTasks.prepare_admission -> remote._prepare_execution_admission:254-339 -> WorkspaceClient.prepare_task_admission:889-966 keeps that spec.inputs shape. Targeted execution requests merge/check their descriptors and exact ordered manifest; none of these functions converts a render's inputs to params. The spec.inputs-to-params conversion in invocation.py:2617 is exclusively generation.generate_image_codex.
6. RuntimeService.create_task:5682 preserves the inner spec. RealmStore._freeze_managed_render_inputs:1753-1759 returns immediately unless spec.params contains timeline_ref. Ordinary admission keeps the supplied managed file list and project checks.
7. GenericPackHost._materialize_inputs:6888-6904 requires an admitted CAS identity, fetches/hash-checks it and writes theme.json. rendering_backend._resolved_theme_for_render:89-123 is the ONE semantic resolver, merging authored overrides; Remotion gets props.theme. Explicit invalid input must refuse, never default.

Therefore the ordinary green proof corresponds to the documented explicit-file user workflow, although that report's RuntimeService-only probe is not itself end-to-end SDK/renderer proof. No new SDK invocation or renderer test was run here.

## Where timeline_ref actually enters

There is **no integration migration hunk changing the above Main file invocation into params.timeline_ref** in the inspected sources. This premise of the task is not established by the supplied evidence.

- For the separate SDK managed workflow, inputs.timeline_ref is supplied by the user/CLI or set by _prepare_managed_render_inputs:1253/1277 after canonical scope/default resolution. Those branches already exist in origin/main. SDK preparation places its snapshot, authority and named file descriptors under spec.inputs, then appends prepared registry media and snapshot identities to its manifest. It does not enter the raw params-only freeze seam.
- The actual raw App caller is useRenderState.startAstridRender:853-935 -> renderRouter.enqueueAstridRuntimeRenderTimeline:940-975. The exact wire hunk is input_object_ids: [] at957 and spec.params.timeline_ref: payload.timeline_id at961. It forwards neither inputs.theme nor payload.theme_id. The same hunk exists in App origin/main860d43b3. Current renderRouter.ts differs from Main only in comments; useRenderState's integration changes affect command projection, transitions and extent, not this admission route.
- A theme_id slug/browser-resolved Theme is not imported-object authority. The App raw path's missing forwarding is a separate, pre-existing limitation; it cannot be relabelled as a newly broken Main explicit-file path.

SDK capture certification remains separate: invocation.py:2882-2896 retains candidate-forwarding and CAS/UNCERTIFIED behavior. Runtime capture_validation.validate_capture continues to verify saved/candidate projection. Routing arbitrary file mode through a canonical label would bypass that distinction and is not proposed.

## Why the unchanged red node cannot authorize a Runtime patch

Regression68465ef's _managed_theme_request calls test_canonical_render_admission._request, which constructs spec.params.timeline_ref and input_object_ids: []. It then replaces only that list with [theme_object_id] and adds spec.inputs.theme/input_digests. It never invokes the current SDK/RemoteTasks and never supplies an execution_request.

The existing Runtime exact-list rule is unchanged from Runtime origin/main: a nonempty supplied list must equal the complete derived film list. This probe supplies only Theme, omitting every canonical media object. The failure is therefore expected under the present raw-reference contract; it is not evidence that the SDK's complete named-file manifest was rejected.

A second independent source inconsistency exists beyond the first red assertion: the test expects [theme, package, entry, audio, snapshot]. Runtime95bd derives [audio, package, entry]: expanded registry assets are appended at store.py:2042-2096, then _freeze_prepared_scene_objects appends package and entry at1690-1692. The test fixture has one registry music asset and two scene clips. Passing the unchanged test would require either reordering canonical film media or changing the test expectation, both outside this brief. No test was edited or weakened; its original negative remains retained.

## Owning handoff / bounded next decision

Decision: retain the working Main imported timeline+theme route and do not
widen Runtime from this raw probe. Agent owns a genuine SDK regression
witness if that actual route fails. Viewing owns physical Theme parity and the
existing resolver/props consumer. App owns the precise raw request hunk above;
a slug must never be used as a replacement descriptor.

No such raw managed-reference exception is proposed here. Before any future
acceptance discussion, peers must identify a live caller with an already
imported descriptor and reconcile the omitted closure and asserted order. The
old conditional seam was not an implementation authorization and must not be
treated as a repair plan.

Scope findings and this decision were sent through flat design/peer-runtime-to-{runtime,agent,app,viewing}-main-theme-caller-reconcile-decision.md (hub-sync's normal peer delivery). The earlier custody review is retained as historical evidence and superseded on its current-SDK-fixture premise; it is not being re-reviewed. No cross-area ACK for a Runtime change was observed at report time.

## Validation and limits

Source inspection commands included:

- git show tl/rt-m3-main-explicit-theme-normal-regression:tests/test_timeline_explicit_theme_main_preservation.py — inspected unchanged committed positive/negative and helper.
- git -C /home/user/work/agent show 6efc8150:astrid/sdk/invocation.py and :astrid/sdk/remote.py — confirmed normal-client shape and file-mode behavior.
- git -C /home/user/work/agent diff origin/main 6efc8150 -- astrid/sdk/invocation.py — no file-to-managed routing migration; candidate/verified-source changes remain distinct.
- git -C /home/user/work/app diff origin/main HEAD -- src/tools/video-editor/lib/renderRouter.ts src/tools/video-editor/hooks/useRenderState.ts — no admission-route migration hunk.
- git diff origin/main 95bd3c5 -- runtime_protocol/store.py — exact supplied canonical-list comparison is inherited from Main.
- git diff --check; git status --porcelain — run at completion; no diff/working-tree changes.

**No pytest/test-service request or rerun was made.** No committed reviewed product fix exists, so the instruction to rerun ONLY the failed node once after such a fix is not triggered. Prior regression evidence remains exactly 1 passed / 1 failed with the positive red and foreign/tamper negative green. No full/default-five/old28/browser/socket/renderer/MP4 suite, dependency write, artifact generation or physical-parity claim.
