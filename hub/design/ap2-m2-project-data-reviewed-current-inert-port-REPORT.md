# App project-data reviewed current inert port

Date: 2026-10-20 UTC

## Result

Ported the reviewed donor packet from `tl/ap2-m2-project-data-main-merge-lowering`
onto current App integration root `20ea14c26526fe4924354f10a177aebbaf6002bc`
(`hub/tl/integration`). Only the two allowed files were added:

- `src/tools/video-editor/commands/projectDataMember.ts`
- `src/tools/video-editor/commands/projectDataMember.test.ts`

Both files are byte-identical to the donor blobs:

- `projectDataMember.ts`: `89974b1be146a70f4726870bf9829f4d94f5591c`
- `projectDataMember.test.ts`: `704baa3652086b949161638173d8f75bde8b6ada`

The helper remains inert. Existing namespace validation, closed replace command,
raw leaf/container guards, absence/null/opaque preservation, stable namespace
order, mixed-batch atomic refusal, and legacy writer behavior remain unchanged.
Main-compatible lowering is present: omitted mode is replace; merge recursively
combines only two non-null object cells; arrays, null, absent, and scalar cells
replace; explicit order is ascending with stable source-index ties and unordered
operations last. No dispatcher, generic routing, session/provider, Runtime
activation, pin, DTO, schema, public API, dependency, or legacy-writer change
was made. No delete/unset operation was guessed or introduced.

## Tests and checks

Passed:

```text
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/projectDataMember.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts
=> 2 files passed; 24 tests passed

./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/lib/compiler-canary.test.ts src/tools/video-editor/lib/source-map-runtime.test.ts -t 'project-data|source-map|source map|DSL source|persists|delete removes|updated'
=> 2 files passed; 10 tests passed, 80 skipped

./node_modules/.bin/tsc --noEmit --pretty false
=> passed

./node_modules/.bin/eslint src/tools/video-editor/commands/projectDataMember.ts src/tools/video-editor/commands/projectDataMember.test.ts --max-warnings 0
=> passed

git diff --check
=> passed; untracked files were additionally checked with git diff --no-index --check
```

The focused result is 24 tests because the current integration generic-capture
neighbor contains its current test set; the project-data helper itself is the
reviewed 17-test packet plus the direct neighbor tests. No full suite,
browser, localhost, live socket, Runtime HTTP, native activation, or repeated
cross-repo parity lane was run. Repeated Agent parity was intentionally not
run because both production and direct test files are byte-identical to the
reviewed donor.

## Merge-forward attempt

Immediately before finishing, ran:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/merge-forward ap2-m2-project-data-reviewed-current-inert-port hub/tl/integration
```

It failed with exit 128 before any merge mutation:

```text
fatal: update_ref failed for ref 'ORIG_HEAD': cannot lock ref '/home/user/banodoco/reigh-app/.git/worktrees/ap2-m2-project-data-reviewed-current-inert-port/ORIG_HEAD.lock': Read-only file system
```

Exact roots after the attempt:

- worker HEAD: `20ea14c26526fe4924354f10a177aebbaf6002bc`
- `hub/tl/integration`: `20ea14c26526fe4924354f10a177aebbaf6002bc`
- merge base: `20ea14c26526fe4924354f10a177aebbaf6002bc`

No conflict markers or owner-file overlap were produced. The unresolved item
is only the harness/owner Git metadata restriction; the worker tree remains
ready for remote delivery. Runtime392/provider-door qualification remains a
prerequisite for activation. This packet makes no deletion claim.

## Next step

Send this inert two-file packet through the App remote merge harness, then
qualify it with the paired Runtime392/Agent provider-door controls before any
consumer activation or legacy-writer retirement.

