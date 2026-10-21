# Runtime current production tuple

## Current compatible server (post-Speech merge source)

**CURRENT SERVER — 2026-10-21T03:48:20Z — compatible Speech source overlay, not a new publication**

The immutable publication below remains the producer and consumer pin. The
current Runtime integration server is the descendant below; consumers may use
it as the compatible source for the Speech follow-up facts, but this update
does not change the published 0.2.14 tuple, pins, or release version.

| Field | Exact value |
| --- | --- |
| Current compatible Runtime source | `b92d3e7a05eec65c142294ef4873edd059e9b31d` |
| Current compatible server tree | `6abc2f117391de8e7e35c0283f575a002199894d` |
| Current server parents | `30413e3c3e6db027f450e864ea9cb4a07446475b` + `40708263d26ef39ac484cbc9f1ae7f34cfc368bc` |
| Approved Speech source merged | `40708263d26ef39ac484cbc9f1ae7f34cfc368bc` / tree `6abc2f117391de8e7e35c0283f575a002199894d` |
| Published source producer retained as base | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| External full-run source tuple | Agent `7ab6cbae273f133b3adf2a7bae9f2439f02ce71e`; App `c45cc175a62701593af4ec2503467d681ec9c2f7`; Composition `7bb54bbd64107e5090643ecca1e4d33164173e85` |

The Speech product delta is limited to the existing primary-WAV fallback:
the first settlement now accepts the already-declared `audio` or `speech`
output port when the settled output is WAV and duration is absent. It remains
absent-only, respects explicit duration metadata and null/value behavior, and
does not consult sidecars or caller authority. The restored audio positive and
new speech behavior are covered without changing the DTO, generated clients,
schema, accepted metadata/catalog/receipt rows, or publication identity. The
merge is an actual descendant of published producer `95bd…` through
`30413…`; the earlier `30413` full is historical after this source change.
The source qualification retained the prior **36 passed, 1 deselected** local
speech controls and **16 passed** central targeted settlement controls; the
restored legacy audio positive then passed as **1 passed** and the speech test
body remained identical to the prior passing source.

All 76 paths listed by the published `contract/artifacts.json` were compared
byte-for-byte between `95bd…` and current `b92d…`: **0 differences, 0 missing
paths**, and all 76 current blobs match the published manifest hashes. The
immutable artifact facts therefore remain producer `astrid-runtime`, version
`sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`,
artifact manifest
`sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
Runtime schema `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`,
and raw Agent schema
`sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
(55 definitions, 29 operations; raw bundle
`sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3`).

The one requested central integration run on current `b92d…` is terminal and
green: `runtime-full-retained-owned-temp-integration-1021035028-28646`, status
`pass`, exit `0`, on Runtime tree `6abc2f117391de8e7e35c0283f575a002199894d`;
`6002 passed, 26 skipped, 15 xfailed, 12 warnings` in 298.37 seconds. The
exact command was `env ASTRID_CHECKOUT=/home/user/work/agent
PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m4-full-temp-retain-all-final/runtime-full-retained-temp.py
-- /home/user/work/venv-runtime/bin/python -m pytest -q -n 3`.
The 26 skips are Windows-native API cases; the 15 xfails are the held RT02/D04
legacy timeline-writer/clip-replacement cases; the 12 warnings are Python
3.13 fork deprecations (10 from `tests/test_realm_admission_hardening.py`, 2
from `tests/test_t4_replacement_foundation.py`). There were no failures. The
prior `30413` run `runtime-full-retained-owned-temp-integration-1021033039-31374`
(`6000 passed, 26 skipped, 15 xfailed, 14 warnings`) remains historical and
its baseline is not relabeled or lowered.

The current private C3d Speech descendant is separate. Ordinary Main014 is
not a private15 tuple; no pin, version, adoption, or release change follows
from this compatible-server fact. No browser, renderer, root/outer Speech
workflow, gate-closure, or ZIP claim is made.

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

The prior compatible server was `be8d…`; the current server named above is
`30413…`, not the immutable published producer `95bd…` and not the frozen
physical `8f…` source.

Existing exact full evidence is 31902: **5,988 passed, 26 skipped, 15
xfail, 12 warnings**, exit 0. This tuple does not claim the separately
requested post-publication integration full, native App bootstrap, renderer,
browser, owner-film, ZIP, or whole-project completion.

The prior public013 tuple is preserved verbatim in
`runtime-current-tuple-public013-historical.md`.

