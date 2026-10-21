# Runtime current production tuple

## Current compatible server (post-publication source)

**CURRENT SERVER — 2026-10-21T03:01:50Z — compatible source overlay, not a new publication**

The immutable publication below remains the producer and consumer pin. The
current Runtime integration server is the descendant below; consumers may use
it as the compatible source for the merged follow-up facts, but this update
does not change the published 0.2.14 tuple, pins, or release version.

| Field | Exact value |
| --- | --- |
| Current compatible Runtime source | `be8d254aef249cd421946cbf06ed86d58bc4b307` |
| Current compatible server tree | `6d74348b66ee4a3602cfa4fd56b9b7c0ed7508e0` |
| Current server parents | `2a9bd811ba1d1e65c0fb2c829eefd12939eed83` + `60a919a22f42f0b5b0a246ce84cb43e9f46c2106` |
| Published source producer retained as base | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Transcript source and integration merge | `e2912b3afb6a6d019154185ac8214724da058d58` -> `2a9bd811ba1d1e65c0fb2c829eefd12939eed83` / tree `4fa58b2551f716c35cab6005cc8add84e59da8a9` |
| Rational source and integration merge | `60a919a22f42f0b5b0a246ce84cb43e9f46c2106` -> `be8d254aef249cd421946cbf06ed86d58bc4b307` / tree `6d74348b66ee4a3602cfa4fd56b9b7c0ed7508e0` |

The transcript delta admits retained transcript source reads in
`runtime_protocol/timeline_commit_port.py` and adds its source-boundary
coverage. The rational delta accepts authored rational FPS object mappings at
the inspection boundary and reads them locally at the visual seam without
rewriting stored payloads. Relative to the published `95bd…` tree, the exact
delta is five files, 112 insertions and four deletions: three Runtime modules
and two tests. There is no schema, generated-client, artifact, pin, or
release-version delta.

The two source controls are separately bounded: transcript has the exact
public native `786` node pass plus 29 neighboring cases; rational has 14
controls plus actual admission and malformed-mapping negative coverage. This
does not activate broader association or free-multi behavior.

All 76 paths listed by the published `contract/artifacts.json` were compared
byte-for-byte between `95bd…` and `be8d…`; the comparison returned no
differences. The immutable artifact facts therefore remain producer
`astrid-runtime`, version `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`,
artifact manifest `sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
Runtime schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
and raw Agent schema `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
(55 definitions, 29 operations; raw bundle
`sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`).

The one requested central integration run is terminal and green:
`runtime-full-retained-owned-temp-integration-1021025626-25226`, status
`pass`, exit `0`, on Runtime tree `6d74348b…`; `5997 passed, 26 skipped,
15 xfailed, 12 warnings` in 311 seconds. Command and external snapshot are
recorded in the run summary at
`tests/runtime-full-retained-owned-temp-integration-1021025626-25226/summary`
under the shared orchestration directory. No duplicate full, browser,
renderer, pin, release-version, gate-closure, or ZIP claim is made here.

**PUBLISHED — 2026-10-21T02:51:25Z — ordinary Main014**

| Field | Exact value |
| --- | --- |
| Published Runtime source | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` |
| Published source tree | `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Integration merge | `108713019688b95af4394a8f0395f97d1cf233af` |
| Integration tree | `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Protocol / clients | `workspace.v1` / `0.2.14` Python + TypeScript |
| Runtime schema | `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| Component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| Health schema | `sha256:dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e` |
| Services schema | `sha256:10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018` |
| Raw commit bundle | `sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |
| Artifact manifest | `sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` / `76/76` |
| Contract manifest | `sha256:75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14` |
| Artifact producer/version | `astrid-runtime` / `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |
| Ordinary Agent schema | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` / `55 definitions, 29 operations` |

The source is the exact candidate tree after a successful integration merge;
the merge SHA is recorded for ancestry, while the tree SHA is the publication
identity. Main ancestry is `8bd92de606647d6ffc8887436a3dde3f95ea2330`, with
parents `7a956c027cbbcb498a50de59d85f3b424897f70b` and
`b535646faaad2f8ae7968dfe0f4fa3057f960264`. The shared durable helper is
`runtime_protocol.platform.durable_replace`; the supported verified-read
family is `getProjectMediaSelection`, `getProjectVerifiedMedia`,
`getProjectVerifiedDocumentObject`, and `getProjectVerifiedDocument`.

Client changes are the normal generated Python and TypeScript 0.2.14 package
and metadata outputs, carrying the `/v1` local-door operations
`commitTimeline`, `listTimelineCommits`, and `getProjectMediaSelection`.

The compatible current server named above is `be8d…`, not the immutable
published producer `95bd…` and not the frozen physical `8f…` source.

Existing exact full evidence is 31902: **5,988 passed, 26 skipped, 15
xfail, 12 warnings**, exit 0. This tuple does not claim the separately
requested post-publication integration full, native App bootstrap, renderer,
browser, owner-film, ZIP, or whole-project completion.

The prior public013 tuple is preserved verbatim in
`runtime-current-tuple-public013-historical.md`.

