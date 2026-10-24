## P2 verdict: FAIL

SAME-ID run `app-pin-587316e3-d73-p2-current-1747-1024175319-22847`:

- Exit `1`, terminal duration `402s`
- Original cases: `8 selected / 4 executed / 1 PASS / 3 FAIL / 5 NOTRUN`
- JUnit: `tests=8 failures=3 skipped=5 errors=0`
- Native seed/history: PASS
- Readiness: `1 PASS`

Case boundaries:

1. Element apply — FAIL, 14.506s. Dialog status `"applied"` absent after 5000ms; retained UIApply evidence ended `pending` at teardown. No accepted response proven.
2. Popup ADD — FAIL, 35.080s. HTTP `422`, `validation_error`, `invalid_records`: `provider created shot owner differs from its authenticated occurrence`. Provider validation, not classifier safety denial.
3. Parent move — FAIL, 115.403s. Accepted path reached reload, but the expected `Committed ...` revision label was missing at lines 631/689. Guarded undo unproven.

Explicit NOTRUN cases:

- registerAsset save
- automatic child placement
- popup SWAP
- transition None single
- transition None bulk

Compared with 25943: element failure is unchanged; popup’s message differs and the old physical-observation cause is not reused; parent advanced beyond the old history-reads assertion and failed later during reload. All eight remain CORE.

Identity verified:

| Repo | SHA | Tree |
|---|---|---|
| App | `587316e37891f1b474c2c3734e19044246b62285` | `84886c6b1915ca9748d04bb36c0fe8b6861efca6` |
| Agent | `f4d6c72ce336da66813fc39828187bccbaf80a5b` | `5d328a24dd64fb216ae527b6c05f51d99d7c564e` |
| Runtime | `327da207ed30880fe2ae0cd0b116722bb2c6f7a6` | `0140a9ab2bf8582c4712dbf84498a6d5dcb132cf` |
| Composition | `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` |

Actual service snapshot verified after completion: head `3a56e7a70b2c04d2c1acfbe3ca7f9b62a75ff2f1`, sole parent App SHA `587316e37891f1b474c2c3734e19044246b62285`, exact App tree, zero content diff.

Versions: Node `v20.19.4`, npm `10.8.2`, `AstridRuntime/0.1 Python/3.13.16`, protocol `workspace.v1`, schema `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`, provider `astrid-v1`, compiler `authoring-bundle-1`.

No-weakening evidence: protected six source hashes matched:

`2b9723db262978ebbb410d5925163fe61c4a83f05f3b44fbbd524bc9df301593`, `50960dd2efadc8350b8647a1f7e88a6cad2b44907bf36a7108832ee0ea9ebf17`, `4292d0b5928e1390c48d0e33876621a2e9b6c7e0616607a72f1b3fa3873d1de9`, `07fe3d84831e2e5977405811ceaa7a592614871e15ec108d812eb024ebed2f3c`, `c0624a04200c40acaf6866d270d9b9b9665b33173565ee709df384ddcdc0e797`, `a6468188ff21c4fd8bd397ff242b0260ee92ab6f2f90ac94786973eaf3c1e99a`.

Runtime safe-phase output: `UNAVAILABLE`; no daemon/direct-private custody inferred.

Checks:

- SAME-ID `bin/wait-test`: exit 1, 402s.
- Preflight `6282`: PASS, exit 0.
- Missing-runtime-SHA control `10754`: expected refusal, exit 1.
- `git diff --check`: PASS.
- Assigned worktree: clean.
- Reused prior source14D73 qualification: focused checks `9/9` PASS and scoped ESLint PASS; strict TypeScript remained at its known baseline missing generated modules. No suites were repeated.

No product files changed. Commit message and `DONE` marker were created.