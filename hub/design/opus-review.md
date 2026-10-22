# Review of the M0–M4 finish plan: speed, quota, sequencing

## Verdict
The plan aims at the right goal, and its inventory is honest and well researched. Several calls are right: merge rather than rebase (§2), no internal releases (§1), Sol from the start on hard tasks that sit on the critical path (§15.5), a cheap gate 6 (WP8), and no §13 work in M4 (§11). The critical path in §0/§10 is wrong, though, and the plan contradicts itself. §1 says "work by slice", but §10 hands out the tasks by repo again, with six or more hand-offs between managers. Each hand-off was measured at 1–3 h. The plan also misses three risks that could each cost half a day, and it rebuilds a 44-scenario live suite that scope-cuts #4 had already shrunk. As written, 2–2.5 days is not credible; I'd expect 3–4. With the changes below it becomes realistic.

## Top changes, in priority order

**1. Redraw the critical path, because WP3 is not Runtime work** (saves about 6–10 h).
- The command schema (`astrid/core/timeline/schema/edit-command.schema.json`) and its executor (`sdk/timeline/commands.py`) live in Agent. Runtime only holds a byte-identical copy of the schema, and contains no `clip.move` code.
- So RT-3 → RT-2 (schema v32) is a false dependency.
- So is "Runtime → Agent → App" for the merges (WP1). Agent and App need Runtime only for the re-vendor step (AG-2, APP-4).
- Most of Runtime's 16 conflicts are generated files.
- New order:
  - start all three merges at H0;
  - write the RT-5 conformance cases first, in Agent;
  - build the Agent executor and APP-6 in parallel against them (§15.2's idea, given to the right owner).
- The chain becomes App merge ‖ (cases → TS twin) → APP-8/9/12 → APP-23 → RT-8 → WP11.

**2. Make §1 real: single-owner slices on the chain** (saves 4–6 hand-offs, about 5–12 h).
- **"Vocabulary and drags".** One Sol-led owner covers the Agent schema and executor, APP-6, G2 and G5.
- **"Route cut".** One owner covers WP6's composition consumers, RT-6 to RT-9 and the D13 assembler.
- Write RT-9 (the test) and RT-8 test-first on a branch now, so RT-8 lands minutes after APP-23.

**3. Turn WC8 (AG-11, size L, XHard) into a refusal** (saves about 6–8 h of Sol).
- Upstream 4eea1dd24 now says when a reused working copy is behind the head, and points to "discard + checkout --fresh".
- Native commands are already rebased on the server (gate 2).
- Once WC7 deletes `publish_bundle`, the remaining `three_way` merge (`checkout.py:242`) can refuse instead of being rebuilt.
- This needs an owner decision, like decision 4.

**4. Take mechanical work off Codex** (about 25–35% fewer worker runs).
- Run these as Claude scripts, without a worker or a review:
  - modify/delete, docs and supabase conflicts (APP-1);
  - generated-file conflicts (regenerate them);
  - re-vendors and pins (AG-2/3, APP-4/5, VW-1);
  - grep audits, APP-24 and the ledger.
- Review only product-code merges. Reviews were already 27% of all workers.

**5. Shrink WP9 to one data-driven gesture tour that extends `three-products`** (saves about 8–10 worker-hours plus flaky reruns).
- `three-products.spec.ts` already covers the Agent edit showing in the App (:408, X01), concurrent edits (:495, X03) and a Runtime restart (:665).
- Keep the commit recorder, the old-route counter, and reload plus undo for each gesture. Prove restart and lost acknowledgement once.
- Gate 6 asks for "representative gestures", not 44 ten-step scenarios four times a day.
- Drop `content_digest` (RT-4). It exists only for a test, and `live.ts` already compares canonicalised documents.

**6. Close two audit holes the WP1 grep misses.**
- **A new gesture.** Upstream 874366eae added "drag a clip from an extension panel". It saves through `applyEdit` → `scheduleSave` and never names `saveTimeline*`. Build the true caller list by deleting `saveTimeline*` and the save branch on a scratch branch and letting typecheck list every caller.
- **The installer pin.** Upstream deed0eb3e's `installManifestSkew.test.ts` requires the installer-pinned Runtime to speak a schema digest the App accepts. Our v32 contract fails that until the owner's release moves `public/install-manifest.json`. Add it to WP2's known gap and §12's release step.

**7. Reclassify G8/G9 (popup ADD and SWAP) as a risk, not a Normal task.**
- The ledger says native ADD never reached the editor ("zero commit POSTs").
- SWAP has an unresolved mismatch between the local and the accepted projection.
- scope-cuts says neither may be activated until that is settled. Spike it with Sol in the first hours.

**8. Merge cadence** (saves 2–4 h).
- Turn on `git rerere`, so conflict resolutions are reused.
- Run a free `merge-tree` check at each checkpoint, but do real merges only at restart, at the end of Day 1 and at the final refresh.
- Ask the owner for an upstream freeze of about 6 h before WP11. Upstream is the owner's own sessions, so this is the cheapest lever.

## Q3: should §13 be pulled into M4?
No.
- **Why not.** The protocol doesn't need the TS twin: `CommitRequest` carries commands only. The outbox does need it. Each queued edit's computed `after` bundle is the base for the next local edit (`commitSession.ts:411-426`). Offline chaining and the R01/R02 and gate 2/5 behaviour rest on that, so replacing it now would destabilise exactly what M4 must prove.
- **Pull in only the no-regret parts:**
  - (a) Keep APP-6 to the `track` field and the transition values. A group move is just N × `clip.move`.
  - (b) RT-8 deletes the route bodies and leaves a 410 stub, rather than refusing now and deleting later.
  - (c) Each writer removal deletes its own bridges and guards in the same diff.
  - (d) Strike §13's "add a dry-run call". It already exists: `CommitRequest.dry_run` (`timeline_commit_port.py:524`).

## Quota and allocation
- **Sol** only for: the WP3 cases and executor, APP-9, the popup spike, RT-6/RT-7, AG-12 and AG-13.
  - RT-2 becomes Luna: dev realms are recreated anyway, and it is now off the critical path.
  - RT-3 moves into Agent (change 1).
- **Luna** for the rest of the product work.
- **Claude** for the orchestrator, scripts, the farm and read-only spikes, plus reviews if the owner allows (§15.3).
- **Machines:**
  - App Child 1: the App merge, then G1/3/4/6/7.
  - Child 3: vocabulary and drags, then the tour.
  - Agent Child 4: Agent writers plus the route cut.
  - Main: Runtime.
  - Viewing (about 21 h of work): WP8, then G10–G16.
- **Budget.** Set a Codex budget per slice and check the burn at H6.

## Estimate: biggest risks, de-risked first
1. **The App merge.** It also hits the preview hand-port files (`VisualClip.tsx`, `AudioTrack.tsx`, `renderRouter.ts`), which affect WP8.
2. **The farm's browser lanes.** Gate 6 has never reached its body. Prove them in the first 6 h.
3. **Popup ADD/SWAP.**
4. **Gate 7 tooling.** Dry-run it on day 1.
5. **Quota.**

## The first 6 hours
- **H0 (no Codex).** Owner decisions 1–7, plus WC8-as-refusal, the freeze window and the installer pin. Issue one slice task board in under 1 h. Fetch main and enable rerere.
- **H0.5, in parallel:**
  - the three merges (App part 1 scripted);
  - the WP3 cases in Agent;
  - VW-2 and VW-1;
  - farm: the upstream baselines.
- **H1–2.**
  - Popup spike (Sol), and the funnel-deletion caller list (Claude).
  - Farm: dry-run of `delivery-build`.
- **H2–4.**
  - The Agent executor ‖ APP-6.
  - RT-9 written test-first.
  - Farm: three-products and QUICK on the current head.
- **H4–6.**
  - G1, G3 and G4 once the App writer files are merged.
  - Farm: one physical parity run.
- **H6 go/no-go.** Check four things:
  - the merges are green or have named blockers;
  - the executor is done;
  - both browser lanes have been proven on the farm;
  - the quota burn is within budget.

  Then re-estimate from what was measured.
