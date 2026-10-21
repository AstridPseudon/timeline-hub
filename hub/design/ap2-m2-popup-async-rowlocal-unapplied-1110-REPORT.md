# ap2-m2-popup-async-rowlocal-unapplied-1110

## Result

Stopped at the first legitimate prerequisite: the current App2 caller graph
does not carry an explicit occurrence owner plus approved newborn raw child
row. No product source or test files were changed. No browser, socket, or
service run was performed. Durable proposal: [UNAPPLIED patch](ap2-m2-popup-async-rowlocal-unapplied-1110-PATCH.md).

Changed live callers: **NONE**.

## Evidence

- Current HEAD: `0cc2583aa`; approved dormant port is present through
  `9990054a5` / merge `5ff11809e`.
- `GenerationDropData` carries generation/variant/media URL metadata only;
  `TimelineDropPosition` carries track/time only.
- `TimelineProvisionedAsset` carries the optional original five-field media
  selection but no occurrence owner or raw child row.
- `buildAssetDropEdit` at
  `src/tools/video-editor/lib/timeline-asset-plans.ts:321-425` creates an
  ordinary visual `ClipMeta` (`id` is only the map key), not an approved
  occurrence birth row.
- `handleFileDrop` creates `uploading-*` placeholders and passes
  `preparedAsset` plus `removeClipId`; those identities are explicitly
  transient and cannot become canonical occurrence IDs.
- The only existing approved row-building carrier found is the HOME-owned
  parent path in `src/tools/video-editor/hooks/useTimelineCommandsService.ts:520-563`.
  It uses `parentClipAddMedia`, not occurrence ownership, so it cannot be
  repurposed.
- The rejected `6fcddfcb3` packet fabricated a popup row/owner path and was
  correctly rejected by r48 for missing ownership/source/track guards, early
  async success, changed missing-port behavior, and no direct new-branch test.

## Exact HOME request

At the HOME-owned `useTimelineState.ts:962` assembly, add only the optional
carrier already specified by the handoff:

```ts
occurrenceAddMediaPort?: OccurrenceAddMediaCapturePort;
```

and pass:

```ts
occurrenceAddMediaPort: save.commands.occurrenceAddMediaPort,
```

Separately identify/expose the existing approved occurrence newborn/birth
result as `{ ownerRef, row }` to this caller. Do not add a normalizer, owner
inference, latest-media read, local snapshot, fallback writer, new DTO, or
new store. Until that result exists, App2 must remain on the existing route
or visibly refuse; it must not select an occurrence branch.

## Entry points and boundaries

Real candidate entry points are Add Images chooser, desktop file drag/drop,
gallery single-generation drag, gallery multi-generation drag, bare
`asset-key` drag, and gallery shot/group drag. The first four need an explicit
one-to-one owner/raw-row/media carrier; the latter two are unsupported for
occurrence ADD without one and must not infer. Guidance-video, audio picker,
parent/list-level drops, text-tool drops, and effect-layer drops are outside
this seam.

## Tests

Read-only checks run:

```text
git show --stat --oneline 5ff11809e
git show --stat --oneline 9990054a5
git diff --check
pwd
realpath node_modules
realpath node_modules/.bin/vitest
```

All completed successfully; effective Vitest resolution is the shared
`/home/user/work/app/node_modules` install. No targeted Vitest run was started
because no allowed product/test edit was made and the required raw carrier is
missing. Full suites, browser, sockets, and live services were not run.

## Limitations / next step

The caller ordering, async refusal/no-fallback, and transient-placeholder
cleanup tests are specified in the durable patch but remain unimplemented and
unverified until HOME supplies the real carrier. The next worker should apply
only the three named caller files and direct tests after that seam is present.
