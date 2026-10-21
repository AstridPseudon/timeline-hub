# AP2 M2 owned overlay ADD handoff — unapplied

## Disposition

**UNAPPLIED row-local proposal.** No App product source, generated contract,
Provider, shared command session, pin, activation, or legacy-writer cut was
made.

The normal project-pack producer already carries the legitimate source in the
raw admitted element record. The current `ElementsLibraryPanel` consumer does
not receive that raw binding, and this App tree is still public014, whose
`clip.add` command type is row-only. Consequently there is no safe executable
panel/helper hunk in this tree. The handoff below is the smallest signature
contract for HOME/Agent to compose at the next authorized containing change.

The hosted SYSTEM8e path remains exactly where it is: a `packId: "rendering"`
row continues through the existing legacy adapter. It must not be relabeled as
a literal/no-owner row, replaced with the hosted 2a9b built-in, or admitted at
save time.

## Existing owner carrier and exact mapping

The normal project-owned carrier is already present at the producer boundary:

| Source/result | Exact current mapping | Consumer use |
| --- | --- | --- |
| Agent project-pack resolver result | `descriptor = {packId, id, kind, revision}` and `binding = {projectId, documentId, documentVersion, contentDigest}` | Reuse all four descriptor fields and the binding; do not reconstruct either from catalog data. |
| Runtime project-pack document admission | `content.admissions[]` matched by exact `id/kind/revision`, with its existing `snapshot_object` | Retain this exact object as the retained-source input; do not hash browser/config data or choose the newest object. |
| App selection adapter | `config/vite/projectElementSelection.ts:62-84` matches the admission, checks the Agent binding against the same document, and carries `selected.snapshot_object` into the raw selected element. | This is the producer/result boundary to preserve. |
| Existing Vite result module | `config/vite/astridElementAdmissions.ts:132-140` strips only build-only `snapshot` paths; the raw `binding` and `snapshot_object` survive in `elements`. | A future row-local consumer may read the exact raw record, but the public catalog must remain presentation-only. |
| Existing selected-parameter authority | `selectedParamAuthority.ts:317-355`, followed by `commitSession.ts:917-937` and `readRetainedParamInputs` | Use the same original accepted pin and retained document/object rule; never replace it with a latest/catalog lookup. |

The resulting command inputs are existing values, not new descriptor fields:

```text
elementRef    = raw admitted descriptor {packId, id, kind, revision}
schema_source = {
  document_id: binding.documentId,
  version: binding.documentVersion,
  content_digest: binding.contentDigest,
}
snapshot_object = the exact admission snapshot_object for that same ref/pin
```

The snapshot object is an authority/read input. It is not copied into the
overlay row and is not a replacement for `schema_source`.

## Why this is not applied on public014

The current panel receives `editorContext.elementContext.catalog` at
`ElementsLibraryPanel.tsx:58-65`; `admitted-elements.ts:128-136` projects raw
admissions to catalog presentation fields and drops the raw binding from that
public shape. The current owned branch at `ElementsLibraryPanel.tsx:118-160`
therefore remains on `elementOperationAdapter.execute`.

The native overlay helper and port are also literal-only in this tree:

- `elementOverlayCapture.ts:15-20,227-238` accepts a row and rejects an
  owner-qualified `elementRef` without authoritative Agent capture.
- `elementOverlayCapture.ts:230-236` constructs `clip.add` with
  `args: { row }` only.
- `elementGesture.ts:50-52,69-72` exposes only `{row, track?}` for create.
- `timeline-commit-types.ts:29` has public014 `ClipAddArgs = { row }`.

Exact017 is known to support the additive `clip.add.args.schema_source`
carrier, but that field is not present in this public014 tree. Adding it only
at the panel, by putting it in the row or by casting the public command, would
not produce a valid current command and would fabricate an activation claim.

## Smallest handoff signature (proposal only)

HOME/Agent should carry one existing source object from the raw admitted
element to the row-local consumer. The proposed boundary is:

```ts
// Proposal for the next matched containing source; not added here.
type OwnedOverlayAddSource = {
  elementRef: { packId: string; id: string; kind: 'effect'; revision: string };
  schema_source: DocumentPin;
  // Retained admission object used by the existing Agent read/validation path;
  // not serialized into the clip row or invented by App.
  snapshot_object: VerifiedDocumentObject;
};

// Proposal for the existing helper/port call; no caller is activated here.
captureElementOverlay(bundle, {
  row,                         // complete row, including the exact elementRef
  schema_source: source.schema_source,
});
```

The shared session must eventually pass that same `schema_source` into the
existing exact017 `clip.add` command argument and preserve the retained object
association for later reads. That pass-through is necessarily a shared seam
change (`elementGesture.ts`/`commitSession.ts` and the session surface), so it
is outside this worker's authorized scope. No shared file was edited.

Before any future capture, the row-local panel branch must:

1. Match the catalog row against the raw admitted descriptor on **all** of
   `packId`, `id`, `kind`, and `revision`.
2. Require the raw binding's project to equal the active project and derive
   `DocumentPin` only from that binding.
3. Require the exact retained snapshot object for the same admission/pin.
4. Refuse visibly, preserving the draft and making no capture/submit call, when
   any of those values is absent, foreign, malformed, or changed.
5. Use the complete existing row factory and existing native capture; do not
   re-admit, read latest, compute a browser hash, or allocate a wrapper.

If the panel cannot see the original binding at activation time, the required
result is the signature handoff above—not a catalog-only fallback. The existing
legacy owned adapter remains the safe behavior until the containing exact017
carrier is present.

## Direct-test proposal for the unapplied hunk

These are acceptance cases for the later matched source, not claims of tests
run in this public014 worktree:

- `ElementsLibraryPanel`: an exact admitted owner row prepares one ADD with the
  unchanged four-field `elementRef` and the original `DocumentPin`; the
  legacy adapter is not called.
- `ElementsLibraryPanel`: missing binding, foreign project, mismatched
  revision, or missing snapshot object refuses before capture and preserves the
  row/draft.
- `elementOverlayCapture`: exact017 parity accepts
  `clip.add.args.schema_source` only with an owner-qualified effect row,
  preserves the complete row and opaque fields, and retains command
  claims/inverse/replay parity.
- `ElementsLibraryPanel`: the hosted
  `rendering/effect/audio-reactive-colour` SYSTEM8e entry remains on the legacy
  path; neither the 8e project source nor the 2a9b hosted builtin is
  substituted.

No test should assert activation on public014, and no existing passing legacy
assertion should be rewritten to expect refusal.

## Evidence and limitations

Read-only source checks used for this handoff:

```text
sed -n '1,240p' /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md
git log --oneline -8
nl -ba config/vite/projectElementSelection.ts
nl -ba config/vite/astridElementAdmissions.ts
nl -ba src/tools/video-editor/runtime/admitted-elements.ts
nl -ba src/tools/video-editor/components/ElementsLibraryPanel.tsx
nl -ba src/tools/video-editor/commands/elementOverlayCapture.ts
nl -ba src/tools/video-editor/commands/elementGesture.ts
nl -ba src/tools/video-editor/commands/selectedParamAuthority.ts
nl -ba src/tools/video-editor/commands/commitSession.ts
nl -ba src/integrations/runtime/timeline-commit-types.ts
```

Result: current raw project-pack binding/object preservation and the public014
row-only overlay boundary were verified. The prior Read0040, Agent f83
source-ACK, and selected-parameter retained-source reports were reused; no
source-contract audit was repeated.

```text
git diff --check
git status --short --branch
```

Result: `git diff --check` passed; the product source worktree is clean. The
report is ignored by the repository's existing `*.md` rule but is present at
the required design path.

No product test was rerun because no product source or direct test was changed.
No full, browser, localhost/socket, Runtime-door, generation, pin, activation,
or shared-dependency operation was performed. The product tree remains clean
apart from this design report.
