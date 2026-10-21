# Parent archive prose attribution correction 0303

## Result

Corrected only the misleading archive label in
`ap2-m2-parent-selector-causal-fix-custody-review-0252-REPORT.md`. No App
source, guards, dependencies, pins, artifacts, qualification result, or test
was changed or rerun.

## Exact prose change

Replaced:

```text
Public13 archive:  895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
```

with:

```text
Private App dependency-graph source archive: 895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
Official immutable Composition 0.0.13 archive: 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
```

The `895c628…` digest is retained as the legitimate scoped digest for the
private App dependency-graph source archive. It is not the Composition
archive. The official immutable `@banodoco/timeline-composition@0.0.13`
archive is identified by `9412ae25…`.

## Existing supporting evidence

The settled attribution report
`ap2-m2-private014-archive-attribution-correction-REPORT.md` records that
`895c628…` hashes the 300,830,720-byte private App graph archive containing
the App root manifests, private file packages, symlinked dependency graph,
and the vendored Composition tarball. Its existing `normal014-source-common.sh`
guard separately extracts that vendored tarball and checks its digest as
`9412ae25…`.

That report also records the immutable Composition package as 58,477 bytes,
with package-lock integrity
`sha512-6qgEAcfYqEGuiesoRlBFj1QnEgDKdZsisQdrMivONtc3lAct8thdzVbNV6L7lY5f2D9vvTIZHTD8vKhfWgLOuQ==`.
The existing release evidence records the official 77-member proof in
`handoff-vw-m3-release13-final-gate-REPORT.md` and the sorted member manifest
`handoff-vw-m3-release13-member-manifest.txt`.

## Live callers

The unchanged live mounted path named by review 0252 is:

`onTimelineDrop` → `useExternalDrop.ts:dispatchTimelineDrop` →
`external-drop-utils.ts:handleFileDrop` → `useTimelineState` parent-media
commands → `useAssetManagement.placePreparedAsset` → native
`createTimelineCommands.addClip` → existing `commitSession` /
`useTimelineCommandSession` outbox and commit path.

## Verification

No tests, browser/socket runs, qualification, dependency installation, or
full suite were run. This was a read-only evidence review plus the requested
two-line documentation correction.
