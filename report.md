# F-D22 final census-return review

Final review: **FAIL for the return artifact**. The corrected classification
and terminal inventory are **PASS separately**.

## Preserved evidence

- Service `agt-F-D22-full-1342-full-current-v3-1229-1023134453-10679` remains
  terminal **FAIL**, exit 1: 185 failed, 19 errors, 16,733 passed, 4 skipped,
  565 passed subtests, 86 warnings, elapsed 3712.16 s.
- Agent `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`, Runtime
  `3b926efab2eed122d374540baee297d4cdcec62a`, and profile archive
  `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234` are
  unchanged. Raw terminal SHA-256 is
  `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.
- The corrected JSON has 204 unique entries and these exact groups: 17
  child-probe, 87 child-import-or-recipe, 11 custody-process-assertion, 2
  fixture-declared-gap, 23 g5-inverse, 37 profile-fixture, 9 child-import,
  1 d13-preflight, 7 r1-private, 2 g5-publisher, 2 g5-schema, 1 r3-docs,
  3 d09-probe, and 2 r5-retired-route. Sum: 204.
- Four skip identities remain unavailable; `u=565` remains passed subtests;
  xfail/xpass and deselection remain zero; D14 and D23 remain unexercised;
  Base583 remains distinct from the actual 8c355 run. No upstream,
  pre-existing, deferred, or PASS credit was added.

## Classification audit

The 11 named custody/process nodes are correctly separated from the former
97-node environment group and remain source-backed but unconfirmed. Their
raw/source causes are: network denial and engine-fd assertions at
1972–2028/2031–2087 (`child_exec_from_environment`); empty observation at
12988–13083 (`_run_command_definition`, `_observe_owned_review_session`,
`_retire_owned_review_session`); absent shutdown markers at 13084–13332
(`GenericPackHost.run_task`, `shutdown`, `_ManagedTaskAdapter`,
`verify_tree_absent`); and unexpected
`ASTRID_TIMELINE_SCHEMA_PYTHONPATH` at 14790–14924
(`_child_environment`, `_launch_worker_probe_environments`,
`_run_command_definition`, `_registry_context`). The exact 11 IDs and their
allowed files/acceptance briefs are retained in the flat handoff and JSON.

The Remotion owning-pack-root node is correctly moved from profile to the
87-node environment group: its source is
`tests/packs/rendering/test_remotion_backend.py:672–700`, and the raw trace at
14927–14960 ends in `ModuleNotFoundError: runtime_protocol` (summary line
22648). The remaining 37 profile nodes correctly stay unconfirmed: 14
archive 80-vs-77, 9 composition 0.0.14-vs-0.0.13, 11 missing
`chunk-SE4TPVLW.js`, and 3 unmapped generated scopes. These are causal
profile/oracle mismatches, not non-regression claims.

## Return defects

1. The corrected JSON entry for the moved Remotion node says
   `raw-terminal.log:2252x`; that is not the node’s raw failure window.
   The authoritative window is 14927–14960, with summary line 22648. The
   flat handoff has the correct window, so this is a JSON evidence defect.
2. The return reused and overwrote the original
   `agent-F-D22-terminal-classify-1442-e0036c850d1a7b7c.json` path. No
   separately named return JSON with a new hash was produced, so the original
   completed-1442 artifact is not independently retained as required.

## Commands and results

No tests, type checks, lint, provisioning, environment qualification, or full
suite were run. Read-only checks were:

- Python structural/raw/source audit: **PASS** — 204 unique entries, group
  sum 204, all 11 custody IDs plus the moved ID present in JSON/flat/raw;
  identities/counts/guardrails match.
- `sha256sum raw-terminal.log`: **PASS** —
  `e0036c850d1a7b7c78d14e3d287350795ccb8c4b03c9cd30103d9f8b9a3c60a5`.
- Corrected JSON SHA-256: `cc8b7d96dadaa6f9022a064fcd5a5db3d72f008b1565afc1f63c72e4adbcc397`.
- `git diff --check`: **PASS**; no product, test, schema, pin, dependency, or
  merge changes.

Recommended next step: preserve the original 1442 JSON, write a distinct
return JSON named with the new content hash, correct the `2252x` evidence field,
and rerun only the static audit.
