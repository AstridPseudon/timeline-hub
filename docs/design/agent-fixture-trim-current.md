# Current M2 fixture trim

The ten M2 editing fixtures were factored on current Agent integration head
`df2739f9`. The fixtures still contain the complete semantic vectors; only
duplicate inputs and duplicate recorder fields were removed. There are 15
distinct golden cases: one each for scalar fields, clip add, split, trim,
occurrence delete, and occurrence duplicate; two occurrence-media cases; two
placement cases; two create/unplace cases; and three shot-pool cases.

The Python editing-conformance tests load the compact files through
`tests.editing_conformance.fixture_loader.load_fixture`. Record restoration is
context-aware: the loader has an explicit path for each known golden `records`
collection and copies only missing `created`, `reads`, or `selections` fields
from that record's command. It never recursively interprets authored input or
output data whose keys happen to be `records`, `command`, or `reads`. Shared
placement inputs, occurrence-media inputs/media pins, and the create/unplace
input are restored only for their named fixture controls. No product or schema
loader consumes this compact representation.

The expanded source files are exported flat for external consumers at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-agent-expanded-<stem>.json`.
They are byte-identical copies of the pre-trim current fixtures and remain
ordinary expanded JSON. App/TypeScript handoffs must use these exports (or an
equivalent expanded copy), not the private Python compact syntax.

## Counts and hashes

Line counts treat a one-line JSON file as one logical line. `sourceSHA` and the
handoff hash identify the pre-trim expanded fixture; `rawcompactSHA` identifies
the compact file committed here.

| fixture stem | before bytes / lines | after bytes / lines | sourceSHA / handoff SHA | rawcompactSHA |
| --- | ---: | ---: | --- | --- |
| recipe_m2_app_clip_scalar_fields | 161268 / 6317 | 133227 / 5070 | `8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06` / same | `52dac614ac1b13efda13de9b79ecd3a1713939fd7e6f5f7d07d57ca8ec500348` |
| recipe_m2_clip_add | 20541 / 906 | 17592 / 770 | `5e9a54e75a0901724dedd3e62c0f37f78840a8edee001f30b92306383800479b` / same | `cebe45dbf6806c2fb772665ad2c3a416eae172df48d1b0cc48d023cbc80345ff` |
| recipe_m2_clip_split | 57241 / 2524 | 45197 / 1951 | `a0e24c1f78d8580f908973745950ed0196c17257831197ec2f75a55abc638f63` / same | `46bce505cbba3d72f7eb6c060ed9f1cf890e0c50c42a8f50a8edee7d6287e204` |
| recipe_m2_clip_trim | 52208 / 2275 | 38282 / 1587 | `4d71a9d184db1b85c220de10842b2dc68e5eb9b48afee180b6c29cf0d5b06152` / same | `60fcc84d769a2a68b5330288e842ca286f3907510a5dd18bc240c6e314ee612c` |
| recipe_m2_occurrence_delete | 123486 / 4491 | 116619 / 4236 | `e66b2464f5d0b779619554aaf2b7ff49e255941e1d3932c5ebe84ad78a0d50ac` / same | `9a52d55130a4c857e3cb4d8962ea63155c2d3c3b2a6ed035d8babf38666d1e96` |
| recipe_m2_occurrence_duplicate | 94420 / 3469 | 88184 / 3230 | `2d0009f60947d4f5f2f8f8f204827315c14319f20da0373789578d0076b39b9f` / same | `b64b9f9bbed418c5a58455931ad0bdae549ed0ae6e0a6be5c79b30571f19d829` |
| recipe_m2_occurrence_media | 108547 / 3898 | 82650 / 2919 | `761153bb5c9de335d212c033bce976315a6846c4bde456b1d32f6aeb35919ad6` / same | `cf9650d82a3171236dd72a14ca1df2fabee8184edbef63d2020f5eeebcc15d69` |
| recipe_m2_placement | 79188 / 1 | 58978 / 1 | `7404b665b2918ebf095abc68bd3a20176afb0589b79cf785887c1da50b68d271` / same | `49bf7e046e79c5d81b3ab183ac11868294a6e5261b727d876f782cf4e4700060` |
| recipe_m2_placement_create_unplace | 177115 / 6815 | 124951 / 4742 | `2ee887fd375f9a68682843eb21c69323c2b8bb42d92230e8b50bf7c78791292a` / same | `e0f01074d0136990b9bc39d882f8015169240cb3167510d870491feeb32c55b0` |
| recipe_m2_shot_pool | 43819 / 1642 | 34421 / 1269 | `13f59f8fd0734dff915515efcf2243ceeb1b3f026973793560a6b773ed634078` / same | `34edbb5e0f99a0b63b8ca8a5c087074ec871b99151df70e58a792ce806c4b484` |

Total: 917833 -> 740101 bytes (177732 fewer), and 32338 -> 25775 logical
lines (6563 fewer). The exports are the handshake-preserving expanded form;
the compact files are test-only.
