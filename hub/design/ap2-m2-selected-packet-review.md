# ap2-m2-selected-packet-review

## Flat verdicts

- **Current-root resolver branch: APPROVE as source-only authority logic.** The resolver is based on current root `0034cc30e`, restores the accepted `c90277edd` helper shape, and uses only the accepted history direct triple (`schema_source`, `params.schema`, exact `params.snapshot`, fixed `params.element` binding). It does not use a latest catalog, manifest winner, HA relabel, authority store, browser validator, or synthetic binding. Parent/occurrence scope checks are conservative; missing, pending/raw-invalid, ambiguous, incomplete, reversed, legacy-after-selection, inverse, and structural-reorientation cases refuse while retaining the draft.

- **Authenticated shared seam proposal: REQUEST CHANGES before merge.** The four-file patch is real and applicable, but the session accessor has two correctness gaps and the pagination boundary needs one more fail-closed guard:
  1. `useTimelineCommandSession.ts` calls the resolver with only `history`, `head`, `select`, and `rawClip`. It does not pass `basis.canonicalDocument` or `basis.graph`, so every occurrence-scoped selection lacks the concrete owner/shot identity required by the resolver and refuses even when the accepted basis contains that identity.
  2. The poll callback stores `basisRef.current = basis` before checking that the fetched head matches the current head. On a head race it returns without `session.observe`, but leaves the unadopted basis available to the synchronous accessor. Cleanup also does not clear `basisRef`, so a new/closing session can briefly resolve against a prior session's basis. Update the ref only after the same acceptance guard as `session.observe`, and clear it on teardown/loading.
  3. `loadTimelineCommandBasis` dereferences `firstHistory.head`/`next.head` before validating that each page has a concrete head. Missing or malformed page heads should produce the existing schema-incompatible refusal, not a raw `TypeError`; retain the frozen-head, cursor-cycle, and final predecessor/order checks.

  The proposal remains a seam for App to finish; no DataProvider/Provider final join or production activation is claimed here.

- **Row-local PropertiesPanel proposal: APPROVE as prop-only seam; HOLD production activation.** Its two nonempty hunks only add optional retained-pin/TimelineOps/command-state props and forward them to `ClipPanel`; they add no capture, submit route, direct POST, DTO, store, or native PARAM claim. App still owns the Provider join and must mount the accessor result only after successful authority resolution, with the existing pending/refusal draft retention preserved.

## Evidence

- Current worktree focused Vitest: `selectedParamAuthority.test.ts` plus `dataProvider.test.ts` — **81 passed**.
- Private current-candidate combined lane (six files) — **181 passed**; `commitSession.selectedParams.test.ts` — **19 passed**. The six files were selected resolver, Runtime data provider, retained-input bridge, selected/lifecycle/mounted PARAM panel controls.
- Qualified native Agent archive at `47c1ee60`, read-only `/home/user/work/venv-app2-native`: selected authority suite — **27 passed**.
- Direct native refusal probe against that archive (reversed authenticated history page and parent `config.clips` reorientation) — **2 passed**; one pre-existing unknown-mark warning. The isolated Agent fixture maps its Runtime ABI exception to the test provider exception for this direct probe.
- Existing portable counterexample replay over the current TypeScript resolver — **2 cases, `exactParity=true`**.
- Private overlay with both proposals applied: targeted ESLint (`--max-warnings 0`) — **passed**; `npm run typecheck:strict-islands -- --pretty false` — **passed**.
- `git apply --check --whitespace=error-all` for both shared and row-local patches — **passed**; `git diff --check` — **passed**; review worktree clean.

No source/test/dependency/Git/ledger changes were made by this review. No full, browser, localhost, live-socket, or e2e suite was run.
