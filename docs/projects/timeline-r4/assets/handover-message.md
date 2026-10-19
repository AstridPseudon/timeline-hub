# Receiving handover message

Continue Timeline R4 in **delivery** mode from the new Astrid host control branch. The canonical receiving control root is tracked `docs/projects/timeline-r4/`; source `.otto` history remains on the original machine.

## Vision and original scope

North Star: **“One timeline, many hands.”** A film keeps the same history wherever it is edited: the CLI, sheet, Python/scripts, extensions, agents, and App use one validated, journaled change path, while the same evaluator feeds preview and render. The full original 95-card A–J portfolio, adopted amendments, IP0–IP8, and all three releases remain in scope. Read `northstar.md` and `agent_goal.md` for the complete vision and literal criteria.

## Current phase and evidence

The cross-machine handover source and control have been published, the private transfer has been built and independently checked, and fresh Astra 263 has completed its audit. Its bounded setup/documentation corrections are included here. Product delivery remains incomplete; publication and handover assurance do not establish product acceptance. At the frozen cutoff `2026-10-19T14:10:14Z`, 29/95 original cards are accepted, 0/3 releases are accepted, and there are 262 completed advisories (225 delivery/direction + 37 scheduled) and 0 new product reviews. This is a packaging and custody transfer; it does not complete product work.

Product source tests, installed-runtime qualification, public App behavior, release acceptance, and owner film viewing are separate evidence claims. Preserve all review UNKNOWN states, consumed caps, prior history, and named human/security/publication/live-migration gates exactly as recorded. No new product review or acceptance is claimed here.

Choose a new canonical host destination in `ASTRID_DEST`, then run this guarded, filtered clone:

```sh
python3 - "$ASTRID_DEST" <<'PY'
import pathlib, subprocess, sys
dst = pathlib.Path(sys.argv[1]).expanduser().absolute()
if dst.exists() or any(part.is_symlink() for part in (dst, *dst.parents)):
    raise SystemExit('destination exists or uses a symlink; choose a new canonical path')
subprocess.run(['git', 'clone', '--filter=blob:none', '--single-branch', '--no-tags', '--no-checkout', '--branch', 'codex/handover-timeline-r4-20261019-control', 'https://github.com/peteromallet/Astrid-agent.git'] + [str(dst)], check=True)
PY
```

Read the exact control commit/tree from the ZIP's `transfer/ZIP-REFERENCE.json`, checkout that commit, and verify both values plus `docs/projects/timeline-r4/handover-manifest.json`.

The four product candidate refs are: 

| Role | Source origin | Publication remote | Candidate branch | Commit / tree |
|---|---|---|---|---|
| app | [https://github.com/banodoco/reigh-app.git](https://github.com/banodoco/reigh-app.git) | [https://github.com/banodoco/reigh-app.git](https://github.com/banodoco/reigh-app.git) | `codex/handover-timeline-r4-20261019-candidate-app-qualified` | `8f0c2484463e9b666d184a744d52e252984e551a` / `26ad064632fac9ff123670aa7d6ed0e3d8f89178` |
| composition | [https://github.com/AstridPseudon/timeline-composition.git](https://github.com/AstridPseudon/timeline-composition.git) | [https://github.com/peteromallet/timeline-composition.git](https://github.com/peteromallet/timeline-composition.git) | `codex/handover-timeline-r4-20261019-candidate-composition` | `c82eb7c459d0a41263954bf007071a6a0e8e0a6a` / `49975e7a54fd594e1b7fc807681fe28611d57864` |
| runtime | [https://github.com/banodoco/banodoco-workspace-runtime.git](https://github.com/banodoco/banodoco-workspace-runtime.git) | [https://github.com/banodoco/banodoco-workspace-runtime.git](https://github.com/banodoco/banodoco-workspace-runtime.git) | `codex/handover-timeline-r4-20261019-candidate-runtime` | `31c7ac3a00f7a205f507bf5bd4d4625628d429bd` / `73e676f420ba0545b6eebe45870d532344a9e69b` |
| sdk | [https://github.com/peteromallet/Astrid-agent.git](https://github.com/peteromallet/Astrid-agent.git) | [https://github.com/peteromallet/Astrid-agent.git](https://github.com/peteromallet/Astrid-agent.git) | `codex/handover-timeline-r4-20261019-candidate-sdk` | `11caf1d9de291d76f491cf69f7942606b7471d7a` / `f6f4fad77ded050b1e9c2d802cc3da35b459e610` |

Review `source-refs.json` for actual current-installed identities and separately preserved candidate/WIP identities. Use `scripts/clone-pinned.py` with an explicit new empty destination for the four current candidates; it verifies commit and tree and refuses existing paths. If the SDK URL matches the Astrid host, it adds a separate SDK candidate worktree sharing that object store and leaves the control checkout intact; Runtime, App, and Composition use filtered single-branch clones. Historical preservation/WIP refs stay on GitHub for on-demand fetch.

## Continue from the completed handover

The cross-machine handover source and control have been published, the private transfer has been built and independently checked, and fresh Astra 263 has completed its audit. Its bounded setup/documentation corrections are included here. Product delivery remains incomplete; publication and handover assurance do not establish product acceptance.

Actual post-cutoff advisory 263 makes 263 completed advisories (226 delivery/direction + 37 scheduled), with 0 new product reviews. Read [current next operations](current-next-operations.md), [setup](receiving-setup.md) and [handover assurance](handover-assurance.md). The four qualified/preserved source identities above are unchanged. All necessary handover source refs are already published; do not rebuild/re-publish the transfer as a prerequisite.

Use the delivered E/F/EB/G terminal checkpoint map; establish fresh receiving ownership and continue implementation/integration within recorded delivery authority. Preserve named human/security/data/publication/deployment/live-migration gates. Allthree product review stages retain cap 1 with historical usage UNKNOWN;0 new reviews does not reset usage. Both old-machine schedules and delivery owners remain held.
