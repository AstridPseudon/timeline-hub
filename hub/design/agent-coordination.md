# Agent M0 coordination

Agent semantic contract/design workers are running: agt-m0-recipe (EditCommand/provider/rebase/inverse + executable hard cases), agt-m0-ext (existing pack seams + M5 criteria), agt-m0-spike (disposable real R4 overlay + file-by-file port manifest). Environment baseline agt-m0-env waits for a heavy slot.

Drafts will be published to edit-recipe.md and extensions.md. App and Viewing review are needed before Checkpoint A; Runtime commit-contract.md is an input to the recipe worker. I will reconcile wire fields/provider signatures and revision identity before marking M0 complete. No semantic design is approved yet.

The shared env /home/user/work/venv-agent is dependencies-only; all worker code must be selected with PYTHONPATH. Agent environment worker installs Remotion dependencies only in its own worktree to avoid colliding with Viewing-owned integration paths. Existing assets/music/fades/transitions playback stay required. Spike branch is experimental and will not be merged.

## M0 completion follow-ups (2026-10-19 17:59 UTC)

Agent agt-m0-suffix-basis was dispatched at 17:53:36 to write suffix-basis.md; Runtime review now says rt-m0-suffix-basis is independently writing the same path. Both results are design-only. Preserve both outputs as suffix-basis-agent.md and suffix-basis-runtime.md before integrating the shared suffix-basis.md; no extra wire field is approved implicitly. Agent will snapshot its worker output/report when available and reconcile with Runtime.

agt-m0-command-schema supplements the recipe schema with exact inverse/restore examples and schema validation. Recipe worker has now also created schemas/change-contract/edit-command.schema.json in its branch. Review both as one authoritative canonical artifact before delivery; do not install two competing schemas. Future packaged artifact may live in core/timeline/schema to use current package-data rules, or existing schemas/change-contract plus explicit packaging; final choice pending evidence. Runtime's initial slim ABI 1 is accepted by Agent given absence of any main ABI and the new contract digest; recipe's old v2 wording must be corrected.

agt-m0-spike committed 8003c8dd and remains intentionally NOT FOR MERGE. Follow-up agt-m0-port-audit will separate experiment status from forward-port recommendations and enumerate every failed/error node with a/b/c taxonomy using now-ready shared env.

## Superseding suffix decision adopted (18:03 UTC)

Orchestrator's PLAN/INBOX decision supersedes Agent's optional base_view proposal: no new DTO field. agt-m0-suffix-conformance is running the mandated A5/B absolute7 or relative+2/C/read-selection/retry/reload/created-ID tests using original value+identity guards. Equal-state ABA is intentionally allowed for suffix handoff; publication inverse retains its separate PLAN ABA guards. suffix-basis-agent.md is historical proposal only, not final requirements; shared suffix-basis.md will be rewritten around the decision. No further contract escalation absent executable visible-film error.

agt-m0-recipe completed 03d05130: actual frozen-source + main fixture observations 14 passed (157.21s); forward overlay 9 cases fail missing CheckAdmissionContext, precisely documented as a required validation adaptation. Manager is reviewing schema supplement to choose one artifact, not installing both sources.

## Agent wire/schema confirmation (18:10 UTC)

Canonical M0 schema is design/edit-command.schema.json with `$id=https://astrid.local/schemas/timeline/edit-command.schema.json`; future packaged authority astrid/core/timeline/schema/edit-command.schema.json; Runtime byte-identical projection contract/schemas/edit-command.json. Exact copy/equality/generated export checks and all semantic leaves are in command-schema-handoff.md. Supplement reviewed independently: **95 tests passed**. The recipe's earlier branch schema is retired as a source.

Inverse: op timeline.inverse, schema_version:1, operation version:"1", select:null, args:{publications:[receipt,...]} oldest-to-newest explicit unique accepted targets; guards/expanded inverse come from Runtime history, never supplied writes. Restore: timeline.restore version:"1", select:null, args:{revision_id,content_digest}; sole command and strict request head-pair guard/no semantic rebase. Initial slim ABI1/factory/provider_id, frozen Runtime §4.1 DTOs, bootstrap/baseline fail-closed rules and rationale are accepted by Agent. Minimal numeric clip.move is absolute timeline seconds (on), with explicit adapter from R4 cut-relative clip.on; this is a design, not an implementation claim.

Only Agent M0 evidence still running: default main baseline and mandated dependent-suffix conformance. No additional wire decision is open under the orchestrator rule. App/Viewing can final-review the reconciled edit-recipe/extensions/schema now; actual M1/runtime/browser/renderer gates remain unrun.

## Agent baseline prerequisite limitation for Viewing (18:27 UTC)

agt-m0-env provisioned exact Node 20.19.4/npm10.8.2, but npm ci in its OWN Remotion worktree cannot fetch locked @banodoco/timeline-theme-2rp v0.1.1 GitHub archive (HTTP403). Earlier root npm cache EROFS was corrected using a writable worker cache; the retry remains403. Thus make check stops at missing remotion/node_modules preflight; independent Python doctor/mypy checks also fail as documented. No Remotion typecheck or renderer parity pass is claimed. Logs: /home/user/work/wt/agt-m0-env-logs/09-remotion-install-retry.log. This is an M0 recorded environment limitation, not a reason to loosen locks or claim parity. Viewing's package/dependency closure work needs to account for the unavailable locked artifact; integration Remotion was not modified.

## Agent designs ready for final reviews (2026-10-19T18:33Z)

M0 DESIGN COMPLETE: edit-recipe.md, extensions.md, port-manifest.md plus sole canonical edit-command.schema.json / command-schema-handoff.md and settled suffix-basis.md. All source/test review is recorded in agent-review-notes.md. Mandated no-field suffix proof now **35 passed** (b82dba0c), manager key-case rerun **2 passed**; canonical schema **95 passed**, recipe observations **14 passed**, extension probes **4 passed**. App/Viewing/Runtime final review can proceed; orchestrator checkpoint-a-ready notified. Main full default baseline remains running; do not infer M0 overall completion or any M1 gate pass.

## Astra changes and baseline classification (2026-10-19T18:40Z)

Direction approval acknowledged; agt-m0-a-guards and agt-m0-a-primitives are making the decided short edits in existing docs (exact real-browser move capture, retained transcript/config content, one recorder/derived commands, identity-only map, structural M1 proof; bounded marker/signal interfaces and fail-closed missing marker). No new docs/framework/M1 code. Agent make-check failures all occur on pristine e51595c6: Remotion locked artifact403 is environment admission; doctor is a deps-only-vs-installed-source setup mismatch; Mypy Python3.13/NumPy2.5.2 vs configured3.11 plus missing YAML stubs is environment/toolchain. Main CI uses3.11 + editable dev install; no claim CI itself fails. Detailed source/log evidence is in agent-review-notes.md. Full main baseline continues ONCE (seven visible failures, full node list pending).

## Astra edits reviewed (2026-10-19T18:50Z)

All Agent-owned decided changes are now in existing recipe/suffix/schema-handoff/extensions docs. Browser clip.move capture is normative in edit-recipe.md (source paths, supported mapping, follow clear/duration freeze, queries, real App tests). Clarified that child materialization revision/digest pins authenticate images but are not equality guards on the entire containing snapshot: A/C can change them while B's original semantic reads still hold. Normalize stable authoring owner via main source_mapping; guard actual consumed source/window/map identities. Add same-child disjoint/shared-first-materialization tests in M1. Accepted dependency content snapshots, one authoritative recorder/derived commands and identity-only map are adopted. Marker/signal pre-stop scope is bounded refs/resolvers+fixtures; missing marker refuses republication. No Python-handler transpiler, extension host, generalized signal/policy work before M5. Only remaining Agent M0 work is the one main baseline run/report.
