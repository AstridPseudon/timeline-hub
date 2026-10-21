# Runtime Main014 publication record

**PUBLISHED — 2026-10-21T02:51:25Z**

This is the ordinary Main014 Runtime publication after the authorized merge.
It is a source and artifact record only: no external registry or push was
performed, and it makes no test-gate, renderer, browser, owner-film, ZIP, or
whole-project completion claim.

## Exact source and integration identity

| Field | Value |
| --- | --- |
| Runtime candidate/source | `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` |
| Candidate/source tree | `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Actual integration merge | `108713019688b95af4394a8f0395f97d1cf233af` |
| Actual integration tree | `d3a290b407fa61e6ab2d476f50c068073f70df00` |
| Integration merge parents | `9d1c43c647301da48a6e86ad82e466b501bd2418` + `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` |
| Integration parent tree | `50e74e3243c5da4cf77b6e6cc76605fae8aeb649` |
| Candidate true merge parent | `d1bde2c9c29f5fc088b9076db12ebc0a16411d3a` |
| Main-merged base | `8bd92de606647d6ffc8887436a3dde3f95ea2330` (tree `d964d7138be203f7f18d8ff1f4f109805161cf5d`) |
| Main parents | `7a956c027cbbcb498a50de59d85f3b424897f70b` + `b535646faaad2f8ae7968dfe0f4fa3057f960264` |

The post-merge identity was checked directly: `95bd3c5f` is an ancestor of
`1087130`, and `git diff 95bd3c5f 1087130` is empty. The resulting merge SHA
therefore differs while the published source tree remains exact.

## Contract, artifacts, and normal metadata

| Field | Value |
| --- | --- |
| Protocol | `workspace.v1` |
| Python and TypeScript client/package | `0.2.14` / `0.2.14` |
| Runtime schema digest | `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| Component manifest digest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| `health.json` digest | `sha256:dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e` |
| `services.json` digest | `sha256:10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018` |
| Raw commit bundle digest | `sha256:6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |
| `contract/artifacts.json` digest | `sha256:a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` |
| `contract/manifest.json` digest | `sha256:75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14` |
| Artifact count | `76/76` |
| Artifact producer | `astrid-runtime` |
| Artifact version | `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |
| Raw Agent command schema | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Ordinary command shape | `55 definitions / 29 operations` |

The generated Python/TypeScript clients and contract metadata are the normal
0.2.14 outputs. Main's existing `runtime_protocol.platform.durable_replace`
is the shared durable publication helper (`runtime_protocol/platform.py:212`);
there is no second timeline writer, `/astrid/v1` route, or paired relay.

## Existing qualification evidence

The matched Runtime full is
`rt-m2-main014-reference-fixture-clock-repair-full-retained-owned-temp-integration-1020233140-31902`:
**5,988 passed, 26 skipped, 15 xfailed, 12 warnings**, exit 0. This is the
qualified full result on exact `95bd3c5f` / tree `d3a290b4`; it is not a new
full run by this publication worker. Existing qualified consumer identities
are Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556` and App normal pin
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a` / tree
`01fd2a04ff0c383ec5281043c7e5a4c843d1d835`.

The manager separately requested one integration full after this publication;
that result is not represented here.

## Supported reads and adoption boundary

The supported verified-read family is the existing four-operation family:
`getProjectMediaSelection`, `getProjectVerifiedMedia`,
`getProjectVerifiedDocumentObject`, and `getProjectVerifiedDocument`. Their
wire shapes remain separate and use exact retained declarations/object inputs;
no latest-head fallback is implied.

Agent and App must make **one normal coordinated pin adoption** to this
published Runtime source. Agent must include the HELD Main497 upstream merge
(`497714c73531f164082555ec81b61ca5bc8b6554`) in that same unit. App keeps its
current initializer path; dormant `timeline.init` native bootstrap is not
activated by this publication. The App 409 capture-mismatch diagnosis remains
a separate post-publication item.

Composition13 stays in force. Composition14, private15, ref/raw/launcher,
and any other follow-up are separate and are not included in this record.

