# Viewing → Runtime/App: five-case freeze and compatibility ACK

Please ACK this exact compatibility tuple for the current App five-case
controller. This is a compatibility/source-freeze handoff only; it is not a
grant, capture, browser, render, physical-mix, or foundation approval.

## Runtime tuple

```text
server_sha=8f105c26e3b62f9c2683f717a9773a12bc775a8e
server_tree=b7f456d5135cba6049980ebc43a91c7a72ab8f7e
producer_sha=2c4ac180c2220bdad966bc01e95ad230e99ce26a
producer_tree=7ab412cc4bcbe517efcfa806e092336390312e18
contract_version=0.2.13
schema_digest=sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4
artifact_version=sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56
artifact_count=75
```

Runtime audit evidence is **143 targeted compatibility tests passed**,
generated/artifact checks passed, and no public013 wire incompatibility found.
Please confirm that the server SHA is intentionally distinct from the normal
client/artifact producer SHA and that the published contract/artifact bytes
remain unchanged. The ACK does not authorize any live run.

## Current App freeze facts

- Current App source at inspection: `20ea14c26526fe4924354f10a177aebbaf6002bc`
  / tree `83cfad527f8b2264085571316cede1c6ae482b5f`.
- Offline controller discovery: exactly five current
  `native-codec-chrome155` cases; Playwright list: 5 tests in 1 file.
- Node real path:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node`,
  `v20.19.4`, SHA-256
  `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`.
- Public13 Composition artifact: 77 members,
  SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Chrome guard: 155.0.8059.84, executable SHA-256
  `cb19b59995072b86cc7f887b3b1c7ab1f63518a7f2ed9f0d33249e1a040e2c76`,
  full tree SHA-256
  `5b9b48fad617dc414d4a18ccfe9c7933c7bc4a8efd78c70d4f7a9e853808de0e`,
  255 files.
- Current flat owner ports are complete: App `a8283307`, `a04f90cf`,
  `f084855e`, `379c1950`; Agent public13 normal pin
  `6f0cdc7d`. `MISSING_OWNER_PORTS=[]`.
- The source tuple still requires six exact peer paths per App/Agent consumer:
  Remotion shared-audio-tags, Remotion ESM index, Player CJS
  use-player-methods, Player ESM index, Player CJS use-playback, and Player
  CJS PlayerUI. No manager-frozen six-value hash tuple was supplied here, so
  no values were invented or silently repinned; missing/changed values remain
  refusal conditions.

The controller still preserves stale-source refusal: its historical App13 pin
is `ea38656fe62950440b36cafee780698cff2c3f9c` /
`8bd8f741f7c8b28b8682aa960a658417f70c8522`, not the current App source above.
The exact Node20 controller/unit/source-tuple lanes pass, and the no-capture
`--ready` probe exits 1 in this sandbox at `spawnSync git EPERM` before it can
print the expected source mismatch. This is not a readiness approval.

The normal reviewed973 MP4 prerequisite, fresh grant/marker, manager-frozen
tuple/private graph, and central browser lock remain required before any grant
or browser action. Raw media and provenance are preserved.
