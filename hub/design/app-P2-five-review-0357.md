## Result

Independent static review complete against:

- App `f90e708b379145ac456924742cc51c187ed6e0c6`
- Agent `079580ca46af77e0292d49dc34386b25c8391f99`
- Runtime `37eb6c7bdb79dcae2523883e66b5cea5be721ffd`

No product code or tests changed. No live/P2 credit awarded.

| Case | Verdict | Finding / correction |
|---|---|---|
| `transitionNone` single | **FAIL-static** | The UI sends a generic transition patch: `ClipTransitionSection.tsx@72e39df:130-147`, then `handleSelectedClipChange` supplies no gesture basis for transition fields (`useClipEditing.ts@cc0df7f:246-248`). The canonical child closure is therefore rejected by the handoff guard (`timelineLocalSaveHandoff.ts@890e2a6:231-239`). Owner **0349** must connect this gesture to the child-aware carrier. Existing lossless removal correctly preserves absent/null/unknown data if reached (`timelineLocalSaveHandoff.ts@890e2a6:198-212`; `documentPatchIntent.ts@5e1b1d1:201-212`). |
| `transitionNone` bulk | **FAIL-static** | Bulk transition clearing uses `handleUpdateClipsDeep` without a gesture basis (`PropertiesPanel.tsx@bae86d1:540-547`; `useClipEditing.ts@cc0df7f:203-232`), so it hits the same child-closure refusal. Owner **0349** must provide a valid child-aware carrier preserving one guarded `remove` per selected clip. |
| `registerAsset` save | **PASS-static** | File drop creates `place-prepared-media` (`useAssetManagement.ts@405afcb:93-121`), the commit marks `prepared-media` (`useTimelineCommit.ts@873fe8e:428-439`), and the handoff emits semantic `clip.add-media` with exact five-field media selection and created asset/clip identities (`timelineLocalSaveHandoff.ts@890e2a6:317-393`). Agent registers and executes the operation (`commands.py@d349ebd:67-103`; `native_parent_media_commands.py@433f94a:25-40`). Live behavior remains unverified. |
| `automaticchildplacement` | **FAIL-static** | The fixture has one occurrence (`harness.ts@793f49a:788-797`), so `sharedPopupMediaCommands` returns `null` (`shotTimelineDataProvider.ts@eb6f90f:739-766`). The non-shared branch emits `doc.patch` (`:1171-1208`), while the original case requires `occurrence.add-media` (`three-products.p2-elements-assets.spec.ts@836d144:522-543`). This contradiction is real. Owner **0349** must make the one-occurrence path carry the required occurrence-owned semantic command. |
| `popupSWAP` | **PASS-static** | The prepared popup fixture creates shared placement (`p2-popup.spec.ts@3cb6908:261-291`). The provider verifies occurrence/shot/internal pins and obtains authenticated old/new Runtime selections (`shotTimelineDataProvider.ts@eb6f90f:739-818`), then emits `occurrence.fork` + `occurrence.swap-media`, matching the original assertion (`p2-popup.spec.ts@3cb6908:427-468`). Agent/Runtime support both operations (`commands.py@d349ebd:82-90`; Runtime schema `timeline-commit-bundle.json@252f71f:1526-1555`). Live behavior remains unverified. |

The full-v2 request carrier and idempotency reservation are present in `localSaveSession.ts@c8eb507:158-188` and `commitOutbox.ts@8f6c157:464-503`; Runtime DTOs cover the requested commands, steps, replies, conflicts, and invalid details (`timeline_commit_types.py@8cfbcc4:35-39,78,96-103`).

Checks:

- `git diff --check` — passed
- `git diff --quiet HEAD` — passed; worktree clean
- Tests/browser/backend/service/full suite — not run, per task restrictions

DONE marker and commit message were written.