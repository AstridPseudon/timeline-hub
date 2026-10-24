**4065 remains NO-GO. The first failure is a harness/oracle mismatch before any commit POST; no production repair is justified by this evidence.**

- Exact App commit/tree: `c0fe88994405fd517b58473c14678a0d1b73056d` / `8e3ef15ee5f7c08381d8dc9efb38b5c98845466d`. The recorded snapshot commit `f182af84` has that same tree and App commit as its parent.
- Original Gate5 blob remains `37caf28577d42fbe98afd2320dffa3c72e6e74b1`; SHA256 remains `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`.
- No source, tests, helpers, harness, artifacts, dependencies, or pins changed. No rerun performed.

The first failed expectation is the POST `/commit` response wait at [three-products.spec.ts:1538](/home/user/work/wt/app-P3-D45-original-cause-sol-0501/tests/e2e/local/three-products.spec.ts:1538). It times out after 90 seconds. The following `reset.status() === 200` assertion is **unreached**, rather than failed.

The retained canonical revision places `f2-app-clip` at **0 seconds** and the reference clip at **15 seconds**. Gate5 nevertheless invokes a **5→0** reset. The [drag helper](/home/user/work/wt/app-P3-D45-original-cause-sol-0501/tests/e2e/local/support/app.ts:273) consequently calculates 48 px/s and moves the pointer from x=181 to x=−59. The trace shows the drag ghost remaining at the timeline origin.

Source explains the absent mutation: [drop positioning clamps time to zero](/home/user/work/wt/app-P3-D45-original-cause-sol-0501/src/tools/video-editor/lib/drop-position.ts:131), [document diffing returns null for empty changes](/home/user/work/wt/app-P3-D45-original-cause-sol-0501/src/tools/video-editor/commands/documentPatchIntent.ts:216), and [the local session returns without appending that intent](/home/user/work/wt/app-P3-D45-original-cause-sol-0501/src/tools/video-editor/commands/localSaveSession.ts:310). **High confidence:** the isolated case assumes a prior 5-second state that its fresh fixture does not supply. The trace does not instrument every internal callback, so the precise internal return point remains inferred.

| Boundary | Retained evidence |
|---|---|
| Connected editor, immutable reads, owner readiness | Reached; fresh scoped owner has empty intents and no pending request |
| Initial reset commit | Zero commit POSTs; response wait fails |
| Outbox → door → Runtime37eb → Agent079 → reply/adoption | Mutation chain unreached; no request body, key, receipt, or mutation head transition to inspect |
| Accepted A, intervening Agent C, lost ACK, newer B | Unreached |
| Exact retry, reload persistence, restart, recovery | Unreached |
| Merged B, canonical closure, guarded undo, history tail | Unreached |
| Zero old routes | No film-write traffic observed in this prefix; final assertion unreached |

This is neither a demonstrated provider refusal nor a demonstrated Runtime/adoption defect. Actual daemon/provider import provenance remains **UNKNOWN** from the retained Gate5 evidence; selected pins and installed-backend qualification do not prove those imports.

Historical P1 used **App f8 / Agent787 / Runtime2a9**, a one-video parent fixture with empty shot/internal closure. It passed split→trim/restart/retry and refusal/rollback cases. Current Gate5 uses **App c0fe / Agent079 / Runtime37eb**, the three-products fixture and nonempty child closure. Historical P1 GO cannot transfer.

Retained execution commands/results:

- `npm run test:e2e:three-products -- tests/e2e/local/three-products.mounted-readiness.spec.ts` — **1 passed**, 16.7s test / 35.9s process.
- `npm run test:e2e:three-products -- --grep 'M2 real gate 5 \(M1 real mounted path\): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent$'` — **1 failed**, response timeout; complete retained service run **exit 1 / 277s**.
- Native fixture/history GREEN is recorded in the retained log. Joined **523 tests, three typechecks and lint** remain background source qualification.
- Executed here: `git diff --check`, unstaged/staged `git diff --exit-code`, and clean-status/hash checks — all passed.

**Next owner: Proof.** Independently adapt fixture/setup isolation while retaining the original reset expectation and every downstream authority/read/key/closure/owner/recovery/history assertion. No weakening or product fix here. Commit message and empty `DONE` marker created.