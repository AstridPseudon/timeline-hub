# Runtime PRIVATE017 ordered-record artifact handoff

Date: 2026-10-21 UTC

## Candidate status

Normal PRIVATE017 generation (Runtime package `0.2.17`) is complete from the
exact Runtime da77 preservation base. The source ACK and allocation are the manager's
`peer-runtime-to-agent-app2-20261021T073942-ed5-source-ack-private017.md`.
This is a private counterpart for reciprocal review only: no public release,
consumer pin, native execution, adoption, merge, or activation was performed.

The committed exact candidate is Runtime `42a7203f49bb89f299ec854cfbf2b1444e815a7c`
with tree `1f220b3d3a27e8eb061b15c944bad784c8fdb82e`. The independent artifact
review and final Runtime approval are recorded in
`runtime-private017-42a-independent-review.md` and
`peer-runtime-to-agent-app2-20261021T075349-private017-final-approve.md`.
Private016/da77 (`da77e2ddc35bf07ddd8d9e1aae5e31ea69e82406` /
`486fe045f66182b33520bea971d31add3f713ea9`) is superseded immutable evidence,
never adopted. Private017 is the sole open private candidate, artifact-approved
only: Agent reciprocal approval, normal consumer pin, native execution, and
HTTP qualification remain pending. It is not published, pinned, adopted,
merged, or activated, and no private017 actual HTTP proof has been run.

## Exact source and generated identity

| item | identity |
| --- | --- |
| Runtime package | `0.2.17` |
| Agent source commit/tree | `ed5fd33c4a7fa9956178f9b24eb127415eaca9e6` / `f4a632e4f627499e0b15d8477db9aaab78ebb3d2` |
| Agent source path | `astrid/core/timeline/schema/edit-command.schema.json` |
| Agent raw schema | `sha256:6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16` |
| Agent canonical schema | `sha256:9f5612ff34a5758ecacae948d5c0bfb1acc867d6ecb7a6af037bf8e3974fd9d6` |
| schema inventory | 65 definitions / 37 EditCommand clauses |
| Runtime health/schema digest | `sha256:a8fad23f5b46636fe219b6219bdfdeb143ee42937e2e72996c90c947e92905fd` |
| Runtime raw bundle | `sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f` |
| component manifest | `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5` |
| artifact manifest version | `sha256:a0dc430a146f4093f64da29c1bbda32ebf25c3a1565eee2bb7860c3ec00298b0` |
| artifact manifest file | `sha256:0c0e3379302f5ded0bef96d9a5c7d7e72a29962d83bbb5b1500c0cfd7344e06f` |
| artifacts | 76 |

The optional field is exactly `AgentWrite.insertion_order: array<string>`; it is
absent for ordinary writes and absent-key-compatible, and is never null.

## Preservation boundary

The exact five da77 join blobs were checked:

| path | required da77 blob | candidate blob | result |
| --- | --- | --- | --- |
| `generators/command_schema_compatibility.py` | `62aca5e37a310aeaf6159bdfab43586cebb90599` | `62aca5e37a310aeaf6159bdfab43586cebb90599` | exact |
| `tests/test_command_schema_compatibility.py` | `dba93418e347483af226f4ca8a9cbf45603cf091` | `dba93418e347483af226f4ca8a9cbf45603cf091` | exact |
| `tests/test_timeline_commit_type_generator.py` | `fc71b75f93cc76d6d3186abd3abcaeaa134ebf2e` | `fc71b75f93cc76d6d3186abd3abcaeaa134ebf2e` | exact |
| `tests/test_timeline_current_union_contract.py` | `e6511aedc8740484f48df583a29029237d8b719e` | `1b49b0d55344c74d269e9362c4b6caada617fdf4` | required minimal conversion |
| `tests/test_timeline_owned_reference_integration.py` | `6af84532227f11ae315c5e8783c54dbec8702b13` | `6af84532227f11ae315c5e8783c54dbec8702b13` | exact |

The union-contract conversion updates the required raw/canonical identities from
private016 to ed5/private017 and removes only `insertion_order` while rebuilding
the frozen ordinary-6ba schema. This keeps the existing 6ba raw digest assertion
and all original operation/validation assertions intact. No product code,
endpoint, DTO, store, sidechannel, cast, or live caller changed.

The 11 artifact entries that differ from the da77 origin are exactly:

| artifact | da77 origin | private017 |
| --- | --- | --- |
| `contract/schemas/edit-command.json` | `sha256:9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec` | `sha256:6dd2b082ebdb630b4fc8ec3eeeea3b40c1eebe910c84557e45ab8fab05322b16` |
| `generators/release.json` | `sha256:7537bd04cf704e312f4ecab2a0cc8a02bddacf3ce467e01d9fd830a004caebde` | `sha256:3cea3fc42dad75c0d5561e874c9ae46fc477736b5aacea3d76d321c4b8404254` |
| `packages/python/astrid_runtime_client/contract_metadata.py` | `sha256:970637c096eded9cde2d5abb9e48ea5e113f64e9aefb85fea5685e982e6b4edf` | `sha256:e6d8286ca342bbb7a7d6554bb37357548b95bf2df123e7d46f60d6fce8fe53b1` |
| `packages/python/astrid_runtime_client/generated.py` | `sha256:e4d4e7e3724a460310897b4f8026589d47ee9a7cdf8215d4fef8cba55769cfa4` | `sha256:e58f0fbe652b2baf8a3cd113def468dde3b32d1522f946a733c2b2a3b8461350` |
| `packages/python/astrid_runtime_client/timeline_commit_types.py` | `sha256:c1af03349a9d0c97ff58a3297d78e4c82e0037d1399a209cf4d9d4bd8f77d037` | `sha256:af295393450db831c43e6559eb0aa8f645e6cd0e79f4beb078df949bdb58e0d3` |
| `packages/python/pyproject.toml` | `sha256:d55b45a54db77637103595a90d47f875e4b3f997c495d2cb57bb50ab5fc0078e` | `sha256:17866547fe2f37b301c165a9fafabac6b63a848fe4ed455d537d8ca37b166ec3` |
| `packages/typescript/package-lock.json` | `sha256:df8edd4d20110d7572def5d1347e7602365b001f87a3ba7ac0b8bd8327a52cb3` | `sha256:8aa6882819445670f60af0cba148acd87d643cd46c7372d643023cb3580ee1ee` |
| `packages/typescript/package.json` | `sha256:b13da4efa203d661b73d642330e323924f7d8bfca205307866258e0372abf764` | `sha256:ff03214e78c444ec9af5457f0b8161a08b2f67fd9cf0b6ad81f9167e7769392f` |
| `packages/typescript/src/contract-metadata.ts` | `sha256:9cde6324a09e6f8369363f52fc66bc2ceb8847baca4d1e8a33acc5c655fcee96` | `sha256:15f8a909c07f94a166e5d4eff46988586c0b08148e06a9d86251b23a3e0e9b23` |
| `packages/typescript/src/timeline-commit-types.ts` | `sha256:b2681fb5679628cb89370094292b821b766a72098b32d0f23ba41a53f5de854a` | `sha256:3f9fe0416b66b047eafe0d2b40c7ffa4ec3083589eb8cf9ed585efa63494bf11` |
| `runtime_protocol/schemas/timeline-commit-bundle.json` | `sha256:1bbc786daab05597f7a4d910ef0f8dcda531912b2d1e37318a35544ef039d7e9` | `sha256:e6fb80e7961b3e9eb34908b532a042a9f024e52b5178cd906d9c1d45a18a5f8f` |

The remaining 65 artifact entries retain their da77 hashes. The complete 76-entry
da77 origin list follows.

## All 76 da77 origin hashes

- `conformance/fixtures/canonical-timeline-parity.json` — `sha256:8404ad42d817e60f6255113624e0f17a8100e3c6d0c4baf24029e818d8e5ff00`
- `conformance/fixtures/event.json` — `sha256:29c739974e7bad256804feaceccd44e5a4633d144c1a6229cfe853737bca8ead`
- `conformance/fixtures/handshake.json` — `sha256:259f06fa225aec0cb0e0cfc593fa89db4578fc26db9664e2b7632ce2f4fec234`
- `conformance/fixtures/managed-object.json` — `sha256:db5646c5c47415bbb6fe7c84751bf1b7b56cae6074df0bd28040990db9f5f031`
- `conformance/fixtures/preferences-user-mutation.json` — `sha256:5b176a96f941ddb8ae737493d2b51547568710f6e54aaa164bd7fa640410eabe`
- `conformance/fixtures/preferences-user.json` — `sha256:1220094f6d80ce36fd8e0ed891b0c5418647b43ace19e74d127f3af5043125fa`
- `conformance/fixtures/project.json` — `sha256:b526be614ff35276608630c602213078edc8a291eb5241dd14b82bcffad71e29`
- `conformance/fixtures/settlement.json` — `sha256:f9cd0958061a2a2a25def05966b5c9ffd5837a1f7197eec2b1f1cd482ac09086`
- `conformance/fixtures/shot-composition-compatibility.json` — `sha256:9d5201dd62121c278bd51037863afb59508794b96b06e1bf3f89d7b300e19fc2`
- `conformance/fixtures/task.json` — `sha256:7dc2f5d3f82219b439f1c1147aa230f39e706a3c3b24a7d177efc1b975f543b9`
- `conformance/fixtures/visual-boundary-v1.json` — `sha256:1fc778b42f7a5ef91a1fd8620fd92417131e44f97dd5c6a238c78f13bcabfc55`
- `conformance/responses/events_page_1_200.json` — `sha256:6aaaabe512589beddddd5ef64f2307c39d365a99565c5a3291a15933a114be0d`
- `conformance/responses/events_page_2_200.json` — `sha256:d5bffdc93e9939779c92a18c047e70df21711f12e16c345f43f3cbdec5b27eb2`
- `conformance/responses/invalid_cursor_400.json` — `sha256:16a1db399e06b8d059472f567a091b4bd579d13d8885595376f61835646bfbff`
- `conformance/responses/managed_outputs_200.json` — `sha256:6bcef19aca4ad8d574c60d738b54ba57fce6a3a9d4e1481c6f8f088dd460858d`
- `conformance/responses/not_found_404.json` — `sha256:4a40fedbeccd345f24944e4af368c50430593d976a923c12af93ba21faa21af6`
- `conformance/responses/publish_conflict_409.json` — `sha256:19d664d035691202da03b22b858456c49983e253c7485a6347baa1cf350eea57`
- `conformance/responses/task_admission_201.json` — `sha256:108559a92c9e681e3ade37fa6b567e1eaac3edce221665a07a81c2c2c06bb48c`
- `conformance/responses/task_read_200.json` — `sha256:cc590c4f7d34820382b684d737f1cdb45eebeb20fbad2d5edda2dadac8ab2829`
- `conformance/responses/validation_error_422.json` — `sha256:2a02a9147bc0a8b74727d9c577803b0aca333bd0dd035602dafcf2503b00ff1a`
- `conformance/second-client-core-v1.yaml` — `sha256:3a0a5aff4e66435212ba567850a0a27c5555601a33ecbd3ed7e21737948662e3`
- `contract/component-manifest.json` — `sha256:1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5`
- `contract/manifest.json` — `sha256:75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14`
- `contract/openapi/workspace-v1.yaml` — `sha256:ab50e4643f39c62511251cbd6ab94d25c40ca180b9ea355c776ef2ef30dbf9ba`
- `contract/schemas/backup.json` — `sha256:71ec2f4bc9ad63ac05e8149cf0d1a4f96fa8d5aa4b85bf12a61938fbafb2151e`
- `contract/schemas/common.json` — `sha256:65e0196e36a0565f3a2f69e489e4c1fa6114df039eb25666c60591f266e06f19`
- `contract/schemas/doctor.json` — `sha256:d0caac9e7bf6a81d68abb52e757b321f7a45d4f2afff43bd4880089ea8dcc243`
- `contract/schemas/document.json` — `sha256:6d8fe08563eb96504c874c1d3535527371a8a67f54b06bcd324c32f99cb286e3`
- `contract/schemas/edit-command.json` — `sha256:9cb9597a618f51949fe9ec35686e544dca812b8b252a96a4cff1f686afdfb3ec`
- `contract/schemas/envelope.json` — `sha256:3afb9c6346eae95743e102cde2a405790c174a113ac952187c746ed2bef7f7ca`
- `contract/schemas/event.json` — `sha256:61c478fcffb5f68da0f8b6247094a3f0f4c6a6a622f0a91fa7726702d64d1c7a`
- `contract/schemas/export.json` — `sha256:f97729b94e4c6a761dfe0966996218c964ac7ab8eb61da45f4d842a2e2913d71`
- `contract/schemas/generation.json` — `sha256:be22c8359ebf8a6be6b37c7121683a20222676849d40f5f4245c5ae2bf759d06`
- `contract/schemas/handshake-response.json` — `sha256:2bd6af50af148b4371e0ae26cffe88cd58270d91a7190349b6b306fcb7824ff1`
- `contract/schemas/handshake.json` — `sha256:66dde8a212cf4a9b58d8607a2022752566028081d7c8dd3cb148d82f4c6daf13`
- `contract/schemas/health.json` — `sha256:dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e`
- `contract/schemas/managed-object.json` — `sha256:1b71eed89b69f4007b73cf5d5fc45d535bc3ef7ed108fbe0d6a0e859bc8a6630`
- `contract/schemas/managed-output.json` — `sha256:ee5dd30209c7000bd9fdb673e04dccbb424e211c4a953886737a7b6c9c4ab106`
- `contract/schemas/media-relation.json` — `sha256:b0a107e445b64cb93ed0db671a93c657030fefb2af08106b1af300cbf9843fe0`
- `contract/schemas/media-selection.json` — `sha256:8484eb04c00048af09c3ba88d079522106c86c59d10ed69d30e817f7c817795d`
- `contract/schemas/object-location.json` — `sha256:a84d8652987b3b23878a15dc492fe1eaac846101d591566204462cb3640c0148`
- `contract/schemas/preferences.json` — `sha256:3c3fbf9c5046c8f7e87acf8bed7b35fa013a260cce1e4728064fec2572425ada`
- `contract/schemas/project.json` — `sha256:f6dafdf23512eb9292a7da4bd74bcaff41af3ad6450a98bdba033bde286536d2`
- `contract/schemas/realm-lifecycle.json` — `sha256:ad337dc5bec2ae95958e9742a0a3a81119a9466c7597f6b6dbd0915434d45541`
- `contract/schemas/realm.json` — `sha256:bb1d4d1eed025bc26414f5cb3231e695d9843bcfa066c1f5cab6523bcf0be3ad`
- `contract/schemas/run.json` — `sha256:07613763162af9d11571093e7aac7f43694ca5dd2a26171d51dcd08508e46c3f`
- `contract/schemas/services.json` — `sha256:10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018`
- `contract/schemas/shot-composition.json` — `sha256:fd1a6a82567f817a06d906a793e188757ba22d7bb656ba579dc3c173a49c1791`
- `contract/schemas/shot-text-binding.json` — `sha256:312a12cc7e3e4a8f97fdade1097387f990380d15965dffafdbb35f830bb4cae9`
- `contract/schemas/task.json` — `sha256:2bc3a98edcd9d5c7221944a7602a342876261fb2c927f7f909528719ba757ba3`
- `contract/schemas/timeline-clip-replacement.json` — `sha256:844cf65e5647f89eef6e5787371def679bd5379211b322da5489e44e0372ab31`
- `contract/schemas/timeline-commit.json` — `sha256:7676f0112799fe4bd140b88e49590d5c0789c229c4702235a4f6e705187b05b8`
- `contract/schemas/timeline-config.schema.json` — `sha256:f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1`
- `contract/schemas/timeline-config.schema.provenance.json` — `sha256:fd3ab1f852aeecd494704330ac577d9f849d4d579a73b22a8e5ed3b50d59ce83`
- `contract/schemas/timeline-diff.json` — `sha256:ad112dd68ca71fa349dd654109f5f67284b761263f85107c083846aa039c1d88`
- `contract/schemas/timeline-inspection-result.json` — `sha256:67eae8bffc92ecc47817dc48ea3c68e2a22a8e903f7e371942bfb5d3721af1bf`
- `contract/schemas/timeline-inspection.json` — `sha256:9ed0f0e92676f5c5bc985c3018fadaecd5fec33271510978be9b9feecf581a6a`
- `contract/schemas/timeline-revision.json` — `sha256:cf02579485e098366b3c54665e233e604d57bba3ae51c20d2e372d1e71db568a`
- `contract/schemas/timeline-view.json` — `sha256:f28d4e7f22d00e3fa0c600143fac3a3d838e7b7f087d1dbccfa7e9b837f34a55`
- `contract/schemas/timeline.json` — `sha256:52aa33cf51a3b2cb1707e18c273f1a82d2b048049f37fafcd6e12827449a4728`
- `contract/schemas/worker.json` — `sha256:ce9046dd139b5c3368dfbb523ad9f8c1fc17a58749cd2fc8265a5e77a49bfc2b`
- `generators/release.json` — `sha256:7537bd04cf704e312f4ecab2a0cc8a02bddacf3ce467e01d9fd830a004caebde`
- `packages/python/astrid_runtime_client/__init__.py` — `sha256:7e602716931ca03930e1801596e098b83aa7344b7c54fe34b26e2308f82f15b2`
- `packages/python/astrid_runtime_client/contract_metadata.py` — `sha256:970637c096eded9cde2d5abb9e48ea5e113f64e9aefb85fea5685e982e6b4edf`
- `packages/python/astrid_runtime_client/generated.py` — `sha256:e4d4e7e3724a460310897b4f8026589d47ee9a7cdf8215d4fef8cba55769cfa4`
- `packages/python/astrid_runtime_client/timeline_commit_types.py` — `sha256:c1af03349a9d0c97ff58a3297d78e4c82e0037d1399a209cf4d9d4bd8f77d037`
- `packages/python/pyproject.toml` — `sha256:d55b45a54db77637103595a90d47f875e4b3f997c495d2cb57bb50ab5fc0078e`
- `packages/typescript/package-lock.json` — `sha256:df8edd4d20110d7572def5d1347e7602365b001f87a3ba7ac0b8bd8327a52cb3`
- `packages/typescript/package.json` — `sha256:b13da4efa203d661b73d642330e323924f7d8bfca205307866258e0372abf764`
- `packages/typescript/src/contract-metadata.ts` — `sha256:9cde6324a09e6f8369363f52fc66bc2ceb8847baca4d1e8a33acc5c655fcee96`
- `packages/typescript/src/generated.ts` — `sha256:4d0874a88614c8c0da0beea4aad528acc93c899586479ef8877cab6a78a8df1f`
- `packages/typescript/src/index.ts` — `sha256:2d23f8ee1cb38e6b1d3366663887b88a4981ec298d8c8d5a758a62a7ad8cc0e4`
- `packages/typescript/src/operation-handle.ts` — `sha256:3f8c69044a0efd5171290f925b0bc3706495c4c0da0252d0008d8056671fa460`
- `packages/typescript/src/timeline-commit-types.ts` — `sha256:b2681fb5679628cb89370094292b821b766a72098b32d0f23ba41a53f5de854a`
- `packages/typescript/tsconfig.json` — `sha256:48bc718286b70c7ff5af00d1adfea37ad7c7f8820d3050117dc9d6aea239181b`
- `runtime_protocol/schemas/timeline-commit-bundle.json` — `sha256:1bbc786daab05597f7a4d910ef0f8dcda531912b2d1e37318a35544ef039d7e9`

## Evidence and decisions

- The generator was run normally with the exact ed5 schema path, then checked
  read-only with the same path. No generated file was hand-edited.
- The existing generated Runtime carrier now exposes the optional field in
  Python as `NotRequired[list[str]]` and in TypeScript as
  `insertion_order?: Array<string>`; `CommandRecord.writes` remains
  `Array<AgentWrite>`.
- The original source semantic test
  `tests/editing_conformance/test_recipe_m2_project_data.py::test_remove_pruned_namespace_restores_exact_order_after_reload_and_redo`
  passed. It proves JSON serialization/reload, inverse, redo, exact list-key
  order, and exact bundle restoration.
- A direct current-bundle schema probe accepted the source-created record and an
  absent optional key, and refused null and non-string insertion-order values at
  the expected paths.
- No full, HTTP, browser, socket, native, renderer, install, release, public
  adoption, or normal consumer-pin lane was run.
- The unrelated legacy TypeScript fixture
  `tests/fixtures/timeline-commit-types.mts` still reports its pre-existing
  unused `@ts-expect-error` for empty `TrackSetArgs`; it was not changed or
  weakened. The affected bundle projection fixture and generator TS projection
  checks pass.

