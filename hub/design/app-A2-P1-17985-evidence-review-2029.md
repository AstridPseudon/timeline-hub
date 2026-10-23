# A2/P1 actual17985 independent retained-evidence review

## Verdict

**FAIL for causal completeness / P1 GO.** The authored result is supportable as a bounded, read-only stage diagnosis, but it does not establish the exact originating guard or the downstream P1 chain. **PASS** for retained-artifact custody, strict safe-export scope, protected source identity, and the observed App-local stage. Proof should retain the P1 second-POST assertion and keep the overall P1 NO-GO.

## Findings

The retained D26 run is the pinned App base `be890a1fa5d6db02e4964522aa356f88f115a22a1` / tree `f794d795dbefc2ead9a3f770a7566826da2b1f4e`, with one pass and one failure in 460 seconds. The first case passed in 30.5 seconds. The second case timed out while polling for two page-observed commit POSTs; it observed one. Agent move, second trim request, Runtime refusal/409, and App rollback assertions were unreached.

The retained JSON is 12,296 bytes and the trace/error-context/raw-log artifacts remain private in the run folder. The authored safe JSON is byte-equal to the retained JSON. The export audit is finite and allowlisted; no raw trace/network body, credential, principal, header, cookie, full URL, or sensitive hash was exported. Mounted capture data, callback patch, original basis transition, capture result, and mounted data reference remain `UNKNOWN`. The later outbox snapshot is one idle owner at generation 1 with zero intents and no pending request; it is not a capture-time state.

The original source identities independently match: first P1 case lines 1339–1506 (`4b04ad7e…`), second case lines 1507–EOF (`2f750118…`), entire P1 spec (`be63db71…`), and Gate-5 blob `37caf285…`. No original assertion was weakened.

Private trace inspection confirms the cited order in case 2: selected right clip → Timing tab → visible Source In `0` → fill `3` → Enter → Tab → conflict dialog, before the second page-observed POST. Final retained DOM shows Start `2`, Duration `5`, Source In `3`, Source Out `8`, Speed `1`. The two HTTP-200 network records around the split are forwarded/duplicate observations before input, not a second authored trim. These facts support an App-local save/conflict boundary, but they do not identify the rejecting guard or prove a particular mounted payload, `hold`, owner transition, or basis transition.

Against PLAN A2/P1, contract items 1–5, and D24/D25/D26, the case-2 evidence cannot credit the merged/refused dependent chain or its exact conflict/recovery assertions. Whole P1 is therefore **NO-GO**. Do not invent Runtime409, `mountedDataRef`, or a causal repair.

Prospective producer `201044ee60` was absent from actual17985. Its bounded events could cover schedule/capture/basis/owner/adoption ordering, but its rejection projection is fixed `errorCode: operation-rejected`, with `errorClass` and pending-intent count `UNKNOWN`; it cannot identify the exact historical guard. Adapter compatibility was not a historical qualification. Any future qualification must remain separate and bounded.

No source or test change was made. `git status --short` was clean, `git diff --check` passed, and no tests/typecheck/lint/browser/service run was performed.
