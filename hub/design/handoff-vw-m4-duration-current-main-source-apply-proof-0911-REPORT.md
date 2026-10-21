# Composition current-source main-apply proof

## Result

PASS. The current Composition source applies cleanly to the actual frozen
`origin/main` through the existing normal Git patch/bundle delivery recipe.
The source worktree remained unchanged and clean. No package, build, product
test, browser, renderer, Runtime, install, full-suite, or ZIP tooling ran.

## Exact source frontier

| Item | Identity |
| --- | --- |
| Current source ref/commit | `tl/integration` / `df7b86308902fae90eda1dc3080d17d8fc30ea78` |
| Current source tree | `71d8e95edb1bb2d187c3193ef3462d4cfde277fa` |
| Last proven source commit | `7bb54bbd64107e5090643ecca1e4d33164173e85` |
| Last proven source tree | `20467712e66dbadff4d562c0d5baae22b8c077a7` |
| Actual base ref/commit | `origin/main` / `67b8aa3d0d6831d3e3504a340ff583c3da253707` |
| Actual base tree | `62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120` |
| Main-to-current changed paths | 118 |
| Current source tracked paths | 120 |
| Current-vs-last-proven paths | 2 |

The exact current-vs-last-proven delta is:

- `typescript/src/lib/duration.ts`
- `typescript/tests/duration.test.ts`

The duration source change narrows only the input declaration to
`<T extends Pick<TimelineConfig, 'clips'>>`; its function body and runtime
arithmetic are unchanged. The new test covers clip-only, resolved, and full
configuration inputs.

## Delivery artifacts

Retained under the worker's private delivery directory:

- Patch:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-duration-current-main-source-apply-proof-0911/delivery/composition-origin-main-to-df7b8630.patch`
  SHA-256 `870937a269d61ea7ae85f7a154a938e4ac2430de1192061ff84a556853b443b5`
- Bundle:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-duration-current-main-source-apply-proof-0911/delivery/composition-origin-main-to-df7b8630.bundle`
  SHA-256 `ea1228dd9cfa1ab10ba6ca2e608b9ad19f57013c4933e5d3f153541521b762a8`
- Manifest:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-duration-current-main-source-apply-proof-0911/delivery/composition-origin-main-to-df7b8630.manifest.json`
  SHA-256 `7955f9502cfd049254e42f1a52325f820851817e69693554443dadac60e45d8e`

No final ZIP or package archive was created.

## Commands and results

- `bash -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-duration-current-main-source-apply-proof-0911/COMMAND` — PASS.
- `bash /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-duration-current-main-source-apply-proof-0911/COMMAND` — PASS.
  The command checked exact refs/trees and ancestry, the 2-path current
  frontier, all-100644 modes, the retained `.gitignore`, `Makefile`, and
  TypeScript configs, and the two intentional deletions
  (`typescript/tests/scaffold.test.ts` and
  `typescript/tests/theme-api-smoke.ts`).
- Bundle verification — PASS: bundle head is
  `df7b86308902fae90eda1dc3080d17d8fc30ea78 refs/heads/tl/integration`;
  prerequisite is `67b8aa3d0d6831d3e3504a340ff583c3da253707`.
- Fresh-main reverse apply — PASS: 29 paths equal the fresh base by SHA-256
  bytes and stat mode.
- Fresh-main forward apply — PASS: 120 paths equal the current source by
  SHA-256 bytes and stat mode.
- `git status --short --branch` — PASS; source worktree is clean.

The private fresh-main stage was removed after comparison. The retained
delivery directory contains only the patch/bundle proof outputs, path lists,
verification text, manifest, hashes, and command log.

## Decisions and limits

I reused the existing `git diff`/`git bundle`/fresh-archive
`git apply` recipe and changed only its exact source/frontier guards for the
current `df7b8630` source. A private command-text awk escaping defect stopped
the first attempt before artifact creation; it was corrected and the complete
run then passed. No source decision was changed.

Unchanged full85/build evidence from the 0817 recipe was not rerun, as
directed. No new full suite, pack/public14 attempt, browser/render/Node helper,
socket, Runtime, install, or graph copy was run. This is source patch/bundle
application proof only, not a package, ZIP, or all-repository qualification.

