# Private014 archive attribution correction

## Result

Corrected the App-owned `ap2-m2-private014-enabled-runtime-final-candidate-REPORT.md`
prose only. No App product source, dependency, pin, lockfile, generated file,
or qualification result changed. No qualification rerun was made.

## What `895c628…` is

`895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30` is the
SHA-256 of the private entire App dependency-graph source archive:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar`

The archive is 300,830,720 bytes and contains the graph's root
`package.json`/`package-lock.json`, private file packages, symlinked dependency
graph, and `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`. It is
not a Composition tarball. The graph handoff records 532 package entries and
34 bins in the private graph, with 425 symlinks and the Composition package's
77 extracted regular files byte-matching the official tarball.

## Exact official Composition package

The existing immutable package artifact is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-release13-banodoco-timeline-composition-0.0.13.tgz`

- Package: `@banodoco/timeline-composition@0.0.13`.
- Size: 58,477 bytes.
- SHA-256: `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- App `package-lock.json` integrity: `sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`.
- Immutable Composition source commit: `73bd62b1e1b710a730545c862bd2da76e324ca46`.
- Composition source `package.json` SHA-256:
  `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`.
- Composition source `package-lock.json` SHA-256:
  `f0665832797f59b20afc1e868a11499035046930e1b406d3823cfb704b3018e6`.

## What passed Gate 5 actually guarded

The exact central result remains unchanged:

- Test: `ap2-m2-private014-enabled-runtime-final-candidate-normal014-integration-e2e-gate5-1020195447-8973`.
- Result: **PASS**, exit 0; one test passed in 129 seconds (Playwright journey 32.4 seconds).
- App central snapshot tree: `171d388a9a093f139e1a2519663133ec9ced2f67`.
- Agent: commit `3c4f6de4fa777323b3386c01c7266b619b86af6d`, tree `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`.
- Runtime: commit `202074110717146fc7f08af2306a8dd7f695b0b1`, tree `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Immutable producer: commit `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Runtime artifact: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`; 75 entries; manifest SHA-256 `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- Shared command schema: SHA-256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Runtime wire digest: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.

The run log records `verified artifacts=75`, `private node graph: packages=532
bins=34`, successful runtime-lock checks, and the passing Gate 5 journey. The
existing `normal014-source-common.sh` graph guard checked:

1. source archive SHA-256 equals `895c628…`;
2. graph package metadata is version `0.0.13`;
3. extracting `vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`
   from that graph archive yields SHA-256 `9412ae25…`;
4. the graph is private/read-only and its public13 `computeMediaTrim` export
   behaves as expected.

That Gate 5 guard did **not** count tar members. The separate immutable
Composition release evidence is the 77-file proof:

- `handoff-vw-m3-release13-final-gate-REPORT.md` records 58,477 bytes, 77
  regular members, and an exact sorted-list match.
- Existing manifest:
  `design/handoff-vw-m3-release13-member-manifest.txt` — 77 lines, SHA-256
  `2aeb7aa398d764b86bec9c4d32823bfdaa7b7bb0d2b02a5f09cfb7bf47e88322`.

Therefore this correction does not claim nonexistent 77-member validation in
the `0148973` Gate 5 run. It claims the exact official tarball-byte guard used
by that run and separately identifies the existing official 77-member guard.

## Limits and tests

The original report's tested tuple, one central PASS, focused local results,
and limits are otherwise preserved verbatim. In particular, this correction
does not claim public pin/adoption, repack/publication, dependency install,
browser/native/full-suite rerun, or requalification of the unchanged tree.

Read-only inspection only; no test or qualification command was rerun for
this attribution correction. Evidence was taken from the existing 0148973
log, `normal014-source-common.sh`, the locked-graph report, the Composition
release reports, the package/lock source at the immutable release commit, and
the existing 77-member manifest.
