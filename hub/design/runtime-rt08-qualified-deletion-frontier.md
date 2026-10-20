# RT08 qualified private deletion frontier

Date: 2026-10-20

Status: **PRIVATE / HELD.** This is a current-base Runtime source delta and
adoption handoff. It is not a public pin, release, integration-ready
code-only switch, or RT08 deletion. The ledger row remains **OPEN** until the
matched Agent/Runtime artifacts are adopted and the orchestrator authorizes
the deletion.

## Decision

No original identity-only behavior remains unqualified in the private 952
tuple. The evidence covers the original occurrence/identity, lost-ACK and
restart, materialization/version/map, and schema/client cohorts, and the final
private HTTP pair covers the original semantic batch reload/inverse/redo and
lost-ACK/restart/key/body/receipt/strict-inverse controls.

The remaining unqualified item is adoption of the new source-bound allocation
form on current integration. It is not an original identity-only behavior:
the current public schema still refuses its typed source/item references, and
the current integration has not adopted the private 952 artifacts. Therefore
the old blanket admission cannot be marked deleted yet.

## Original behavior and evidence

| Original behavior | Evidence | Qualification boundary |
| --- | --- | --- |
| Empty `id_map` and identity pairs continue through the ordinary path without source claims or allocation authority | Existing Runtime identity-map controls; Agent private pair preparation retained the occurrence/identity cohort (**51 passed**) | Preserved. The current branch does not change this path. |
| Accepted ordinary edits retain exact request/retry identity across lost acknowledgement, restart, inverse and redo | Agent private pair preparation: lost-ACK/restart subset (**17 passed**); final private HTTP pair `agt-m2-private952-http-reload-finish-private952-sockets-integration-1020193342-28209` (**44 passed**) | Private pair only; no public adoption claim. |
| Materialization/version/map and schema/client compatibility behavior remains intact | Agent private pair preparation (**66 passed**, **59 passed** respectively); Runtime 952 schema/generator lane (**147 passed**) | Private 952 tuple only; public 0.2.13 and ordinary 0.2.14 remain frozen. |
| Reloaded source closure is compared by canonical authoring fields while GET decorations remain preserved | Agent source-shape repair: six-case reload (**6 passed**); native ingress (**40 passed**); final pair retained the exact selected ingress (**40 passed**, six-case subset **27 passed**, direct adapter neighbors **53 passed**) | Source repair is private Agent evidence, not a public pin. |

The final native qualification is the exact Agent `909bfad8...` / tree
`3775e2e...` with normal private Agent pin `a53703ce...`, paired to Runtime
`95202c2b09e83aaae028287d6c59b773410141f3` / tree `d438d3e...`. The one
central HTTP run was **44 passed in 55.07s**, result
`agt-m2-private952-http-reload-finish-private952-sockets-integration-1020193342-28209`.
The wrong-source prior run was cancelled and receives no qualification credit.

## Current-base delta

This branch carries the independently reviewed source-bound join onto current
Runtime `8f105c2` without importing the obsolete `3730`/`f802` or incomplete
union artifacts:

- `runtime_protocol/timeline_materialization.py` is the closed, read-only
  join. It authenticates the exact parent/source pin, occurrence owner,
  source membership, bijective item map, sealed bindings, current before/after
  edges, and canonical closure digests. The derived map is evidence, never a
  caller-granted authority or a semantic birth.
- `runtime_protocol/timeline_commit_port.py` invokes the join from the
  request-private captured closures and compares source-bound bindings to the
  sealed request. It keeps the existing authorization, captured revision/shot,
  selected-media CAS, text/narration, document-input, and current-source
  revalidation guards.
- `runtime_protocol/timeline_commit_store.py` removes only the unconditional
  nonidentity-map refusal. It routes nonidentity maps through the join,
  preserves identity-only maps, checks authenticated inherited inverse
  provenance, and retains current catalog/headless/occupancy/identity/CAS
  fences and ledger-first retries. Semantic creation reservations remain a
  separate path.

There is no schema, DTO, API, table, version, generated-client, manifest,
public artifact, or service-route change. `public013` and ordinary `014` are
unchanged. Since the current schema remains unchanged, the existing public
schema gate still refuses typed item/source-bound claims before provider
execution. This branch is consequently a source/adoption candidate, not an
integration-ready switch.

## Remaining adoption dependency

The matched adoption step must use the independently reviewed private tuple:

- Runtime `95202c2b` / tree `d438d3e...`, unpublished internal `0.2.14`;
- Agent source `357230816c86da65d5f8cc92b10a3a90d29874e0`, tree `94692e...`;
- byte-identical raw command schema SHA-256
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`;
- Runtime raw bundle `4a0779...`, health digest `ddf6396d...`, and artifact
  manifest `b397e5...`.

Adoption must happen through normal generation/vendor-lock checks, preserving
the current public/ordinary floors and all existing assertions. Then one
matched native pair must exercise the typed source-bound positive and its
current catalog/headless/CAS/text/current-source neighbors. Until that lands,
the current branch must keep the public refusal and ordinary identity path;
do not mark RT08 `DELETED`, publish 952, or merge this candidate as a
code-only behavior switch.

## Evidence not rerun here

The reviewed source-join evidence was read, not duplicated: the approved
current-source join lane recorded **199 passed**, the raw/ordinary neighbor
lane **148 passed**, and the central neighbor lane **65 passed, 16 deselected,
10 unchanged xfails**. Those runs were on their recorded source snapshots and
are not relabeled as current native qualification. No comprehensive native
rerun or full suite was requested.
