# App2 M2 owned raw admission custody review — 0115

## Disposition

**Approved after the smallest required preservation fix.** The original dormant
accessor commit was not sufficient as an end-to-end retained-read handoff:
Agent's raw resolver binding survived into the selected element, but the exact
Runtime `admission.snapshot_object` was read and then dropped before
`current.elements`. The accessor's positive test therefore exercised a shape
that the real selection path could not produce.

The repair is limited to the existing Vite selection adapter and its focused
test. It carries the already-read matching `snapshot_object` beside the
already-returned Agent `binding`, preserves both through the existing virtual
module spread, and includes the document ID, version, and content digest in the
existing resolver cache key. No route, DTO, store, authority, provider field,
save-time admission, or activation was added.

## Reviewed source and smallest fix

- Base dormant source: `016975a433662a64c1c1a6c575f5e0ec88793c5`.
- Reviewed worktree: `/home/user/work/wt/ap2-m2-owned-raw-admission-custody-review-0115`.
- Changed files in this review:
  - `config/vite/projectElementSelection.ts`
  - `src/tools/video-editor/runtime/project-element-selection.test.ts`
- The original accessor files remain unchanged in this review.

The adapter now matches the selected Runtime admission by all four
owner-qualified fields (`packId`, `kind`, `id`, and `revision`) and carries its
existing `snapshot_object` to the raw element record. The existing Agent
resolver binding is still checked against the same project, document ID,
version, and content digest. The cache identity now includes that document
identity, so a newer document with the same element revision cannot reuse an
older raw pin/object pair.

## Ten focused controls

1. Exact source key: pass. The accessor matches all four fields, including the
   full pack owner and revision; no partial ID or kind lookup is used.
2. Agent binding provenance: pass. The DocumentPin is projected only from the
   existing raw `binding` (`documentId`, `documentVersion`, `contentDigest`).
3. Runtime object provenance: pass after the fix. The object is the exact
   `content.admissions[]` `snapshot_object` selected by the same four-field
   admission match.
4. Existing types: pass. The accessor reuses `DocumentPin` and
   `VerifiedDocumentObject` field types; no replacement DTO was introduced.
5. Project custody: pass. Element project, binding project, Runtime document
   project, and requested project are checked; foreign project input refuses.
6. Object integrity: pass. The accessor requires the exact four object fields,
   `sha256:` identity, equal object ID/digest, positive safe size, and JSON
   media type.
7. Visible refusal: pass. Missing owner/ref, missing binding, foreign element
   or binding, and missing/malformed object return a status/refusal reason.
8. No manufactured authority: pass. No browser hash, latest lookup, catalog
   revision, system 8e value, new pin, object, endpoint, or persistent store is
   created by the accessor.
9. Dormancy boundary: pass. `git grep` finds only the accessor definition and
   its three focused test calls; there are no production callers, Provider
   wires, on-save admissions, or f83 activation.
10. Retained handoff and cache race: pass after the fix. The focused selection
    test proves the Runtime object survives into the generated module and that
    a changed document version/object causes a fresh resolution.

The result remains dormant because the current App/Agent pin does not contain
the approved f83 `clip.add.args.schema_source` consumer contract. No add
consumer was activated.

## Evidence

Passed:

- `TMPDIR=$(mktemp -d /tmp/ap2-m2-owned-raw-admission-custody-review-0115.XXXXXX); TMPDIR="$TMPDIR" ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --testNamePattern='reads one canonical|invalidates only|loads no artifact|rejects stale|does not substitute|rejects a different' src/tools/video-editor/runtime/project-element-selection.test.ts`
  — 6 passed, 1 existing Vite-server test excluded.
- `TMPDIR=$(mktemp -d /tmp/ap2-m2-owned-raw-admission-custody-review-0115.XXXXXX); TMPDIR="$TMPDIR" ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/runtime/admitted-elements.test.ts`
  — 1 file, 10 tests passed.
- `./node_modules/.bin/eslint config/vite/projectElementSelection.ts src/tools/video-editor/runtime/project-element-selection.test.ts src/tools/video-editor/runtime/admitted-elements.ts src/tools/video-editor/runtime/admitted-elements.test.ts --max-warnings 0`
  — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false -p tsconfig.node.json`
  — passed.
- `git diff --check HEAD^ HEAD && git diff --check`
  — passed.

Baseline classification:

- `./node_modules/.bin/tsc --noEmit --pretty false --skipLibCheck -p tsconfig.app.json`
  — exit 2 on pre-existing unrelated generated Runtime/Composition and target
  diagnostics; no diagnostics mention the changed accessor, selection adapter,
  selection test, or timeline commit types.

The full `project-element-selection.test.ts` file was not run because one
existing test starts a localhost Vite server. An attempted combined run
reached the sandbox's expected `listen EPERM` restriction; it is not treated
as product evidence. No browser, live socket, full suite, or broad 28-test
repeat was run.

## Decisions and next steps

The required decision was to repair the retained-read handoff rather than
approve synthetic accessor data as if it were produced by the real module.
This follows the HOME preservation proposal 0100 and keeps all custody on the
existing Agent binding plus Runtime admission document.

The harness should commit this worktree with the supplied commit message. The
next functional step is a separately qualified consumer only after the f83
pin-bearing contract exists; until then, keep `admittedElementSource` dormant.
