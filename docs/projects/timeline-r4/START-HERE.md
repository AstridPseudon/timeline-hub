# Timeline R4 — receiving guide

Astrid is the host repository. The four product repositories are SDK, Runtime, App, and Composition. The new receiving control root is the tracked `docs/projects/timeline-r4/` directory in the Astrid control branch below. Receiving `.otto` directories may hold execution worktrees only; do not recreate or copy the original operative run tree.

The North Star is **“One timeline, many hands”**: preserve one film history and one validated, journaled change path across the CLI, sheet, Python/scripts, extensions, agents, and App; the same evaluator feeds preview and render. The original scope remains the complete 95-card A–J portfolio, adopted amendments, IP0–IP8, and all three releases.

- Host repository: [https://github.com/peteromallet/Astrid-agent.git](https://github.com/peteromallet/Astrid-agent.git)
- New control branch: `codex/handover-timeline-r4-20261019-control`. Its final commit/tree are pinned in the ZIP's `transfer/ZIP-REFERENCE.json` to avoid a self-referential commit.
- Frozen cutoff: `2026-10-19T14:10:14Z`; counts at cutoff: 29/95 cards, 0/3 releases, 262 advisories (225 delivery/direction + 37 scheduled), 0 new product reviews.

Current phase: The cross-machine handover source and control have been published, the private transfer has been built and independently checked, and fresh Astra 263 has completed its audit. Its bounded setup/documentation corrections are included here. Product delivery remains incomplete; publication and handover assurance do not establish product acceptance.

Read `status.md`, `handover-manifest.json`, `source-refs.json`, `run.yaml`, `agent_goal.md`, `northstar.md`, `plan.md`, `tasklist.md`, `cards.md`, `dependency-graph.json`, `testing.md`, `release-contract.md`, `source-custody.md`, and `briefs/manager-current-guidance.md`. The complete 95-card criteria and dependency graph are preserved.

Source refs distinguish candidate branches, actual current installed versions, and separate preservation/WIP refs. Do not treat an incomplete Runtime diagnostic WIP as an accepted candidate. GitHub is authoritative for source; the private ZIP carries only essential fixtures, evidence, and tool amendments.

The default receiver bootstrap fetches only one current candidate branch per product repository. When the SDK publication URL matches the Astrid host URL, it creates the SDK candidate as a separate Git worktree sharing the host checkout object store; the tracked control checkout stays intact. Other product repositories use filtered single-branch clones. Historical preservation/WIP branches stay on GitHub and can be fetched on demand; they are not expanded into extra clones or checkouts.

The receiving toolchain and model availability must be checked on the new machine. Do not silently substitute configured models. No host credential, source-machine Runtime identity, database, lease, process handle, or environment is carried.

## Start from receiving state

Read [receiving next operations](assets/current-next-operations.md), [setup and dependency layout](assets/receiving-setup.md), [handover assurance](assets/handover-assurance.md) and the explicit UNKNOWN review table in [status](status.md). The actual fresh handover advisory 263 is post-cutoff; total 263 (226 delivery/direction + 37 scheduled), 0 new product reviews. Both old-machine schedules and delivery owners remain held. Origin worker guidance is retained historical technical context, not active receiving custody.
