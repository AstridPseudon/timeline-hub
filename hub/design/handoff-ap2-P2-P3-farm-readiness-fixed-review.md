# Flat review: App P2/P3 farm-readiness handoff — FAIL

Verdict: **FAIL; no P2/P3 acceptance credit.** The repaired handoff closes the
prior forbidden-xfail, v1/v2-status, two-source history, Gate-5 ordering, and
suite-registration findings substantially, but it still needs exact contract
and current-implementation corrections.

## Closed prior findings

- Lines 29–34 and 154–156 correctly require original successful snapshot-route
  journeys to migrate as passing tests and explicitly forbid `it.fails`,
  `xfail`, skips, weaker expectations, and refusal expectations.
- Lines 36–57 correctly classify the inspected App as v1/native only, including
  `accepted|rebased` versus v2 `merged`, absent request `steps`/`merge`/`reads`,
  and absent v2 authoritative step history.
- Lines 59–84 correctly require both network `COMMITS` POST and Runtime
  `/commits` evidence, publication-ID joining, intended-field deltas, reload,
  mounted guarded Undo, command records, step records, and inverse records.
- Lines 111–146 correctly separate Gate-5's fixture reset from the adversarial
  sequence and preserve App A → Agent C → lost ACK → dependent B → reload →
  Runtime restart → exact A retry → B recovery → guarded Undo.
- Lines 174–188 correctly report only `full-e2e-three-products` and the
  non-P2-specific `e2e-m1-gesture`, with no P2/P3 named suite; this is a future
  farm dependency, not grounds to demand a new launcher or heavy run now.

## Required corrections

1. Add the exact §1 compatibility defaults: omitted `label` → `"Timeline edit"`;
   omitted `steps` → synthesized `{id: "edit", label: commit label,
   intent: "", tags: [], command_ordinals: all commands}` with provider-derived
   complete patch; explicit empty/null label or steps invalid; omitted `merge`
   → `"fields"`; omitted `dry_run` → `false`.

2. Name the missing PLAN prerequisites explicitly: R1/Agent's `doc.patch`
   semantics, previous-value/read/conflict/inverse handling, and U4p/App's
   adoption of the regenerated U1 schema/client. Do not invent a new route or
   launcher.

3. Use exact history field names from contract §7: `merge` (requested),
   `merge_mode` (effective), `reads`, `steps`, `records.steps`,
   `records.commands`, `records.undo_steps`, and `records.undo_of`, plus
   `label`, `publisher`, `intent`, `records`, and `receipt`.

4. Clarify the current pagination API: GET
   `/v1/projects/{project_id}/timelines/{timeline_id}/commits` currently accepts
   `limit` and `cursor`, returns `head` and `next_cursor`, and binds the opaque
   cursor to the fixed through head. There is no current `through` query
   parameter; if a future explicit query is required, mark it pending rather
   than present.

5. Correct the line-53 citation: only lines 1050 and 1186 are the M1/Gate-5
   status assertions; lines 1352 and 2001 belong to ordinary-extension and
   mixed-editing journeys. The stale `rebased` observation remains valid.

## Evidence and limits

The App worktree was clean at `8b979bd2139c96e029dbc42be9a47f4309c8ee37`
(`e5cde440ce2f31bd0e20dbf2bb7d9d5cbd9d09da`). Static reads of the contract,
App DTOs/tests/config, Runtime service/server, and `tests/suites.conf` confirmed
the findings above.

`npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts tests/e2e/local/three-products.selected-param-dev.spec.ts`
passed list-only with 14 tests in 2 files.

`npx playwright test --config playwright.three-products.config.ts --grep 'M1 real' --list`
passed list-only with 3 tests in 1 file.

No browser, localhost, live socket, integration, farm, full, or heavy suite was
run. Typecheck/lint are N/A for this zero-source-delta review. No product,
tracked file, test, schema, pin, launcher, selector, suite configuration, or
process was changed.
