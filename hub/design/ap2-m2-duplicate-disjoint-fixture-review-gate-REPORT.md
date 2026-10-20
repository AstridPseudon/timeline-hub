# App M2 duplicate disjoint-fixture review and gate

Date: 2026-10-20 UTC  
Worker: `ap2-m2-duplicate-disjoint-fixture-review-gate`  
Candidate: `846d2b018af63b63977ea399d33e3470989836e7`  
Candidate tree: `96a71df0f907e841ff4c22d84de07d4420e64cc0`

## Result

The read-only fixture review is approved, but the candidate is **not
qualified**: the one authorized central effective-graph gate failed at a
later final-document assertion. Do not claim HOME deletion readiness from this
run.

## Review

The candidate changes only `tests/e2e/local/three-products.spec.ts` relative
to `9caf57adb` (6 insertions, 3 deletions). Agent C now edits the seeded,
independent `parent/track:S1`; local B remains `parent/track:V1`. The retry
assertion requires both labels, and the first guarded undo asserts that C's S1
label survives. No production guard, recapture, schema, API, pin, or Runtime
change is present.

The duplicate journey retains its assertions for:

- duplicate command and raw occurrence/copy preservation;
- opaque parent and child data;
- no legacy graph/task save traffic;
- lost ACK, dependent local B, byte-identical retry, and rebase;
- App reload plus Runtime restart/recovery;
- guarded undo of B and then the duplicate;
- final zero-legacy traffic, opaque-data closure, and credential checks.

The separate `M1 real dependency conflict retains B original guards and
pending identity` case remains unchanged and still asserts a genuine
dependency conflict (`409`, non-stale-head reason), retained B intent/guards,
reload recovery, opaque preservation, and zero legacy traffic.

No private runner source guard referenced `9caf`, so no runner edit was made.
The effective graph attachment remained the existing private Composition 0.0.13
graph with Agent `8130a401bf44a518d5a40ae274d398b8c560be55` and Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a`; the runner's source pins were not
changed.

## Validation

Passed locally:

```text
./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts
  3 files, 45 tests passed
npm run typecheck:strict-probe
git diff --check
```

One central request was made on the clean committed candidate:

```text
ap2-m2-duplicate-disjoint-fixture-review-gate-e2e-m2-duplicate-effective-graph-three-products-1020202150-1717
```

Result: **failed**, exit 1, 230 seconds. The private effective graph and
hosted build passed, and the browser journey reached the final duplicate undo.
The first causal conflict was fixed: exact retry, restart/recovery, rebase,
and the first guarded undo completed. The failure was at
`tests/e2e/local/three-products.spec.ts:1342`:

```text
expect(undoDuplicate.data.canonical_document).toEqual(agentEdit.data.canonical_document)
```

The received final document correctly no longer contains the copied occurrence;
the earlier `agentEdit` response still contains that occurrence because C was
captured over the already-duplicated A revision. The deep diff therefore shows
the expected duplicate-only graph versus the received post-undo graph. The
later final zero-legacy, opaque-closure, and credential assertions were not
reached by this failed run, although they remain in the source.

Central log:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-duplicate-disjoint-fixture-review-gate-e2e-m2-duplicate-effective-graph-three-products-1020202150-1717/log.txt
```

No full suite or second central run was requested. No local browser, socket,
or direct central runner execution was performed. The worktree is clean.

## Recommended next step

Repair the final expected-state assertion so it compares against the state
after C with the duplicate removed (or checks the intended preserved fields),
while retaining the existing positive and negative assertions. Then request a
newly authorized central gate; this worker did not rerun after the first result.
