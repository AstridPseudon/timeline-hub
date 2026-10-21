# APPROVE — canonical stage-sort packet 1140

Independent review result: **APPROVE for the next central prerequisite only**.
This review covers only the new canonical graph-binding correction; it does not
re-review unchanged stage/root custody or source diagnosis.

Packet:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-canonical-stage-sort-packet-1140/packet`

Exact identities:

- packet `SHA256SUMS`: `341d40cf87d379ff2257ad9710752a0c65d2b1ce5680dc962ebde1dd816c9f53`
- `stage-audit.mjs`: `70f2394e2fa174605f73f275d166bcb922955ff02004be115a744269b87c0a41`
- `run.sh`: `82a9171a93dbc2bed1cb7a58b287aa3aa1640380f24c95069355206a6715a9a9`
- `issue.mjs`: `1e1ad3572e8c2d3c6d9a1464920bd86f4a24189c513a3fb29ea05d2c05b29509`
- frozen App0d43 controller: `f536eff2773cd1ffd87678d647b99facd01c7cfa6d649d98ae7a0b7387038c27`
- frozen controller `hashTree` function: 870 bytes, `15e7a670adfc914fca2eed54b9c1c70d53f5df1e1ff16534247d0e6841767469`
- 1131 diagnostic packet `stage-audit.mjs`: `9d3b661a592f656189f5db2818a3edf64060be11428376f0b23ac14a9b2919f8`

The changed `tree()` binds directly to the frozen controller export, whose
complete-record lexical sort is exactly:

```js
entries.sort(([left], [right]) => left < right ? -1 : left > right ? 1 : 0);
```

The packet's actual audit reports source and stage as
`4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c / 21455`.
`SOURCE_GRAPH` remains that expected constant; it was not replaced with the
diagnostic `f06d7fe955f936e7a6370cee1900bd4d32a5676d65a8f9a7f46f8b4ce8ec352a`.
The stage custody bindings remain `MANIFEST=b349c5344ec607bc32b0e4711adf317aacd984ce98d3e5a316ba726079bb37ac` and
`NODE_MANIFEST=0d9da325991bfed2fda247284adb37885d118a08f5f4fc655128f6b7481c04de`.

The 1140 operational namespace/grant/marker references are the only packet
reference changes. The direct readlink and gzip/tar-header paths are
child-spawn-free equivalents used for the local audit; fixed source, lock,
manifest, archive, graph, inode/link, closure, disk, CLI, environment, socket,
and cleanup assertions remain present. The fixed public13 hash remains
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738` with 77
regular members; the lock remains
`c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24`.

Producer evidence reports the tiny changed-byte and missing-file fixtures
refused. No stale 1120 failure evidence is in the packet and no graph was
copied or modified.

Checks run for this review:

- `(cd packet && sha256sum -c SHA256SUMS)` — PASS, all nine files.
- Independent controller extraction/hash — PASS: 870 bytes and the exact
  `15e7a670…` function hash; final lexical sort present.
- Packet evidence and constant scan — PASS: `4913…/21455`, expected manifests,
  no stale `f06d…` result, fresh 1140 grant/marker references.
- Assigned Composition worktree `git status --short` — PASS, clean.

Not run by this review: helper, browser, Runtime, server, socket, central or
physical execution, install, graph copies, and full suites. Central must still
perform its separately authorized single preflight against these exact packet
bytes; no physical authorization is implied by this review.
