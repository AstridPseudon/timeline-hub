# Upstream conflict census

Captured at `2026-10-25T18:47:50.824772Z`. This is a read-only `git merge-tree --trivial-merge BASE OURS THEIRS` preview; no merge, checkout, rebase, fetch, ref movement, or conflict resolution was performed.

## Summary

| Repo | Ours | Named upstream | Merge base | Files changed by ours | Files changed by upstream | Conflicting files |
|---|---|---|---|---:|---:|---:|
| runtime | `e319fdbcd512` | `dbcdb97c50af` | `d4f496ec4fbc` | 323 | 29 | 10 |
| agent | `547e10456250` | `886a3183bd4a` | `92443771676e` | 919 | 98 | 40 |
| app | `d5a1d1ab6550` | `213318f1ec6e` | `3881e9440688` | 565 | 154 | 16 |
| composition | `635f4de06fda` | `67b8aa3d0d68` | `67b8aa3d0d68` | 118 | 0 | 0 |

## Conflict paths and source hunks

Hunk headers are from the exact three-way preview. `ours_hunks` and `upstream_hunks` are direct `git diff --unified=0 BASE SIDE -- path` ranges against the same merge base.

### runtime

| Path | Base blob | Ours blob | Upstream blob | Merge hunk locations |
|---|---|---|---|---|
| `.github/workflows/ci.yml` | `741e027678a38d0c17cc74b83f8b1e8479085508` | `94ffdaf70b7b44d12c9f41a67d6632b0e07d7531` | `80517dd88d253b921bf463e585ba4753e371bdb2` | @@ -89,6 +89,14 @@ |
| `docs/runtime-portability-testing.md` | `57289e7cc1a9f3a532a1d9d6d9553f85c5ec43ad` | `6c490e2bcc9e95e0ac7528474f49fe3b4a098941` | `0e5fa5426b98fd3c640d4c0cd90a232fef653250` | @@ -52,6 +52,27 @@ |
| `runtime_protocol/daemon.py` | `31ca7eeef3deb7401edd7bc4d69b122273faaa5e` | `725d4386c2e2690ddd10a233a028ac2f9d48c96c` | `d406ef24cff8676f5c4a78ba60facf2af5db9c7f` | @@ -5,6 +5,7 @@; @@ -243,7 +244,14 @@ |
| `runtime_protocol/door.py` | `b352613ffad3b9f6cd738738f0f5a4c02edbb7c8` | `674d8b55865dfdffa66c20cb51d7331fab18c4cd` | `1c5ef0337a2f49fbc290f908d5898078f18e4773` | @@ -139,7 +139,7 @@; @@ -154,6 +154,7 @@; @@ -199,6 +200,8 @@; @@ -236,6 +239,13 @@ |
| `runtime_protocol/platform.py` | `9f0d8b21582162d48cf1e646a2cd49aedf680184` | `70049865a0c11d1f874339259884dd5102350cb7` | `9f5cd8aa6cafcb024515a47e28939b55110d3141` | @@ -8,6 +8,9 @@; @@ -978,7 +981,15 @@; @@ -1060,8 +1071,192 @@; @@ -1110,7 +1305,13 @@ |
| `runtime_protocol/server.py` | `13537c0cda2fb8975d4560488218e227f6beeea5` | `65aa761a3187486d4847ef063192a06434b24d91` | `5c2b62737dedf8b4d77ee2ffc0f29c4e55da082a` | @@ -5,6 +5,7 @@; @@ -421,7 +422,12 @@ |
| `runtime_protocol/service.py` | `be200b27f228e3526d5cd7cd3129d477012719aa` | `48f9d1b94e0cda5feece2bf51cb7d6e1fca03144` | `63c944106eaf729afb424c078fcc1019550fa769` | @@ -7955,9 +7955,11 @@ |
| `tests/conftest.py` | `68b75310a620fe8ea672f9b8e2e268b264f5c455` | `9b50df102d31971f90d9b34e1f7bf9339eb0203b` | `0b1014372d2a58a11b86ec2fb4a934c3dfce6fad` | @@ -14,6 +14,38 @@; @@ -76,7 +108,9 @@; @@ -85,7 +119,7 @@ |
| `tests/lanes.py` | `ba2097d5a169c4a5af6eea8632471a64e9aae438` | `410f3144b440b4df933bd351ffca77f044e91aac` | `381a1b2cea580fe6d6a80d244fe742135e917aea` | @@ -32,6 +32,7 @@; @@ -283,6 +284,10 @@ |
| `tests/test_door_routes.py` | `9851e7240db6e484751fed727aa52da60678df2c` | `046dc68015752e0c445b0e9541302aa27175a972` | `78bf364cc445371f663c01057198964882825a05` | @@ -37,6 +37,7 @@; @@ -110,6 +111,8 @@ |

### agent

| Path | Base blob | Ours blob | Upstream blob | Merge hunk locations |
|---|---|---|---|---|
| `astrid/chat/acpProcessHost.test.ts` | `c1e9602b23b1f46ef4b8c089916cff28e3e2a90d` | `8619d6ebdefd8c6f259b53002a6c6a452dc9e3eb` | `4fef09d77e2655de84f90e5265d6a8bb3cdeb8cf` | @@ -124,6 +124,27 @@ |
| `astrid/chat/acpProcessHost.ts` | `c410008357d85b695896f0ccb4ae4baeac4b6851` | `971388aa835af637972501e7666a41450b66d1fd` | `4aa1d7de8c7e123c7b327c4e6201b0a3e842eb2c` | @@ -58,11 +58,15 @@; @@ -70,6 +74,7 @@; @@ -78,6 +83,7 @@; @@ -449,8 +455,12 @@ |
| `astrid/chat/astrid-acp-bridge.ts` | `6b7329a3f6d807305fea46434c68812cbb377cf8` | `90818a91e509a270899dcfff11be7343fee5d06a` | `455d13f34b4b1c3aa121afbc79066d73163ae3e9` | @@ -7,12 +7,14 @@; @@ -105,6 +107,7 @@; @@ -346,7 +349,7 @@; @@ -380,11 +383,13 @@; @@ -429,8 +434,11 @@; @@ -438,7 +446,8 @@; @@ -450,6 +459,19 @@; @@ -705,6 +727,8 @@ |
| `astrid/chat/astrid-acp-models.test.ts` | `ab398a8f5e6ba1525039b3f93df110f91b6369c0` | `63d5b69eb9b979debac8c371ee2b81e59e59e49b` | `6bc1c1b8c90ba5bc415e4857159b1df116aaaeca` | @@ -4,7 +4,7 @@; @@ -126,6 +126,11 @@; @@ -214,11 +219,14 @@ |
| `astrid/chat/astrid-agent-models.test.ts` | `1599b6c98a1f9df64ba15f5cdafed383a23f0213` | `ec407f3cc8514253042d40632f2be4838de835e7` | `21fa3c0c168a49d7c5464032c0539063b97ccedf` | @@ -18,6 +18,7 @@; @@ -26,8 +27,13 @@; @@ -62,6 +68,17 @@; @@ -71,9 +88,15 @@; @@ -144,7 +167,7 @@ |
| `astrid/chat/astrid-agent-models.ts` | `82ae8f42a1cdeaa26b88285c9bbcb24727b15838` | `3888b90d8fae241f1752f8a833948a25c0fed2c4` | `6223a477ec1e36750c29034abeefc564ad322fb8` | @@ -12,6 +12,10 @@; @@ -29,7 +33,8 @@; @@ -51,6 +56,10 @@ |
| `astrid/chat/astrid-local-agent-host.ts` | `f4258dd781697032459928e1c8b8d732d904d16d` | `e223c10ac00986c5a9a6a3ef58ee23f4ab85cb0f` | `aa938dd6765c2c752c468d4353858a0f3066a2a0` | @@ -2,7 +2,7 @@; @@ -101,8 +101,8 @@ |
| `astrid/chat/astrid-local-agents.test.ts` | `31c8f3fe305e134b1362c880b58568e632c4f775` | `0fcbe2999d13bf0590644067cbf9fe3aa71b2df1` | `6e614214b69905a65999f6c0048fc6124d8582e8` | @@ -3,7 +3,7 @@; @@ -43,7 +43,7 @@; @@ -53,6 +53,7 @@; @@ -85,7 +86,7 @@; @@ -106,12 +107,14 @@; @@ -131,7 +134,7 @@; @@ -257,11 +260,13 @@; @@ -297,11 +302,11 @@; @@ -310,6 +315,7 @@; @@ -364,3 +370,62 @@ |
| `astrid/chat/astrid-local-agents.ts` | `9fe3e410c3d968404a5782f38d38489b889cad3d` | `e7b15de9f5add03f5432efa5737cd918a0e56758` | `2344c0dafdf56b6baa75b3079aacf92885618d1c` | @@ -3,7 +3,8 @@; @@ -229,13 +230,13 @@; @@ -260,7 +261,7 @@; @@ -285,9 +286,9 @@ |
| `astrid/chat/astrid-project-chat.test.ts` | `42c112ac990bc9a65029f84da0f1774012898807` | `e1fe377ff8af99d9de11ec7694c7ea76b1c1d896` | `f399a7c64eb802f9a1bb118072f2e5039dd3e12c` | @@ -73,6 +73,27 @@ |
| `astrid/chat/astrid-project-chat.ts` | `f33578bc20b21df3d356e881b1b149bdb0631ad7` | `13f1b6c0113202ad79242d8d79938f7539069639` | `c8efeaf87a403c3056b9870a3ac701588c4499ad` | @@ -279,46 +279,53 @@ |
| `astrid/chat/astrid-shared-acp-sessions.test.ts` | `fa469335d2bd4636032e1d7b0a643cc358733fa5` | `c3bc7b16d52302212e46470c33adf5219a766001` | `790c31642a30321273d428d92059aad445e13196` | @@ -175,6 +175,29 @@ |
| `astrid/chat/astrid-shared-acp-sessions.ts` | `aacf7ffe99c4f9ce4f21edbfabc5f67b48be1be2` | `f31f2fc92f7990ad480796316e1f502704c779a1` | `8e6c944bff0feeff1fb41f0b57904957a233c765` | @@ -326,7 +326,13 @@ |
| `astrid/chat/discoveryProbe.ts` | `a328096587b3a850011906dcdcb6eb32f37b9eac` | `09ba9f0b007097bae3b5e36fdf4182f508fb2d49` | `ade24dfe88bc54254fdb8dc581b63229e4dec875` | @@ -2,11 +2,11 @@; @@ -44,6 +44,10 @@ |
| `astrid/chat/localAgents.ts` | `adc3829fb0332ea5f60f4b2d404170df6d088654` | `5f3dbcb908121958983a3bc3b78d67555246d538` | `7bd7d4d419d6ce55f8edafe91c214369af781896` | @@ -1,4 +1,5 @@; @@ -6,7 +7,8 @@; @@ -15,19 +17,24 @@; @@ -37,7 +44,7 @@; @@ -58,6 +65,28 @@; @@ -80,17 +109,22 @@ |
| `astrid/chat/modelCatalog.ts` | `c01412c65eee7ecba641f2ae6f61f22d4b73cc65` | `5de3f13200a72ecbaa5d071af0fc774ac7b09764` | `7c650c0c4415ceb56387f83f6c149ba8c901eebd` | @@ -12,6 +12,8 @@ |
| `astrid/chat/service.mjs` | `c04a5c992684d30378f07c09c977f4af869fe13e` | `945a9bcf8d0dd7ba0237afc0229ac31b3f816f23` | `011689ea7756036fe71dd725e64de7f0f68a03d9` | @@ -1,4 +1,5 @@; @@ -7,10 +8,21 @@; @@ -81,3 +93,50 @@ |
| `astrid/chat/service.test.ts` | `a498d3e9124331cc00b4e962db82c33462bde225` | `f88e5e44a24981d8ad6a7a4191234b1d8ea15d96` | `4cc86ad0985733d8776294a6e0c6bc2b45842d1c` | @@ -51,15 +51,16 @@; @@ -68,6 +69,7 @@ |
| `astrid/chat/service.ts` | `fc30a4eef1dca949e5d09283366bb6a71ac4f651` | `3b6dfa004bcc452d1c55712aa760d81dae85367c` | `ec6b9ca21483b242fb0c50f55a8309e907644904` | @@ -1,4 +1,5 @@; @@ -13,6 +14,7 @@ |
| `astrid/core/gateway/dispatch.py` | `faee0ff3e1a1c400e8bdaca212b88fe966ef31cd` | `239587646b1cb0b259d454bc2cc1faa7922b2c7a` | `402362763963c5858bd1003bce5b26c0cf42fbbd` | @@ -72,6 +72,11 @@; @@ -551,6 +556,7 @@ |
| `astrid/core/generation/gpu_environment.py` | `da1b528d46e3504e54b3024c16a84a04336986f9` | `f42e84cce1a9dccf50dadd2f53b3c193890b5f4f` | `9bccdf3fdeb510c687e971930c8f96ec0729f4c3` | @@ -18,6 +18,8 @@; @@ -104,7 +106,10 @@ |
| `astrid/installer/backend.py` | `e28357d09172bce9c09540ae3bf777f6cf280f5a` | `73930778510cb08d5a50f86767ffea0098fc2007` | `a609940892e8d2507fe77e661a4018f6e9fd5c1e` | @@ -30,6 +30,7 @@; @@ -510,6 +511,26 @@; @@ -591,6 +612,7 @@; @@ -599,6 +621,9 @@; @@ -640,8 +665,26 @@ |
| `astrid/installer/core.py` | `2db5d9f8b16f058cd728596e15542653d01c2c10` | `15feb564a12299642b168c3aa6bf9a555bee0716` | `8b7c68acd64654d46309046c0c3c69d7266d7cf7` | @@ -204,16 +204,16 @@; @@ -271,6 +271,10 @@; @@ -300,8 +304,8 @@ |
| `astrid/installer/launcher.py` | `c803aadda87f7e9f9b0dd59d6eb020d1993c3d0a` | `2d9b58ea07588c5058b213ee99da9a03926fea5e` | `6537e27183aee0d09c8c03f10c057b0e307dd415` | @@ -2,11 +2,121 @@ |
| `astrid/installer/omp/recipe.json` | `3a3c3290ba1fd0a2c68d78b19afab9ab1a8b4359` | `e1ac1cfe00bcad6a40daf1a015b77c4a43548031` | `0cbf40c60a51b5d62e0db80dfb7030ee6a1e7299` | @@ -1,46 +1,46 @@ |
| `astrid/installer/service.py` | `2974b81ddc0f7213d1a30a1e3354b5e577dc32b6` | `a916575d476a7dc60501151ad824aa778683cb5b` | `a3aa8e5ba45e98e3f124b909541ce8683a68fd22` | @@ -110,8 +110,10 @@ |
| `astrid/installer/tools.py` | `868f7179bc673e67484180c76ae065316c2ce051` | `8a456b340050be5eff7678cbd5db9645f79e4fb9` | `3efcc8dfd64b24eb7e79023ed95886af86466252` | @@ -20,7 +20,7 @@; @@ -317,7 +317,7 @@; @@ -388,7 +388,7 @@ |
| `astrid/packs/rendering/docs/SKILL.md` | `f5c18de30093a3013dcf8c9951445f25d55e7ef2` | `7dee1d8c84afc9a1f8b15150f55db0642d2be142` | `715b37ce9b3d10dda3fd0a1c048967e86ffd3249` | @@ -535,8 +535,8 @@ |
| `astrid/packs/vibecomfy/environment.windows-nvidia.json` | `e553ad26f259f64b9723b7c35551b5dc539ee7b6` | `3242b3bedb504c636b1486943aef7626fe5986c4` | `1eb15b7c4b5ba5c92a1882953d0f728d8d928880` | @@ -12,8 +12,7 @@ |
| `docs/install/OMP-LANDING.md` | `726609bfa437190c051e9023a645160b5fb0310e` | `7e425adf1c8eb666a462d4961927ddd6ce64be68` | `e4ade615a2b8cd010884248a6acb61ec8eac64d7` | @@ -1,67 +1,161 @@ |
| `docs/reference/services.md` | `99f72358b32f7caad7732714f0a8c6bfabe61381` | `1cd0d382bdc335c17d63a18f1a91a8ab3981e66b` | `24ebff2bab996fd09401b5cd3bcc0bdfffff7273` | @@ -25,8 +25,10 @@ |
| `docs/testing/TESTING.md` | `c54152de6586cbf60daebb83264a9dfb4d66def8` | `fbcfcddc4c0276b8f3418180ebe4f31e8f693c26` | `df416ca4ed5f82bf30251191239e26834ce1dd5e` | @@ -396,7 +396,7 @@; @@ -585,15 +585,18 @@ |
| `scripts/refresh_omp_recipe.py` | `b822d323bfa0f017ad13618e47758e42d1119aeb` | `277031f1d06d5c34a7f8ce65986697e92602e99d` | `b1d630b5f487f37aa50ff8f8dcd22b8688f45e5d` | @@ -1,38 +1,24 @@; @@ -45,6 +31,8 @@; @@ -56,40 +44,19 @@; @@ -109,10 +76,8 @@ |
| `tests/core/generation/test_gpu_environment.py` | `bac871fb2f2f25d7643921dbbed47d5599cdc721` | `f1b0783bb2badb5b094a3ed0bdbc058bd33c5ae9` | `76f2ec69264eb03b4ad843ddead8d8bf091eed7c` | @@ -52,11 +52,9 @@ |
| `tests/test_installer_acl.py` | `ca328ec1ee9f25d35f22ce52a2593a0a6ce04889` | `67bb7505c0f270ad55952360f11bb12962f83806` | `88dd45748db6677ed9dd9f602c060cb4de68a219` | @@ -128,8 +128,9 @@ |
| `tests/test_installer_cleanup.py` | `e5ea5450114e2b96700368a992e2ea1f47f581c3` | `c4381c3140282cce74a94cb9e5d09de04c3cc62b` | `f030558f1aa47eed8e896116ce7bc296c05e232c` | @@ -25,6 +25,7 @@ |
| `tests/test_installer_lifecycle.py` | `4c7c2e604b24df9d4d068c070220c2db39c03ad4` | `e77c7d2d29df9970472acc0d99e5f2c9bf2edfe6` | `6db70490bde7eb33e3b5b8c91d3c882631f3e283` | @@ -39,6 +39,7 @@; @@ -65,6 +66,16 @@; @@ -78,6 +89,11 @@; @@ -98,10 +114,6 @@; @@ -116,13 +128,81 @@; @@ -164,7 +244,7 @@ |
| `tests/test_installer_omp_source.py` | `f8ff6760732bad2da455680ac35fe4acc9a36a25` | `18b560d48889ca6462778a49282413196b9e6488` | `3ac8b3a080b2359b5e0654c8262c8a353c8600e4` | @@ -38,11 +38,11 @@; @@ -90,13 +90,13 @@; @@ -104,9 +104,9 @@; @@ -185,7 +185,7 @@; @@ -199,7 +199,7 @@; @@ -252,12 +252,12 @@; @@ -268,7 +268,7 @@; @@ -384,3 +384,60 @@ |
| `tests/test_installer_platforms.py` | `791311144204eec7d33d73fda7b89dc38502c669` | `55d0bbfd4200756d1a5322ed63e52ada32a44560` | `94a7e05012357ba4d906cc611716e8f18b38d250` | @@ -134,7 +134,10 @@ |
| `tests/test_installer_wheel.py` | `a21f3238ccb2071c9955b3980272ed51600f94ea` | `cfe1729e4188eecfc14387e07e4abf7a7bb96880` | `549e079eb4fcbac9cea9ebb7324dc86e20e6f012` | @@ -65,7 +65,7 @@ |

### app

| Path | Base blob | Ours blob | Upstream blob | Merge hunk locations |
|---|---|---|---|---|
| `package.json` | `a91b81dbbba7c2e00a1e0a22b57e9da91abeca87` | `84e4f6e61ae28f094f159c4869a5b20899b98e8c` | `5bdc5b0aaab190884feea72120b3d9d12ab926f4` | @@ -9,6 +9,9 @@ |
| `public/install-manifest.json` | `52f4898421560448a383afd516c1c6b9a3828565` | `47df36d127f0b04517e24756cd87147512bbda94` | `4ba29b084df42dc1dfa41d2b23549b05752568e2` | @@ -1,11 +1,22 @@; @@ -42,7 +53,7 @@ |
| `src/app/onboarding/WelcomeConnection.test.tsx` | `30fdfd9527f2da15bbaced1c792f44f1ec96ee41` | `26df345b4496372cc93d2e805976e89ccca4bb56` | `b685a48015b52de2e382d710e21de4725b80a587` | @@ -18,6 +18,11 @@; @@ -154,7 +159,7 @@ |
| `src/integrations/astrid/localAgents.ts` | `7cb0a23ec932716eef4e99f8dad6eaf1e769ec10` | `d0e540ea595be85c644c2273942a05a76624fcb2` | `4dd520e91bafce42277ba859b92bc37933ea440f` | @@ -32,20 +32,66 @@; @@ -57,11 +103,18 @@ |
| `src/integrations/paired/pairedRoutePolicy.test.ts` | `ba560ef0f59d65ac034933ef111419aed2fbd755` | `3e920fffa81bd88877f66bd60d5b81fda96810ce` | `f66fdbaf5a700b0eb0eac1082aa8578b4ba923e6` | @@ -21,6 +21,7 @@; @@ -74,6 +75,7 @@ |
| `src/integrations/runtime/client.ts` | `35f523c35ed8fd56f0a42da5a484e029aa881564` | `9f1050799bd86a46d35cf5c07daa4ed05187e6b5` | `126ef1d1cbc6fb71b301b6c0f6e0f213e3f24174` | @@ -620,6 +620,10 @@ |
| `src/shared/components/SettingsModal/sections/ConnectionSection.tsx` | `7f36f6c12c64e523324dfb7eecbdb76b66ef8e98` | `d3b24fdccbed282fd63f5aaaa8a3dfe3393328d6` | `9e7f4f342491110ccdfafe8bd82ab6a590aef07a` | @@ -1,7 +1,7 @@; @@ -54,8 +54,14 @@ |
| `src/tools/video-editor/components/AgentChat/AgentChat.projectContract.test.tsx` | `6ccf2f8679385f5ee7e81fa151b92406e81911b0` | `3b25e68e194d2826529fd9048515ae197cbdf7cc` | `aff454f75905cbe6eb01314ec02504844a445810` | @@ -4,6 +4,7 @@; @@ -33,6 +34,9 @@; @@ -43,6 +47,7 @@; @@ -65,8 +70,10 @@; @@ -103,6 +110,7 @@; @@ -119,6 +127,7 @@; @@ -186,6 +195,121 @@ |
| `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` | `162e62562d6bb5256d0c60fefea92edd39b6becc` | `06c5ef55809f67a4fb19925f71dd11a1fe551fd1` | `e48139a8e4f6d9c0a3fef9bd37b359c76c02ea3d` | @@ -6,7 +6,11 @@; @@ -175,6 +179,8 @@; @@ -182,6 +188,8 @@; @@ -265,6 +273,13 @@; @@ -314,7 +329,219 @@; @@ -452,7 +679,7 @@; @@ -513,6 +740,12 @@; @@ -1365,7 +1598,11 @@; @@ -1374,8 +1611,16 @@ |
| `src/tools/video-editor/components/AgentChat/AgentChat.tsx` | `a82ace6b6a75d4a0f34f54ad71685925adecae02` | `db6cf3f86d6996d2c2f3ee5dbcc58851fac2ed02` | `7c0fc8efc38edd61df9a8f2dea61330dff48bebb` | @@ -3,7 +3,7 @@; @@ -45,7 +45,12 @@; @@ -315,8 +320,15 @@; @@ -521,9 +533,11 @@; @@ -534,7 +548,17 @@; @@ -546,11 +570,69 @@; @@ -657,6 +739,7 @@; @@ -668,11 +751,10 @@; @@ -683,7 +765,7 @@; @@ -882,6 +964,8 @@; @@ -906,49 +990,57 @@; @@ -1017,7 +1109,7 @@; @@ -1038,10 +1130,17 @@; @@ -1057,7 +1156,36 @@; @@ -1080,7 +1208,7 @@; @@ -1142,20 +1270,48 @@; @@ -1185,7 +1341,8 @@; @@ -1201,7 +1358,8 @@; @@ -1373,7 +1531,7 @@; @@ -1396,6 +1554,7 @@; @@ -1461,6 +1620,35 @@ |
| `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx` | `1f8ec360ccaa22b9523f51039a8e7b2be1121792` | `fa386e33b828ea613da3a8114df7991a89d92ae2` | `9305a1690c661242812032fc950eefa7105aaf43` | @@ -1,3 +1,4 @@; @@ -9,6 +10,14 @@; @@ -55,6 +64,8 @@; @@ -84,9 +95,14 @@; @@ -299,6 +315,7 @@; @@ -365,6 +382,26 @@ |
| `src/tools/video-editor/components/AgentChat/AgentChatModelLine.tsx` | `bafb8fdc879b10da663a90a70b8a6be925771e74` | `a851a9bc80d20f2ef3ed28792dfbe9fc312388ca` | `831f3bb0144b9d1eeb8aee1b974c155560f5396c` | @@ -6,7 +6,7 @@ |
| `src/tools/video-editor/components/AgentChat/TourChatPanel.tsx` | `cba152e0a30c55dd0f62aa756497095838382317` | `3d8001013ad1a70253fe28f251f0376f5373e4a7` | `d4c5e76ff7c6b54365f9c6537337e97cf0acaf18` | @@ -152,8 +152,18 @@ |
| `src/tools/video-editor/hooks/useAgentSession.ts` | `33297d969f64f1bdefe107a7dcb949a70dde2b2f` | `08bb37ddcbc1b8faac87f8b59f96c1eb0f72f53e` | `2f250db12d21659166c6243939f5f911fbb3a160` | @@ -1,4 +1,4 @@; @@ -13,7 +13,7 @@; @@ -71,6 +71,7 @@; @@ -91,7 +92,9 @@; @@ -352,7 +355,7 @@; @@ -363,7 +366,7 @@; @@ -388,6 +391,10 @@; @@ -416,7 +423,7 @@; @@ -430,7 +437,7 @@; @@ -443,7 +450,7 @@; @@ -464,14 +471,14 @@; @@ -497,18 +504,18 @@; @@ -536,7 +543,7 @@; @@ -550,7 +557,7 @@; @@ -589,6 +596,7 @@; @@ -616,7 +624,7 @@; @@ -651,9 +659,11 @@; @@ -784,7 +794,7 @@; @@ -1324,7 +1334,7 @@ |
| `src/tools/video-editor/pages/VideoEditorPage.test.tsx` | `f7546db6121de17afebe7eb972489105bc4ebfb5` | `9cb4d5da89cf82258f17bca96175f06342c3ff38` | `7565bdcfd6db01c3e3feee2f85d4f7bd68d158f9` | @@ -1212,9 +1212,7 @@; @@ -1542,6 +1540,21 @@ |
| `tests/e2e/fake-runtime/server.contract.test.mjs` | `d519e7437e73b3a465a989e97555946d48ad12bc` | `62a0e80dcd4b70523cbf4490e20cb7fe17518558` | `ab92ec3028eb4a94d163469f3e44b48efaca6cce` | @@ -103,7 +103,7 @@; @@ -335,6 +335,23 @@; @@ -584,8 +601,11 @@ |

### composition

Clean trivial merge in this snapshot; no conflicting paths.

## Dry-run / installed-script risks

### runtime
- runtime_protocol/* and test harness conflicts carry process-control/door/platform semantics; resolve with source-owner review, not automatic marker removal
### agent
- astrid/installer/{backend,core,launcher,service,tools}.py, recipe, refresh_omp_recipe.py, and installer tests overlap; preserve the current D123 platform predicate and re-check installed-script inputs after resolution
- workflow pin additions and VibeComfy pin script are upstream additions/overlaps; no pin/generated write was made here
### app
- public/install-manifest.json is an actual conflict in source/pin metadata; public/install.sh and tour/agent-setup files are upstream-only additions in this preview
- runtime client, paired route policy, AgentChat, and connection UI conflicts require App/Runtime contract review; no public-shape resolution was attempted
### composition
- no conflict paths; upstream tip is the merge base, so no Composition resolution is required by this snapshot

## Preservation boundaries

- D68’s reviewed direction is preserved as a rule reference: frozen `upstream_base -> gated_tip` source delta onto current upstream, with source refs/status immutable during the private dry-run. This census did not invoke the wrapper, installer, build, ZIP, or any live service.
- D123 `b0ff4205…` and its `2b16085…` product source tree are historical/current-normal evidence references only. The live Agent census source is the captured `547e104…` integration head and its `68df11…` tree; no older D123 source was substituted.
- Both upstream and live predicates remain represented by separate exact refs/blobs; conflicts are intentionally unresolved.
