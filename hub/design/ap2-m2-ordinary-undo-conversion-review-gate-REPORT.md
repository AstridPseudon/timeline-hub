# AP2 M2 ordinary undo conversion review gate

## Decision

**APPROVE the assertion conversion; central ordinary qualification remains
UNVERIFIED.** The committed donor is `tl/ap2-m2-ordinary-mounted-journey-gate`
at `966472b615024d8f874379b4e6a5eb3df0145419`.

The old whole-document equality was circular/wrong: it compared ordinary undo
with the Agent document derived from the ordinary revision, even though undo
must restore the pre-ordinary authored state and preserve the disjoint Agent
edit. The replacement derives its expected value independently from the
pre-edit Runtime document and overlays only the literal `S1` Agent label. It
does not derive expected data from the inverse response or weaken the raw
closure checks.

## Assertion review

- `beforeDocument` is fetched from the Runtime head before the ordinary batch.
  The new oracle clones `beforeDocument.payload`, requires the independent `S1`
  track, and sets its label to `F2 Agent ordinary sibling`.
- It compares the complete resulting parent payload, the complete pre-edit
  `shot_revisions`, complete `internal_timeline_revisions`, and complete
  `dependency_manifest`. Existing position, opaque-field, immutable-closure,
  credential, token, and zero-legacy-save assertions remain in place.
- The ordinary App batch and Agent edit are disjoint in the authored model:
  App uses `V1`; Agent uses literal `S1`. The retry/rebase assertions retain
  both labels and the ordinary positions before either inverse.
- The native parity fixture remains exact: `bundle_from_document`, ten bare
  commands through the native `execute`, exact command/record equality,
  final-bundle equality, verified re-execution, and input immutability are all
  checked. The focused App capture test also retains native read order,
  dependency pins, ordinals, no-created-ID, transition, opaque child data, and
  bundle-preservation checks.
- The conversion matches the approved duplicate assertion-conversion
  precedent: replace only the invalid derived-document equality with an
  independent authored-state oracle while preserving structural/raw coverage.

No circular expected value, dropped assertion, weakened matcher, or changed
compiler-revision expectation was found. The native revision semantics remain
the existing exact `execute`/record contract; the candidate only repairs the
occurrence read ordering and makes the fixture exercise the literal disjoint
track.

## Central gate

Submitted exactly once, with no local browser/socket run:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-mounted-journey-gate e2e-m2-ordinary-committed-driver-gate --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-ordinary-mounted-journey-gate-e2e-m2-ordinary-committed-driver-gate-1020225056-30322
```

Result: **FAIL before the ordinary test ran**, exit 1, 68 seconds.

Retained result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-ordinary-mounted-journey-gate-e2e-m2-ordinary-committed-driver-gate-1020225056-30322/`

The absolute driver passed its clean-tree, private-graph, Chromium smoke,
exact-one-test collection, Agent `8130a401bf44a518d5a40ae274d398b8c560be55`,
Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, and Composition 0.0.13
guards. Hosted build then failed because the committed donor does not contain
`src/tools/video-editor/lib/theme-api.fallback.tsx`, which
`src/tools/video-editor/compositions/TimelineRenderer.tsx` imports through the
Vite fallback alias. No journey assertion, command POST, retry, rebase,
restart, or undo was reached, so this is not evidence for or against the
converted oracle.

## Verification and next step

The candidate worker's recorded focused evidence was 21 passing tests (17
native/ordinary capture tests plus 4 authoring-admission/marker tests), with
lint and `git diff --check` passing. The recorded commands were:

```sh
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryRealBatch.test.ts
node_modules/.bin/vitest run --no-cache --maxWorkers=1 --no-file-parallelism src/test/threeProductsAuthoring.test.ts
node_modules/.bin/eslint --max-warnings 0 <all changed TypeScript files>
git diff --check
```

Those commands were not rerun in this read-only review; no local browser,
socket, full, or pin suite was run.

Do not rerun the central gate under this review. Restore or otherwise resolve
the donor's pre-existing hosted-build fallback-source mismatch in the owning
App integration, then submit a new committed candidate and a new central run.
