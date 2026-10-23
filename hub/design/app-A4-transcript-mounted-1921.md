# App A4 transcript mounted persistence

## Result

Added only `src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx`.
No production code, existing tests, schema, generated files, pins, locks, or
the old `transcript.associate` capture path were changed.

The test mounts the real `useProjectTranscriptHost` with the real
`useTimelineSave` consumer. The binding under test is:

```text
host.importTranscript
  -> project-transcript-host.associate
  -> commitData(next, { save: true, semantic: true })
  -> useTimelinePersistence.scheduleSave
  -> TimelineLocalSaveHandoff.capture
  -> createLocalSaveSession.appendDocument / commitOutbox
  -> RuntimeDataProvider.commitTimeline
  -> generated WorkspaceClient POST /v1/projects/.../timelines/.../commit
```

The narrow transport mock parses the actual serialized request, returns a
Runtime-shaped accepted reply, or refuses it with a guarded 409. The refusal
case checks that the exact body and idempotency key remain in the durable
outbox.

## Old behavior map

| Existing behavior | Mounted A4 result | Evidence |
| --- | --- | --- |
| Import source and associate one asset; preserve source identity and null/absent segment fields | Kept. Mounted request is one generic v2 `doc.patch`; the canonical bundle retains the exact `media.transcript.references/v1` association and the source item plane remains empty because project transcript documents are the source authority | New test lines 267–315; existing `project-transcript-host.test.ts` primary import/null-vs-absent cases remain unchanged |
| Exact source media pin and project-owned transcript document identity | Kept. Repository create uses the canonical `transcriptDocumentId`; host derives media from the registered asset and the accepted request carries the resulting document reference | New test lines 270–304; existing `importTranscriptHandoff.test.ts` pin/identity cases remain unchanged |
| Prior source replacement/version guard | Kept by existing host/repository tests; no replacement is synthesized in the mounted proof because the current mounted caller does not expose a separate association operation | Existing host tests around loaded-version replacement remain unchanged |
| Config-mirror fallback when primary parent clips are empty | Not claimed. The current App `TimelineData` caller has one canonical `config.clips` plane; it does not expose the old capture fixture's distinct empty `parent.clips` mirror | Existing old capture test lines 269–368; current caller `project-transcript-host.ts:617–651` |
| Caption destination collision and shared review ownership | Kept by existing host reconciliation tests at the local `commitData` boundary. Not reimplemented as a new mounted semantic operation; the current caller emits the resulting generic document patch only | Existing `project-transcript-host.test.ts` collision/shared-row cases; old capture test lines 370–382 |
| Malformed pinned source refuses before nested writes | Kept by existing host/import handoff validation. The mounted transport proof covers the save boundary's refusal/retention, not a new source-authority rule | Existing host/import handoff tests and old capture test lines 384–396 |

## Mounted request assertions

The accepted case asserts the actual request's API/project/timeline identity,
exact `r0/p0` base pair, label, `atomic` merge, `dry_run: false`, App source,
`doc.patch` command shape, created list, step id/intent/tags/ordinal/patch,
wire body equality, canonical `r1/p1` adoption, sibling order, and opaque
`null`/`false`/`0` preservation. It explicitly rejects any
`transcript.associate` operation or metadata-authority field.

The current caller does not declare `reads` for this association save; the
request therefore does not claim a fabricated read set. This is an uncovered
caller limitation, not a test omission or a new authority decision.

The refused case asserts `associationSaved: false`, retained local association
preview, unchanged visible head, generic `doc.patch` request shape, and the
outbox's exact POST path/body/key. The current local-save status is `retry`
after the transport refusal; no alternate/settings save path is used.

## Verification

All commands were run from the assigned App worktree. The repository config
needs the existing dirname preload under `--configLoader=runner`.

```text
node --require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx
PASS: 2 tests

node --require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-complete-stored-cap-producer-consumer-current-join/notes/dirname-preload.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=2 src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx src/tools/video-editor/lib/project-transcript-host.test.ts src/tools/video-editor/data/typed/importTranscriptHandoff.test.ts src/tools/video-editor/commands/transcriptAssociateCapture.test.ts
PASS: 4 files, 52 tests

node_modules/.bin/eslint src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx --max-warnings 0
PASS

flock -w600 /home/user/work/.app-tsc.lock node_modules/.bin/tsc -p tsconfig.json --noEmit --pretty false
PASS

git diff --check
PASS
```

No full, browser, HTTP/live, seed, P1, control, benchmark, dispatcher, or
generic Python suite was run.

## Uncovered / next steps

- No current mounted caller supports the old capture operation's config-mirror
  fallback, caption-fingerprint collision record, or shared-review ownership
  refusal record as independent wire semantics. Keep the old implementation and
  tests until an approved caller/provider contract supplies those semantics.
- No association-specific operation or metadata authority was added.
- No declared association `reads` are emitted by the current generic host save.
- Runtime response validation exercised the accepted and refused transport
  boundary; merged/historical/invalid reply variants remain outside this App
  test and should be qualified by their existing Runtime/contract suites.

