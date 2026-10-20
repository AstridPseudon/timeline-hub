# Runtime D11 groundwork: R4 documentation retirement

**Status:** read-only cut plan; D11 remains `planned`, not deleted. This is M4 groundwork and does not claim final architecture, product acceptance, or a completed delivery.

## Evidence and replacement page

The settled source of truth is `PLAN.md`, especially the process cut: `docs/projects/timeline-r4/` is archived, not ported, and is replaced by one architecture page plus runnable build/test instructions. The reviewed replacement draft is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/architecture-draft.md`

It is 417 words, explicitly marked M4 groundwork, and names the current open writer, capture/`RenderRequest`, parity, export, and owner-film gaps. The product landing target should be a new Agent-owned `docs/architecture/timeline.md`; do not repurpose the existing broad `docs/reference/architecture.md`. Runtime/App/Composition should link to that page from their owned contract or user documentation. Until that landing PR exists, the external draft is the only replacement artifact; no R4 status page should be rewritten to imply completion.

Exact source trees inspected:

| area | current integration SHA | frozen R4 candidate SHA |
|---|---|---|
| Agent / SDK | `cf7448ed6c1298b172d004914cfe2bb8c99048e7` | `11caf1d9de291d76f491cf69f7942606b7471d7a` |
| Runtime | `c1fb9ef2f7736459ceaaaaf85b5f9650e32c942d` | `31c7ac3a00f7a205f507bf5bd4d4625628d429bd` |
| App | `6ff21cac9deee3aae014e5c9e65d9871a3452f77` | `8f0c2484463e9b666d184a744d52e252984e551a` |
| Composition / Viewing | `e80c46baf5aa4b50a10b77a5ceadcb7ec4ab27ab` | `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` |

The R4 control branch itself is Agent `codex/handover-timeline-r4-20261019-control` at `5249ac07903af36532840d5c5ed3f8960a2fe07c`. The frozen Composition candidate has no merge base with that repository's `origin/main`; that is a source-history fact, not a reason to alter it here.

## Real R4 ceremony inventory

The only complete `docs/projects/timeline-r4/` tree is in the Agent control checkout, not in any of the four product integration trees: 58 files, 2,092,907 bytes at the control SHA. The exact files and byte sizes are:

```text
START-HERE.md 3503
agent_goal.md 7984
amendment-integration.md 3396
architecture.md 11062
cards.md 154795
dependency-graph.json 69528
handover-manifest.json 172129
manager-brief.md 10153
northstar.md 3215
open-questions.md 7566
plan.md 51227
portfolio.md 6150
release-contract.md 11829
run.yaml 14484
source-custody.md 9553
source-refs.json 72376
spec-agent.md 5920
spec-hardening.md 9775
spec-later.md 5587
spec-rendering.md 14342
spec-save.md 8577
spec-timing.md 25748
spec.md 9419
status.md 2481
tasklist.md 90924
testing.md 12882
amendments/20261015-human-historical-gate-challenge.json 954
amendments/20261015-human-no-arbitrary-limits.json 1273
amendments/20261016-upstream-transcript-extension-integration.md 31350
amendments/20261016-user-message-5.txt 5649
amendments/20261016-user-message-6.txt 4586
amendments/20261016-user-message-7.txt 4374
amendments/20261016-user-track-mirror-addendum.txt 747
amendments/20261018-remaining-typed-inputs-166.md 3586
amendments/r4-release3-extension-kinds-restored.md 11797
assets/adaptive-resource-ruling.md 4196
assets/composition-publication-ruling-262.md 3922
assets/current-next-operations.md 3333
assets/handover-assurance.md 3745
assets/handover-message.md 6041
assets/pathmap.md 1975
assets/receiving-setup.md 6232
briefs/codex-exec-common.md 9618
briefs/manager-current-guidance.md 23523
scripts/clone-pinned.py 5493
source-attachments/HISTORICAL-PUBLICATION-PROGRESS.json 60960
source-attachments/HISTORICAL-TIP-COVERAGE.json 995068
source-attachments/source-attachments.json 7699
source-attachments/README.md 992
source-attachments/SUPPLEMENTAL-SOURCE-PRESERVATION.md 1357
source-attachments/preserved-source/j029-fresh-vignette-029-historical-snapshot/docs/SKILL.md 450
source-attachments/preserved-source/j029-fresh-vignette-029-historical-snapshot/extensions/timeline.component/vignette.tsx 4972
source-attachments/preserved-source/j029-fresh-vignette-029-historical-snapshot/extensions/timeline.component/vignette.yaml 568
source-attachments/preserved-source/j029-fresh-vignette-029-historical-snapshot/pack.yaml 374
source-attachments/preserved-source/primary-app-audio-resume-wip/primary-app-audio-resume-wip.patch 35454
source-attachments/preserved-source/unbound-git-blobs/060022ecd99a9b16873f41ce2607c6c31d8aaf60.source 46527
source-attachments/preserved-source/unbound-git-blobs/0e000d48b2295af37cbc80fd25d424aa820ba2fa.source 7165
source-attachments/preserved-source/unbound-git-blobs/0e007645565cc3c428258580adbffaa451be9384.source 4322
```

The control root is 26 top-level files plus 9 amendments, 7 assets, 2 briefs, 1 helper script, and 13 source-attachment files. `source-attachments/**` is 1,165,908 bytes and is preservation/source custody, not ceremony.

There are no `docs/projects/timeline-r4` paths in Runtime, App, or Composition at their current integration SHAs. The following frozen-candidate paths are R4-adjacent but are not D11 deletion targets:

| repo / frozen SHA | path | bytes | disposition |
|---|---|---:|---|
| Agent `11caf1d9` | `docs/timeline-editing-guide.md` | 23119 | retain; current user/contract guidance |
| Agent `11caf1d9` | `docs/reference/continuous-slot-command.md` | 2333 | retain; command reference |
| Agent `11caf1d9` | `docs/reference/registry-command.md` | 1759 | retain; command reference |
| Agent `11caf1d9` | `docs/reference/timeline-offline-inspection.md` | 3129 | retain; user-facing inspection reference |
| Runtime `31c7ac3a` | `contract/edit-command-candidate.md` | 3855 | retain/move only with Runtime contract ownership; candidate schema notes, not ceremony |
| Runtime `31c7ac3a` | `contract/timeline-commit-candidate.md` | 12976 | retain/move only with Runtime contract ownership; candidate contract specification |
| Runtime `31c7ac3a` | `contract/timeline-retention.md` | 6169 | retain as contract candidate or explicitly deferred; not a final architecture claim |
| App `8f0c2484` | `docs/video-editor/timeline-patch-operations.md` | 22653 | App-owned active M3 operation reference; transitional semantics need architecture link, not deletion |
| App `8f0c2484` | `docs/video-editor/semantic-gesture-consumers.md` | 15620 | App-owned consumer/evidence note; keep while fallback rows remain |
| Composition `c82eb7c4` | `README.md` | 23481 | package contract/readme; retain |

Source fixtures and contract surfaces are separate from docs: Agent `tests/fixtures/**`, Runtime `conformance/fixtures/**` and `contract/schemas/**`, App `src/**/fixtures/**`, and Composition package sources are not R4 ceremony and must not be removed by D11. The same applies to generated OpenAPI/client artifacts. A compressed Runtime fixture contains incidental bytes that match `R4`; it is data, not a document reference.

For the current integration trees specifically, Agent has `docs/timeline-editing-guide.md` (24,860 bytes), `docs/reference/timeline-offline-inspection.md` (3,129 bytes), and the separately owned `docs/plans/astrid-naming/README.md` (149,768 bytes); Runtime has none of the three candidate contract notes; App has `docs/video-editor/timeline-patch-operations.md` (22,653 bytes) but not the frozen consumer note; Composition has only its `README.md` (23,481 bytes) among these paths. These presence differences are why the cut must be reference-based rather than a directory-wide product-repo deletion.

## Inbound references and link repair

Read-only scans over all four current integration trees found zero literal references to `docs/projects/timeline-r4`, `handover-manifest.json`, or `handover-timeline-r4` in production code, tests, or docs. The only meaningful product-tree references are:

* Agent `docs/plans/astrid-naming/README.md:12,13,114,236,241,243,368,395` describes R4 branches/docs and a later naming-plan cleanup. This is a separately owned naming plan, not a D11 consumer. If it remains after D11, its “R4 docs” prose should point to `docs/architecture/timeline.md` or be removed by the naming-plan owner; D11 should not edit it opportunistically.
* Agent `tests/sdk/test_timeline_sheet.py:86` calls a synthetic sheet fixture a “handover fixture”; it does not read the control docs and requires no repair.

No Runtime, App, or Composition code/test consumer requires a replacement path. Necessary semantic references after the landing page exists are:

* Agent `docs/timeline-editing-guide.md` and relevant command references → `docs/architecture/timeline.md` for cross-product ownership; their detailed command semantics remain local source documentation.
* Runtime `contract/timeline-commit-candidate.md` and `contract/edit-command-candidate.md` → the architecture page for ownership/flow only; schemas and generator contracts remain authoritative for wire shape.
* App `docs/video-editor/timeline-patch-operations.md` → the architecture page for the transitional App-adapter boundary; the operation reference remains App-owned until the command migration is complete.
* Composition `README.md` → the architecture page only for the evaluator/save boundary; package API and version claims remain Composition-owned.

## Minimal PR-sized cut plan and ownership

1. **Agent-owned landing PR:** add `docs/architecture/timeline.md` from the reviewed draft, with the nine verified code anchors already listed in the draft. Add only the links above. Do not alter the broad `docs/reference/architecture.md` or product behavior.
2. **Preservation/archive PR:** Runtime delivery coordinates, but Agent owns the actual control-repo target. Move or otherwise preserve the 13 `source-attachments/**` files and their `source-attachments.json` manifest at an explicitly owned archive destination before removing the control tree. The destination is not settled in PLAN, so this report does not invent one and the files must not be deleted.
3. **Ceremony deletion PR:** after step 2, Agent removes the operational/control-only set: `START-HERE.md`, `agent_goal.md`, `amendment-integration.md`, `architecture.md`, `cards.md`, `dependency-graph.json`, `handover-manifest.json`, `manager-brief.md`, `northstar.md`, `open-questions.md`, `plan.md`, `portfolio.md`, `release-contract.md`, `run.yaml`, `source-custody.md`, `source-refs.json`, `spec-agent.md`, `spec-hardening.md`, `spec-later.md`, `spec-rendering.md`, `spec-save.md`, `spec-timing.md`, `spec.md`, `status.md`, `tasklist.md`, `testing.md`, `amendments/**`, `assets/**`, `briefs/**`, and `scripts/clone-pinned.py`. This is a proposed cut list, not an authorization to delete in this task.
4. **Runtime/App/Composition follow-up:** each owner may add the one architecture link to its retained local contract/readme. Runtime remains the delivery owner for D11 acceptance and checks; it must not edit the Agent/App/Composition worktrees. Viewing/Composition owns any Composition README change.

The old `architecture.md` and six workstream specs contain useful design prose, but the PLAN explicitly retires the R4 ceremony. Before deletion, durable semantics not present in the replacement page must either be landed in the owning contract/user docs above or preserved in the archive. In particular, do not infer that Runtime’s candidate retention spec authorizes purge: PLAN defers retention/purge machinery. Do not delete current contract schemas, generated clients, fixtures, or positive behavior tests merely because R4 docs mention them.

## Acceptance commands for the future cut

These are meaningful structure/reference checks, not deletion-mirroring tests. They are not run now because this task made no repository edits.

```sh
# From a clean Agent landing/deletion PR:
python3 scripts/reshape/check_doc_references.py
python3 -m scripts.reshape.compare_structure_baseline
git diff --check

# Cross-repo stale-reference scan; expected zero output after link repair,
# except separately reviewed historical prose in the naming plan if retained.
for repo in /home/user/work/agent /home/user/work/runtime /home/user/work/app /home/user/work/composition; do
  rg -n -i --hidden -g '!.git/**' -g '!node_modules/**' \
    'docs/projects/timeline-r4|handover-manifest\.json|handover-timeline-r4' "$repo"
done

# Runtime retained contract surfaces, if any Runtime contract docs move:
python generators/generate.py --check
python scripts/artifact_manifest.py --check

# App retained documentation maturity/reference surface, if App docs move:
npm run check:docs-maturity-sync
```

The cross-repo scan should be run with an allowlist only if the naming-plan owner deliberately retains its historical R4 prose; no code or test should be allowlisted. No full suite, browser, localhost, ZIP, publish, checkout, branch mutation, or product-file deletion was performed.

Architecture replacement landed: Agent130b4937 (401words +guide link), docrefs0errors/0warnings. Four currentintegration docs/projects/timeline-r4 inventories remain empty:
- agent 130b4937856872b7abac35128cdf66222cf67165: 0 paths
- runtime 16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5: 0 paths
- app 41fff23a29f13bd9aede6343592ffba8adebe1a3: 0 paths
- composition 5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8: 0 paths
D11 is removed from the integration surface by non-port; the historical control archive remains unchanged. This is not a fictitious deletion commit or M4 completion.
