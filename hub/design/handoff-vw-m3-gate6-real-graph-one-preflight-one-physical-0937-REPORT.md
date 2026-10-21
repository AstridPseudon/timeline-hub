# Gate 6 real graph / one preflight / one physical — HELD

Status: HELD before request. The required 09:34 readiness manifest is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-gate6-physical-graph-clone-readiness-0934-MANIFEST.json`.

The exact App pin is
`/home/user/work/wt/app-pin-0d432391` at
`0d4323913b92c4e0e3830bf14ec7f35d981475ca` /
`5a1e0e85d0f336f642426b91ccf3b3f1984ebd14`, with retained dist at
`/home/user/work/wt/app-pin-d00a6613/dist`. The source graph
`/home/user/work/wt/app-pin-d00a6613/node_modules` is
`8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b` /
32393 entries and 555896832 allocated bytes. The private destination was not
materialized because free space ended at 10926952448 bytes, below the exact
11876144076-byte pre-copy requirement, leaving STORAGE NEED 949191628 bytes.

The exact 0923/0930 packet remains the only packet in scope:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-pinned0d43-preflight-and-one-actual-0923/packet`.
Its checksums are in `packet/SHA256SUMS`; no packet file was changed. Neither
`run.sh --preflight` nor `run.sh` was invoked by this worker. No central
request, grant, marker, or physical output exists.

Frozen tuple: Agent `d0a5072bbe7b7ce9489f43aa0a81027ec400343` /
`6adb4a1190dfb2874e101565f37eccd392b1ae2f`; Runtime server
`8f105c26e3b62f9c2683f717a9773a12bc775a8e` /
`b7f456d5135cba6049980ebc43a91c7a72ab8f7e`; producer
`2c4ac180c2220bdad966bc01e95ad230e99ce26a` /
`7ab412cc4bcbe517efcfa806e092336390312e18`; Composition
`5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8` /
`13e375534fffd704305eced5686699d2c8c9c948`; public13
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, 77
members; Runtime graph `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`,
21455 entries; App graph `8bdc...`, 32393 entries; Node hash `43d6...`; helper
`b70b9d...` / `bc75...`; Chrome155.

All five exact cases are FAIL with body `none` because no run was admitted.
The frame comparison, frame+PCM comparison against the same normal CPU export,
picture negative, and half-gain negative are therefore unverified and fail the
zero-body rule.
