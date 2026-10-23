# P1 mounted-chain bounded repair

Completed the two assertion groups requested after review0309, on App base `d054162c9`. Only product-repo change: `tests/e2e/local/three-products.p1-chain.spec.ts` (+18/-0). All existing assertions remain; no skips, xfails, product/harness/fixture/generated/pin/lock/suite changes.

## Changes and derivation

- The merged canonical new clip must retain the entire foreign `app['org.example']` namespace, own `clear: null` value, and absent `app.astrid`, alongside the existing opaque-field assertions.
- Every refusal conflict must have kind/ref, a string-token path array, tagged base/theirs/ours states, and choices. Require an `atomic_scope_changed` entry at physical `ref: 'parent', path: []`, and the same root path in structured details.
- This root address is intentional for the original intended from/hold-only trim with absent app.astrid: those field writes are disjoint from the Agent move's at/intent writes, but the omitted-read patch guards the entire parent scope. It is not a guessed clip field or native `parent/clip:...` alias.
- Sources: ORCH `design/commit-v2.md` §§1–5,7 (especially §§2–4); official Runtime `780da6d6:contract/schemas/timeline-commit.json` definition `Conflict`; App `9b7e7b59:src/integrations/runtime/timeline-commit-types.ts` types `Conflict`/`AgentState`; Agent `cedc07280d2e97b4210544f3772d2f6978751714:astrid/sdk/timeline/_commit_patch.py` lines 448–453 and 768–787, `_doc_patch.py:102`, `_command_state.py:13`, and `commit.py:1153`. Atomic dependencies use parent/[]; the rebase scanner emits that guarded physical address; CommandError serializes the required conflict shape. No response is synthesized.

Preserved pending split → locally authored trim of the stable created ID, both interleaving boundaries, Agent acceptance before trim fetch, required modern merged status, post-durable-acceptance lost ACK, exact original request bytes/key/full reply replay, one history entry, order/creation/before guards, canonical raw/opaque/null/absence checks, step dependencies and legacy-route observation. Request scope/base IDs, api_version 1, commands, label, steps, optional reads, merge and dry_run assertions are unchanged.

## Static acceptance

Run from `/home/user/work/wt/ap2-P1-chain-sol-0327`; `TMPDIR=/tmp/w-a841d33b43` for Node/npx commands. The worker's ORCH `tmpdir` file points to that private scratch directory. Shared node_modules resolves to `/home/user/work/app/node_modules`; it was not modified.

| Exact command | Result |
| --- | --- |
| `node node_modules/playwright/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.p1-chain.spec.ts --list` | PASS, exit 0, exactly 2 tests in 1 file |
| `npx tsc --noEmit` | PASS, exit 0 |
| `npx eslint tests/e2e/local/three-products.p1-chain.spec.ts --max-warnings 0` | PASS, exit 0 |
| `git diff --check` | PASS, exit 0 |

No browser, socket, test-body, full or heavy run; no central test request.

## Current joined A2 assessment (read-only)

Assessed `hub/tl/app-A2-official780-current-join-r6 = 9b7e7b59cb0de98a0c08d654dfe9165ced892f1e`. The production caller is present: `useTimelineSave.ts:201` constructs the handoff and `useTimelinePersistence.ts:1008` captures local documents. Parent-only ownership permits this seed without substituting a parent document for a child. Collection does not demonstrate that this production path executes successfully.

Concrete incompatibilities remain, reported rather than repaired under this bounded brief:

1. **Original split semantics:** `lib/editor-utils.ts:138` treats any numeric hold as a hold clip. This seed has hold 8. `splitClipAtPlayhead` lines 306–319 spreads the source into both halves and changes only hold/ID/at, retaining source windows and app.astrid.for. The original spec requires source-window splitting and absent right app.astrid. These unchanged assertions cannot be satisfied by that branch. The handoff encodes local changes; it does not turn that edit into a Python semantic split.
2. **Source In locator:** `ClipPanelBody.tsx:378` renders FieldLabel beside NumberInput without id/aria-labelledby. `clip-panel-primitives.tsx:16` renders FieldLabel as a div, and NumberInput has no automatic association with it. The spec's unchanged `getByLabel('Source In')` has no matching label association in this source.
3. **Required merged landing:** `timelineLocalSaveHandoff.ts:188` supplies no reads/merge to appendDocument. `documentPatchIntent.ts` preserves omission; `localSaveSession.ts:166–169` consequently sends atomic. C0c §3 requires refusal when the intervening track label changes the same parent scope. Thus the original required merged trim after that Agent label cannot currently succeed. No inferred empty reads, alternate executor, split port or weaker status assertion was introduced.
4. **Existing refusal absence expectation:** Agent `capture.py:226–232` creates app.astrid and writes fixed_start/for for a native move. The original refusal test's final absent-right-app.astrid assertion conflicts with that canonical Agent move state. It remains unchanged as required; the orchestrator must settle this seam before a real proof.

## Limits and next steps

This repairs source assertion coverage only; it does not qualify H3 or the real mounted chain. Accepted, merged and conflict/refusal are encoded but their bodies were not executed. Invalid code/path/hint, preview would_status accepted|merged, historical rebased receipt replay, and undo variants were not executed; their official wire definitions remain untouched.

The retained seed is the existing bounded parent/media scenario, not the entire original real-document corpus. `tests/fixtures/p1-feasibility/cases.json` contains descriptors referring to App trim/label/move/batch fixtures, Agent split/trim/tiny3 fixtures and the existing e2e seed/recovery harness; none was replaced.

Next: independent Luna source review; orchestrator/App/Agent owners resolve the concrete seams above without weakening original intent; import only this spec onto the reviewed current A2 stage and qualify its production caller through the existing central runner. No commit, merge, checkout, ref mutation or push was performed.

