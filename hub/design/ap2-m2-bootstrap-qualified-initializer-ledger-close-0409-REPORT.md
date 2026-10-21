# Bounded initializer ledger closure

## Result

The bounded `D01-app-bootstrap-default-initializer` sub-entry is marked `DELETED (bounded sub-entry)` in both `deletion-ledger.app.md` and `deletion-ledger.md`. The broader `D01-app-bootstrap` row and Wholebootstrap/D04 remain open.

## Evidence

- HOME integration merge: `1557c312b999ddc0a21c1728acbc64052ef6491f`; candidate deletion commit: `5c53ed21f94fd944e03642d1b6e007760082143c`; current tree: `cf94daef960fe1426f6f50e4000b00c0fc42867e`.
- The candidate diff reports `12 additions, 28 deletions` in `src/integrations/runtime/createDefaultTimeline.ts`; an independent deleted-line count reports `deleted_lines=28`. The removed legacy helper/call path was the old `publishEmptyTimeline` publication body and its create/repair callers. `git diff --check` passed.
- Current initializer code delegates through `RuntimeDataProvider.initializeNativeBootstrapTimeline` and has no `publishParentComposition` call. The remaining precise headless carrier is `src/integrations/runtime/dataProvider.ts:295`, which still invokes `this.client.publishParentComposition`.
- HOME status at 2026-10-21 04:02 records native proof `1021034025-7782` as PASS1/exit0 on App `f045`/tree `642b`, Agent `6ef`, Runtime `95bd`, public13: create/init, lost ACK, exact original request/key/body, reload, restart, outbox drain, two ordered raw history rows, and raw readback. All 17 current1557 activation paths were byte-identical; implementation325 and independent288 focused tests passed. Native activation is current1557; published013 rollback27912 is historical.

## Remaining action

Qualify and cut the HOME-owned headless caller at `dataProvider.ts:295`, then coordinate D04/WC10 closure after the remaining Agent peer callers migrate. This bounded deletion does not close Wholebootstrap/D04.

## Verification and limits

- `git -C /home/user/work/app diff --numstat 5c53^ 5c53 -- src/integrations/runtime/createDefaultTimeline.ts` — PASS (`12 28`).
- Deleted-line count over the same diff — PASS (`deleted_lines=28`).
- Current-source caller scan — PASS for native initializer delegation and the remaining headless caller at `dataProvider.ts:295`.
- `git -C /home/user/work/app diff --check 5c53^ 5c53 -- src/integrations/runtime/createDefaultTimeline.ts` — PASS.
- Own worktree status — clean.
- No tests, browser, build, or replay were run, per task instruction. No separate r26 report artifact was present in the reviewed shared paths; the HOME 04:02 status and merged source supplied the closure evidence. No conflicting active ledger owner was found.
