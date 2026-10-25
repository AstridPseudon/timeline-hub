# Validation — App16 corrected classification

## Source and preview

- Fixed source tuple: base `3881e9440688f774878e18806da2dc5c993a9b00`, ours `d5a1d1ab6550187e377fd7387d300102b8b82ece`, upstream `213318f1ec6ea5c324787bbd1c30a73072d1151a`.
- Ours tree: `7be73e2cbbcf89d627bf7b9da940b4ce17968c20`; merge base equals the fixed base.
- Read-only command: `git merge-tree --trivial-merge BASE OURS UPSTREAM`.
- Preview: 769,114 bytes; SHA-256 `6c7cf7073a554a81ddbfe9aca90da2a192e73bed90245e137e030998c4439535`.
- Qualified 1844 census and independent 1850 review were read as inputs; their App count is 16, and the fixed tuple/header order is retained.
- Original delivery route was checked in the prior review: `delivery-build:195-198` invokes `git am -q`; no `git apply --whitespace=error` route exists. No whitespace-error flag and no EOF cleanup are inferred.

## Exact artifact checks

- JSON parse: PASS for `conflict-classes.json`, `findings.json`, `hunk-map.json`, and `source-manifest.json`.
- Exact path set: PASS, 16 paths.
- Exact preview-header set and order: PASS, 81 headers; `hunk-map.json` has ordinals 1–81 with no duplicates.
- Conflict-marker classification: PASS, 14 true marker hunks, 67 clean/nonconflicting hunks.
- Semantic/trivial split: PASS, 13 semantic true conflicts and one textual import union.
- Coverage: PASS, 81/81 classified, zero unclassified.
- Source blobs: PASS, 48/48 base/ours/upstream blob IDs match the immutable source manifest and all resolve as Git blob objects.
- Source bytes: PASS, all 16 files have base/ours/upstream SHA-256 entries in `source-manifest.json`.
- Current worker worktree: PASS, `git status --short` is empty and `git diff --check` is clean.
- Outside-blobs check: PASS, no source blob or ref object was written or changed; no checkout, fetch, merge, rebase, reset, or commit was run.

## Boundary checks

- Mounted caller and registered Runtime `commitTimeline` transport are documented in `findings.json` and `conflicts.md`; helper-only and fixture-only paths received no credit.
- C0 full v2 request fields, command shape, replies, dry-run null-receipt form, authority, guards, privacy, live inputs, and predicates are recorded as preserved constraints.
- Both test families remain required; no tests were changed, skipped, weakened, or rewritten.
- No semantic resolution, normal merge, clone/fetch/ref mutation, ZIP/build, package install, typecheck, lint, Vitest, browser/live socket, body test, acquisition, D130, or full suite was run. These are NOTRUN by task scope.
- `trivial-resolutions.patch` is prepared only as a mechanically justified artifact and was not applied.
- Evidence-only patch check: PASS with `git apply --check` against a temporary copy of the immutable base file; no repository path was modified.
