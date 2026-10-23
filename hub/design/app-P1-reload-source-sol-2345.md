**P1 remains NO-GO.** Read-only first-case investigation completed on App `18befa48`, tree `abe418cd`. No source, tests, helpers, timeouts, dependencies, or artifacts changed.

Confirmed timing in actual **13781**, relative to reload invocation:

| Observation | Time |
|---|---:|
| Reload returned | +10.640s |
| Connected assertion passed | +14.334s |
| Track name assertion began | +14.339s |
| Project-list GET returned 200 | +19.116s |
| Timeline-list GET returned 200 | +19.328s |
| Track name assertion failed | +19.342s |

Decoded snapshots at connected success and after failure show `data-boot-hold`, no editor-shell marker, and no Track name field. Both URL identities remain unchanged. At +19.870s, a snapshot shows **Loading project**. HTTP success does not prove query validation or selected-project restoration completed.

No post-reload timeline-detail/composition GET is retained. One failed commit record appears at +0.049s; it cannot establish that the newly mounted owner invoked automatic recovery. The pending response observer was armed before reload; its eventual page-close failure is secondary.

The source call graph explains the boundary:

- [`expectConnected`](/home/user/work/wt/app-P1-reload-source-sol-2345/tests/e2e/local/support/app.ts:128) checks only the connection badge.
- [`useRuntimeEditorDiscovery`](/home/user/work/wt/app-P1-reload-source-sol-2345/src/tools/video-editor/hooks/useRuntimeEditorDiscovery.ts:94) negotiates connection, loads/validates projects, then enables timeline discovery.
- [`selectionVerified`](/home/user/work/wt/app-P1-reload-source-sol-2345/src/tools/video-editor/pages/VideoEditorPage.tsx:323) gates provider/editor mounting.
- [`useTimelineSave`](/home/user/work/wt/app-P1-reload-source-sol-2345/src/tools/video-editor/hooks/useTimelineSave.ts:166) requires original document/head, verified basis, identity and session before [`session.recover`](/home/user/work/wt/app-P1-reload-source-sol-2345/src/tools/video-editor/hooks/useTimelineSave.ts:264) reaches [`pump`](/home/user/work/wt/app-P1-reload-source-sol-2345/src/tools/video-editor/commands/localSaveSession.ts:300).

**Conclusion:** connection readiness preceded observable editor readiness. Genuine post-reload editor readiness and owner recovery remain **unavailable**, not proven defective or successful. The five-second expiration does not establish product versus harness root cause.

**Smallest next owner action:** Proof should qualify the existing [`openSeededTimeline`](/home/user/work/wt/app-P1-reload-source-sol-2345/tests/e2e/local/support/app.ts:134) sequence—selected project text → timeline control → original Track name assertion—using the same assertion timeouts. This is a readiness candidate, not a demonstrated fix. Preserve automatic recovery, exact body/key, restart, drain and history assertions.

If still unavailable, capture only stage completion times/UI booleans plus the existing [`mounted diagnostic snapshot`](/home/user/work/wt/app-P1-reload-source-sol-2345/tests/e2e/local/three-products.p1-chain.spec.ts:1227): phase, sequence/time, basis status, session/current/closed booleans, owner count, status and classified error. No state dump is needed.

Evidence SHA256:

- Trace: `08ee43d214fdc899966c12cebc557833af4557b93da657ccdb85c9077424117a`
- Error context: `9ed8aa2f1f92fe16accfd8ca4b471ee22def20d57f125ad96d8bed79441f6eed`
- 8,019-byte diagnostic: `2b6ec924d00f4a48d7aecaf057104bcc51e521a50385512c728ce3e0849e98c5`

Validation:

- `python /tmp/w-f7014fe151/reload_metadata_probe.py` — PASS; bounded offline metadata/snapshot projection.
- `git diff --check` — PASS.
- `git status --short` — clean.
- Browser/backend/service/product suites — not run, per scope.

No product fix justified; case 2 untouched. Commit message and empty `DONE` created.