# Agent manager M0 review notes (drafts in progress)

No approval claimed. Current recipe draft aligns with PLAN on semantic footprints and server authority. Resolve these details jointly with Runtime before completion:

1. Explicit unchanged writes must reach accepted history. State exactly whether an intentional `set x=A` at A advances a semantic revision/event despite identical snapshot bytes. If it is dismissed as a no-change transport result, later inverse cannot detect another author's A→A. Distinguish an authoring API deciding to emit no command from a command that explicitly wrote unchanged state. Existing CLI conformance expects no undo step for ordinary idempotent no-change; retain that behavior only where no intention is submitted, and test the distinction.
2. Match concrete provider DTO/signature and EditCommand fields across edit-recipe.md and commit-contract.md. Trusted actor/authority comes from Runtime; client footprints are reconstructed claims, not authorization. Provider may read only pinned dependencies; exact-retry reconstruction must never invoke scene evaluation.
3. Accepted response revision must identify the exact accepted candidate even if head moves before reload. Read views and preview must label actual immutable loaded revision and child closure, not merely compiler/provider version (see viewing-coordination.md).
4. App's durable prefix/suffix/tab fencing review is in app-contract-review.md. Keep exact request bytes and scope across Runtime restart; suffix retains original intent/reference basis.
5. Main conformance has a pre-existing skipped preview parity placeholder. Do not claim pixel/audio gate 6 from that suite; Viewing owns actual parity with a planted mismatch.

The spike branch remains disposable; no bulk R4 overlay merge is authorized.

## Runtime draft review (2026-10-19 17:49 UTC)

commit-contract.md now covers item 1: accepted receipt/publication edge even for unchanged authored value, immutable revision reuse allowed, both publication+revision head CAS. This resolves the semantic concern in principle. Agent supports that design and the same-project pinned dependencies/fail-closed legacy history boundary. Confirm in final recipe.

Concrete reconciliation still needed: use one metadata name (`reason` in commit envelope vs `rationale` in recipe); declare command `schema_version` vs envelope `api_version` vs operation `version`; provider ABI v2 and `create_runtime_commit_service` compatibility export; `timeline.inverse`/`timeline.restore` arguments; bootstrap pin behavior. Three-attempt head-race budget is acceptable if each attempt preserves the recorded base plan/IDs and exact request identity. Record source `via` should include sheet or use `script` consistently for that frontend. No objection to Runtime's three narrow operations or additional restore publication guard.

## Extension deliverable review (2026-10-19 17:55 UTC)

Reviewed extensions.md and agt-m0-ext diff (only 102-line isolated probe, no product changes); manually re-ran `python3 -B tests/m0_extensions/probe_extensions.py -v`: 4 passed. Worker also ran main sheet/show/conformance: 219 passed, 4 existing parity skips, 2 missing-timeout-plugin warnings; shared-env rerun/baseline remains pending. Corrected one stale reason/rationale spelling in shared design. The marker proposal explicitly needs stable set/item IDs and pinned publication reads; ordinal counterexample confirms why. Editable view proposal needs base+surface+scope; parser probe confirms printed scope alone is lost. Ten persona/code walks and M5-only criteria are present. No checkpoint approval or extension implementation claimed. The branch is diagnostic evidence only and intentionally unmerged because it reads frozen local R4 paths; preserve its commit 56fc0dc6 for reconstruction rather than adding a frozen-ref dependency to the product default suite.

Recipe must reconcile extension counterexamples: selected marker publication ABA/follow behavior; partial sheet membership/hidden fields; unknown reference-bearing payload during remap. Existing future marker admission remains outside M0.

## Port manifest first review (2026-10-19 17:57 UTC)

port-manifest.md currently describes which files were copied/edited in the disposable experiment, but that is not yet the file-by-file forward-port RECOMMENDATION requested by the brief. For example drafts.py, story.py and copy_sync.py are listed port-as-is despite PLAN deferrals/cuts; compiler.py is listed port-as-is although rational fps/main timing rules still need adaptation. Minimal M1 list omits commit/provider/CLI/SDK which are explicitly M1 deliverables. No bulk merge is contemplated, but fix these labels before checkpoint-ready. Each recommendation needs specific main fixes/source dependencies. Failure categories are currently aggregate per log, not per failed node; a machine-readable failure index linking every exact failed/error node to a/b/c plus cause is needed. Import smoke uses unsupported/optional shims and must state that limitation prominently; these are not acceptable production ports. Shared env is now ready, so rerun the focused lane without excluding the known missing generator and classify that failure separately.

## Superseding orchestrator suffix decision (2026-10-19 18:03 UTC)

PLAN and Agent INBOX now settle the original-basis question: no new DTO field/base_view. Dependent B waits for A acknowledgement, then submits at HA retaining original commands/read/selection/value+identity guards; mismatch is conflict, equal-state ABA is deliberately allowed for this handoff. Earlier proposal/escalation is superseded. Accepted inverse still follows PLAN's separate publication/intervening-write ABA guard. agt-m0-suffix-conformance replaces the reduced proposal model with mandated A→5/B absolute7 or relative+2/C/retry/reload/created-ID cases. Recipe must remove its Open DTO issue and original-result proposal assumptions.

## Completed hard-case/port review (18:07 UTC)

Reviewed agt-m0-recipe 03d05130 source (770 lines: isolated tests + design schema only), strong real-code assertions for all PLAN cases; independently reran main occurrence/chapter/transcript fixtures plus frozen inverse ABA/ancestry: **4 passed in 19.31s**. Worker final full observations: 14 passed; overlay comparison: all 9 blocked by missing CheckAdmissionContext. Those failures are now indexed individually as recipe-overlay in port-failure-index.tsv. No frozen-ref tests/schemas are merged into the product default lane.

Reviewed port audit: 140 distinct run/node failures across original/focused runs with no missing/extra/duplicate nodes; full focused lane reports 104 passed/5 failed rather than deselecting freshness. Shared-env clean-main selected lane 196 passed/17 deselected resolves the earlier fonttools environment failure. Corrected manifest fact that both main/R4 use app.astrid, removed nonexistent main scene_answers.py, and added omitted look.py/reflow.py/store.py recommendations. All R4 SDK Python paths now appear. Audit has no branch diff and its inherited experimental branch remains not for merge.

## Canonical schema final review (18:09 UTC)

Reviewed agt-m0-command-schema b8c79fbb (293-line isolated schema validation only), independently reran all examples and leaf/batch constraints: **95 passed in 0.48s**; diff check passed. Its final schema adopts recipe ref/token-array leaves while retaining R4 expect/authorship keys and binding/created types. Selected ORCH/design/edit-command.schema.json as the SOLE M0 source, later packaged core/timeline/schema with byte-identical Runtime projection. Recipe branch candidate schema is superseded. Applied handoff corrections to edit-recipe.md (explicit clears, required wire versions, artifact paths/equality, sole-restore batch, minimal absolute clip.move and explicit R4 conversion, path/structural restoration). Runtime DTOs remain unchanged. Inverse/restore args are now explicit and consistent. Dependent-suffix PLAN decision replaced the old open issue. No M1 source implemented or merged.

## Final suffix review / design-ready (2026-10-19T18:33Z)

agt-m0-suffix-conformance b82dba0c replaces rejected c71db63e proposal: **35 passed in 675.05s**, actual frozen R4 execution/recording/compiler/rebase/inverse plus bounded original-read/selection guards and modeled publication/outbox reload. Independently reran two key cases using private basetemp: **2 passed in 46.71s**. A prior concurrent review failed imports after the worker globally removed suffix-prefixed pytest temp paths; private basetemp resolves it. Do not glob shared pytest temp roots in future briefs. Accepted undo ABA guard is separate from deliberately allowed equal-state dependent suffix ABA. No new DTO field or unresolved semantic choice. Real Runtime/browser/process durability remains M1 work.

All Agent design artifacts are now reviewed and reconciled for checkpoint/Astra review. Default-main baseline still running (~49%); M0 overall completion is not claimed until that report finishes. No product code merged.

Final clarification: named M0 legacy→V2 version drift is a characterized gap, not an exception to PLAN lossless undo. Migration must be its own recorded/guarded reversible edit (or explicit atomic group); ordinary edits restore exact authored presence from their real base. Monotonic identity reservations are outside authored content. No wire or settled decision changed.

## Unchanged-main make-check blocker classification (2026-10-19T18:40Z)

Read-only evidence: agt-m0-env branch remains e51595c6 with `git status --short` and `git diff e51595c6 --stat` empty; no Agent product changes are integrated. All three blockers were observed on unchanged main, so none is an R4-port regression. Distinguish causes rather than asserting CI itself is red:

- Remotion preflight: environment/artifact admission failure. Main's unchanged lock requests @banodoco/timeline-theme-2rp v0.1.1 GitHub archive; worker npm (exact Node20.19.4/npm10.8.2, writable cache) gets403, so node_modules stays absent. No source defect or CI failure proven; no typecheck/parity run.
- Doctor: M0 setup limitation. Main `scripts/reshape/ci_doctor.py:hermetic_env` drops PYTHONPATH and runs in a temporary cwd; dependencies-only shared env intentionally has no installed Astrid. `.github/workflows/ci.yml` instead installs Astrid editable with dev extras. `No module named astrid` is expected for this different setup, not evidence of a new doctor product bug. Required future green gate needs a disposable installed-source overlay/wheel, not a source pointer installed into the shared deps-only env. No rerun now.
- Mypy: M0 environment/tool-target mismatch, with missing YAML stubs also reported. Shared Python3.13.16 selects locked NumPy2.5.2; repo Mypy1.17 config targets Python3.11 and cannot parse NumPy's newer type-statement stub syntax. Main CI uses Python3.11 (lock selects NumPy2.4.6) and installs editable Astrid/dev. PyYAML6.0.3 exists but types-PyYAML is absent. These are observed unchanged-main environment/prerequisite errors; this run cannot establish a main-CI regression or a successful type comparison.

Per orchestrator, let the full default suite finish once; do not rerun it or these gates now. Final baseline will preserve complete failing-node output (seven failures observed so far) and these classifications.

## Decided marker/signal scope review (2026-10-19T18:45Z)

agt-m0-a-primitives docs-only result reviewed: extensions.md now limits pre-stop markers/signals to bounded refs/resolvers and fixtures; missing referenced marker refuses entire republication with prior publication/bindings/state intact. No orphan/last-known fallback, registration/detector reconciliation/general signal binding/policy/query-growth/host framework before M5. Exact consumed transcript/config content is retained through Runtime-owned immutable snapshots, separate from Documents history. Retained existing word/beat playback. Manager corrected the M1 table to include the decided structural recorder proof and real browser capture, and clarified identity-only commit id_map versus future producer event correspondence. No product code or behavioral test pass claimed by these documentation edits.

## Decided guard/recorder changes reviewed (2026-10-19T18:50Z)

agt-m0-a-guards docs-only result reviewed; 95 schema-design tests passed with private basetemp, no schema or product change. Exact browser move contract now records scope/occurrence/window/rate/selection and follow clears; limits unsupported mappings; requires real App command+drag capture and structural M1 framework proof. Runtime removed independent PreparedCommit.commands; derive response commands from records. Ingress normalizes legacy address strings once; id_map identity-only; accepted exact content snapshots consumed without mutable Documents lookup. Manager clarified normalized authoring-owner guards vs physical child revision/digest provenance, with same-child disjoint and shared-first-materialization M1 cases, plus type-aware JSON equality. No blanket container hash equality or Python transpilation framework is permitted. No new wire field or changed dependent-ABA policy.

## M1 handwritten bridge review (19:25Z)
Reviewed a6cabc4d against a6502806:96 product add/4remove across handwritten workspace_client+remote, generated artifacts untouched. Public frozen request body/key/envelope retained through existing allowlisted adapter. Manager pytest tests/sdk/test_workspace_client_timeline_commit.py --basetemp=/tmp/agt-manager-bridge-review:8passed0.58s. Worker broader48focused/110neighbor1skip. Merged fa0542ad. Runtime pin still required; no live transport acceptance claimed.
Readback fix38tests manager passed1.78s, but held: actual cli_history._store passes RemoteTimelines, which exposes history not list_timeline_commits. Assigned agt-m1-readback-live-adapter to prove actual facade/CLI path and strict loaded identity; fake direct-client cases alone insufficient.

## M1 reviewed integration evidence (19:34Z)
Integrated readback5cb918b6 (chain ba08fd9b): manager normal integration PYTHONPATH=$PWD venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_revisions.py tests/sdk/test_timeline_show_views.py tests/packs/timeline/test_cli_history.py --basetemp=/tmp/agt-manager-integrated-readback =>53pass3.31s. Portable actual RemoteTimelines facade test, no sibling imports in committed tests.
Generated Runtime client live cutover: central agent-client-cutover-integration-1019192950-24951 PASS39/105.45s, tree25ae6d8ca2f26851b2cf4471fad88eb4685b98ef. This proves old normal client journeys/socket issues resolved centrally, not new M1 commit gate.
Corrected core manager56recipe tests6.82s; provider manager6targeted passes2.17s (shared occurrence undo, shared sibling rebase, exact inverse, retained transcript/config closure, ABA) on real corrected core overlay. Worker120neighbors+50provider pass. Prefix bug resolved via exact deterministic main materialization equivalence, no namespace heuristic.
Visualize-read8ca850b1 reviewed; manager59shared-venv tests3.02s; merge queued. Actual native inspection/output label; historical input-only content+revision pins unmodified closure reader and removes unrelated current hashes. Broader worker neighbor batch interrupted; no full/browser/native journey claim.

## Integrated M1 source batch93624e8f
Manager normal-source command from integration (NO overlays):
`PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m1_commands.py tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/sdk/test_timeline_sync.py tests/packs/timeline/test_cli_commit_move.py tests/sdk/test_workspace_client_timeline_commit.py tests/sdk/test_timeline_revisions.py tests/sdk/test_timeline_show_views.py tests/packs/timeline/test_cli_history.py --basetemp=/tmp/agt-manager-m1-integrated-batch`
=>233 passed17.78s. Full queued agent-full-1019193420-11899 (one merged batch), old a650 baseline still running. Await official Runtime raw immutable codec correction and actual realpath/CLI/browser central tests; no M1 gate claim yet. All reviewed worker merge chains recyclable, preserve reports.
