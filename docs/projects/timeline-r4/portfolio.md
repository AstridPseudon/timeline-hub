# Portfolio playbook: timeline-platform-r4, "One timeline, many hands"

Execution authority: [run.yaml](run.yaml) and the current [orchestrator goal](agent_goal.md) govern models, stages, custody and escalation. Historical names do not launch agents or override them.

**The orchestrator's programme document.**
- **North Star:** [northstar.md](northstar.md).
- **What ships:** [release-contract.md](release-contract.md).
- **Design:** [architecture.md](architecture.md) and [spec.md](spec.md).
- **Cards:** [cards.md](cards.md), indexed in [tasklist.md](tasklist.md).
- **The orchestrator's brief:** [agent_goal.md](agent_goal.md); the managers': [manager-brief.md](manager-brief.md); testing: [testing.md](testing.md).
- **Rulings:** [plan.md](plan.md) (R-1 to R-14) and `reviews/DECISIONS-*.md`.

**Project folders** (`projects/A-…` to `projects/J-…`) retain their archived card indexes; managers inherit root configuration. Do not run the legacy generator, which would restore obsolete Otto bindings. The machine-readable setup is [dependency-graph.json](dependency-graph.json): one gate per card milestone, the entry dependencies and the one external prerequisite. The [latest user amendment](amendments/r4-release3-extension-kinds-restored.md) restores five extension kinds in R3; see [integration record](amendment-integration.md).

## 1. Projects A–J (the [tasklist](tasklist.md) is the index)

Ten projects, each with its own manager inheriting root run.yaml. The orchestrator dispatches every card to its project's manager; project A's manager is the merge manager. The plan: <!-- generated:figures -->95 cards, 137.25 worker-days: R1 69 cards / 97 d, R2 15 cards / 21 d, R3 11 cards / 19.25 d; 38 normal, 57 xhard; largest card 2.5 d. At 2 workers Release 1 is about 48.5 working days before coordination losses (arithmetic, not a promise).<!-- /generated -->

The per-project card lists, sizes and entry dependencies (the project-entry graph; preserve all card-level dependencies as well) are generated into [tasklist.md](tasklist.md); each project's own `tasklist.md` lists its cards and their dependencies.

**A milestone counts once its card has merged.** A card is ready when every dependency is merged; nobody builds ahead against fakes. The one external prerequisite, `codex-accepts-base`, gates only RELEASE-1.

**Module table** (a dispatch hint only: don't run two cards on one module at once):

| Project | Files |
|---|---|
| **D** | `astrid/sdk/timeline/{runner,command,commit,adapt,merge,external,journal,transaction,store,checkout,publish,revisions}.py`, the `timelines` CLI (`packs/timeline/cli.py` + `cli_*.py`), `tests/editing_conformance/` |
| **F** | `sdk/timeline/{reflow,timing,model,lookup,edits,units,doc}.py`, `core/timeline/{moments,music_edit,cuts,duration}.py` |
| **B** | `core/timeline/astrid_ns.py`, `sdk/timeline_intent.py` (until B closes, then F) |
| **G** | the composition repo (`T/`, our fork), `core/timeline/onscreen.py`, `packs/rendering/**`, App `src/tools/video-editor/compositions/**` (with the App owner) |
| **E** | the App's save state machine and editing UI (`src/tools/video-editor/{hooks,lib,components,data}/**`, `src/integrations/runtime/dataProvider.ts`) |
| **C** | Runtime publish/acceptance/history routes and the one coordinated schema change |
| **H** | the connector, relay, loopback and ACP bridge, and the Astrid host confinement |
| **A** | `schemas/` (the frozen contracts), `tests/fixtures/`, `tests/integration/`, `tools/{parity,golden}.py` |
| **J** | `astrid/core/extensions/**`, the pack-builder skill |

## 2. Capacity
See the WIP caps in [agent_goal.md](agent_goal.md). The orchestrator applies them when it dispatches; managers wake on events.

## 3. The critical path
```
A#base → B#compat + D#commands + F#characterized → F#compiler → D#merge → D#commit-service (needs C#acceptance, A#contract-commit)
       → E#gestures → E#save-rebase → E#collab-ux → A#r1-accepted
```
EVAL (G) and the hosted-security chain (H) are parallel release blockers that can become critical.

The Release 1 forecast is redone when `E#save-rebase` merges.

## 4. The two frozen contracts
Only what crosses repos is frozen, in its existing home:
- **CONTRACT-COMMIT:** CommitRequest/Result, the HTTP routes, the Runtime acceptance interface and the dry-run rebase that gives the App its rebased suffix.
- **CONTRACT-COMMAND:** the EditCommand envelope with shared request/result and timing fixtures; each repo proves only its own part against them.

Fakes exist only where a live consumer needs one. **A change to either is a card the orchestrator approves.** Astrid-internal APIs are not frozen.

## 5. Order
No waves: a card is ready when its dependencies are merged. One ordering note stays: dangerous proofs go early (real-provider save and recovery in B/X0, actual-Player parity with audio in G, hosted-route feasibility on disposable data in H, Runtime commit cost in C).

## 6. Testing
See [testing.md](testing.md): red then green for bug fixes only, unchanged for preservation, and nine named integration points with one status.md line each. Reviews happen in three places: the contract schema (inside CONTRACT-COMMIT), the rebase and commit diff (inside COMMIT), and the owner watching the film (RELEASE-1, FINAL-R3).

## 7. Coordination
- **The orchestrator** dispatches each card to its project's manager, routes consequential decisions to the designated oracle, unblocks, answers escalations and writes the daily report. It doesn't merge or run tests.
- **The merge manager** (project A's manager, always attached) owns the merge queue across the four trunks, including the composition artifact, and runs the integration points through the lease.
- **Managers** (all ten projects) give each card they receive to a worker and hand it back, in one line, to the merge manager.
- **Card states:** todo, doing, merged (and blocked).
- **Codex's Runtime and App lines:** the merge manager sends PR packets; their review does not block.
- **Wake:** event driven; this packet creates no scheduled loop.
- **Escalation:** the list in [agent_goal.md](agent_goal.md).
