# Source, integration and resource custody

Delivery custody update — 2026-10-15: all four exact-pin isolated source worktrees and immutable local base tags are established; see [final custody receipt](projects/A-integration/receipts/source-custody-runtime-app-composition.md) and the authoritative current [status](status.md). Setup does not imply BASE or release acceptance. Earlier preparation observations below are retained provenance.

## Source identity

The archive assumes branch `claude/fork-base-20261015`, frozen tag `timeline-r4/base-20261015`, and mutable integration branch `timeline-r4/trunk` in all four repositories. The full branch SHAs were checked read-only against GitHub during packet preparation; future BASE verifies them again. The archive's short pins and claims of local tags/branches are historical claims, not proof that a current local checkout is suitable.

| Repository | Remote | Required base commit |
|---|---|---|
| Astrid (`A/`) | https://github.com/peteromallet/Astrid-agent | `a046263f1f15c4ff90830eb34bb7ae85cd35afe7` |
| Runtime (`R/`) | https://github.com/banodoco/banodoco-workspace-runtime | `ba348514d0f2dc9431dad49f2f3d6f1a03a9db3e` |
| App (`P/`) | https://github.com/banodoco/reigh-app | `434d9bf34606fbbf74f6c9f047e7f1711d59b489` |
| Composition (`T/`) | https://github.com/AstridPseudon/timeline-composition | `6bd784d8e51005ce15b7b9714ea9fb4df9730373` (v0.0.7) |

No live checkout has been selected or changed. The archive's `~/Developer/astrid-video/astrid-local/…` and Hannah paths are historical locations. The current Documents workspace's Astrid, Runtime and App are dirty, have different HEADs, and include a separate active transcript run; the composition checkout was not found. Preserve these roots, their data and running processes. Discover suitable repositories or arrange authorized clones at delivery kickoff; record exact roots and refs without silently using or excluding dirty work.

Current execution simplification093 and artifact-lifecycle229 govern future custody: reuse the task-owned exclusively held receiver across compatible cards/increments. A new checkout is justified only by a real concurrent writer, incompatible environment or required frozen execution. When needed, create it inside the selected repository at `<repo>/.otto/worktrees/<run-id>/`, with the assigned branch (new default `codex/`). A card ID alone does not require another physical checkout or installation. Existing recorded branches/paths and frozen readers keep their identities. Record each repo's root, worktree, branch, base/head SHA, staged/unstaged/untracked state, remotes and protected local material before mutation. Capture dependency/environment identity and run-owned temporary/output paths before expensive work. `.otto` is storage and must remain locally excluded from Git, never force-added. Do not stash/reset/clean live checkouts.

## Merge and artifact custody

A's manager owns all four integration trunks, the merge queue and IP0–IP8. Managers hand back commits; source mutation/check execution is delegated to leaves. Only orchestrator-assigned, dependency-ready cards run. Every milestone is complete only when all participating repositories merge and bounded proof passes. A multi-repo partial merge never completes the milestone: record the landed/unlanded tuple, hold dependents and route repair to the orchestrator.

Rebase each card onto coherent current trunks, re-run bounded checks and fast-forward the isolated integration trunk. Record before/after SHA per repo and the command/result, inspect that scope and tests were not weakened, then complete the milestone in the root tasklist and dependency ledger. A dispatch must consume the current merged dependency tuple, not a stale parallel branch. Oldest hand-backs and broken-check repairs take priority over A's next card. Remove only run-owned completed worktrees/branches after evidence is retained and authorization permits cleanup.

Composition changes merge first in T. A delegates `npm pack` once for that exact commit, retains a SHA-addressed artifact in the selected run-owned output location, records its digest, and repins Astrid `remotion/package.json` and, after PINS-APP, App `vendor/timeline-composition` together. Record the four-SHA revision tuple plus artifact digest in every integration/release receipt. Rollback repins both consumers to the previous artifact and reverts the composition merge. Never call a three-repo tuple sufficient.

Codex owners merge into their own Runtime/App lines. Prepare review-ready PR packets (base/head SHAs, paths, contract delta, bounded tests/migration evidence); record them locally. Sending messages or writing another session's production reply files requires explicit current authorization. Their comments become scoped follow-ups; rejection escalates. Do not write into their trees, push remotes, deploy, or rewrite the frozen base. Import newer upstream tips only as deliberate needed changes with affected proofs, never rerun IP0 merely because a tip moved.

## Resource custody

The older limits and preparation descriptions below are historical where superseded. Current run.yaml adaptive admission/execution simplification and status.md govern actual dispatch and source state; do not reinstate fixed worker/time/disk limits or repeated per-card setup from this archive.

The root configuration retains the archive's WIP limits. A's manager is the sole owner of broad/expensive checks and heavy-job admissions. Workers use only card-bounded tests and authorized light checks; full suites, journeys, renders and parity matrices run at IP0–IP8. PRACTICE agents consume worker slots; IP5's three-agent measurement is a heavy-job exception solely for that measurement.

Use an existing machine-wide serialization mechanism compatible with this packet's no-Otto requirement; record its exact invocation, ownership, weight/time semantics and sharing with concurrent sessions before heavy work. The old `otto-heavy` wrapper is not an active instruction. If no compatible shared lease is available, hold heavy checks while the orchestrator resolves custody; do not start a new service or run unleased heavy work. Equivalent local/off-box execution must preserve inputs, assertions, data custody and measured machine-state evidence. Never signal another session's jobs.

Preserve original weights: light frame/browser/visualize = 1; journey/full suite = 2; full-film render = 3. Heavy durations are about three times the last comparable measured run (initial journey bound 15 minutes); light frame/browser bound 10 minutes. At most one weight-2+ job at a time. Capture lease ID and machine state. Deadline before completion yields `not observed` and one quieter-machine requeue; an observed assertion failure remains failure regardless of load.

Film checks use a disposable fixture or duplicate timeline; an APFS realm clone is an original validation option only when the current user authorizes persistent backup creation. Do not create extra full realm copies during setup. Never touch the live film, `production/`, runtime data, or non-duplicate realms. Real data reaches astrid.haus only after SEC-1…5 pass on the actual transport; live migration and film viewings retain explicit human gates.

Native capacity: discover actual active-agent and nesting limits before dispatch. Ten project managers are logical assignments, launched/resumed lazily; orchestrator, managers, workers, reviewers and oracle all consume host slots. Archive WIP limits in run.yaml are ceilings, never required concurrency. Shrink fan-out for available capacity and keep A attached logically even when its process is idle. If a manager cannot spawn a leaf at the current depth, route the exact brief through the orchestrator without losing manager ownership or escalation order.


## Current Composition source restoration — Delivery139 / integrated005

A admitted005 at12:52:33Z; receipt projects/A-integration/receipts/A-COMPOSITION-EASING-RESTORE-005-source-admission-001.md SHA04dd5e11522c269ed1f7dd1bc62cd86d0b9e3ddd61642767ebc5ed4e2b3c0774. The original owning T locator ROOT/clones/timeline-composition was absent; one exact0d fetch failed. Ruling139 authorizes the truthful new repo there: archive025 payload importf9da6c0477feb73a7d0f13f37bed3e4861254cd2/tree1d92ed9b6a1a77ee382c84205419e878cf49ef4d, no parent/history reconstruction. Fresh source worktree ${ASTRID_EXECUTION_WORKTREE} holds currentT67245fb4f734e2c4d9138e8ab3df87921f51b492/tree23854d166c8692bb8c21f1da1f5ae0203215fb98. The archive is the package payload, not the lost former complete repo/tests/Git history. Preserve old0d/df38/source receipts as historical, not ancestors of this new lineage.

One new archive724b8818d5787687abfc72be9e9cffc185bcbffa9a122dd0a43750be337f62b6 supplies Astridcc6e53fb4366a19bb2178d7627782488ac7c7011/tree95f820ff798af8a8e15c921c640b6e129a29e787 and Apped33ddbb822f4e91362a6cd795636c008fe036df/tree637237a42d767199225dd1cc880c569e738871cb through their fresh in-repo005 receivers. App preserves its existing one-field schema resolver overlay. Both source bodies/inventories are authenticated by the005handback. No live/dirty root or original archive was changed; T remains sole source owner, both vendors consumers. Compiler inheritedexit2/13diagnostics remains explicit. No release/public/visual claim or remote publication authority is added. Full details/paths/proof are in005handbackSHA6bf148988bdfe1aa45229509749b24907bfa26124b74ca7a268e9dae34dd4a69 and CURRENT.
