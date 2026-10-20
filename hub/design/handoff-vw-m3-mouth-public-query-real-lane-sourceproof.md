# D09a source and environment proof

## Source/module identities

| Item | Value |
|---|---|
| Agent revision | `d051bee072cef25e706b060e3318a80aa104f29c` |
| Agent tree | `03f5f61d81bd88136886635454bca6deac60fa24` |
| selected-cut test module | `tests/packs/rendering/test_presenter_selected_cut_aggregate.py` |
| normal presenter fixture module | `tests/packs/rendering/test_presenter_scene_capability.py` (`presenter_query`) |
| selected frame keys | `[0, 3, 4, 5]` |
| selected query file SHA256 | `fbe9155dbe93778d69eb55dae99395bc955b3edccc4476e583b817c3a9dd3bd9` |
| selected test file SHA256 | `a8ec67c5c361071a803232999274ccecde7797d7d15199a8be7d9fd9c26d8f0d` |
| normal fixture file SHA256 | `bbe8feb39d0580295af82582b94e2778063f207dc4ba106559dffef5789b5a43` |
| normal fixture query SHA256 | `267c504dbd8fccaf46ea1a33d45a6daa42bb99a5a7e0a3e91480eccd8c8216ef` |
| retained inspection SHA256 | `eabcc179baa4b97b6bdf1c8343ca270ef090e1306ab8791ee32787c3226385af` |

## Node/package identities

| Item | Value |
|---|---|
| Node | `v20.19.4` |
| Node SHA256 | `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490` |
| public12 tarball SHA256 | `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3` |
| public12 members | `77` |
| peer root | `/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules` (read-only) |
| retained f816 graph | `21,488` entries; SHA256 `9e556a876a02ee4f4ed3e8215eaaf793ac0ba66a6d85e503747f635521acc425` |
| peer files observed | `21,429` |

The test fixture itself discovers `pack:astrid_motion`, verifies the owner root
against this checkout, generates the ordinary host registries, extracts the
immutable public12 package, and checks peer identities. The public query uses
the same prepared Root and ordinary `querySceneFrame`; it does not copy Python
clock/hash/geometry/codebook logic or construct a fake source certificate.

## Central result

`vw-m3-mouth-public-query-real-lane-integration-viewing-mouth-selected-cut-public-query-1020151841-32447` passed with `1 passed in 3.67s`, no skips, and no deselections.
