## P3/D75b current submission

Submitted once with the existing D66 plain-stack submit command from `/home/user/work/app`.

- preflight ID: `app-pin-3c29d553-d75b-p3-current-1855-preflight-1024185442-20128`
- normal ID: `app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908`
- preflight status: `pass`, exit 0, 3s
- normal status at publication: `running`
- service target: `app-pin-3c29d553`
- submit plan: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P3-D75b-submit-produce-1855/submission/p3-submit-plan.json`

Captured source pins and trees:

| repo | commit | tree | detached checkout |
|---|---|---|---|
| App | `3c29d553a7af0b0e0876760052855818ea834658` | `2f0aa476b5cd40e2b80b5f4dec37571b7152a55f` | `/home/user/work/wt/app-pin-3c29d553` |
| Agent | `831df37ffdfbb7cf802c95f91eac30681efdbb45` | `52213c5a56f332532759826f04be6659d8ddd34a` | `/home/user/work/wt/agt-pin-831df37f` |
| Runtime | `1bae0e8ccb8f912d50ad16e80d2e42f8e2ea603f` | `4feab0185b3750a55b8f0c21c92c6015aaf8e2f7` | `/home/user/work/wt/rt-pin-1bae0e8c` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `/home/user/work/wt/vw-pin-635f4de0` |

The preflight manifest is retained at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-preflight-1024185442-20128/d66/manifest.json`

It records the service snapshot as App tree `2f0aa476b5cd40e2b80b5f4dec37571b7152a55f`, one parent `3c29d553a7af0b0e0876760052855818ea834658`, and all four detached source identities above. The normal result directory is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-pin-3c29d553-d75b-p3-current-1855-1024185512-26908`

Awaiting the same normal ID for the original Gate5 and readiness verdict.
