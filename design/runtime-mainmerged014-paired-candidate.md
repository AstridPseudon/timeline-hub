# Runtime Main-merged014 paired candidate

**PRIVATE CANDIDATE — NEVER PUBLISHED.** Internal handoff only. No consumer pin,
integration merge, release, activation, or public artifact mutation is authorized
by this page. The owner sequence is: one full first; then paired Agent/App pins;
then coordinated merge/publication.

## Frozen status and exact tuple

The final source is the approved test-forward candidate, not the earlier generator
commit. The one authorized full is **PENDING** under worker
`rt-m2-mainmerged014-one-full-gate`; no pass is inferred here. The request targets
the exact final SHA below and is the only full run for this candidate.

| Field | Exact value |
| --- | --- |
| Runtime final commit | `4dd643808e93be431f8250c0b6d34320918776ec` |
| Runtime final tree | `d396f8f4f2caa956a8b6689c9af09e9088fb8c27` |
| Final parent / generated producer | `8d53e2e1043eddfcfd92fe5983a5404b94745d63` |
| Generated producer tree | `1cbfb180773526bb18de833dcb50879b812272c7` |
| Main-merged base | `8bd92de606647d6ffc8887436a3dde3f95ea2330` |
| Main-merged base tree | `d964d7138be203f7f18d8ff1f4f109805161cf5d` |
| Main parents | `7a956c027cbbcb498a50de59d85f3b424897f70b` + `b535646faaad2f8ae7968dfe0f4fa3057f960264` |
| Source-prep input | `0f88ecb301fdc514667786268e2c637cd1301c5a` |
| RT02 test input | `96d473c7e87dca16a6f7f4e0380332e8d52e3864` |
| Unpublished contract/package version | `0.2.14` |
| Raw Agent command schema | `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` (55 definitions / 29 operations) |
| Runtime schema digest | `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816` |
| Artifact manifest file | `contract/artifacts.json`, SHA-256 `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d` |
| Artifact manifest | 76 paths; producer `astrid-runtime`; version `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac` |

The final test-forward commit changes only the three approved test files relative
to `8d53e2e`; all generated/client/product bytes are byte-identical to `8d53e2e`.
The final branch must remain immutable while the full and paired qualifications
run.

## Required generated and service identities

| Artifact | SHA-256 |
| --- | --- |
| Raw command schema `contract/schemas/edit-command.json` | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| Raw commit bundle `runtime_protocol/schemas/timeline-commit-bundle.json` | `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |
| Health schema `contract/schemas/health.json` | `dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e` |
| Services declaration `contract/schemas/services.json` | `10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018` |

Health requires `status`, `protocol`, `schema_digest`, `runtime_epoch`,
`runtime_session_id`, and `runtime_instance_id`; `services` entries require
`name`, `state`, `last_exit`, and `restart_count`, with optional `reason`.
Service declarations require `version: 1` and `services`; each service requires
`name`, `argv`, and `restart`, with optional `env` and `ready` (`file` and optional
`timeout_seconds`).

The seven new Python root exports are `AssembledTargetArgs`, `ClipAddMediaArgs`,
`ClipAnchorArgs`, `OccurrenceCreateArgs`, `TimelineInitArgs`,
`TextBindingSetArgs`, and `WordAnchor`; each is in `__all__` and identity-matches
the generated DTO module. The TypeScript generated root re-exports the six
command DTOs (`WordAnchor` is the nested generated type) from
`packages/typescript/src/generated.ts`; the root generated files and metadata are
the exact bytes listed in the manifest.

## Complete 76-path manifest freeze

The following is the complete committed `contract/artifacts.json` path/digest
map. It is the source of truth for both consumer pins.

```text
conformance/fixtures/canonical-timeline-parity.json 8404ad42d817e60f6255113624e0f17a8100e3c6d0c4baf24029e818d8e5ff00
conformance/fixtures/event.json 29c739974e7bad256804feaceccd44e5a4633d144c1a6229cfe853737bca8ead
conformance/fixtures/handshake.json 259f06fa225aec0cb0e0cfc593fa89db4578fc26db9664e2b7632ce2f4fec234
conformance/fixtures/managed-object.json db5646c5c47415bbb6fe7c84751bf1b7b56cae6074df0bd28040990db9f5f031
conformance/fixtures/preferences-user-mutation.json 5b176a96f941ddb8ae737493d2b51547568710f6e54aaa164bd7fa640410eabe
conformance/fixtures/preferences-user.json 1220094f6d80ce36fd8e0ed891b0c5418647b43ace19e74d127f3af5043125fa
conformance/fixtures/project.json b526be614ff35276608630c602213078edc8a291eb5241dd14b82bcffad71e29
conformance/fixtures/settlement.json f9cd0958061a2a2a25def05966b5c9ffd5837a1f7197eec2b1f1cd482ac09086
conformance/fixtures/shot-composition-compatibility.json 9d5201dd62121c278bd51037863afb59508794b96b06e1bf3f89d7b300e19fc2
conformance/fixtures/task.json 7dc2f5d3f82219b439f1c1147aa230f39e706a3c3b24a7d177efc1b975f543b9
conformance/fixtures/visual-boundary-v1.json 1fc778b42f7a5ef91a1fd8620fd92417131e44f97dd5c6a238c78f13bcabfc55
conformance/responses/events_page_1_200.json 6aaaabe512589beddddd5ef64f2307c39d365a99565c5a3291a15933a114be0d
conformance/responses/events_page_2_200.json d5bffdc93e9939779c92a18c047e70df21711f12e16c345f43f3cbdec5b27eb2
conformance/responses/invalid_cursor_400.json 16a1db399e06b8d059472f567a091b4bd579d13d8885595376f61835646bfbff
conformance/responses/managed_outputs_200.json 6bcef19aca4ad8d574c60d738b54ba57fce6a3a9d4e1481c6f8f088dd460858d
conformance/responses/not_found_404.json 4a40fedbeccd345f24944e4af368c50430593d976a923c12af93ba21faa21af6
conformance/responses/publish_conflict_409.json 19d664d035691202da03b22b858456c49983e253c7485a6347baa1cf350eea57
conformance/responses/task_admission_201.json 108559a92c9e681e3ade37fa6b567e1eaac3edce221665a07a81c2c2c06bb48c
conformance/responses/task_read_200.json cc590c4f7d34820382b684d737f1cdb45eebeb20fbad2d5edda2dadac8ab2829
conformance/responses/validation_error_422.json 2a02a9147bc0a8b74727d9c577803b0aca333bd0dd035602dafcf2503b00ff1a
conformance/second-client-core-v1.yaml 3a0a5aff4e66435212ba567850a0a27c5555601a33ecbd3ed7e21737948662e3
contract/component-manifest.json 1ad76db27c1d9716bb234f811bf63e1f5898cb3d5f9b835a821765e6cad895e5
contract/manifest.json 75dc4d088d6647af9f0aa3f7f4a1a30e65195f85b81f81f7b354fd7e418f6d14
contract/openapi/workspace-v1.yaml ab50e4643f39c62511251cbd6ab94d25c40ca180b9ea355c776ef2ef30dbf9ba
contract/schemas/backup.json 71ec2f4bc9ad63ac05e8149cf0d1a4f96fa8d5aa4b85bf12a61938fbafb2151e
contract/schemas/common.json 65e0196e36a0565f3a2f69e489e4c1fa6114df039eb25666c60591f266e06f19
contract/schemas/doctor.json d0caac9e7bf6a81d68abb52e757b321f7a45d4f2afff43bd4880089ea8dcc243
contract/schemas/document.json 6d8fe08563eb96504c874c1d3535527371a8a67f54b06bcd324c32f99cb286e3
contract/schemas/edit-command.json 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
contract/schemas/envelope.json 3afb9c6346eae95743e102cde2a405790c174a113ac952187c746ed2bef7f7ca
contract/schemas/event.json 61c478fcffb5f68da0f8b6247094a3f0f4c6a6a622f0a91fa7726702d64d1c7a
contract/schemas/export.json f97729b94e4c6a761dfe0966996218c964ac7ab8eb61da45f4d842a2e2913d71
contract/schemas/generation.json be22c8359ebf8a6be6b37c7121683a20222676849d40f5f4245c5ae2bf759d06
contract/schemas/handshake-response.json 2bd6af50af148b4371e0ae26cffe88cd58270d91a7190349b6b306fcb7824ff1
contract/schemas/handshake.json 66dde8a212cf4a9b58d8607a2022752566028081d7c8dd3cb148d82f4c6daf13
contract/schemas/health.json dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e
contract/schemas/managed-object.json 1b71eed89b69f4007b73cf5d5fc45d535bc3ef7ed108fbe0d6a0e859bc8a6630
contract/schemas/managed-output.json ee5dd30209c7000bd9fdb673e04dccbb424e211c4a953886737a7b6c9c4ab106
contract/schemas/media-relation.json b0a107e445b64cb93ed0db671a93c657030fefb2af08106b1af300cbf9843fe0
contract/schemas/media-selection.json 8484eb04c00048af09c3ba88d079522106c86c59d10ed69d30e817f7c817795d
contract/schemas/object-location.json a84d8652987b3b23878a15dc492fe1eaac846101d591566204462cb3640c0148
contract/schemas/preferences.json 3c3fbf9c5046c8f7e87acf8bed7b35fa013a260cce1e4728064fec2572425ada
contract/schemas/project.json f6dafdf23512eb9292a7da4bd74bcaff41af3ad6450a98bdba033bde286536d2
contract/schemas/realm-lifecycle.json ad337dc5bec2ae95958e9742a0a3a81119a9466c7597f6b6dbd0915434d45541
contract/schemas/realm.json bb1d4d1eed025bc26414f5cb3231e695d9843bcfa066c1f5cab6523bcf0be3ad
contract/schemas/run.json 07613763162af9d11571093e7aac7f43694ca5dd2a26171d51dcd08508e46c3f
contract/schemas/services.json 10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018
contract/schemas/shot-composition.json fd1a6a82567f817a06d906a793e188757ba22d7bb656ba579dc3c173a49c1791
contract/schemas/shot-text-binding.json 312a12cc7e3e4a8f97fdade1097387f990380d15965dffafdbb35f830bb4cae9
contract/schemas/task.json 2bc3a98edcd9d5c7221944a7602a342876261fb2c927f7f909528719ba757ba3
contract/schemas/timeline-clip-replacement.json 844cf65e5647f89eef6e5787371def679bd5379211b322da5489e44e0372ab31
contract/schemas/timeline-commit.json 7676f0112799fe4bd140b88e49590d5c0789c229c4702235a4f6e705187b05b8
contract/schemas/timeline-config.schema.json f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
contract/schemas/timeline-config.schema.provenance.json fd3ab1f852aeecd494704330ac577d9f849d4d579a73b22a8e5ed3b50d59ce83
contract/schemas/timeline-diff.json ad112dd68ca71fa349dd654109f5f67284b761263f85107c083846aa039c1d88
contract/schemas/timeline-inspection-result.json 67eae8bffc92ecc47817dc48ea3c68e2a22a8e903f7e371942bfb5d3721af1bf
contract/schemas/timeline-inspection.json 9ed0f0e92676f5c5bc985c3018fadaecd5fec33271510978be9b9feecf581a6a
contract/schemas/timeline-revision.json cf02579485e098366b3c54665e233e604d57bba3ae51c20d2e372d1e71db568a
contract/schemas/timeline-view.json f28d4e7f22d00e3fa0c600143fac3a3d838e7b7f087d1dbccfa7e9b837f34a55
contract/schemas/timeline.json 52aa33cf51a3b2cb1707e18c273f1a82d2b048049f37fafcd6e12827449a4728
contract/schemas/worker.json ce9046dd139b5c3368dfbb523ad9f8c1fc17a58749cd2fc8265a5e77a49bfc2b
generators/release.json bc2e426715c604f06e1e286470eb4bbb58238b6518cecb4bb400f101f26986ce
packages/python/astrid_runtime_client/__init__.py 78a69901f7c68d67b152410732f1c42dd30954ca07e7b4b9a319d4ddbd9035e6
packages/python/astrid_runtime_client/contract_metadata.py cdedeb72880102ff6557320d908eac9068470b5088256c4441514e9d7db40514
packages/python/astrid_runtime_client/generated.py e2e66babca52a7ff95b8387dd6b36a5e46b4a4085bc9082ea664ab8d054bd468
packages/python/astrid_runtime_client/timeline_commit_types.py 4b23c46311210f5fa3a5684eceeab2772b30c40b61c623eacf0fcd1183d45457
packages/python/pyproject.toml 6c15723214b1d240f1e9fbea6692019da4893acc486dabcb74ab28e2efaf879f
packages/typescript/package-lock.json bb5b79bd79ddd6c780a16e658763f7d534718a739703abcf809b75b664957d66
packages/typescript/package.json 8510b0cb8e15630ef999539e697b4f480e6b640d8c9b56c121fa58b66fb451f3
packages/typescript/src/contract-metadata.ts 4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
packages/typescript/src/generated.ts c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
packages/typescript/src/index.ts 2d23f8ee1cb38e6b1d3366663887b88a4981ec298d8c8d5a758a62a7ad8cc0e4
packages/typescript/src/operation-handle.ts 3f8c69044a0efd5171290f925b0bc3706495c4c0da0252d0008d8056671fa460
packages/typescript/src/timeline-commit-types.ts f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
packages/typescript/tsconfig.json 48bc718286b70c7ff5af00d1adfea37ad7c7f8820d3050117dc9d6aea239181b
runtime_protocol/schemas/timeline-commit-bundle.json 6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3
```

## Consumer handoff after full PASS only

Root must first provide an immutable checkout of `4dd643808e93be431f8250c0b6d34320918776ec` and bind it as `RUNTIME_PRODUCER`. Then use the repositories' normal updater, never hand-edit generated files:

```sh
# Agent / Astrid, from the Agent checkout
python3 scripts/vendor_lock.py update runtime.lock.json --producer "$RUNTIME_PRODUCER"
python3 scripts/vendor_lock.py check runtime.lock.json --producer "$RUNTIME_PRODUCER"

# App / Reigh, from the App checkout
node scripts/vendor-lock.mjs update runtime.lock.json --producer "$RUNTIME_PRODUCER"
node scripts/vendor-lock.mjs check runtime.lock.json --producer "$RUNTIME_PRODUCER"
node scripts/vendor-lock.mjs check runtime.lock.json
```

Agent and App pins are one cohort and must record their final source/tree,
generated-byte, lock, version, schema-digest, artifact-version, contract/client,
and `/v1` door qualification against this exact Runtime. The three local-door
operations remain `commitTimeline`, `listTimelineCommits`, and
`getProjectMediaSelection`; no `/astrid/v1` or paired relay route is introduced.

## Evidence and frozen comparison

Completed before the full: normal generation checks, artifact checks, 1,581 local
tests, central commit integration (11), door (1,293), safety/startup (102), and
Gate 4 (29 Python + 61 TypeScript); the test-forward worker additionally verified
76/76 manifest hashes, raw `6ba7…`, three direct tests, 72 non-socket tests, and
`git diff --check`. HTTP/catalog socket evidence and the one full remain pending;
they must not be described as passing until the named full result arrives.

The old private a0 comparison is frozen and is not an input: old Runtime commit
`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
`4b7dd0fe44be973c344bab3de568eaf0bdd28476`, artifact version
`sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`,
and artifact file SHA `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
The rejected parent `806636baf42e9ed1e4c7f9fe76c3e14d7330fcc1` and artifact
`sha256:8023c665f0e32835cf06b793c6f5ffa0a278a7ca5aadbfe971d52d163d66c7a3` are
not consumable. Public Runtime `0.2.13` (`2c4ac180c2220bdad966bc01e95ad230e99ce26a`)
and its historical fixtures remain untouched.
