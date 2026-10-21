# M2 transcript capture contract review

## Verdict

**HOLD exact source tree `bac1fa0dad486b4b6d41cfc8682ee01fb4cac875` (tree `aeadfada318978c1b7afafe9c747b66ba0e4aba2`).** The dormant helper is correctly scoped and has no live callers, but it is not exact Agent `53c2c6f95632bf104b8bb13698e7a262822ecfdb` parity yet.

## Concrete mismatches

1. **New pin is not bound to the submitted command.** `applyTranscriptAssociation` checks that `previous_document` matches the supplied prior source, but never checks `args.document` against `source.pin` (around lines 408–423). Therefore `finishTranscriptAssociation` or `executeTranscriptAssociation` can receive a command carrying new pin A and a valid same-media/source document carrying pin B. The result then writes/projects B and records `transcript.document` dependency B while the command still declares A. Add an exact equality check between `exactPin(args.document, 'new')` and `source.pin` before any candidate writes, and add a regression for this swapped-document case.

2. **Clip mirror write path differs from Agent.** The helper chooses `parent.clips` whenever it is an array (around lines 488–490). Agent `parent_clip_path` chooses `config.clips` when the primary `parent.clips` array is empty and the config mirror is populated. In that shape the App helper directly changes the empty primary collection and then may add a derived mirror write, whereas Agent changes only the populated authored collection. Preserve Agent’s path-selection rule and add the empty-primary/populated-mirror neighbor control.

The nested carrier is otherwise correct: writes are limited to `parent.config.bundle.transcriptReferences` and `itemsBySchemaRef["astrid.transcript_segment/v1"]`; legacy/root spellings refuse. The no-asset caption/review reconciliation matches the corrected Agent behavior, retaining text/style/timing/opaque metadata and refusing destination collisions, shared ownership, and ambiguous mappings before writes. Source-item and association order, unrelated bundle planes, exact prior dependency, and explicit new/prior dependency recording are retained in the covered path.

## Caller and scope review

- Live callers changed: **none**. `git grep` found imports/calls only in the new focused test.
- No host/CRUD/persistence/provider/session wiring, pin adoption, generated types, HTTP, browser, or activation change is present.
- Existing `project-transcript-host` remains the sole live transcript association writer; this helper is dormant and uses the existing `VerifiedDocument` carrier.

## Evidence

Source-worker evidence on the exact two added files:

```text
vitest ... transcriptAssociateCapture.test.ts
  1 file, 5 tests passed
vitest ... transcriptAssociateCapture.test.ts importTranscriptIdentity.test.tsx project-transcript-host.test.ts timelineBundle.test.ts
  4 files, 52 tests passed
npm run typecheck:strict-islands
  passed
eslint ... transcriptAssociateCapture.ts transcriptAssociateCapture.test.ts --max-warnings 0
  passed
git diff --check
  passed
```

Independent review checks:

```text
git diff --check c45cc175a..tl/ap2-m2-transcript-nested-dormant-capture-0342
  passed
git show <each added file> | eslint --stdin --stdin-filename <path> --max-warnings 0
  passed
```

No full, browser, HTTP/socket, or Runtime qualification was run, as required. No source change was made in this review worktree.

## Recommendation

Keep the exact source dormant. Apply the two narrow parity corrections above, add the two regressions, rerun the same focused App/type/lint checks, then request a fresh independent review before any consumer wiring or pin adoption.
