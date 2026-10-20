# Render producer migration to commands

2026-10-20 source review: Agent `fc324e83`, Runtime `9f9b25c0`, App `2bfde69e`.
PLAN §4.1 and `orch/design/commit-contract.md` govern. **Blocked on operations
and normal host authority/recovery. Keep live producers; hold Runtime 410 and
all M2 integration until the M1 record and migrated producer proof.**

| Source (paths relative to the named repo) | Authored mutation / command equivalent |
| --- | --- |
| Agent `astrid/packs/rendering/actions/assemble_timeline/run.py:309`, `build_authoring_proposal` | Emits files: track `{id:"visual",kind:"visual",label:"Generated visuals"}`; two continuation-derived distinct clip/asset IDs; assets `{media_id,content_sha256,type,duration,origin:"immutable-public"}`; media clips `{id,at,track,clipType,asset,from:0,to:duration}` at 0 and first duration. Requires two distinct succeeded child tasks, ordered primary videos and exact digest/duration. Reused media stays two clips/assets. |
| Agent `astrid/core/execution/generic_host.py:8401`, `_publish_assembled_timeline`, called at `:9632` | Reads the proposal and admitted timeline/document version/render settings; calls `RuntimeProtocolClient.publish_timeline_render:4902` before settlement. Agent manager owns replacement routing. |
| Agent `astrid/packs/video_editing/shared/runtime_orchestration.py:426`, `publish_stitched_render` → rendering `shared/runtime_stitch.py:104`, `publish_authoring_proposal` | Arbitrary config/registry snapshots, attempt fence and expected version; no original command intent or base publication. Exported writer seam, but search finds only definition/export and negative test caller, not a production invocation. Cover before retirement without claiming a live caller. |
| Runtime `runtime_protocol/service.py:7613`, `publish_timeline_render` | Replaces projection Document config/registry (optional slug/name), increments version/emits save event, creates frozen render task and checkpoint. No command recorder or parent command publication. This entire writer must retire after replacement proof. |

**Agent operation handoff:** installed `astrid/sdk/timeline/commands.py:34,52`
supports only move, track.create, inverse and restore. Track creation suffices:
`{schema_version:1,op:"track.create",version:"1",select:"parent",args:{row:<above>}}`
with `capture.py:247` guards. Asset/clip insertion and explicit replacement intent
are absent. Frozen R4 `commands.py` provides reference operations
`timeline.register-asset` (`select:null,args:{asset_id,entry}`, handler `:2607`)
and `timeline.add` (`select:"parent/track:visual",args:{media:<five-field selection>,
at,clip_id,duration,source_range:[0,duration]}`, handler `add_project_media:2692`).
Agent's ordinary registry workers must supply their final versioned equivalents,
preserving IDs, source bounds, fixed non-ripple placement, distinct asset bindings,
opaque/null data and recorded same-value writes. R4 insertion adds hold/intent
metadata and owns registry insertion; do not assume exact equivalence.

Media selection requires `{association_id,object_id,version}` or
`{asset,generation_id,variant_id}` → `{asset,generation_id,variant_id,object_id,
catalog_digest}` (Runtime `timeline_commit_port.py:429,468`). Exact child output
objects alone do not prove registered variant/association authority; preserve
generation settlement and carry exact association/lifecycle pins from resolved
outputs. Confirm continuation asset-key support: selection currently returns a
variant-derived key. No fabricated `media_record`, current-primary lookup or
new DTO. Additive assembly is equivalent only on a guarded empty target;
populated targets/stitch snapshots need explicit source-authored remove/clear/set
operations, with membership/order/dependency guards. No diff-derived intent,
generic replace, historical immutable rewrite or silent append conversion.

**Agent host handoff:** replace the normal hook, not pack execution, with an
explicitly approved/auto-approved proposal returned to the requesting client, whose existing command session submits `commitTimeline`:
`{api_version:1,project_id,timeline_id,base_revision_id,base_publication_id,commands,
source:{via:"python"}}`. Capture the observed head pair before authoring;
`expected_version`/`runtime-current` is insufficient. Persist original guards,
ordered children, IDs, realm/actor, exact request/key before send; reuse
`sdk/timeline/{sync,outbox}.py`. Public session queue is currently move/inverse
only; Agent owns batch/recovery. Worker scopes (`generic_host.py:4412`) lack
**projects:write and tasks:write**, required by commit/task admission. Agent and
Runtime must return the proposal to the REQUESTING CLIENT, which commits with its own authority and original guards through its existing outbox. No existing authorized parent/coordinator was found; do not invent one or grant renderer edits.
The old endpoint atomically rejects cancelled/stale attempts; ordinary commit
has no attempt fence. A preflight lease read cannot preserve that guarantee:
owners must resolve approval/lifecycle semantics before replacement.

**Render after acceptance:** durably retain accepted revision, receipt publication
and pending render before clearing command recovery; `TimelineSession.flush`
currently clears flight without a producer continuation. Existing `admitTask`
accepts `rendering.render`, pinned ready digest and `spec:{family:"rendering.render",
params:{timeline_ref:<ID>,canonical_project_id:<ID>,canonical_parent_document_id:
<timeline ID>,canonical_head_revision_id:<accepted revision>,selector,output_name}}`,
ordinary output policy/storage estimate, empty caller media manifest and
artifact-only settlement. Persist a separate exact admission body/key. Runtime
`store.py:1692,1820` freezes the closure or refuses changed head; never remove
the guard to render latest. The approved additive admission contract must select the explicit immutable accepted revision plus receipt publication/digest; current-head expectation is not a historical selector. Runtime owns the exact negotiated shape and retained-closure resolution. Do not substitute latest or invent inline provenance.
**Runtime permanent regression now proves the defect (d19fd01; repair candidate76f2f95 held):** `store.py:2226` freezes before replay lookup
at `:2295,2341`; render A/lost ACK/new head C/restart/exact retry can fail before
replay. Runtime must prove/reconcile this within the existing task API.

**Proof before cutover:** preserve assembler tests; add original guard/ID/order,
duplicate media, occupied IDs, nonempty target intent, opaque/null, media-race
and guarded undo with later dependencies/ABA
cases. Agent owns renderer-off atomic commit, zero legacy calls, exact retry across
restart and crash after ACK/before admission. Runtime owns stale/cancelled attempts,
refusal/no render, head advance, render lost ACK+restart, one pinned task and
artifact-only settlement. Preserve original publication-chain behaviors and move their positive assertions to the proven command/task replacement before retirement. No new strict xfail or it.fails for lost producer behavior. Keep slow media/CAS work,
task completion/billing and relational metadata. App `renderRouter.ts:960` already
admits tasks with canonical guards; no nongenerated publication caller found.
No product changes or behavior tests ran. Worker checked an incorrect relative orchestration path; the actual absolute QUIET marker existed. Manager observed source-only completion and granted capture only AFTER this worker exited. No capture overlap occurred. Viewing implements the thin proposal only after
Agent supplies operations/host recovery and Runtime proves task replay.

Manager review: branch documentation/report artifacts will NOT merge into product. This ORCH design is the maintained handoff. Source facts reviewed; Runtime retry behavior remains unexecuted, worker-scope limits remain intentional. PLAN decision2026-10-20 supersedes the old parent/coordinator recommendation: producers NEVER commit, requesting clients do. No broad scope grant is proposed.
