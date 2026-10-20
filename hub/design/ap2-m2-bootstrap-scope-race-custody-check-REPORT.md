# AP2-M2 bootstrap scope-race custody review

## Verdict

**APPROVE — `ce47d30a0654f25ec25613e4ac95b60d77c8e912`** for the bounded
project-scope assertion repair. This approves the source/assertion candidate,
not the real browser gate. The next real bootstrap gate may proceed only after
this approval; it was not run here.

The candidate commit is based at `812a609ee`, while the requested
`hub/tl/integration` is `e4ee1dceb` and already contains the f487 bootstrap
source. Thus ce47 is a carrier commit. The effective repair delta against the
current base is the three scope/journey files plus the wrapper; the apparent
`genericPatchCapture`/`ordinaryTrimMember` snapshot differences in
`git diff hub/tl/integration..candidate` are branch-age divergence, not part of
this custody approval. Merge-forward must preserve the effective delta.

## Old -> new assertion map

| Before | After |
| --- | --- |
| `await expect(page).toHaveURL(/\\/tools\\/video-editor\\?project=/, CEILING);` accepted any project URL, including the pre-create project. | `page.waitForResponse(...)` first captures the normal `POST /v1/projects` whose request name is the submitted unique project name, requires HTTP 201, and reads `data.project_id` and `data.name`. |
| `new URL(page.url())` immediately after the broad wait supplied the stale project (`36498405a10c4b2ab9a5412eaf22a9a5`). | `waitForCreatedProjectUrl(page, createdProjectId, CEILING)` requires pathname `/tools/video-editor` and query `project === createdProjectId` before taking the URL snapshot. |
| The original strict `expect({ realmId, projectId, timelineId }).toEqual(createScope)` was reached with a mixed-time `projectId`. | That strict equality remains unchanged, with an additive `page.url().project === createdProjectId` assertion. |

The causal regression uses the retained 26944 IDs. With the old broad
predicate, the regression is **2 pass / 1 fail** at the intended premature
settlement assertion (`true !== false`). With the repaired exact predicate it
is **3 pass / 0 fail**. It also rejects a previous-project URL with the right
timeline and a different route with the right created-project query.

## Custody and authority review

The normal project-create response is the authority for the new project ID:
the test matches the response to the submitted unique name, checks 201 and
response name, reads `/v1/projects/{createdProjectId}`, and requires the
native timeline-create route’s project segment to equal that response ID.
The outbox reservation and native init are then matched by the complete
realm/project/timeline scope. Final navigation uses that same response ID;
the selected timeline is looked up by exact `timeline_id` from the explicit
`/v1/projects/{projectId}/timelines` list. No foreign project, arbitrary list
item, latest-head guess, undo result, or shortened URL assertion is adopted.

The original controls remain present in the reviewed candidate: reservation
before POST; held create/init ACK ordering; exact create/init outbox scope;
create-before-init audit ordering; cancel/uncertain-prefix behavior; stale
generation fencing; dirty-draft retention; one bootstrap history entry with
`previous: null` and the original `timeline.init`/two `track.create` records;
lost ACK, reload/runtime restart, byte-identical retry, guarded
`timeline.inverse`, original track restoration, and zero legacy snapshot
traffic. The source repair adds no production provider/session authority.

## Wrapper/source custody

The existing wrapper still uses donor ref
`f487c0ca9a7b916bf842dd7a2cb3fa442ebeda3e`, donor tree
`6444fffcaa606bfe83101ccb561c47fbd0d10ce4`, the locked normal014 tuple, and
the exact one-test Playwright list proof (`1 test in 1 file`). It compares the
13 non-repaired approved files byte-for-byte with the donor and pins the three
repaired source hashes:

```text
three-products.spec.ts                  fda4df2030ff09d8c6606611c84f5ed761ca4cf7836190903348c579d95a08f6
timeline-scope.ts                        a2965d220628de15bb169baff96dd1db020248d3df727ea6e2d83640b17346ab
timeline-scope.test.ts                   71e73fd4fc59ae5079144518d1aa0d0be5fa1818e3b9c9e7c529b037527175ee
```

The new custody-path cleanup delta is limited to a status-preserving EXIT
cleanup trap and copying only the test’s sanitized `bootstrap-scope.json`
snapshots to the named evidence directory before deleting the private run
root. The wrapper no longer overwrites the repaired three files with frozen
donor blobs. No raw credentials, headers, bodies, Runtime database, or broad
browser output is retained.

One non-blocking metadata note: the candidate wrapper mode is `100644` versus
the prior `100755`. The central suite invokes it explicitly as `bash
tests/.../bootstrap-wrapper-selector-source-fix.sh`, so this does not affect
the requested gate command; restore executable mode if direct `./wrapper`
invocation is required.

## Evidence

Reported by the candidate worker and checked within this read-only review:

- App targeted Vitest: **128 tests, PASS**.
- Native parity pytest: **12 tests, PASS** (one existing unknown-mark warning).
- Scope regression/helper: **3 tests, PASS**.
- ESLint, strict-island typecheck, `tsconfig.node` typecheck, shell syntax,
  and `git diff --check`: **PASS**.
- Playwright `--list`: **1 test in 1 file**, no browser launched.
- Independent extracted-candidate scope run with `node --import tsx`: **3/3
  PASS**; candidate wrapper blob `sh -n`: **PASS**; all three pinned hashes
  match.

Not run by this review: browser, socket, request-test, full suite, build, or
the unchanged 26944 gate. The real create/init/retry/restart/undo behavior on
the repaired candidate therefore remains unverified and must be established
by the next authorized bootstrap gate.
