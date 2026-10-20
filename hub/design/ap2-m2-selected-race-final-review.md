# ap2-m2-selected-race-final-review

## Flat verdict

- **Source graph/history repair: APPROVE for the repaired source mechanics.** `loadTimelineCommandBasis` captures the first accepted head, validates every paginated head, rejects cursor cycles/head drift, reads the pinned parent/shot/internal materialization, and returns the existing canonical document plus graph. The session resolver forwards both. The resolver rejects reversed authenticated item order, incomplete predecessor chains, missing occurrence materialization, and structural reorientation; it returns only the accepted direct-triple P1 and never refreshes/relabels it.
- **Async selected-authority qualification: HOLD.** The repaired hook fences generic bootstrap/poll display adoption, but the existing race tests do not invoke `resolveSelectedParamAuthority` while a read is pending. `basisRef` is cleared when the session effect starts/tears down, but not when each poll effect starts, and accepted command projections do not update it. Thus an old prepared basis can remain available while a newer poll/accepted command is in flight. This is not proof of the requested “original history/head/bundle/generation before async read, same fence on adoption, clean only its own prepared basis” behavior; the final join needs a narrow basis-lifetime fix plus an accessor-specific race control.
- **Shared proposal/final join: NOT QUALIFIED.** `DataProvider`/`RuntimeDataProvider.paramReadClient` and the retained Runtime client methods remain a private seam proposal. No PropertiesPanel/Provider production PARAM capture/submit join exists here. Native PARAM production remains unqualified; prop wiring would not change that.

## Source checks

- Canonical graph/materialization: PASS by inspection. Occurrence resolution requires a unique occurrence, shot revision, internal timeline and matching raw clip; document/graph disagreement refuses.
- History: PASS. `selectedParamAuthority.ts:78-115` validates predecessor ancestry and exact supplied order. Runtime pagination at `dataProvider.ts:789-818` validates first/later heads, freezes the first head, and rejects cursor cycles/head drift.
- Visible refusal/draft preservation: PASS in the resolver’s existing error path for malformed/incomplete/order-changed history, missing materialization, inverse/legacy-after-selection and reorientation.
- Original-pin policy: PASS as source-only logic. No latest catalog, HA relabel, synthetic binding, new DTO/store/pin, or browser validator was added.

## Evidence

- Focused Vitest: 5 files, **149 passed**.
- Existing async-race controls: **2 passed** (late-poll fence and project-switch race; these are generic session controls, not selected-accessor proof).
- Existing malformed-head controls: **2 passed** (first-page and later-page malformed history head).
- Locked native Agent lane: **27 passed** using `/home/user/work/venv-app2-native` and read-only `/home/user/work/agent`.
- Strict project types: `npm run typecheck:strict-islands -- --pretty false` **passed**.
- ESLint on repaired source: **passed**.
- `git diff --check HEAD^ HEAD`: **passed**.
- The requested 181+19 source lanes are absent from this assigned current-root tree and are **not claimed**.
- No full, browser, localhost, live-socket, e2e, source edit, new test, dependency, pin, Git, or ledger operation was performed.

## Recommended next steps

1. Have the App owner join the private DataProvider/Provider seam only after fixing basis lifetime: invalidate/retire the prior basis when each async selected-authority read starts, and publish a prepared basis only after its exact history/head/bundle/generation fence passes; clear only if the ref still belongs to that read.
2. Add the missing accessor-specific async race/restart/removal controls, then separately qualify native PARAM capture/submit and draft-retention behavior.

