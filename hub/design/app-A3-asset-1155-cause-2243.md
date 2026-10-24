## Result

Implemented the minimum App repair in [`timelineLocalSaveHandoff.ts`](/home/user/work/wt/app-A3-asset-1155-cause-2243/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:395): transient `removeClipId` cleanup is now allowed for prepared image drops. Existing authored-clip, ownership, registry, media-selection, and placement guards remain intact.

Added a regression test covering the real uploading-skeleton flow.

Evidence:

- Retained browser trace: media import `201`, media selection `200`, inspect polling `200`; no browser `/commits` POST.
- Runtime recorded two successful setup requests; intended gesture Runtime outcome remains unknown.
- Focused Vitest: `97/97` passed.
- TypeScript: passed.
- ESLint: passed.
- `git diff --check`: passed.
- Protected retained E2E hashes unchanged.
- No browser/service/full-suite rerun performed.

Commit message and `DONE` marker created. Independent review is still recommended before merge.