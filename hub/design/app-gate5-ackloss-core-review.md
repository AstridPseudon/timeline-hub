# Gate 5: new intent after uncertain ACK — core review

Worker: app-m2-ackloss-new-intent-unit. Base: App `1be0efdde` (ROOT8). Source-only work on the existing clip.move capture port, commit session and IndexedDB outbox. M1 is not reopened by this report.

The new case exposed a bounded core bug: after fake transport acceptance of A5 and a lost ACK had already produced session status `retry`, submitting a newly captured B7 automatically called the pump, retried A and sent B. The session reached `saved` without an explicit retry. Capture itself already supported B correctly. The fix gives the append-triggered pump `retryPending=false`; it persists B and preserves the uncertain flight. Existing explicit retry, recovery and flush retain their authority to transmit. No outbox/wire/history model changes.

Executable proof uses `RuntimeDataProvider`, its generated HTTP client and the existing transport fixture; transport move acceptance calls the real `executeClipMove` and `authoringBundleFromDocument`. No replacement guard logic. The fixture now records actual transmitted JSON text and applies previews/recovery patches with the real `compileTimelinePatch`, rather than only counting preview callbacks.

- A is accepted by the fake transport at r1/p1 before ACK loss. The actual session reaches `retry`; the displayed head remains r0/p0 and real local preview is A5.
- B is captured and submitted only AFTER that retry outcome. Its at guard is 5; its reads, selection and complete original command are retained. A mismatched displayed revision/publication and reuse of a stale capture refuse.
- B is durably appended with `basis.after = A.intentId` and no ready base; original display closure and both queued payloads survive disposal. There is exactly ONE commit POST before explicit owner recovery. The original pending flight, including its retry outcome, is unchanged.
- Live owner exclusion and realm/actor/project/timeline isolation remain enforced. Undo cannot discard an uncertain prefix.
- Reopen on the server's accepted HA still requires explicit owner recovery. Recovery first projects the ORIGINAL H0 closure plus the original A/B preview patches, then retries A with identical method/path/JSON text/key. B gets a fresh key, base r1/p1 and exactly its original complete command. Accepted projection is r2/p2 with clip x at 7.
- Undo submits `timeline.inverse` for p2 at r2/p2, using a new key through the same provider/client/outbox. This is proof of inverse command submission; the fake transport does not prove real Runtime inverse execution or inverse mathematics.
- A final-conflict injection on exact A retry keeps both original intents, marks their dependency chain conflicted and leaves B unsent. Subsequent retry/flush cannot silently drop or resend them. This is an adverse response control, not a claim that a real Runtime may reject an already accepted identical idempotent retry.
- Disk failure on B append keeps the B7 preview, reports `Unsaved move: disk full`, and sends nothing ephemeral. The durable record still has exactly original A. An explicit retry after storage restoration persists B and retries the original A before guarded B.

Exact source scope: 3 tracked files; 140 added / 12 deleted lines, net +128. Product `commitSession.ts`: 8 added / 2 deleted, 372 final lines. Test `commitSession.test.ts`: 113 added / 0 deleted, 567 final lines. Existing helper `__tests__/commitSessionEnvironment.ts`: 19 added / 10 deleted, 143 final lines. `clipMoveCapture.test.ts` and its 28 Agent capture goldens are unchanged (283 source lines). Session cases: 37 existing + 3 new = 40; capture cases: 78; total 118. No gesture UI test file was edited.

Validation (all commands run in `/home/user/work/wt/app-m2-ackloss-new-intent-unit`):

```sh
node_modules/.bin/vitest run --config config/testing/vitest.config.ts --maxWorkers=1 src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts
```

- Initial RED, 07:16:23 UTC: 115 passed / 2 failed; both new post-retry cases expected `retry` but got `saved`, confirming the automatic retransmission bug.
- Intermediate, 07:17:22 UTC: 115 passed / 2 failed; queue/wire assertions passed, but a test spy expected one finish invocation while the test itself deliberately invoked a second, refusing stale finish. Corrected the assertion to require exactly one return followed by one throw.
- Final, 07:18:15 UTC: **2 files passed; 118 tests passed; exit 0; 9.32 seconds**. This includes the unchanged exact capture/recorder goldens, local basis, closure and recovery controls. No passing expectation was removed, skipped or weakened.

```sh
node_modules/.bin/eslint src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts
git diff --check
```

Both passed, exit 0, no diagnostics. Ignored `node_modules` points to `/tmp/app-m2-coherent-deps8/node_modules` as required. No install/build/tsc/full suite/browser/server/socket run was performed, and no central full was requested. The unrelated running full is not evidence for this source tree.

Remaining Gate 5 risk: these are executable core unit tests with the existing vendored fake IndexedDB and a process-local exclusive lock fixture, not native browser storage/locks. No existing native IndexedDB unit fixture was found in this tree. The real browser must still prove that after the UI displays the uncertain-ACK/retry state, a NEW pointer gesture can reach the port (`useTimelineState.ts` exposes `save.commands.port`), pass the hook's `legacyClean` fence, preview B, persist it, and avoid any implicit UI flush/retry. `useTimelineSave.ts` routes flush into the command session, so flush remains an explicit retransmission entry point and browser callers matter. Poll/re-render fencing, actual restart/native IndexedDB durability, intervening Agent edit, real Runtime rebase/conflict and publication-targeted inverse execution remain the separate Gate 5 journey. The separately assigned gesture source worker owns UI coverage; this worker changed no UI file and makes no real-browser or complete Gate 5 claim.

Decision: apply only the proven automatic-pump fix, preserving existing API and exact request storage. No plan deviation or task blocker. Recommended next step: integrate this bounded core change with the separate after-ACK-loss gesture source work, then run the centrally managed real browser Gate 5 journey on the resulting paired source/release tuple. No M1 reopen claim.
