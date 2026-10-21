# App2 parent-media merged evidence: c395

Status: complete. Updated only the existing App2 parent-media row in both
deletion ledgers. No product code, tests, browser run, new source scan, or
public pin was changed.

## Merge evidence

The actual App merge is:

`c395296db97ddf7876eafa9885e9d1678446ce75`

Its parents are:

- integration parent `3db1e1ac60de8721b8f7a37cc8d02171ae2fd0e3`;
- approved delivery merge `0cc7591f0364cfded00e4d582434753ef0c6085f`.

The nested approved delivery merge retains parents `facd9c65` and
`1be92c689`. This is new remote merge evidence after the earlier `0304`
update, not a repeat of that proof.

## Exact changed row lines

Only these two existing rows changed:

- `design/deletion-ledger.app.md:18`, row `D01-app-parent-media`.
- `design/deletion-ledger.md:44`, row `D01-app-parent-media`.

The changed evidence now says the row-local duplicate-generation port is in
actual App merge `c395296db97ddf7876eafa9885e9d1678446ce75`, including the
HOME two-parent merge `0cc7591f0364cfded00e4d582434753ef0c6085f` with its
`facd9c65` and `1be92c689` parents. It retains the original Runtime
`MediaSelection`, displayed head/projection, and preparation epoch; the
specific `Duplicate generation` menu path has no reachable legacy
registration/publish writer; and the 26 focused source controls plus types
and lint evidence remain retained from reports 0243/0250/0257.

The same rows explicitly retain the boundaries: normal catalog duplication
remains visibly unsupported, native `afterClipId` remains visibly unsupported,
no accepted workflow is claimed, and broad parent-media remains OPEN. The
independent duplicate row remains DELETED at old `8c0e1f` / HOME `71d` evidence;
it was not changed. All other rows and public pins were left untouched.

## Live callers

The unchanged specific menu path is:

`ClipAction.tsx:241-251` -> `TimelineEditorCoreBody.tsx:807` ->
`TimelineEditorCore.tsx:839` -> `AstridTimelineEditor.tsx:544-625` ->
`generation-utils.ts` / `generationLookup.ts` ->
`useAssetManagement.prepareGenerationAsset` ->
`useTimelineCommandsService.addClip` -> the existing `parentClipAddMedia`
capture/verify/submit carrier.

Other registration callers, including pinned-shot-group synchronization and
`useAddVariantAsGeneration.ts`, remain distinct and unchanged.

## Checks and limits

Read-only checks run:

```text
git show --no-patch --format='%H%n%P%n%s' c395296db
git rev-list --parents -n 1 c395296db
rg -n 'D01-app-parent-media|c395296db|0cc7591f' design/deletion-ledger.app.md design/deletion-ledger.md
git status --short
```

Results: the merge SHA and both parents matched; both ledger rows contain the
new SHA and the nested delivery ancestry; the App worktree remained clean.
The handoff file was intentionally not changed because this task requested
only the two ledger rows.

No tests, browser/live-socket run, full suite, or new source scan was run, as
explicitly instructed. The broader parent-media acceptance, placement,
reload, retry, undo, and zero-legacy qualification remains pending.
