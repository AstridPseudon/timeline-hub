# Scene-layer current C13 package identity correction

Date: 2026-10-21 UTC

## Result

The prior packaging gate reported the wrong archive identity. Its quoted
`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` is the
Composition `0.0.12` archive, not current C13. It remains historical evidence
for `0.0.12` and is not relabeled.

The actual current C13 identity is:

- archive: `remotion/artifacts/banodoco-timeline-composition-0.0.13.tgz`
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`
- archive tree: 77 regular files; `package/package.json` version `0.0.13`
- manifest and lock resolution: `file:artifacts/banodoco-timeline-composition-0.0.13.tgz`
- lock package version: `0.0.13`
- lock SHA-512 integrity: matches the C13 archive bytes
- lock SHA-256: `c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`

The retained commands show an artifact-target/transcription error, not a
wrong Composition runtime driving the prior behavior evidence. The old
identity probe explicitly opened the `0.0.12` path; its focused suite ran
Python tests and import/catalog checks and did not execute Node or Composition
runtime code. Therefore the old `0.0.12` hash is historical only, and no
behavioral result is reclassified as C13 from it.

## Current bounded gate

Read-only checks passed against the current worktree and immutable Runtime
checkout `/home/user/work/wt/rt-pin-9d1c43c6` at commit
`9d1c43c647301da48a6e86ad82e466b501bd2418`, tree
`50e74e3243c5da4cf77b6e6cc76605fae8aeb649`:

- C13 archive manifest, 77-file count, SHA-256, lock resolution, and lock
  SHA-512 integrity: passed.
- Node `/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node`:
  `v20.19.4`; installed read-only `@banodoco/timeline-composition`: `0.0.13`.
- Node20 imports of the installed C13 package, `evaluation`, and `registries`
  entrypoints: passed.
- Current Agent `scene_answers` import/resource path, setuptools discovery,
  old-module absence, and immutable Runtime `server`/`timeline_commit_provider`
  import origins: passed.
- Prior exact source predicates: no old `scene_answers` consumers; no
  `astrid.core.rendering` edge from `astrid.core.timeline`; moved helper
  source bytes/AST parity: passed.
- Candidate tree: `07f02438a1171e80eeb6f7bf0859adbec0260c05`.
- `git diff --check`: passed; worktree clean.

No artifact refresh was required: the existing generated C13 archive and lock
already agree. No generator, pin, DTO, root behavior, or test assertion was
changed.

## Scope boundary

The prior source move, test-assertion parity, and current six-cycle graph
evidence are retained as already proved. This correction does not replay the
prior 42-test behavioral lane, run physical/managed/render proof, or perform a
review of a review. Full, browser, live-socket, and behavioral replay suites
were not run.
