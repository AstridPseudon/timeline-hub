# Worker report: authorized Main014 publication

## Result

Published ordinary Main014 Runtime documentation after verifying the
authorized merge. No Runtime source, schema, generated client, lock, registry,
or integration worktree was edited by this worker.

- Candidate/source: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- Candidate/source tree: `d3a290b407fa61e6ab2d476f50c068073f70df00`
- Actual merge: `108713019688b95af4394a8f0395f97d1cf233af`
- Actual merge tree: `d3a290b407fa61e6ab2d476f50c068073f70df00`
- Merge parents: integration `9d1c43c647301da48a6e86ad82e466b501bd2418`, candidate `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`
- 0.2.14 artifact manifest: `sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`, 76/76
- Artifact version: `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`
- Runtime schema: `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`
- Ordinary Agent schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`, 55 definitions / 29 operations

The candidate is an ancestor of the merge and `git diff` between candidate and
merge is empty, so the merge SHA differs but the exact source tree is retained.
The previous public013 tuple is preserved as
`design/runtime-current-tuple-public013-historical.md`.

## Existing evidence recorded

The exact matched full31902 result is **5,988 passed, 26 skipped, 15 xfailed,
12 warnings**, exit 0. Existing qualified consumer identities are Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
and App `10fa2ff9a8216604aa39e3584f89dc9e7a09080a` / tree
`01fd2a04ff0c383ec5281043c7e5a4c843d1d835`.

The supported verified-read family remains the four existing operations:
`getProjectMediaSelection`, `getProjectVerifiedMedia`,
`getProjectVerifiedDocumentObject`, and `getProjectVerifiedDocument`.

## Commands and results

- `git -C /home/user/work/runtime show -s --format=... 1087130`: PASS; merge SHA/tree/parents matched the queue result.
- `git -C /home/user/work/runtime merge-base --is-ancestor 95bd3c5f 1087130`: PASS (exit 0).
- `git -C /home/user/work/runtime diff --stat 95bd3c5f 1087130` and `diff --name-status`: PASS; empty diff.
- `git show 1087130:contract/artifacts.json | sha256sum`: PASS; `a902387c…a532d`.
- `git show 1087130:contract/artifacts.json | jq '.artifacts|length'`: PASS; `76`.
- Hash checks for `contract/manifest.json`, component manifest, health schema, and services schema: PASS; exact values are in the publication record.
- Metadata inspection of Python/TypeScript package and contract metadata: PASS; `0.2.14`, `workspace.v1`, schema/component digests match.
- `git status --short --branch` on this worker worktree: PASS; clean, no product changes.

No targeted product tests were run because this task changed only ORCH
documentation and handoff files. No new full, localhost, browser, renderer,
or integration suite was requested or run; the separately requested one
integration full remains manager-owned.

## Decisions and boundaries

The 02:48Z orchestrator ruling decouples publication from the dormant App
native bootstrap. Therefore the record publishes now, requires one normal
coordinated Agent/App pin adoption, carries Agent’s HELD Main497 merge in that
unit, and keeps App’s current initializer with no dormant `timeline.init`
activation. Composition13 and private15/ref/raw/launcher follow-ups remain
separate. No gate, source, physical render, whole-ZIP, or project completion
claim is made.

