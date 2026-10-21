# App2 M2 transcript nested dormant capture

## What changed

Added only the dormant App helper and focused test:

- `src/tools/video-editor/commands/transcriptAssociateCapture.ts`
- `src/tools/video-editor/commands/transcriptAssociateCapture.test.ts`

The helper uses the existing `EditCommand`, `MoveRecording`, `AuthoredBundle`,
`DocumentPin`, and `VerifiedDocument` carriers. It records one
`transcript.associate` command for `parent/asset:<id>`, with exact new and
optional prior transcript pins. It writes only the canonical nested planes:

- `parent.config.bundle.transcriptReferences`
- `parent.config.bundle.itemsBySchemaRef["astrid.transcript_segment/v1"]`

It retains unrelated bundle/source order and opaque values, projects ordered
segments/words, and ports the Agent no-asset caption/review reconciliation.
Malformed source, carrier shape errors, destination collisions, ambiguous
ownership, shared reviews, and prior-pin mismatches fail before any candidate
write. The input bundle remains unchanged on refusal.

## Source and decisions

Read the settled `PLAN.md`, App manager status/inbox, `/home/user/timeline-hub/hub/status/app.md`,
the original HOLD0215 report, the corrected SOURCE ACK0325 report, and the
current `project-transcript-host.ts` consumer.

The corrected Agent source reviewed was commit
`53c2c6f95632bf104b8bb13698e7a262822ecfdb`, tree
`265e06903721aa1bd27641cbbc3bfd6d8340be7e`. ACK0325 closes the two original
HOLD mismatches: nested carrier spelling and no-asset caption/review ownership.
The helper therefore stays dormant; the existing project-document CRUD,
`project-transcript-host` writer, persistence/provider path, and live callers
remain unchanged. No generated schema or Runtime/App activation was added.

The source carrier is the existing `VerifiedDocument` shape rather than a new
DTO. No published carrier was missing for this bounded helper. The helper is
async only to verify the existing exact digest/document identity utilities; it
does not perform IO or persistence.

## Live callers changed

None. The only imports/calls are in the new focused test.

## Tests and checks

Passed:

```text
PYTHONDONTWRITEBYTECODE=1 ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/transcriptAssociateCapture.test.ts
=> 1 file, 5 tests passed
```

```text
PYTHONDONTWRITEBYTECODE=1 ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/transcriptAssociateCapture.test.ts src/tools/video-editor/data/typed/importTranscriptIdentity.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/timelineBundle.test.ts
=> 4 files, 52 tests passed
```

```text
npm run typecheck:strict-islands
=> passed

./node_modules/.bin/eslint src/tools/video-editor/commands/transcriptAssociateCapture.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts --report-unused-disable-directives --max-warnings 0
=> passed

git diff --check
=> passed
```

Not run: full suites, HTTP, browser/socket, authenticated/native activation,
Runtime qualification, generated-client qualification, or release/cut claims.

## Recommended next step

Have the App/Runtime integration owner qualify this dormant command through the
normal authenticated `/v1` carrier and accepted-history closure before adding
any live producer/session wiring or retiring the existing host writer.
