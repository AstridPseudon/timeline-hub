# U4a / D80 Runtime producer provenance

Verdict: PASS.

## Qualified producer identity

- Normal producer: `/home/user/work/runtime`
- HEAD: `87bc7f74e09330885cfaff551ca629f51beea7b6`
- tree: `6014e9ca72873d122ad9150a362a1618720984a4`
- parents: `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f` and `4dab564628520f4c79a9f99fff035852fa84a9db`
- producer status: clean
- source delta from clean `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f`: only `runtime_protocol/timeline_commit_auth.py` modified and `tests/test_timeline_popup_fork_owner_projection.py` added
- auth source SHA256: `75f5141cadebafc9f887f5968f39f0ff030d1b2e6c724c24de0bd10b94cde2f0`
- popup test SHA256: `e0e008ef8066c1320c6ab87d1fa856f357f957c8fbc55a4841e014da070f9176`
- clean-parent auth SHA256: `a3fbb6a0289396fe84fbe455294747a627f9bae8c7579204a89db6402c66a908`
- `09c79ac` auth SHA256: `a3fbb6a0289396fe84fbe455294747a627f9bae8c7579204a89db6402c66a908`

## Adoption result

Normal refresh changed only `runtime.lock.json`, updating `source_commit` from `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f` to `87bc7f74e09330885cfaff551ca629f51beea7b6`. No generated client, schema, fixture, Agent product, test, or helper file changed.

Each lock mapping compares prior Agent HEAD, current bytes, and qualified producer bytes:

| Consumer | Prior/current/producer SHA256 |
| --- | --- |
| `astrid/core/timeline/schema/timeline-config.schema.json` | `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd` |
| `astrid_runtime_client/__init__.py` | `d095328fdfadc0883aa103147eb8be8d91f24de2f5fc81c6a9ac37be1809ecc2` |
| `astrid_runtime_client/contract_metadata.py` | `b42c58a36fff3e3136824492382eb05e983c247e5ca0656b35836e1a4e9ee72b` |
| `astrid_runtime_client/generated.py` | `952fe98a54c9529af723a029957994efec52821da24a2e9c9c34a8dce99e274b` |
| `astrid_runtime_client/timeline_commit_types.py` | `6c0d21d3eb87cff2977f9e33a5b4d0da13676c4ebad0df4c935f39106a45b417` |
| `tests/fixtures/runtime-responses/events_page_1_200.json` | `6aaaabe512589beddddd5ef64f2307c39d365a99565c5a3291a15933a114be0d` |
| `tests/fixtures/runtime-responses/events_page_2_200.json` | `d5bffdc93e9939779c92a18c047e70df21711f12e16c345f43f3cbdec5b27eb2` |
| `tests/fixtures/runtime-responses/invalid_cursor_400.json` | `16a1db399e06b8d059472f567a091b4bd579d13d8885595376f61835646bfbff` |
| `tests/fixtures/runtime-responses/managed_outputs_200.json` | `6bcef19aca4ad8d574c60d738b54ba57fce6a3a9d4e1481c6f8f088dd460858d` |
| `tests/fixtures/runtime-responses/not_found_404.json` | `4a40fedbeccd345f24944e4af368c50430593d976a923c12af93ba21af6` |
| `tests/fixtures/runtime-responses/publish_conflict_409.json` | `e06c5818e9c37a1e1118d3e2df2447808277d148553bb3c418e48b1a3c6e4c08` |
| `tests/fixtures/runtime-responses/task_admission_201.json` | `108559a92c9e681e3ade37fa6b567e1eaac3edce221665a07a81c2c2c06bb48c` |
| `tests/fixtures/runtime-responses/task_read_200.json` | `cc590c4f7d34820382b684d737f1cdb45eebeb20fbad2d5edda2dadac8ab2829` |
| `tests/fixtures/runtime-responses/validation_error_422.json` | `2a02a9147bc0a8b74727d9c577803b0aca333bd0dd035602dafcf2503b00ff1a` |
| `tests/fixtures/visual-boundary-v1.json` | `1fc778b42f7a5ef91a1fd8620fd92417131e44f97dd5c6a238c78f13bcabfc55` |

The 15-way comparison result was `PASS` (`prior == current == producer == lock` for every mapping). Runtime schema config remains `4d74a4ae…`; generated metadata remains `SCHEMA_DIGEST=sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`.

## Protected originals and ASTs

Protected Agent AST/content hashes before and after adoption:

| Path | Before/after AST or content SHA256 |
| --- | --- |
| `astrid/sdk/workspace_client.py` | `5b5e91d7b1c8122a8542a7334db250bfd8e616301ef336f657680c4cac398741` |
| `astrid/sdk/timeline/commit.py` | `9901c5c81f6413c13d68ebe3d6585a4477055ab8cbaeb85628e8dd384446f338` |
| `astrid/sdk/timeline/commands.py` | `39831015be3e6b98f8b19eeae48a5f186727974dfb9d538a1f7719bdbf66ebca` |
| `astrid/sdk/timeline/_doc_patch_schema.py` | `82345c26ff708dce5a605e73e620a4a81ae5b5f023af248beaf5eb217e90a08c` |
| `astrid/core/timeline/schema/edit-command.schema.json` | `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d` |
| `astrid/core/timeline/schema/timeline-config.schema.json` | `4d74a4ae34fcfa89ce66e4ccad90a3871a3ef9d3adb26c9219ae7dec72deb3bd` |
| `artifacts.json` | `f55b26826af66722864dec72c051d6e5ce0f78b8932e630cb747076f2c9024b9` |

The `09c79ac` empty-range AST hashes remain unchanged at the qualified producer:

- `_inverse_stage_inherited`: `3a42cf79123aa41827393bb59fd9c886ed82598705a7c597c2954191bc1907b1`
- `_inverse_stage_ranges`: `3ea2f7f416fe3162fc6ef3290a5ed3e6ea946f34ca05e79867b8844b8a0f134b`

Both reviewed predicates are present in the qualified source: `effect[0] == effect_end <= effect[1] <= len(source_step["patch"])` and `effect_start == previous_effect_end and effect_start <= effect_end <= len(step["patch"])`.

## Import origins

- Agent caller: `/home/user/work/wt/agt-U4a-D80-owner-adopt-1908/astrid/sdk/workspace_client.py`
- generated client: `/home/user/work/wt/agt-U4a-D80-owner-adopt-1908/astrid_runtime_client/generated.py`
- generated metadata: `/home/user/work/wt/agt-U4a-D80-owner-adopt-1908/astrid_runtime_client/contract_metadata.py`
- Runtime auth source: `/home/user/work/runtime/runtime_protocol/timeline_commit_auth.py`
- `WorkspaceClient.GeneratedWorkspaceClient.__module__`: `astrid_runtime_client.generated`

