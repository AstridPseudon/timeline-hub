# F unconfirmed13 independent review

## Result

**FAIL for qualification; PASS for inventory/static audit.** The central
bounded service result is `agt-F-unconfirmed-env-0900-targeted-1023090053-24359`:
13 collected, **9 passed / 4 failed**, exit 1, 23.44s, on Agent tree
`6f7649a4e0b8f1d936dc94a5fa0bb7c5fb3db276`.

The full run is the sole `agent-full-1023072419-4249` result on snapshot
`fcc33e0eb964dd48d422673e8f692f195c88748c`, Agent commit
`d24da4af0f1ca83880b4b9ef57559e28ebe52a2a`: 240 failed, 16,388 passed,
140 errors, 40 skipped, 5 xfailed, exit 1, 4,269.86s.

## Inventory finding

The 11 bounded selectors expand to exactly 13 unique parameterized node
identities. Read-only comparison against the full report's 24 unconfirmed
nodes found no omitted or duplicate identity; the bounded set is an exact
subset. The actual PASS count is nine, correcting the prior prose count of
seven. No full/new-head, upstream-431, or D14 credit is earned.

## Findings

- **PASS, nine exact nodes:** the exact idle/host/structure identities are
  listed in `Externalreport.md`, including both claimed-task parameterizations
  and the structure-pack node. This is bounded durable-environment evidence
  only.
- **FAIL, D13:** the exact installer profile/bindings/native/browser/tool
  fixture tuple is absent, including the required D13 profile, regular
  bindings file, digest fields, and executable paths. Owner: farm/installer.
- **FAIL, legacy assembler:** the minimal test record has no `adapter`, so
  `_renderer_selection` at `generic_host.py:1639` raises before the intended
  immutable-publication refusal at the subsequent scope check. Owner: Agent
  generic-host/admission; upstream status untested.
- **FAIL, installer ×2:** `Backend.runtime` launches `version.python -I -m
  astrid_runtime`; the exact isolated probe returned `ModuleNotFoundError`,
  so no repair/PID assertion ran. Owner: farm/installer.

## Static caller/contract check

The production path is `Timeline.open` → `TimelineSession` outbox flush →
`client.timelines.commit` → `WorkspaceClient.commit_timeline` → generated
canonical `/v1/projects/{project}/timelines/{timeline}/commit` POST with the
Idempotency-Key. The canonical render action constructs the actual
backend-neutral `RenderService`, whose registry selects and invokes the actual
backend. Static Runtime types/schema retain the complete v2 request and
reply surfaces: scope/base pair/commands/label/steps/merge/reads/key/dry-run/
source/rationale/group; `{data,receipt}`; accepted/merged/historical rebased;
head/document/records/dependencies/effects/steps/history/undo_steps;
preview `would_status`; conflict reason/head; and invalid code/path/hint/
suggested command. This is static evidence only.

## Limits and next owners

No source/test/product/environment/pin/schema/contract/shared-dependency
change was made. No full, browser, heavy journey, P1/P4 HTTP, native14,
crash24, or D14 run was performed. The only new diagnostic was the exact
isolated installer import probe. Farm owns D13 and isolated Runtime
provisioning/durability; Agent owns the minimal admission-record repair.
