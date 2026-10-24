## Report

Completed P2-D73 source preflight.

- Normal merge receipt: App `587316e378…` (`Merge tl/app-D73-service-snapshot-sol-1739`).
- Captured once via normal `--submit` with `D66_SUBMIT_TARGET` unset.
- Stable target: `app-pin-587316e3`.

Captured pins:

| Repo | SHA | Tree | Checkout |
|---|---|---|---|
| App | `587316e37891f1b474c2c3734e19044246b62285` | `84886c6b1915ca9748d04bb36c0fe8b6861efca6` | `/home/user/work/wt/app-pin-587316e3` |
| Agent | `f4d6c72ce336da66813fc39828187bccbaf80a5b` | `5d328a24dd64fb216ae527b6c05f51d99d7c564e` | `/home/user/work/wt/agt-pin-f4d6c72c` |
| Runtime | `327da207ed30880fe2ae0cd0b116722bb2c6f7a6` | `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf` | `/home/user/work/wt/rt-pin-327da207` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | `/home/user/work/wt/vw-pin-635f4de0` |

Four genuine checkout receipts validated before preflight.

Positive preflight:

- ID: `app-pin-587316e3-d73-p2-current-1747-preflight-1024174912-6282`
- Terminal: `pass`, exit 0, 2 seconds.
- Service snapshot HEAD: `5fde471d8e6cc63d4526e153cbc4eac00af30e18`
- Sole parent: `587316e37891f1b474c2c3734e19044246b62285`
- Tree: `84886c6b1915ca9748d04bb36c0fe8b6861efca6`
- No build, import, daemon, browser, gesture, or body execution.

Poison preflight:

- ID: `app-pin-587316e3-d73-p2-current-1747-missing-runtime-sha-1024175007-10754`
- Terminal: expected `fail`, exit 1, 2 seconds.
- Refusal: `D66 runtime SHA must be a full 40-character SHA`
- Refused before checkout access/build/body.

Commands:

```sh
env -u D66_SUBMIT_TARGET D66_SUBMIT_SUITE=d73-p2-current-1747 \
node --import tsx scripts/testing/d66-plain-stack.mjs p2 --submit
```

```sh
bin/request-test app-pin-587316e3 d73-p2-current-1747-preflight --no-cache
bin/wait-test app-pin-587316e3-d73-p2-current-1747-preflight-1024174912-6282
```

Normal recipe and request command were emitted but intentionally not submitted.

Registry installation:

- Original outside bytes: 573,487; SHA-256 `cd2835dc4421040f8df4cf8e80e8866924529546ccd90c88ff89eb9ad8dfcc37`
- Final `suites.conf`: 576,224 bytes; SHA-256 `2260059bf276788e2dd6fbc400fb0207291b26bf5ff4b6162f9694244c354c92`
- Added rows: preflight, normal, and one missing-runtime-SHA poison row.
- Worktree remains clean; no product/test/helper/body/generated/schema/pin edits.

Original collection: P1/P2/P2-element/P3 = `2/8/1/1`. Six original spec SHA-256 values matched across normal App, pinned App, and this source:

`2b9723db…`, `50960dd2…`, `4292d0b5…`, `07fe3d84…`, `c0624a04…`, `a6468188…`.

Observer/bootstrap sources remain present; Runtime helper SHA-256 is `e68425c1…`. `DONE` and commit message `test(app): qualify P2-D73 pinned service preflight` were written.